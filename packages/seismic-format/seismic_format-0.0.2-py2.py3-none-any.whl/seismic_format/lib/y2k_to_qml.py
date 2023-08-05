from copy import deepcopy
import calendar
import datetime
import os
import sys

from obspy.core.event.base import ConfidenceEllipsoid
from obspy.core.event.base import CreationInfo
from obspy.core.event.base import QuantityError
from obspy.core.event.base import WaveformStreamID
from obspy.core.event.magnitude import Amplitude
from obspy.core.event.origin import Arrival
from obspy.core.event.origin import Origin
from obspy.core.event.origin import OriginQuality, OriginUncertainty
from obspy.core.event.origin import Pick
from obspy.core.utcdatetime import UTCDateTime

from obspy.core.event import Catalog
from obspy.core.event import read_events
from obspy.core.event.event import Event
from obspy.core.event.magnitude import Magnitude

from .mappings import (hypoinv_weight_to_obspy_time_error,
                    obspy_time_error_to_hypoinv_weight)

from .lib_y2k import read_format, read_arc_shadow_file
from .liblog import getLogger
logger = getLogger()

from .. import get_format_dir
formats_dir = get_format_dir()

def y2k_to_quakeml(arc_file):

    fname = 'y2k-to-quakeml'

# 1. Read the Hypoinverse Y2000 archive format:
    y2000_format_file = os.path.join(formats_dir, 'format.Y2000_station_archive')
    y2000_header_file = os.path.join(formats_dir, 'format.Y2000_header_archive')
    y2k_format = read_format(y2000_format_file)
    hdr_format = read_format(y2000_header_file)

    # Read in the y2k arc file
    logger.debug("Read y2k arc file into origin + y2k_picks")
    (y2k, y2k_origin)  = read_arc_shadow_file(arc_file, y2k_format, hdr_format)
    if y2k_origin is None:
        logger.error("%s: Problem reading arc_file=[%s] --> Exitting" % (fname, arc_file))
        exit(2)

    # Set up epoch times (may be corrected by leap seconds in the future)
    yyyymoddhhmi = str(y2k_origin['year']) + y2k_origin['moddhhmi']
    moddhhmi = y2k_origin['moddhhmi']
    try:
        (month, day, hour, min) = (int(moddhhmi[0:2]), int(moddhhmi[2:4]), int(moddhhmi[4:6]), int(moddhhmi[6:8]))
        year = int(y2k_origin['year'])
        isecs= int(y2k_origin['seconds'])
        xsecs= y2k_origin['seconds'] - isecs
    except ValueError:
        raise
    da = datetime.datetime(year, month, day, hour, min, isecs)
    # epoch  = origin timestamp   
    # epoch0 = origin timestamp without seconds = base for amps + codas
    epoch = calendar.timegm(da.timetuple()) + xsecs
    epoch0 = calendar.timegm(datetime.datetime(year, month, day, hour, min, 0).timetuple())
    # Do we need to shift times by leap seconds ?  # e.g, are we using a database ?
    use_db = 0
    if use_db: # MTH: this code is implemented in aqms-pdl and depends on db connection:
        epoch += get_leap_seconds(y2k_origin, event)
        epoch0 += get_leap_seconds(y2k_origin, event)

    y2k_origin['datetime'] = epoch

    event = Event()
    # Convert y2k origin to quakeml origin
    origin = y2k_to_origin(y2k_origin)
    event.preferred_origin_id = origin.resource_id

    nsta_ml = y2k_origin['tot_amp_mag_weights']
    nobs_ml = 2*nsta_ml  # Because each station has two amp observations
    nsta_mc = y2k_origin['tot_dur_mag_weights']
    nobs_mc = nsta_mc
    nsta_my = y2k_origin['tot_alt_dur_mag_weights']
    nobs_my = nsta_my

    found_dict = {'ml_found':0,
                  'mc_found':0,
                  'my_found':0,
                 }

    # This mapping comes from UUtah and may not be general!
    #              y2k field     mag_type   nsta    found_flag
    y2k_mag_dict = {'ampmag' :      ('ML', nsta_ml, 'ml_found'),
                    'durmag' :      ('Mc', nsta_mc, 'mc_found'),
                    'alt_dur_mag' : ('Md', nsta_my, 'my_found'),
                   }
    magnitudes = []
    for y2k_mag_key in y2k_mag_dict.keys():
        if y2k_origin[y2k_mag_key] > -9:
            logger.info("%s: Found ampmag:%.2f" % (fname, y2k_origin[y2k_mag_key]))
            #ml_found = 1
            (mag_type, nsta, found_key) = y2k_mag_dict[y2k_mag_key]
            found_dict[found_key] = 1
            magnitude = Magnitude()
            magnitude.mag = y2k_origin[y2k_mag_key]
            magnitude.magnitude_type = mag_type
            magnitude.origin_id = origin.resource_id
            magnitude.station_count = nsta
            magnitudes.append(magnitude)

    if magnitudes:
        event.magnitudes = magnitudes
        event.preferred_magnitude_id = magnitudes[0].resource_id

    nmags_found = 0
    for k in found_dict.keys():
        nmags_found += found_dict[k]
    #nmags_found = ml_found + mc_found + my_found

    logger.info("%s: Hypoinv file contains n=[%d] valid mags:" % (fname, nmags_found))
    logger.info("%s: ml_found=%d mc_found=%d my_found=%d" % (fname, found_dict['ml_found'], 
                                                             found_dict['mc_found'], found_dict['my_found']))
    logger.info("%s: Hypoinv prefmag_label=[%s] prefmag=%3.2f" % (fname, y2k_origin['prefmag_label'], y2k_origin['prefmag']))

    if found_dict['ml_found'] and y2k_origin['prefmag_label'] != 'L':
        logger.warning("%s: ml_found but prefmag_label=[%s] and *not* 'L' --> making ML preferred anyway!" %
                    (fname, y2k_origin['prefmag_label']))
    if found_dict['ml_found'] and y2k_origin['prefmag'] != y2k_origin['ampmag']:
        logger.warning("%s: ml_found but prefmag=[%3.2f] != ampmag=[%3.2f]" %
                    (fname, y2k_origin['prefmag'], y2k_origin['ampmag']))

    # Should check this against y2k_origin['prefmag_label'] and y2k_origin['prefmag']
    if found_dict['ml_found']:
        y2k_origin['prefmagType'] = 'l'
    elif found_dict['mc_found']:
        y2k_origin['prefmagType'] = 'd'

