import unittest

from adastra.svg_loader import load_svg

class Test(unittest.TestCase):

    def testTrianglePath(self):
        paths = load_svg('triangle_path.svg')
        self.assertEqual(paths[0].points, [(100,100), (50,150), (150,150)])
        
    def testPolygonPath(self):
        paths = load_svg('polygon_path.svg')
        self.assertEqual(paths[0].points, [(88.55,89.4), (64,112), (73.01,143.97), (101.50,160.54), (134,151), (125,116), (88.70,89.455613)])

    def testFilledPath(self):
        paths = load_svg('filled_path.svg')
        self.assertEqual(paths[0].fill, '#ABCDEF')

    def testStrokedPath(self):
        paths = load_svg ('stroked_path.svg')
        self.assertEqual(paths[0].stroke, '#998877')

    def testMultiplePaths(self):
        paths = load_svg ('multiple_paths.svg')
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0].points, [(100,100), (50,150), (150,150)])
        self.assertEqual(paths[1].points, [(200,200), (50,150), (250,250)])
