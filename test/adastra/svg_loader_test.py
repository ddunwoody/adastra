import unittest

from adastra.svg_loader import load_svg

class SvgLoaderTest(unittest.TestCase):

    def testTrianglePath(self):
        path = load_svg('triangle_path.svg')
        self.assertEqual(path.points, [(100,100), (50,150), (150,150)])
        
    def testPolygonPath(self):
        path = load_svg('polygon_path.svg')
        self.assertEqual(path.points, [(88.55,89.4), (64,112), (73.01,143.97), (101.50,160.54), (134,151), (125,116), (88.70,89.455613)])

    def testFilledPath(self):
        path = load_svg('filled_path.svg')
        self.assertEqual(path.fill, '#ABCDEF')

    def testStrokedPath(self):
        path = load_svg ('stroked_path.svg')
        self.assertEqual(path.stroke, '#998877')
