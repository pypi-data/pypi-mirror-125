from .liblog import getLogger
logger = getLogger()

'''
  Hypoinverse/Nordic-type4    aqms-pdl ObsPy map           AQMS db
    Weighting-indicator     obspy.pick.time_error       Arrival.quality
        P              S
    ==============   =====    ============              ===========
        0 or blank     5        <= 0.06                     1.0         Best
        1              6        <= 0.12                     0.75
        2              7        <= 0.30                     0.50
        3              8        <= 0.60                     0.25
        4              9         > 0.60                     0.10        Worst
'''
weight_to_error = {
    0: 0.06,
    1: 0.12,
    2: 0.30,
    3: 0.60,
    4: 0.65,
}


def hypoinv_weight_to_obspy_time_error(weight):

    fname = 'hypoinv_weight_to_obspy_time_error'
                                                 # Seisan blank or 0 = full weight
    if (isinstance(weight, str) and len(weight.strip()) == 0) or \
       (isinstance(weight, int) and weight == -9): # but y2k reader sets empty fields = -9
        weight = 0

    try:
        wt = int(weight)
    except:
        logger.error("Can't convert int weight=[%s] to time_error!" % weight)
        raise

    if wt > 9:
        logger.error("weight=[%d] > 9 --> mapping only goes up to 9!" % wt)
        exit(2)

    if wt > 4:
        wt = wt - 5

    logger.info("%s: wt:%d --> time_error:%.2f" % (fname, weight, weight_to_error[wt]))
    #print("%s: wt:%d --> time_error:%.2f" % (fname, weight, weight_to_error[wt]))

    return weight_to_error[wt]


def obspy_time_error_to_hypoinv_weight(time_error):

    fname = 'obspy_time_error_to_hypoinv_weight'

    try:
        x = float(time_error)
    except:
        logger.error("Can't convert time_error=[%s] to float!" % time_error)
        raise

    # dict keys are only sorted for python >= 3.7
    for wt in sorted(weight_to_error.keys()):
        if float(time_error) <= weight_to_error[wt]:
            #print("time_error:%f <= wt_to_error[%d]=%f" %
                  #(time_error, wt, weight_to_error[wt]))
            return wt

    return sorted(weight_to_error.keys())[-1]