# 5. Now count # of arrivals, amps, codas - and use to get sequences
    #write_y2000_phase(hdr_format, y2k_origin)

    codas = []
    amps  = []
    Parrs = []
    Sarrs = []
    all_arrivals = []

    avgMag = {}
    flag119 = {}

    auth = y2k_origin['authority']
# 6. Each y2k arrival line must be sorted for injection into one or more of the tables: {arrival, amp, coda}
    #for sta in y2k:
        #for chan in y2k[sta]:
            #arrival = y2k[sta][chan]
    if 1:
        for arrival in y2k:
            #arrival = y2k[sta][chan]
            #arrival['auth'] = 'UU'
            arrival['auth'] = auth
            # arrival['orid'] = orid
            # arrival['subsource'] = 'uping'
            logger.debug("%s: Process arrival:%s" % (fname, arrival['string']))
            arrival_datetime = str(arrival['year']) + arrival['moddhhmi']

            validP = 0
            validS = 0
            validAmp = 0
            validCoda = 0

            # Is P arrival valid
            if arrival['PwtCode'] >= 0 and arrival['Psec'] > 0.:
                validP = 1
            elif arrival['PwtCode'] >= 0 and arrival['Psec'] == 0. and arrival_datetime != yyyymoddhhmi:
                validP = 1
            if validP:
                arrival['iphase']='P'
                arrival['datetime']=epoch0 + arrival['Psec']
                Parrs.append(deepcopy(arrival))
                all_arrivals.append(deepcopy(arrival))
                logger.debug("%s: Found P arrival: %s %s %s %5.2f" % (fname, arrival['sta'], arrival['chan'],
                              arrival_datetime, arrival['Psec']))

            # Is S arrival valid
            if arrival['SwtCode'] >= 0 and arrival['Ssec'] > 0. and not arrival['Ssec'] == 60.00:
                validS = 1
            elif arrival['SwtCode'] >= 0 and arrival_datetime != yyyymoddhhmi:
                if not validP: #If no P info, then I have to assume the S time is correct (Ssec exactly equals 0 or 60):
                    validS = 1
                elif arrival['Ssec'] > arrival['Psec']: #If we have P, then check S > P in relative sense:
                    validS = 1 
            if validS:
                arrival['iphase']='S'
                arrival['datetime']=epoch0 + arrival['Ssec']
                Sarrs.append(deepcopy(arrival))
                all_arrivals.append(deepcopy(arrival))
                logger.debug("%s: Found S arrival: %s %s %s %5.2f" % (fname, arrival['sta'], arrival['chan'], \
                              arrival_datetime, arrival['Ssec']))

            # Is Amp valid
            if arrival['Amp'] > 0:
                if arrival['AmpMag'] == 0.:
                    logger.error("%s: sta=%s chan=%s: has AmpMag == 0. --> Skip" %
                                 (fname, arrival['sta'], arrival['chan'], arrival['coda']))
                else:
                    validAmp = 1
                    if arrival['chan'][2] == 'H':
                        # Use this chan to set AmpMag on the ?HN, ?HE chans
                        #print '  This is a ficticious H comp --> get AmpMag=[%3.2f]' % arrival['AmpMag']
                        logger.debug("%s: Found Amp ?HH chan: %s %s %s %5.2f" % (fname, arrival['sta'], arrival['chan'], \
                                      arrival_datetime, arrival['Amp']))
                        avgMag[sta]  = arrival['AmpMag']
                        flag119[sta] = arrival['blank4']
                        if arrival['blank4'] == 'X':
                            logger.debug("%s: Found ?HH chan: %s %s %s %5.2f with col.199='X' " % (fname, arrival['sta'], arrival['chan'], \
                                          arrival_datetime, arrival['Amp']))
                    else:
                        #arrival['datetime']=0.
                        arrival['datetime']=y2k_origin['datetime']
                        # This is from U Utah:
                        # magcorr = magcorr_lookup(arrival, epoch0, station_mag_corrs)
                        # For now do this:
                        magcorr = 0.0
                        arrival['magcorr']=magcorr

                        amps.append(deepcopy(arrival))
                        logger.debug("%s: Found Amp arrival: %s %s %s %5.2f magcorr:%.2f" % (fname, arrival['sta'], arrival['chan'], \
                                       arrival_datetime, arrival['Amp'], arrival['magcorr']))

            if 'coda' in arrival:
                if arrival['DurMag'] <= 0.:
                    logger.error("%s: sta=%s chan=%s: Has coda shadow line=[%s] but missing DurMag! --> Skip" %
                                 (fname, arrival['sta'], arrival['chan'], arrival['coda']))
                else:
                    validCoda = 1
                    arrival['datetime']=epoch0
                    arrival['tau']=float(arrival['coda']['end'] - arrival['coda']['beg'])
                    arrival['afree']=arrival['coda']['logA0']
                    arrival['qfree']=arrival['coda']['alpha']
                    arrival['beg']=arrival['coda']['beg']
                    arrival['end']=arrival['coda']['end']
                    codas.append(deepcopy(arrival))
                    logger.debug("%s: Found Coda arrival: %s %s %s %5.2f" % (fname, arrival['sta'], arrival['chan'],
                                    arrival_datetime, arrival['DurMag']))

            if not validP and not validS and not validAmp and not validCoda:
                logger.error("%s: Unable to scan P,S,Amp,Coda info from arrival !!" % (fname))

