from copy import deepcopy
import calendar
import datetime
import os
import sys

from obspy.core.event import read_events

from .lib_y2k import read_format, write_y2000_phase
from .liblog import getLogger
logger = getLogger()

from .. import get_format_dir
formats_dir = get_format_dir()

from .mappings import (hypoinv_weight_to_obspy_time_error,
                    obspy_time_error_to_hypoinv_weight)


def quakeml_to_y2k(quakemlfile):

    logger = getLogger()

    formats_dir = get_format_dir()

    y2000_format_file = os.path.join(formats_dir, 'format.Y2000_station_archive')
    y2000_header_file = os.path.join(formats_dir, 'format.Y2000_header_archive')

# 1. Read the Hypoinverse Y2000 archive format:
    y2k_format = read_format(y2000_format_file)
    hdr_format = read_format(y2000_header_file)

    event = None
    mag = None
    origin = None
    preferred_origin = False

    try:
        cat = read_events(quakemlfile, format="quakeml")
        event = cat[0]
        mag = event.preferred_magnitude() or event.magnitudes[0]
        origin = event.preferred_origin() or event.origins[0]

        if not origin:
            logger.warning("****** There is NO origin in this quakeml!")
    except:
        logger.error("Problem reading quakeml file=[%s]" % quakemlfile)
        raise

    y2k_origin = origin_to_y2k(origin, hdr_format)
    for magnitude in event.magnitudes:
        if magnitude.magnitude_type in ['M', 'ML', 'Ml', 'Mb', 'MS']:
            y2k_origin['ampmag'] = magnitude.mag
        #elif magnitude.magnitude_type in ['Mc', 'Md']:
        elif magnitude.magnitude_type in ['Mc']:
            y2k_origin['durmag'] = magnitude.mag
        elif magnitude.magnitude_type in ['Md']:
            y2k_origin['alt_dur_mag'] = magnitude.mag

    pref_magnitude = event.preferred_magnitude()
    if pref_magnitude:
        y2k_origin['prefmag_label'] = pref_magnitude.magnitude_type[-1]
        y2k_origin['prefmag'] = pref_magnitude.mag

    # MTH: just for testing
    #y2k_origin['event_id'] = 1234567890

    nS = 0
    nP = 0
    for arrival in origin.arrivals:
        if arrival.phase == 'P':
            nP += 1
        elif arrival.phase == 'S':
            nS += 1
        else:
            logger.info("Unkown arrival phase:%s" % arrival.phase)
    y2k_origin['number_S_times'] = nS

    # Note that we can also write out the origin line with this func:
    #write_y2000_phase(hdr_format, origin_to_y2k(origin, hdr_format))
    y2k_out = write_y2000_phase(hdr_format, y2k_origin)

    for arrival in origin.arrivals:
        y2k_phase = arrival_to_y2k(arrival, y2k_format)
        y2k_out += write_y2000_phase(y2k_format, y2k_phase)

    return y2k_out

