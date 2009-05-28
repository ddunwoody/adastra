import unittest

from adastra.content import parse_shapes
from adastra.material import Metal
from adastra.svg.Group import *
from adastra.svg.Path import *
from adastra.svg.Svg import *

class ContentTest(unittest.TestCase):
    
    def setUp(self):
        self.svg = Svg()
        group = Group()
        self.svg.groups['shapes'] = Group()
        self.paths = self.svg.groups['shapes'].paths
        path1 = Path([(10,10), (10,20), (20,20)])
        path1.fill = 1, 0, 1
        path1.data = {'material': 'metal'}
        self.paths.append(path1)
        path2 = Path([(10,10), (10,20), (20,20)])
        self.paths.append(path2)
        
    def testReturnAShapeForEachPath(self):
        shapes = parse_shapes(self.svg)
        self.assertEqual(len(shapes), 2)

    def testIgnoresPathsNotInShapesGroup(self):
        self.svg.groups['foo'] = Group()
        self.svg.groups['foo'].paths.append(Path())
        shapes = parse_shapes(self.svg)
        self.assertEqual(len(shapes), 2)

    def testVerticesAreSet(self):
        shapes = parse_shapes(self.svg)
        # vertices will be flipped in Y-axis because of co-ordinate transform in Svg class
        self.assertEqual(shapes[0].shape_def.vertices, [(10,-10), (10,-20), (20,-20)])

    def testColorIsSet(self):
        shapes = parse_shapes(self.svg)
        self.assertEqual(shapes[0].color, (1, 0, 1))

    def testColorIsNoneIfFillNotSet(self):
        shapes = parse_shapes(self.svg)
        self.assertEqual(shapes[1].color, None)

    def testMaterial(self):
        shapes = parse_shapes(self.svg)
        self.assertAlmostEqual(shapes[0].shape_def.density, Metal().density)
        self.assertAlmostEqual(shapes[0].shape_def.friction, Metal().friction)
        self.assertAlmostEqual(shapes[0].shape_def.restitution, Metal().restitution)


