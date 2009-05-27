from __future__ import division

import unittest

import adastra.svg.store as store

import glob
from lxml import etree
from lxml.etree import ElementTree 
from tempfile import TemporaryFile

class StoreTest(unittest.TestCase):
    
    def setUp(self):
        self.svg = store.load('store_test.svg')

    def testSvgSize(self):
        self.assertEqual(self.svg.size, (450,400))

    def testPathPoints(self):
        self.assertEqual(self.svg.paths[0].points, [(100,310), (80,270), (60,310)])

    def testClosedPathRemovesFinalPoint(self):
        self.assertEqual(self.svg.paths[1].points, [(110,350), (100,310), (90,330)])
        
    def testFilledPath(self):
        self.assertEqual(self.svg.paths[0].fill, (1, 0, 1))

    def testUnfilledPath(self):
        self.assertEqual(self.svg.paths[1].fill, None)

    def testStrokedPath(self):
        self.assertEqual(self.svg.paths[0].stroke, (0, 1, 0))

    def testUnstrokedPath(self):
        self.assertEqual(self.svg.paths[1].stroke, None)

    def testLabelledPath(self):
        self.assertEqual(self.svg.paths[0].label, 'metal')

    def testUnlabelledPath(self):
        self.assertEqual(self.svg.paths[1].label, None)

    def testPathWithID(self):
        self.assertEqual(self.svg.paths[0].id, 'command_module')

    def testPathWithoutID(self):
        self.assertEqual(self.svg.paths[1].id, None)

    def testScale(self):
        self.assertEqual(self.svg.scale, 0.1)

    def testTranslate(self):
        self.assertEqual(self.svg.translate, (-80, -310))

    def testRoundTrip(self):
        filename = 'roundtrip_test.svg'
        tempfile = TemporaryFile()
        store.save(store.load(filename), tempfile)
        tempfile.seek(0)

        old_svg_xml = etree.parse(filename)
        new_svg_xml = etree.parse(tempfile)
        self.assertEqual(etree.tostring(new_svg_xml, pretty_print=True), 
                         etree.tostring(old_svg_xml, pretty_print=True))