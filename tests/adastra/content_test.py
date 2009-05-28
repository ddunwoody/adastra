import unittest

from adastra.content import parse_shapes, parse_thrusters
from adastra.material import Metal
from adastra.svg.Group import *
from adastra.svg.Path import *
from adastra.svg.Svg import *

class ContentParseShapesTest(unittest.TestCase):
    
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
        self.shapes = parse_shapes(self.svg)
        
    def testReturnsAShapeForEachPath(self):
        self.assertEqual(len(self.shapes), 2)

    def testIgnoresPathsNotInShapesGroup(self):
        self.svg.groups['foo'] = Group()
        self.svg.groups['foo'].paths.append(Path())
        self.shapes = parse_shapes(self.svg)
        self.assertEqual(len(self.shapes), 2)

    def testVerticesAreSet(self):
        # vertices will be flipped in Y-axis because of co-ordinate transform in Svg class
        self.assertEqual(self.shapes[0].shape_def.vertices, [(10,-10), (10,-20), (20,-20)])

    def testColorIsSet(self):
        self.assertEqual(self.shapes[0].color, (1, 0, 1))

    def testColorIsNoneIfFillNotSet(self):
        self.assertEqual(self.shapes[1].color, None)

    def testMaterial(self):
        self.assertAlmostEqual(self.shapes[0].shape_def.density, Metal().density)
        self.assertAlmostEqual(self.shapes[0].shape_def.friction, Metal().friction)
        self.assertAlmostEqual(self.shapes[0].shape_def.restitution, Metal().restitution)


class ContentParseThrustersTest(unittest.TestCase):

    def setUp(self):
        self.svg = Svg()
        group = Group()
        self.svg.groups['thrusters'] = Group()
        self.paths = self.svg.groups['thrusters'].paths
        path_up = Path([(80,350),(80,330)])
        path_up.data = {'thrust': '1.5', 'keys': 'UP'}
        path_left = Path([(35,350), (50,350)])
        path_left.data = {'thrust': '1.0', 'keys': 'LEFT'}
        path_right = Path([(125,350),(110,350)])
        path_right.data = {'thrust': '0.5', 'keys': 'RIGHT'}
        self.paths.append(path_up)
        self.paths.append(path_left)
        self.paths.append(path_right)
        self.thrusters = parse_thrusters(self.svg)

    def testReturnsAThrusterForEachPath(self):
        self.assertEqual(len(self.thrusters), 3)

    def testIgnoresPathsNotInThrustersGroup(self):
        self.svg.groups['foo'] = Group()
        self.svg.groups['foo'].paths.append(Path())
        self.thrusters = parse_thrusters(self.svg)
        self.assertEqual(len(self.thrusters), 3)

    def testDirection(self):
        self.assertEqual(self.thrusters[0].direction, (0,1))
        self.assertEqual(self.thrusters[1].direction, (1,0))
        self.assertEqual(self.thrusters[2].direction, (-1,0))

    def testThrust(self):
        self.assertEqual(self.thrusters[0].thrust, 1.5)
        self.assertEqual(self.thrusters[1].thrust, 1.0)
        self.assertEqual(self.thrusters[2].thrust, 0.5)

    def testPosition(self):
        # as usual, Y-axis is flipped
        self.assertEqual(self.thrusters[0].position, (80,-330))
        self.assertEqual(self.thrusters[1].position, (50,-350))
        self.assertEqual(self.thrusters[2].position, (110,-350))

    def testKeys(self):
        self.assertEqual(self.thrusters[0].keys, 'UP')
        self.assertEqual(self.thrusters[1].keys, 'LEFT')
        self.assertEqual(self.thrusters[2].keys, 'RIGHT')

    def testPathLengthOfOneRaisesException(self):
        path_one_point = Path([(125,350)])
        self.paths.append(path_one_point)
        self.assertRaises(Exception, parse_thrusters, self.svg)

    def testPathLengthOfThreeRaisesException(self):
        path_three_points = Path([(125,350), (1,2), (3,4)])
        self.paths.append(path_three_points)
        self.assertRaises(Exception, parse_thrusters, self.svg)

    def testPathWithoutThrustDataRaisesException(self):
        path = Path([(1,2), (3,4)])
        path.data = {'keys': 'LEFT'}
        self.paths.append(path)
        self.assertRaises(Exception, parse_thrusters, self.svg)