# For stations with ?HH channel amp, assign the corresponding AmpMag to the ?HN & ?HE channels:
    for amp in amps:
        if amp['sta'] in avgMag.keys():
                amp['AmpMag'] = avgMag[amp['sta']]
        else:
                logger.warning("%s: sta=[%s] NOT in avgMag keys" % (fname, amp['sta']))

# We want to set ?HN,?HE amp mag weight based on whether there's an 'X' or not in col. 119 of the ?HH hyp2000 shadow line 
        if amp['sta'] in flag119.keys():
                amp['col_119'] = flag119[amp['sta']]
        else:
                logger.warning("%s: sta=[%s] NOT in flag119 keys" % (fname, amp['sta']))


    narrivals = len(Parrs) + len(Sarrs)
    logger.info("%s: Got %d P-arrivals + %d S-arrivals" % (fname, len(Parrs), len(Sarrs)))

    arrivals = []
    picks = []

    #for arr in Parrs + Sarrs:
    for arr in all_arrivals:
        arrival, pick = y2k_phase_to_arrival(arr, arr['iphase'])
        arrivals.append(arrival)
        picks.append(pick)

    logger.info("%s: Scanned [%d] P/S arrivals" % (fname, narrivals))
    for arr in arrivals:
        pick = arr.pick_id.get_referred_object()
        wid = pick.waveform_id
        if wid.location_code:
            wave_id = "%2s.%4s.%2s-%3s" % (wid.network_code, wid.station_code, wid.location_code, wid.channel_code)
        else:
            wave_id = "%2s.%4s.%3s" % (wid.network_code, wid.station_code, wid.channel_code)
        logger.info("arr: %s [%s] %f" % (wave_id, arr.phase, pick.time))

    amplitudes = []
    logger.info("%s: Scanned [%d] amplitudes" % (fname, len(amps)))
    for amp in amps:
        amplitude = y2k_phase_to_amplitude(amp)
        amplitudes.append(amplitude)
        #print(amplitude)
        wid = amplitude.waveform_id
        if wid.location_code:
            wave_id = "%2s.%4s.%2s-%3s" % (wid.network_code, wid.station_code, wid.location_code, wid.channel_code)
        else:
            wave_id = "%2s.%4s.%3s" % (wid.network_code, wid.station_code, wid.channel_code)
        logger.info("amp: %s [%s] %f" % (wave_id, amplitude.type, amplitude.generic_amplitude))

    logger.info("%s: Scanned [%d] codas" % (fname, len(codas)))
    # These seem to be coda (per channel) magnitudes
    for arrival in codas:
        logger.info("%s: Coda: %s %s %s %5.2f" % (fname, arrival['sta'], arrival['chan'],
                      arrival_datetime, arrival['DurMag']))

    origin.arrivals = arrivals
    event.origins = [origin]
    event.picks = picks
    event.amplitudes = amplitudes

    if y2k_origin['prefmag_label']:
        logger.info("Found prefmag:%s val:%.2f" % (y2k_origin['prefmag_label'], y2k_origin['prefmag']))

    catalog = Catalog(events=[event])

    return catalog

