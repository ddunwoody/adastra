from __future__ import division

import unittest

import adastra.svg.store as store

import glob
from lxml import etree
from lxml.etree import ElementTree 
from tempfile import TemporaryFile

class ContentTest(unittest.TestCase):

    def testSize(self):
        size = store.load('files/sized.svg').size
        self.assertEqual(size, (123,456))

    def testSvgTrianglePath(self):
        path = store.load('files/triangle_path.svg').paths[0]
        self.assertEqual(path.points, [(100,100), (50,150), (150,150)])
        
    def testPolygonPath(self):
        path = store.load('files/polygon_path.svg').paths[0]
        self.assertEqual(path.points, [(89, 89), (64, 112), (73, 144), (102, 161), (134, 151), (125, 116)])

    def testFilledPath(self):
        path = store.load('files/filled_path.svg').paths[0]
        self.assertEqual(path.fill, (1, 0, 1))

    def testStrokedPath(self):
        path = store.load('files/stroked_path.svg').paths[0]
        self.assertEqual(path.stroke, (0, 1, 0))

    def testMultiplePaths(self):
        paths = store.load('files/multiple_paths.svg').paths
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0].points, [(100,100), (50,150), (150,150)])
        self.assertEqual(paths[1].points, [(200,200), (50,250), (250,250)])
        
    def testInkscapeLabelledPath(self):
        path = store.load('files/inkscape_labelled_path.svg').paths[0]
        self.assertEqual(path.label, 'foo')

    def testPathWithID(self):
        path = store.load('files/path_with_id.svg').paths[0]
        self.assertEqual(path.id, 'id_value')

    def testScaled(self):
        scale = store.load('files/scaled.svg').scale
        self.assertEqual(scale, 0.2)

    def testTranslated(self):
        translate = store.load('files/translated.svg').translate
        self.assertEqual(translate, (-100, 150))

    def testScaledAndTranslated(self):
        svg = store.load('files/scaled_and_translated.svg')
        self.assertEqual(svg.scale, 0.2)
        self.assertEqual(svg.translate, (-100, 150))

    def testRoundTrip(self):
        for filename in glob.glob('files/*.svg'):
            loaded_svg = store.load(filename)
            tempfile = TemporaryFile()
            store.save(loaded_svg, tempfile)
            tempfile.seek(0)
    
            old_svg_xml = etree.parse(filename)
            new_svg_xml = etree.parse(tempfile)
            print 'comparing %s' % filename
            self.assertEqual(etree.tostring(new_svg_xml, pretty_print=True), 
                             etree.tostring(old_svg_xml, pretty_print=True))