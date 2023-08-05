
import sys
import os

import collections
import math

from .liblog import getLogger

logger = getLogger()


def x_to_a(field_len, x):

    if abs(x) >= math.pow(10., field_len - 1):
        ndec = 0
    elif abs(x) >= 1:
        ndec = field_len - int(math.log10(abs(x))) - 2
        if ndec == 0:
            ndec = 1
    else:
        ndec = field_len - 1

    #if x < 0:
        #ndec -= 1

    xx = "%.*f" % (ndec, x)
    a  = str(xx)

    if x < 1:
        a = a.replace('0', '', 1)
    if len(a) > field_len:
        a = a[0:field_len]

    if len(a) != field_len:
        raise Exception
    else:
        return a

def new_y2k_line(y2kformat):
    d=collections.OrderedDict()
    #for key, value in y2kformat.iteritems():
    for key, value in y2kformat.items():
        d[key] = None
        #d[key] = printf("%*s" % (value['len'], ' '))
    return d

def write_y2000_phase(dformat, arrival):

    #print '1234567890123456789012345678901234567890123456789012345678901234567890'

    buf = ""

    for k, val in dformat.items():

        format = dformat[k]['format']
        w  = dformat[k]['len']

        # print("k=%s val=%s format=%s width=%d" % (k, val, dformat[k]['format'], w))

        if k[0:5] == 'blank' or arrival[k] is None or arrival[k] == '' or arrival[k] == -9:
            buf += ("%-*s" % (w, ' '))
        else:
            if format[0:1] == 'A':
                if val['align'] == 'R':
                    buf += ("%*s" % (w, str(arrival[k])))
                else:
                    buf += ("%-*s" % (w, str(arrival[k])))

            elif format[0:1] == 'I':
                if val['align'] == 'R':
                    buf += ("%*s" % (w, int(arrival[k])))
                else:
                    buf += ("%-*s" % (w, int(arrival[k])))

            elif format[0:1] == 'F':
                (field_len, ndec) = format[1:4].split('.')
                #print "format=%s field_len=%s ndec=%s" % (format, field_len, ndec)
                field_len = int(field_len)
                ndec = int(ndec)

                if k == 'Amp': 
                    buf += ("%*s" % (w, x_to_a(field_len, arrival[k])))
                else: 
                    data = float(arrival[k])*math.pow(10., ndec)
                    #print "k=[%s] arrival[k]=[%s] data=%.0f" % (k, arrival[k], data)
                    if val['align'] == 'R':
                        #printf("%*s" % (w, string))
                        a = "%*.0f" % (w, (data))
                        if len(a) > field_len:
                            #print "Houston we have a problem a=[%s]" % a
                            buf += ("%*s" % (w, x_to_a(field_len, arrival[k])))
                        else:
                            buf += ("%*.0f" % (w, (data)))
                    else:
                        #printf("%-*s" % (w, string))
                        a = "%-*.0f" % (w, (data))
                        if len(a) > field_len:
                            #print "Houston we have a problem a=[%s]" % a
                            buf += ("%*s" % (w, x_to_a(field_len, arrival[k])))
                        else:
                            buf += ("%-*.0f" % (w, (data)))
    buf += ("\n")
    return buf

def parse_y2k_line(line, hformat):
   dd = collections.OrderedDict()
   #for key, value in hformat.iteritems():
   #print("parse line=[%s]" % line)
   for key, value in hformat.items():
        i1 = value['start']-1
        i2 = i1 + value['len']
        data = line[i1:i2]
        form = value['format']
        #print("key=%s value=%s i1=%d i2=%d data=%s" % (key, value, i1, i2, data))

        if form[0] == 'A':
            dd[key] = data.strip()
	#MTH: hack to allow Prmk/Srmk to have leading blank - eg, Prmk=' P' or Prmk='iP', etc
            if key == 'Prmk' or key == 'Srmk':
                dd[key] = data
        elif form[0] == 'I':
            if not any(str.isdigit(c) for c in data):
                dd[key] = -9
                continue
            else:
                try:
                    data = int(data)
                    dd[key] = data
                except ValueError as e:
                    raise
        elif form[0] == 'F':
#MTH: What to do if field is empty in original y2000 file ?  
#     Flag with -9 and then don't print it ??
            if not any(str.isdigit(c) for c in data):
                dd[key] = -9
                #continue
            else:
                (foo, ndec) = form.split('.')
                try:
                    if '.' in data: # Try to read in float directly
                        data = float(data)
                    else:           # Read in int and convert using format specifier
                        ndec = int(ndec)
                        data = float(data)/math.pow(10., ndec)
                    dd[key] = data
                except Exception as e:
                    raise

        #endif form[0] == 'F'
        dd['string'] = line
   return dd


def read_format(file):
    d=collections.OrderedDict()
    f=open(file, 'r')
    #Skip first 4 lines
    lines=f.readlines()[4:]
    nblank=1
    for line in lines:
        line = line.rstrip('\n\r')
        parsedLine = line.split()
        if len(parsedLine) < 5:
            print("Error with line=[%s]" % line)
        else:
            try:
                col_start = int(parsedLine[0])
                col_len   = int(parsedLine[1])
                col_format= parsedLine[2]
                col_align = parsedLine[3]
                col_field = parsedLine[4]
                if col_field == 'blank':
                    col_field = 'blank%d' % nblank
                    nblank += 1
                if col_field == 'Free':
                    col_field = 'Free%d' % nblank
                    nblank += 1
                    #continue
                #else:
                dd = {}
                dd['start'] = col_start
                dd['len']   = col_len
                dd['format']= col_format
                dd['align'] = col_align
                d[col_field] = dd
            except:
                print("Exception!")
                print("parsedLine=[%s]" % parsedLine)

    f.close()
    return d


