import unittest

from adastra.content import parse_shapes
from adastra.svg.Group import *
from adastra.svg.Path import *
from adastra.svg.Svg import *

class ContentTest(unittest.TestCase):
    
    def setUp(self):
        self.svg = Svg()
        group = Group()
        self.svg.groups['shapes'] = Group()
        self.paths = self.svg.groups['shapes'].paths
        path = Path([(10,10), (10,20), (20,20)])
        path.fill = 1, 0, 1
        self.paths.append(path)
        
    def testReturnsAShape(self):
        shapes = parse_shapes(self.svg)
        self.assertEqual(len(shapes), 1)

    def testReturnAShapeForEachPath(self):
        self.paths.append(Path())
        shapes = parse_shapes(self.svg)
        self.assertEqual(len(shapes), 2)

    def testIgnoresPathsNotInShapeGroup(self):
        self.svg.groups['foo'] = Group()
        self.svg.groups['foo'].paths.append(Path())
        shapes = parse_shapes(self.svg)
        self.assertEqual(len(shapes), 1)

    def testVerticesAreSet(self):
        shapes = parse_shapes(self.svg)
        # vertices will be flipped in Y-axis because of co-ordinate transform in Svg class
        self.assertEqual(shapes[0].shape_def.vertices, [(10,-10), (10,-20), (20,-20)])

    def testColorIsSet(self):
        shapes = parse_shapes(self.svg)
        self.assertEqual(shapes[0].color, (1, 0, 1))
