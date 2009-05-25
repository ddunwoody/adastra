import unittest

from adastra.svg.Path import *
from adastra.svg.Svg import *

class SvgTest(unittest.TestCase):

    def testFlipsYAxisOnlyIfScaleAndTranslateNotSet(self):
        svg = Svg()
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        self.assertEqual(points, [(1,-2), (3,-4), (5,-6)])

    def testTranslatesPathAndFlipsY(self):
        svg = Svg()
        svg.translate = (-3,-3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        self.assertEqual(points, [(-2,1), (0,-1), (2,-3)])

    def testAppliesTransformToMultiplePaths(self):
        svg = Svg()
        svg.translate = (1,2)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)]),
                     Path(points=[(7,8), (9,1), (2,3)])]
        paths = svg.transformed_paths()
        self.assertEqual(paths[0].points, [(2,-4), (4,-6), (6,-8)])
        self.assertEqual(paths[1].points, [(8,-10), (10,-3), (3,-5)])

    def testScalesPath(self):
        svg = Svg()
        svg.scale = 0.2
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        for actual, expected in zip(points, [(0.2,-0.4), (0.6,-0.8), (1.0,-1.2)]):
            self.assertAlmostEqual(actual[0], expected[0])
            self.assertAlmostEqual(actual[1], expected[1])

    def testAppliesScaleToMultiplePaths(self):
        svg = Svg()
        svg.scale = 10
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)]),
                     Path(points=[(7,8), (9,1), (2,3)])]
        paths = svg.transformed_paths()
        self.assertEqual(paths[0].points, [(10,-20), (30,-40), (50,-60)])
        self.assertEqual(paths[1].points, [(70,-80), (90,-10), (20,-30)])

    def testPreservesAttributesOnPath(self):
        svg = Svg()
        svg.translate = (-3,-3)
        svg.paths = [Path(points=[])]
        svg.paths[0].label = 'foo'

        label = svg.transformed_paths()[0].label
        self.assertEqual(label, 'foo')

    def testScalesAndTranslatesPath(self):
        svg = Svg()
        svg.scale = 0.1
        svg.translate = (-3, -4)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        for actual, expected in zip(points, [(-0.2, 0.2), (0, 0), (0.2,-0.2)]):
            self.assertEqual(actual[0], expected[0])
            self.assertEqual(actual[1], expected[1])