def printf(format, *args):
    sys.stdout.write(format % args)


def read_arc_shadow_file(file, dformat, hformat):
    fname = 'read_arc_shadow_file'
    d={}
    phase_list=[]
    #logger.info("Enter read_arc_shadow_file")
    try:
        f=open(file, 'r')
        # Read in origin/header line:
        origin = f.readline().rstrip('\n\r')
        origin_dict = parse_y2k_line(origin, hformat)
        origin_dict['string'] = origin
        lines=f.readlines()
    except (OSError, IOError) as e:
        logger.error("%s.%s: Attempt to read phase file=[%s] gives error=[%s]" % (__name__, fname, file, e))
        return None, None
    finally:
        f.close()

    if len(lines) == 0:
        logger.error("%s.%s: phase file=[%s] appears to be empty!" % (__name__, fname, file))
        exit(2)

    current_sta=''

    for line in lines:
        line = line.rstrip('\n\r')
        if not line:
            continue
        if line[0] == '$': #Read shadow line
            if len(line) < 2: #Empty shadow line
                continue
            elif len(line) == 34: #Current length of non-empty shadow lines - Does this vary ?
                (yyyymmddhhmi, alpha, logA0, beg, end) = read_coda_shadow(line[1:])
                coda_dict = {}
                coda_dict['yyyymmddhhmi'] = yyyymmddhhmi
                coda_dict['alpha'] = alpha
                coda_dict['logA0'] = logA0
                coda_dict['beg'] = beg
                coda_dict['end'] = end
                dd['coda'] = coda_dict
                continue
            else:
                logger.error("%s.%s: Expecting 34-char shadow line but len=[%d] line=[%s]" % \
                            (__name__, fname, len(line), line))

        else:
            dd = parse_y2k_line(line, dformat)
            current_sta = dd['sta']

        d[(dd['sta'], dd['chan'])] = dd
        phase_list.append(dd)
        #d[dd['sta']] = dd

    # Rekey from sta --> chan --> params & sort
    temp   = collections.OrderedDict(sorted(d.items()))
    phases = collections.OrderedDict()

    for (sta,chan) in temp:
        if not sta in phases:
            phases[sta] = collections.OrderedDict()
        phases[sta][chan] = temp[(sta,chan)]

    #return phases, origin
    #logger.info("DONE read_arc_shadow_file")
    # MTH: 2020-08-26 phases = dict[sta][cha] of arrivals while phase_list = [arrival] ordered as in arcfile
    #return phases, origin_dict
    return phase_list, origin_dict


def read_coda_shadow(buf):
    '''
Use the following format for the shadow line, which is similar to the format in which these data are stored in the modified UW1-format files.

Columns Format  Description
3-14     I4, 4I2  Reference date-time in the form YYYYMMDDHHMM where YYYY, MM, DD, HH, MM are 
                    the UTC year, month, day, hour, and minute
16-20    F5.2     Alpha (called Qfree by Jiggle), which is the decay constant in the coda 
                    decay function A0(t-tp)-alpha, where t is time and tp is the P-wave arrival time
22-26    F5.2     log(A0) (called Afree by Jiggle), where A0 is the amplitude constant in 
                    the coda decay function
28-30    I3       Begin time for coda-decay analysis in seconds relative to the reference time
32-34    I3       End time for coda-decay analysis in seconds relative to the reference time

12345678901234
$ 201112131506  1.50  4.31  75  94
    '''
    fname = 'read_coda_shadow'

    fields = buf.split()
    if len(fields) != 5:
        logger.error("%s: len(fields) != 5" % fname)
    else:
        (yyyymmddhhmi, alpha, logA0, beg, end) = fields
        try:
            yyyymmddhhmi = int(yyyymmddhhmi)
            alpha = float(alpha)
            logA0 = float(logA0)
            beg = int(beg)
            end = int(end)
        except (ValueError) as e:
            logger.error("%s.%s: Attempt to read shadow line=[%s] gives error=[%s]" % (__name__, fname, buf, e))
            raise

    return (yyyymmddhhmi, alpha, logA0, beg, end)

def write_coda_shadow(val, yyyymmddhhmi):
    '''
Use the following format for the shadow line, which is similar to the format in which these data are stored in the modified UW1-format files.

Columns Format  Description
3-14     I4, 4I2  Reference date-time in the form YYYYMMDDHHMM where YYYY, MM, DD, HH, MM are 
                    the UTC year, month, day, hour, and minute
16-20    F5.2     Alpha (called Qfree by Jiggle), which is the decay constant in the coda 
                    decay function A0(t-tp)-alpha, where t is time and tp is the P-wave arrival time
22-26    F5.2     log(A0) (called Afree by Jiggle), where A0 is the amplitude constant in 
                    the coda decay function
28-30    I3       Begin time for coda-decay analysis in seconds relative to the reference time
32-34    I3       End time for coda-decay analysis in seconds relative to the reference time

12345678901234
$ 201112131506  1.50  4.31  75  94
    '''

    printf("$ %12s %5.2f %5.2f %3d %3d\n" % (yyyymmddhhmi, val['alpha'], val['logA0'], val['beg'], val['end'])) 

    return


