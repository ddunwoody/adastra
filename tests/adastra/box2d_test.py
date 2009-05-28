import unittest

from Box2D import *

import math

# This test exists as a quick playpen for the Box2D API
class Box2DTest(unittest.TestCase):


    def testExample(self):
        aabb = b2AABB()
        bound = 1000
        aabb.lowerBound = -bound, -bound
        aabb.upperBound = bound, bound
        gravity = 0, 0
        doSleep = True
        world = b2World(aabb, gravity, doSleep)
        body_def = b2BodyDef()
        body_def.position.Set(50, 50)
        body_def.angle = math.pi
        body = world.CreateBody(body_def)
        shape_def = b2PolygonDef()
        shape_def.density = 1
        shape_def.SetAsBox(1, 1)
        shape = body.CreateShape(shape_def)
        body.SetMassFromShapes()
        
        self.assertEqual(body.GetMass(), 4)
        
        self.assertAlmostEqual(body.GetLocalPoint((1,1)).x, 49, 5)
        self.assertAlmostEqual(body.GetLocalPoint((1,1)).y, 49, 5)
        self.assertEqual(body.GetLocalVector((0,1)).y, -1)



