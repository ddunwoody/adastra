import unittest

from adastra.svg.Path import *
from adastra.svg.Svg import *

class SvgTest(unittest.TestCase):

    def testDoesNothingIfNoScaleOrTranslatePresent(self):
        svg = Svg()
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        self.assertEqual(points, [(1,2), (3,4), (5,6)])

    def testTranslatesPath(self):
        svg = Svg()
        svg.translate = (-3,-3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        self.assertEqual(points, [(-2,-1), (0,1), (2,3)])

    def testAppliesTransformToMultiplePaths(self):
        svg = Svg()
        svg.translate = (-3,-3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)]),
                     Path(points=[(7,8), (9,1), (2,3)])]
        paths = svg.transformed_paths()
        self.assertEqual(paths[0].points, [(-2,-1), (0,1), (2,3)])
        self.assertEqual(paths[1].points, [(4,5), (6,-2), (-1,0)])

    def testTranslatesPathOnlyOnce(self):
        svg = Svg()
        svg.translate = (-3,-3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]

        points = svg.transformed_paths()[0].points
        self.assertEqual(points, [(-2,-1), (0,1), (2,3)])

        points = svg.transformed_paths()[0].points
        self.assertEqual(points, [(-2,-1), (0,1), (2,3)])

    def testPreservesAttributesOnPath(self):
        svg = Svg()
        svg.translate = (-3,-3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        svg.paths[0].label = 'foo'

        label = svg.transformed_paths()[0].label
        self.assertEqual(label, 'foo')

    def testScalesPath(self):
        svg = Svg()
        svg.scale = 0.2
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        for actual, expected in zip(points, [(0.2,0.4), (0.6,0.8), (1.0,1.2)]):
            self.assertAlmostEqual(actual[0], expected[0])
            self.assertAlmostEqual(actual[1], expected[1])
            
    def testScalesAndTranslatesPath(self):
        svg = Svg()
        svg.scale = 0.1
        svg.translate = (-3, -4)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.transformed_paths()[0].points
        for actual, expected in zip(points, [(-0.2, -0.2), (0, 0), (0.2,0.2)]):
            self.assertEqual(actual[0], expected[0])
            self.assertEqual(actual[1], expected[1])
