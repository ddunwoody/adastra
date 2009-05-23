import unittest

from adastra.SvgLoader import *

class Test(unittest.TestCase):

    def testTrianglePath(self):
        svg_loader = SvgLoader('triangle_path.svg')
        path = svg_loader.parse()
        assert path == [(100,100), (50,150), (150,150)]
        
    def testPolygonPath(self):
        svg_loader = SvgLoader('polygon_path.svg')
        path = svg_loader.parse()
        assert path == [(88.55,89.4), (64,112), (73.01,143.97), (101.50,160.54), (134,151), (125,116), (88.70,89.455613)]
