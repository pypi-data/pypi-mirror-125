import os

from .lib.liblog import getLogger, processCmdLine
from .lib.nordic_to_qml import seisan_to_quakeml

def main():

    logger = getLogger()

    seisan_file, args = processCmdLine('infile')

    infile = os.path.basename(seisan_file)
    # What do seisan files end with ???????
    outfile = infile.replace('.y2k','.qml')
    if outfile == infile:
        logger.info("Infile doesn't have expected .y2k suffix --> Add .qml to infile")
        outfile += ".qml"

    logger.info("infile=%s --> outfile=./%s" % (seisan_file, outfile))

    cat = seisan_to_quakeml(seisan_file, args)
    cat.write(outfile, format="QUAKEML")

    return

if __name__ == "__main__":
    main()
