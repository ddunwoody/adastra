import unittest

from adastra.svg.Path import *
from adastra.svg.Svg import *

class SvgTest(unittest.TestCase):

    def testTranslatesPathUsingReferencePoint(self):
        svg = Svg()
        svg.reference_point = (3,3)
        svg.paths = [Path(points=[(1,2), (3,4), (5,6)])]
        translated_points = svg.translated_paths()[0].points
        self.assertEqual(translated_points, [(-2, -1), (0,1), (2, 3)])
