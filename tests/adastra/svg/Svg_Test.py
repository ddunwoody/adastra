import unittest

from adastra.svg.Group import *
from adastra.svg.Path import *
from adastra.svg.Svg import *

class SvgTest(unittest.TestCase):
    
    def setUp(self):
        self.svg = Svg()
        self.group = Group()
        self.svg.groups['test'] = self.group
    
    def testFlipsYAxisOnlyIfScaleAndTranslateNotSet(self):
        self.group.paths = [Path([(1,2), (3,4), (5,6)])]
        points = self.svg.paths('test')[0].points
        self.assertEqual(points, [(1,-2), (3,-4), (5,-6)])

    def testTranslatesPathAndFlipsY(self):
        self.svg.translate = (-3,-3)
        self.group.paths = [Path([(1,2), (3,4), (5,6)])]
        points = self.svg.paths('test')[0].points
        self.assertEqual(points, [(-2,1), (0,-1), (2,-3)])

    def testAppliesTransformToMultiplePaths(self):
        self.svg.translate = (1,2)
        self.group.paths = [Path([(1,2), (3,4), (5,6)]),
                     Path([(7,8), (9,1), (2,3)])]
        paths = self.svg.paths('test')
        self.assertEqual(paths[0].points, [(2,-4), (4,-6), (6,-8)])
        self.assertEqual(paths[1].points, [(8,-10), (10,-3), (3,-5)])

    def testScalesPath(self):
        self.svg.scale = 0.2
        self.group.paths = [Path([(1,2), (3,4), (5,6)])]
        points = self.svg.paths('test')[0].points
        for actual, expected in zip(points, [(0.2,-0.4), (0.6,-0.8), (1.0,-1.2)]):
            self.assertAlmostEqual(actual[0], expected[0])
            self.assertAlmostEqual(actual[1], expected[1])

    def testAppliesScaleToMultiplePaths(self):
        self.svg.scale = 10
        self.group.paths = [Path([(1,2), (3,4), (5,6)]),
                     Path([(7,8), (9,1), (2,3)])]
        paths = self.svg.paths('test')
        self.assertEqual(paths[0].points, [(10,-20), (30,-40), (50,-60)])
        self.assertEqual(paths[1].points, [(70,-80), (90,-10), (20,-30)])

    def testPreservesAttributesOnPath(self):
        self.svg.translate = (-3,-3)
        self.group.paths = [Path()]
        self.group.paths[0].label = 'foo'

        label = self.svg.paths('test')[0].label
        self.assertEqual(label, 'foo')

    def testScalesAndTranslatesPath(self):
        self.svg.scale = 0.1
        self.svg.translate = (-3, -4)
        self.group.paths = [Path([(1,2), (3,4), (5,6)])]
        points = self.svg.paths('test')[0].points
        for actual, expected in zip(points, [(-0.2, 0.2), (0, 0), (0.2,-0.2)]):
            self.assertEqual(actual[0], expected[0])
            self.assertEqual(actual[1], expected[1])
