from __future__ import division

import unittest

import adastra.svg.store as store

import glob
from lxml import etree
from lxml.etree import ElementTree
import os 
from tempfile import TemporaryFile

class StoreTest(unittest.TestCase):
    
    def setUp(self):
        self.dirname = os.path.dirname(__file__)
        self.svg = store.load(os.path.join(self.dirname, 'store_test.svg'))
        self.paths = self.svg.groups['foo'].paths

    def testSize(self):
        self.assertEqual(self.svg.size, (450,400))

    def testScale(self):
        self.assertEqual(self.svg.scale, 0.1)

    def testTranslate(self):
        self.assertEqual(self.svg.translate, (-80, -310))

    def testPathPoints(self):
        self.assertEqual(self.paths[0].points, [(100,310), (80,270), (60,310)])

    def testClosedPathRemovesFinalPoint(self):
        self.assertEqual(self.paths[1].points, [(110,350), (100,310), (90,330)])

        
    def testFilledPath(self):
        self.assertEqual(self.paths[0].fill, (1, 0, 1))

    def testUnfilledPath(self):
        self.assertEqual(self.paths[1].fill, None)

    def testStrokedPath(self):
        self.assertEqual(self.paths[0].stroke, (0, 1, 0))

    def testUnstrokedPath(self):
        self.assertEqual(self.paths[1].stroke, None)

    def testPathWithID(self):
        self.assertEqual(self.paths[0].id, 'command_module')

    def testPathWithoutID(self):
        self.assertEqual(self.paths[1].id, None)

    def testPathFromSecondGroup(self):
        self.assertEqual(self.svg.groups['bar'].paths[0].points, [(1,2), (3,4), (5,6)])

    def testPathWithoutData(self):
        self.assertEqual(self.paths[1].data, None)

    def testPathWithSingleDataItem(self):
        data = self.paths[0].data
        self.assertEqual(data, {'key': 'value'})

    def testPathWithMultipleDataItems(self):
        data = self.svg.groups['bar'].paths[0].data
        self.assertEqual(data, {'key1': 'value1', 'key2': 'value2'})

    def testRoundTrip(self):
        filename = os.path.join(self.dirname, 'roundtrip_test.svg')
        tempfile = TemporaryFile()
        store.save(store.load(filename), tempfile)
        tempfile.seek(0)

        old_svg_xml = etree.parse(filename)
        new_svg_xml = etree.parse(tempfile)
        self.assertEqual(etree.tostring(new_svg_xml, pretty_print=True), 
                         etree.tostring(old_svg_xml, pretty_print=True))