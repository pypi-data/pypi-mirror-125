===============================
Seismic Format Converter
===============================

.. image:: https://img.shields.io/travis/mhagerty/seismic-format.svg
        :target: https://travis-ci.org/mhagerty/seismic-format

.. image:: https://img.shields.io/pypi/v/seismic-format.svg
        :target: https://pypi.python.org/pypi/seismic-format


Collection of tools for converting between different seismic formats (arc2000, quakeml, seisan)

* Free software: MIT license
* Documentation: (COMING SOON!) https://seismic-format.readthedocs.org.

Installation
-------------

      >pip install some_path_to_whl

Usage
-----------

The pip install makes 3 command-line scripts available on your path:

      >y2k-to-quakeml --y2kfile=path_to_your_arc_file

      >quakeml-to-y2k --quakeml=path_to_your_qml_file

      >seisan_to-quakeml --infile=path_to_your_seisan_file

To set the quakeml network-code and to fix amptype to 'WAS' (unit='other') do:

      >seisan-to-quakeml --infile test.y2k --network-code TX --fix-amptype