def origin_to_y2k(origin, hdr_format):
    '''
    Convert a quakeml origin to y2k_origin dict

    Only reason for passing in hdr_format is so we can auto initialize
      all the y2k fields = None

    :param origin: origin to convert
    :type origin: obspy.core.event.origin.Origin

    :return: converted origin 
    :rtype: python dict

    '''

    y2k_origin = {}

    for k,v in hdr_format.items():
        y2k_origin[k] = None

    t = {}
    for x in {'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'}:
        t[x] = getattr(origin.time, x)
    y2k_origin['year'] = t['year']
    y2k_origin['moddhhmi'] = "%02d%02d%02d%02d" % (t['month'], t['day'], t['hour'], t['minute'])
    y2k_origin['seconds'] = t['second'] + t['microsecond']/1e6

    lat = abs(origin.latitude)
    y2k_origin['lat_deg'] = int(lat)
    y2k_origin['lat_min'] = (lat - int(lat)) * 60.
    y2k_origin['n_or_s'] = '' if origin.latitude >= 0. else 'S'
    #print("lat=%f lat_deg=%d lat_min=%f" % (lat, y2k_origin['lat_deg'], y2k_origin['lat_min']))

    lon = abs(origin.longitude)
    y2k_origin['lon_deg'] = int(lon)
    y2k_origin['lon_min'] = (lon - int(lon)) * 60.
    y2k_origin['e_or_w'] = '' if origin.longitude <= 0. else 'E'

    y2k_origin['depth'] = origin.depth/1.e3
    if origin.depth_errors and origin.depth_errors.uncertainty:
        y2k_origin['error_vertical'] = origin.depth_errors.uncertainty/1.e3

    if origin.depth_type == "operator assigned":
        #program_remark       Auxiliary remark from program (i.e. "-" for depth fixed, etc
        y2k_origin['program_remark'] = '-'

    if origin.creation_info:
        if getattr(origin.creation_info, 'agency_id', None):
            y2k_origin['authority'] = origin.creation_info.agency_id[0]
        if getattr(origin.creation_info, 'version', None):
            y2k_origin['version_info'] = origin.creation_info.version

    #number_S_times          Number of S times with weights greater than 0.1.
    #number_P_first_motions  Number of P first motions. *
    if origin.quality:
        if getattr(origin.quality, 'azimuthal_gap', None):
            y2k_origin['azgap'] = origin.quality.azimuthal_gap
        if getattr(origin.quality, 'used_phase_count', None):
            y2k_origin['n_P_and_S_times'] = origin.quality.used_phase_count
        if getattr(origin.quality, 'associated_phase_count', None):
            y2k_origin['n_valid_P_and_S_reads'] = origin.quality.associated_phase_count
        if getattr(origin.quality, 'standard_error', None):
            y2k_origin['rms'] = origin.quality.standard_error
        if getattr(origin.quality, 'minimum_distance', None):
            y2k_origin['min_dist'] = origin.quality.minimum_distance * 111.19

    if origin.origin_uncertainty:
        uncertainty = origin.origin_uncertainty
        if getattr(uncertainty, 'confidence_ellipsoid', None):
            y2k_origin['pri_error_az']   = uncertainty.confidence_ellipsoid.major_axis_azimuth
            y2k_origin['pri_error_dip']  = uncertainty.confidence_ellipsoid.major_axis_plunge
            y2k_origin['pri_error_size'] = uncertainty.confidence_ellipsoid.semi_major_axis_length/1.e3
            y2k_origin['sm_error_size']  = uncertainty.confidence_ellipsoid.semi_minor_axis_length/1.e3
            y2k_origin['int_error_size'] = uncertainty.confidence_ellipsoid.semi_intermediate_axis_length/1.e3

            #These don't exist
            #y2k_origin['int_error_az']   = uncertainty.confidence_ellipsoid.major_axis_azimuth
            #y2k_origin['int_error_dip']  = uncertainty.confidence_ellipsoid.major_axis_plunge
            #y2k_origin['int_error_size'] = uncertainty.confidence_ellipsoid.semi_minor_axis_length/1.e3
        else:
            if getattr(uncertainty, 'max_horizontal_uncertainty', None):
                y2k_origin['pri_error_size']  = uncertainty.max_horizontal_uncertainty /1.e3
            if getattr(uncertainty, 'azimuth_max_horizontal_uncertainty', None):
                y2k_origin['pri_error_az']  = uncertainty.azimuth_max_horizontal_uncertainty
            if getattr(uncertainty, 'min_horizontal_uncertainty', None):
                y2k_origin['sm_error_size']  = uncertainty.min_horizontal_uncertainty /1.e3 

        if getattr(uncertainty, 'horizontal_uncertainty', None):
            y2k_origin['error_horizontal'] = uncertainty.horizontal_uncertainty/1.e3

    if origin.creation_info:
        if getattr(origin.creation_info, 'agency_id', None):
            y2k_origin['authority'] = origin.creation_info.agency_id[0]
        if getattr(origin.creation_info, 'version', None):
            y2k_origin['version_info'] = origin.creation_info.version

    return y2k_origin

def arrival_to_y2k(arrival, y2k_format):
    '''
    Convert a quakeml arrival to y2k arrival dict

    Only reason for passing in y2k_format is so we can auto initialize
      all the y2k_phase fields = None

    :param origin: origin to convert
    :type origin: obspy.core.event.origin.Origin

    :return: converted origin 
    :rtype: python dict
    '''


    y2k_phase = {}

    for k,v in y2k_format.items():
        y2k_phase[k] = None

    pick = arrival.pick_id.get_referred_object()
    y2k_phase['sta']  = pick.waveform_id.station_code
    y2k_phase['net']  = pick.waveform_id.network_code
    y2k_phase['chan'] = pick.waveform_id.channel_code
    y2k_phase['loc']  = pick.waveform_id.location_code

    t = {}
    for x in {'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'}:
        t[x] = getattr(pick.time, x)
    y2k_phase['year'] = t['year']
    y2k_phase['moddhhmi'] = "%02d%02d%02d%02d" % (t['month'], t['day'], t['hour'], t['minute'])

    phase = 'P'

    if arrival.phase[0] == 'S':
        phase = 'S'
    onset = " "
    if pick.onset == 'impulsive':
        onset = 'I'
    rmk = '%srmk' % (phase)
    y2k_phase[rmk] = "%1s%1s" % (onset, phase)

    if phase == 'P' and hasattr(pick, 'polarity'):
        if pick.polarity == 'positive':
            y2k_phase['PUpDown'] = 'U'
        elif pick.polarity == 'negative':
            y2k_phase['PUpDown'] = 'D'

    y2k_phase['%ssec' % phase]    = t['second'] + t['microsecond']/1e6
    y2k_phase['%srms' % phase]    = arrival.time_residual
    y2k_phase['%swtUsed' % phase] = arrival.time_weight

    # MTH: Does this need to be flagged phase='S' so that wt=0 --> wt=5 for hypoinv, etc ?
    y2k_phase['%swtCode' % phase] =  obspy_time_error_to_hypoinv_weight(pick.time_errors.uncertainty)

    if arrival.azimuth:
        y2k_phase['Azim']    = "%.2f" % arrival.azimuth
    if arrival.distance:
        y2k_phase['Dist']    = arrival.distance * 111.19 #y2k dist = km vs. obspy dist = deg
    if arrival.takeoff_angle:
        y2k_phase['Angle']   = arrival.takeoff_angle

    return y2k_phase

