from __future__ import division

import unittest

from adastra.svg_loader import load_svg
from adastra.svg_saver import save_svg

import glob
from lxml import etree
from lxml.etree import ElementTree 
from tempfile import TemporaryFile

class SvgSaverTest(unittest.TestCase):

    def testSized(self):
        for filename in glob.glob('svg_loader/*.svg'):
            loaded_svg = load_svg(filename)
            tempfile = TemporaryFile()
            save_svg(loaded_svg, tempfile)
            tempfile.seek(0)
    
            old_svg_xml = etree.parse(filename)
            new_svg_xml = etree.parse(tempfile)
            print 'comparing %s' % filename
            self.assertEqual(etree.tostring(new_svg_xml, pretty_print=True), 
                             etree.tostring(old_svg_xml, pretty_print=True))