def y2k_to_origin(y2k_origin):
    '''
    Convert a y2k_origin to quakeml Origin

    :param y2k_origin: origin to convert
    :type origin: y2k origin dict

    :return: converted origin 
    :rtype: obspy.core.event.origin.Origin
    '''

    origin = Origin()

    year = y2k_origin['year']
    mo = y2k_origin['moddhhmi'][0:2]
    dd = y2k_origin['moddhhmi'][2:4]
    hh = y2k_origin['moddhhmi'][4:6]
    mi = y2k_origin['moddhhmi'][6:8]
    ss = y2k_origin['seconds']
    date = "%s-%s-%sT%s:%s:%s" % (year, mo, dd, hh, mi, ss)
    origin.time = UTCDateTime(date)

    longitude = y2k_origin['lon_deg'] + y2k_origin['lon_min']/60.0
    if y2k_origin['e_or_w'] != 'E':
        longitude *= -1

    latitude = y2k_origin['lat_deg'] + y2k_origin['lat_min']/60.0
    if y2k_origin['n_or_s'] == 'S':
        longitude *= -1

    origin.longitude = longitude
    origin.latitude = latitude
    origin.depth = y2k_origin['depth'] * 1.e3  # y2k depth [km] --> obspy depth [m]
    qe = QuantityError()
    qe.uncertainty = y2k_origin['error_vertical'] * 1.e3  # y2k depth [km] --> obspy depth [m]
    # qe.lower_uncertainty
    # qe.upper_uncertainty
    # qe.confidence_level
    origin.depth_errors = qe

    if y2k_origin['program_remark'] == " -":
        origin.depth_type = "operator assigned"
    origin.region = y2k_origin['region']

    quality = OriginQuality()
    #quality.associated_phase_count
    #quality.used_phase_count
    quality.standard_error = y2k_origin['rms']
    quality.azimuthal_gap = y2k_origin['azgap']
    quality.minimum_distance = y2k_origin['min_dist'] / 111.19
    quality.used_phase_count = y2k_origin['n_P_and_S_times']
    quality.associated_phase_count = y2k_origin['n_valid_P_and_S_reads']
    origin.quality = quality

    uncertainty = OriginUncertainty()
    uncertainty.horizontal_uncertainty = y2k_origin['error_horizontal'] * 1.e3 # km --> m
    uncertainty.max_horizontal_uncertainty = y2k_origin['pri_error_size'] * 1.e3
    uncertainty.azimuth_max_horizontal_uncertainty = y2k_origin['pri_error_az']
    uncertainty.min_horizontal_uncertainty = y2k_origin['sm_error_size'] * 1.e3
    origin.origin_uncertainty = uncertainty

    confidence_ellipsoid = ConfidenceEllipsoid()
    uncertainty.confidence_ellipsoid = confidence_ellipsoid
    confidence_ellipsoid.major_axis_azimuth = y2k_origin['pri_error_az']
    confidence_ellipsoid.major_axis_plunge  = y2k_origin['pri_error_dip']
    confidence_ellipsoid.semi_major_axis_length = y2k_origin['pri_error_size'] * 1.e3
    confidence_ellipsoid.semi_minor_axis_length = y2k_origin['sm_error_size'] * 1.e3
    confidence_ellipsoid.semi_intermediate_axis_length = y2k_origin['int_error_size'] * 1.e3

    creation_info = CreationInfo()
    creation_info.agency_id = y2k_origin['authority']
    creation_info.version = y2k_origin['version_info']
    origin.creation_info = creation_info

    return origin


