import logging
import os
import sys

DEFAULT_LOG_LEVEL = 'INFO'

# logging.getLogger() will return the root logger of the parent calling func
#   if it wasn't configured (no handlers) then we'll add a default console handler
def getLogger():
    logger = logging.getLogger()
    if len(logger.handlers) == 0:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)7s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        #logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.getLevelName(DEFAULT_LOG_LEVEL))
    return logger



import argparse
def processCmdLine(fname):
    '''
    Pass in fname to build argparse option: >cmd.py --fname=....
       and return the path in fname
    '''

    logger = getLogger()

    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")

    #required.add_argument("--y2kfile", type=str, metavar='Path to y2k arc file', required=True)
    file_arg = "--" + fname
    required.add_argument(file_arg, type=str, metavar='Path to input file', required=True)
    optional.add_argument("--loglevel", type=str, metavar='LOGLEVEL: INFO, WARN, etc')
    optional.add_argument("--network-code", type=str, metavar='Hard-code network code in output quakeml file')
    optional.add_argument("--fix-amptype", action='store_true')
    args, unknown = parser.parse_known_args()

    usage = "Usage: %s --loglevel=WARN --network-code TX --fix-amptype" % os.path.basename(sys.argv[0])

    if unknown:
        for k in unknown:
            print("Unknown arg:%s" % k)
        print(usage)
        exit(2)


    loglevels = {"ERROR": logging.ERROR,
                 "WARN": logging.WARNING,
                 "WARNING": logging.WARNING,
                 "INFO": logging.INFO,
                 "DEBUG": logging.DEBUG,
                 "CRITICAL": logging.CRITICAL,
                }
    msg = " ".join(list(loglevels.keys()))

    loglevel = None
    if args.loglevel:
        if args.loglevel in loglevels:
            loglevel = loglevels[args.loglevel]
        else:
            logger.warning("Unknown --loglevel=%s (not in:{%s}) --> Use default loglevel=%s" % 
                        (args.loglevel, msg, DEFAULT_LOG_LEVEL))
            loglevel = None

    if loglevel:
        logger.setLevel(loglevel)

    return getattr(args, fname), args


if __name__ == "__main__":
    main()

