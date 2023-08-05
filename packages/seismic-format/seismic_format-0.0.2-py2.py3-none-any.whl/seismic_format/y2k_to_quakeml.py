import os

# Quiet down matplotlib msgs (obspy must import matplotlib with logLevel=DEBUG)
#import logging
#logger = logging.getLogger('matplotlib')
#logger.setLevel(logging.WARNING)

from obspy.core.event import Catalog
from obspy.core.event import read_events
from obspy.core.event.event import Event
from obspy.core.event.magnitude import Magnitude

from .lib.liblog import getLogger, processCmdLine
from .lib.y2k_to_qml import y2k_to_quakeml

def main():

    logger = getLogger()
    arc_file, args = processCmdLine('y2kfile')

    infile = os.path.basename(arc_file)
    outfile = infile.replace('.y2k','.qml')
    if outfile == infile:
        logger.info("Infile doesn't have expected .y2k suffix --> Add .qml to infile")
        outfile += ".qml"

    logger.info("infile=%s --> outfile=./%s" % (arc_file, outfile))

    cat = y2k_to_quakeml(arc_file)
    cat.write(outfile, format="QUAKEML")

    return

if __name__ == "__main__":
    main()
