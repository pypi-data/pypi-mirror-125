#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seismic_format
----------------------------------

Tests for `seismic_format` module.
"""

import filecmp
import glob
import os
import shutil
import sys
import unittest

import seismic_format
from seismic_format import get_format_dir
from seismic_format.lib.lib_y2k import read_arc_shadow_file
from seismic_format.lib.qml_to_y2k import quakeml_to_y2k
from seismic_format.lib.y2k_to_qml import y2k_to_quakeml, read_format
from seismic_format.lib.liblog import getLogger, processCmdLine
from seismic_format.lib.nordic_to_qml import seisan_to_quakeml

import logging
logger = getLogger()
logger.setLevel(logging.ERROR)

class TestSeismic_format(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
            class setup gets called once
        """
        formats_dir = get_format_dir()
        y2000_format_file = os.path.join(formats_dir, 'format.Y2000_station_archive')
        y2000_header_file = os.path.join(formats_dir, 'format.Y2000_header_archive')
        cls.y2k_format = read_format(y2000_format_file)
        cls.hdr_format = read_format(y2000_header_file)

    def setUp(self):
        """
            self setup gets called for each test
        """
        #formats_dir = get_format_dir()
        #y2000_format_file = os.path.join(formats_dir, 'format.Y2000_station_archive')
        #y2000_header_file = os.path.join(formats_dir, 'format.Y2000_header_archive')
        #self.assertEqual(os.path.isfile(y2000_header_file), 1)
        #self.y2k_format = read_format(y2000_format_file)
        #self.hdr_format = read_format(y2000_header_file)
        self.y2k_format = TestSeismic_format.y2k_format
        self.hdr_format = TestSeismic_format.hdr_format

    def test_read_arc(self):
        (y2k, y2k_origin)  = read_arc_shadow_file('test_data/70014958.y2k', self.y2k_format, self.hdr_format)
        self.assertEqual(y2k_origin['year'], 2020)
        self.assertEqual(y2k_origin['moddhhmi'], '03241839')
        self.assertEqual(y2k_origin['seconds'], 1.06)
        self.assertEqual(y2k_origin['lat_deg'], 35.0)
        self.assertEqual(y2k_origin['ampmag'], -0.64)
        self.assertEqual(y2k_origin['azgap'], 78)

    def test_read_arc_shadow(self):
        (y2k, y2k_origin)  = read_arc_shadow_file('test_data/uu_11121315063_arc2000_AQMS_export', self.y2k_format, self.hdr_format)
        # This also works:
        #assert y2k_origin['year'] == 2011
        self.assertEqual(y2k_origin['year'], 2011)
        self.assertEqual(y2k_origin['moddhhmi'], '12131506')
        self.assertEqual(y2k_origin['min_dist'], 4.0)
        self.assertEqual(y2k_origin['durmag'], 2.04)
        self.assertEqual(y2k_origin['pri_amp_mag_type'], 'L')
        self.assertEqual(y2k_origin['prefmag_label'], 'L')
        self.assertEqual(y2k_origin['prefmag'], 1.78)
        self.assertEqual(y2k_origin['alt_dur_mag'], 1.95)

        #self.assertEqual(chan_code[0], band_char, 'Channel code and band code are not equal.')

    def test_quakeml_to_y2k(self):
        infile  = 'test_data/70014958.qml'
        outfile = '70014958.y2k'
        y2k = quakeml_to_y2k(infile)
        with open(outfile, 'w') as fh:
            fh.write(y2k)
        #assert filecmp.cmp('test_data/70014958.y2k', outfile)
        self.assertEqual(filecmp.cmp('test_data/70014958.y2k', outfile), 1)


    def test_y2k_to_quakeml(self):
        infile  = 'test_data/70014958.y2k'
        outfile = '70014958.qml'
        cat = y2k_to_quakeml(infile)
        cat.write(outfile, format="QUAKEML")

        for arr in cat.events[0].preferred_origin().arrivals:
            pk = arr.pick_id.get_referred_object()
            h = pk.waveform_id
            if h.station_code == 'KB04' and h.channel_code == 'HHZ':
                self.assertEqual(pk.time_errors.uncertainty, 0.3)

    def test_seisan_to_quakeml(self):
        seisanfile = 'test_data/22-0106-00L.S202004'
        seisanfile = 'test_data/30-0653-00L.S201904.paul'
        qmlfile = '%s.qml' % os.path.basename(seisanfile)

        sys.argv = ['seisan-to-quakeml', '--infile', seisanfile,
                    #'--network-code=OK', '--fix-amptype',
                    '--loglevel=WARNING',
                    ]
        infile, args = processCmdLine('infile')
        cat = seisan_to_quakeml(infile, args)
        #cat.write(qmlfile, format="QUAKEML")
        for arr in cat.events[0].preferred_origin().arrivals:
            pk = arr.pick_id.get_referred_object()
            self.assertGreater(pk.time_errors.uncertainty, .001)

    def test_something(self):
        assert(seismic_format.__version__)


    @classmethod
    def tearDownClass(cls):
        files = glob.glob('70014958.*')
        for f in files:
            #print("Now remove file:%s" % f)
            os.remove(f)

if __name__ == "__main__":
    unittest.main()
