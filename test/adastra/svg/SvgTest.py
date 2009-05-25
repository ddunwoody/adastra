import unittest

from adastra.svg.Path import *
from adastra.svg.Svg import *

class SvgTest(unittest.TestCase):

    def testTranslatesPathUsingReferencePoint(self):
        svg = Svg()
        svg.reference_point = (3,3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        points = svg.translated_paths()[0].points
        self.assertEqual(points, [(-2,-1), (0,1), (2,3)])

    def testTranslatesMultiplePathsUsingReferencePoint(self):
        svg = Svg()
        svg.reference_point = (3,3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)]),
                     Path(points=[(7,8), (9,1), (2,3)])]
        paths = svg.translated_paths()
        self.assertEqual(paths[0].points, [(-2,-1), (0,1), (2,3)])
        self.assertEqual(paths[1].points, [(4,5), (6,-2), (-1,0)])

    def testTranslatesPathOnlyOnce(self):
        svg = Svg()
        svg.reference_point = (3,3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]

        points = svg.translated_paths()[0].points
        self.assertEqual(points, [(-2,-1), (0,1), (2,3)])

        points = svg.translated_paths()[0].points
        self.assertEqual(points, [(-2,-1), (0,1), (2,3)])

    def testPreservesAttributesOnPath(self):
        svg = Svg()
        svg.reference_point = (3,3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        svg.paths[0].label = 'foo'

        label = svg.translated_paths()[0].label
        self.assertEqual(label, 'foo')
