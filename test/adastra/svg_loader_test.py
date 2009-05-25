from __future__ import division

import unittest

from adastra.svg_loader import load_svg

class SvgLoaderTest(unittest.TestCase):

    def testSize(self):
        size = load_svg('svg_loader/sized.svg').size
        self.assertEqual(size, (123,456))

    def testTrianglePath(self):
        path = load_svg('svg_loader/triangle_path.svg').paths[0]
        self.assertEqual(path.points, [(100,100), (50,150), (150,150)])
        
    def testPolygonPath(self):
        path = load_svg('svg_loader/polygon_path.svg').paths[0]
        self.assertEqual(path.points, [(89, 89), (64, 112), (73, 144), (102, 161), (134, 151), (125, 116)])

    def testFilledPath(self):
        path = load_svg('svg_loader/filled_path.svg').paths[0]
        self.assertEqual(path.fill, (1, 0, 1))

    def testStrokedPath(self):
        path = load_svg('svg_loader/stroked_path.svg').paths[0]
        self.assertEqual(path.stroke, (0, 1, 0))

    def testMultiplePaths(self):
        paths = load_svg('svg_loader/multiple_paths.svg').paths
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0].points, [(100,100), (50,150), (150,150)])
        self.assertEqual(paths[1].points, [(200,200), (50,250), (250,250)])
        
    def testInkscapeLabelledPath(self):
        path = load_svg('svg_loader/inkscape_labelled_path.svg').paths[0]
        self.assertEqual(path.label, 'foo')

    def testPathWithID(self):
        path = load_svg('svg_loader/path_with_id.svg').paths[0]
        self.assertEqual(path.id, 'id_value')

    def testScaled(self):
        scale = load_svg('svg_loader/scaled.svg').scale
        self.assertEqual(scale, 0.2)

    def testTranslated(self):
        translate = load_svg('svg_loader/translated.svg').translate
        self.assertEqual(translate, (-100, 150))

    def testScaledAndTranslated(self):
        svg = load_svg('svg_loader/scaled_and_translated.svg')
        self.assertEqual(svg.scale, 0.2)
        self.assertEqual(svg.translate, (-100, 150))