def y2k_phase_to_arrival(y2k_phase, phase):
    '''
    Convert a y2k phase dict to obspy arrival

    :param phase: 'P' or 'S'
    :type phase: str
    :param y2k_phase: y2k_phase
    :type y2k_phase: python dict

    :return: converted phase 
    :rtype: obspy arrival
    '''

    arrival = Arrival()
    arrival.phase = phase
    if y2k_phase['Azim'] > 0:
        arrival.azimuth = y2k_phase['Azim']
    # epicentral dist in deg
    if y2k_phase['Dist'] > 0:
        arrival.distance = y2k_phase['Dist'] / 111.19  #Convert y2k dist [km] to obspy dist [deg]
    # takeoff angle (deg) measured from downward vertical
    if y2k_phase['Angle'] > 0:
        arrival.takeoff_angle = y2k_phase['Angle']    ###   Verify y2k uses same takeoff angle convention (?)
    arrival.time_residual = y2k_phase['%srms' % phase]
    arrival.time_weight = y2k_phase['%swtUsed' % phase]

    waveform_id = WaveformStreamID(y2k_phase['net'], y2k_phase['sta'])
    waveform_id.channel_code = y2k_phase['chan']
    if y2k_phase['loc'] != -9:
        waveform_id.location_code = y2k_phase['loc']

    pick = Pick()
    pick.waveform_id = waveform_id
    year = y2k_phase['year']
    mo = y2k_phase['moddhhmi'][0:2]
    dd = y2k_phase['moddhhmi'][2:4]
    hh = int(y2k_phase['moddhhmi'][4:6])
    mi = int(y2k_phase['moddhhmi'][6:8])
    ss = float(y2k_phase['%ssec' % phase])
    if ss > 60.:
        mins = int(ss // 60.)
        ss = ss % (60. * mins)
        mi += mins

    date = "%s-%s-%sT%s:%s:%s" % (year, mo, dd, hh, mi, ss)
    pick.time = UTCDateTime(date)
    #pick.backazimuth = 

    arrival.pick_id = pick.resource_id

    onset = y2k_phase['%srmk' % phase][0]

    if onset == 'I':
        pick.onset = "impulsive"
    elif onset == 'E':
        pick.onset = "emergent"
    pick.phase_hint = phase

    if phase == 'P':
        if y2k_phase['PUpDown'] == 'U':
            pick.polarity = 'positive'
        elif y2k_phase['PUpDown'] == 'D':
            pick.polarity = 'negative'

    time_errors = QuantityError() 
    time_errors.uncertainty = hypoinv_weight_to_obspy_time_error(y2k_phase['%swtCode' % phase])
    pick.time_errors = time_errors

    return arrival, pick

'''
OrderedDict([('sta', 'YNR'), 
('string', 'YNR  WY  HHE    4201112131506    0-999  0    0   0   00.21966 0  0   0   0 542 6900  0       9-9.174   0   0  L01 1   X '),
('net', 'WY'), ('comp1', ''), ('chan', 'HHE'), ('Prmk', '  '), ('PUpDown', ''), ('PwtCode', 4), 
('year', 2011), ('moddhhmi', '12131506'), ('Psec', 0.0), ('Prms', -9.99), ('PwtUsed', 0.0), 
('Ssec', 0.0), ('Srmk', '  '), ('SwtCode', 0), ('Srms', 0.0), 
('Amp', 0.21966), ('AmpCode', 0), ('SwtUsed', 0.0), 
('Pdelay', 0.0), ('Sdelay', 0.0), ('Dist', 54.2), ('Angle', 69.0), ('AmpMagC', 0), ('DurMagC', 0), 
('PerMax', 0.0), ('StaRmk', ''), ('CodaDur', -9), ('Azim', 9.0), ('DurMag', -9.0), ('AmpMag', 2.1), 
('Pimport', 0.0), ('Simport', 0.0), ('DataSource', ''), ('DurCode', ''), 
('AmpLabel', 'L'), ('loc', '01'), ('AmpType', 1), ('comp3', ''), ('blank4', 'X'), ('blank5', ''), 
('auth', 'UU'), ('subsource', 'uping'), ('datetime', 1323788816.88), ('magcorr', 0.0), ('col_119', '')])
'''

def y2k_phase_to_amplitude(y2k_phase):
    '''
    Convert a y2k phase dict to obspy amplitude

    :param phase: 'P' or 'S'
    :type phase: str
    :param y2k_phase: y2k_phase
    :type y2k_phase: python dict

    :return: converted phase 
    :rtype: obspy amplitude
    '''

    waveform_id = WaveformStreamID(y2k_phase['net'], y2k_phase['sta'])
    waveform_id.channel_code = y2k_phase['chan']
    if y2k_phase['loc'] != -9:
        waveform_id.location_code = y2k_phase['loc']

    amplitude = Amplitude()
    amplitude.waveform_id = waveform_id
    amplitude.generic_amplitude = y2k_phase['Amp']
    amplitude.type = 'A'                # unspecified amplitude reading 
    if y2k_phase['AmpLabel'] == 'L':
        amplitude.type = 'AML'          # amplitude reading for local magnitude

    amplitude.scaling_time = y2k_phase['datetime']   # Check this

    #amplitude.unit = 
    #amplitude.per = 
    #amplitude.snr = 
    #amplitude.time_window = 
    #amplitude.pick_id = 

    '''
    pick = Pick()
    pick.waveform_id = waveform_id
    year = y2k_phase['year']
    mo = y2k_phase['moddhhmi'][0:2]
    dd = y2k_phase['moddhhmi'][2:4]
    hh = int(y2k_phase['moddhhmi'][4:6])
    mi = int(y2k_phase['moddhhmi'][6:8])
    ss = float(y2k_phase['%ssec' % phase])
    if ss > 60.:
    '''
    return amplitude
