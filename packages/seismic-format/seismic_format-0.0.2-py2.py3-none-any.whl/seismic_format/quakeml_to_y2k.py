import os

import logging

from .lib.qml_to_y2k import quakeml_to_y2k
from .lib.liblog import getLogger, processCmdLine

def main():

    logger = getLogger()
    quakemlfile = processCmdLine('quakeml')

    infile = os.path.basename(quakemlfile)
    outfile = infile.replace('.qml', '.y2k')
    if outfile == infile:
        outfile = infile.replace('.xml', '.y2k')
    if outfile == infile:
        logger.info("Infile doesn't have expected suffix (.qml, .xml) --> Add .y2k to infile")
        outfile += ".y2k"

    logger.info("infile=%s --> outfile=./%s" % (quakemlfile, outfile))

    y2k = quakeml_to_y2k(quakemlfile)

    with open(outfile, 'w') as fh:
        fh.write(y2k)

    return

if __name__ == "__main__":
    main()
