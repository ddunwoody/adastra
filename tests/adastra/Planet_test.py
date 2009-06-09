from __future__ import division

import unittest
import math

from adastra.Planet import *

class PlanetTest(unittest.TestCase):

    def testAttractionForceReducesWithDistanceSquared(self):
        planet = Planet() 
        self.assertAlmostEqual(planet.attract((0,1), 1).y, -1)
        self.assertAlmostEqual(planet.attract((0,2), 1).y, -1/4)
        self.assertAlmostEqual(planet.attract((0,3), 1).y, -1/9)

    def testAttractionForceIsProportionalToMassOfObject(self):
        planet = Planet() 
        self.assertEqual(planet.attract((0,1),   1).y,   -1)
        self.assertEqual(planet.attract((0,1),  10).y,  -10)
        self.assertEqual(planet.attract((0,1), 100).y, -100)

    def testAttractionForceIsProportionalToMassOfPlanet(self):
        planet = Planet(mass=5) 
        self.assertEqual(planet.attract((0,1),   1).y,   -5)

    def testPlanetAtNonZeroPosition(self):
        planet = Planet(position=(100, 100)) 
        self.assertEqual(planet.attract((100,101),   1).y,   -1)

    def testDirectionOfAttractionIsCorrect(self):
        planet = Planet(position=(50, 50))
        self.assertEqual(planet.attract((50, 51), 1).tuple(), ( 0, -1))
        self.assertEqual(planet.attract((50, 49), 1).tuple(), ( 0,  1))
        self.assertEqual(planet.attract((51, 50), 1).tuple(), (-1,  0))
        self.assertEqual(planet.attract((50, 51), 1).tuple(), ( 0, -1))
        self.assertAlmostEqual(planet.attract((51, 51), 1).x, -0.354, places=3)
        self.assertAlmostEqual(planet.attract((51, 51), 1).y, -0.354, places=3)                                                                                                                        