from __future__ import division

import unittest

from adastra.Planet import *

from math import sqrt

class PlanetTest(unittest.TestCase):

    def testAttractionForceReducesWithDistanceSquared(self):
        planet = Planet() 
        self.assertAlmostEqual(planet.get_gravity((0,1), 1)[1], -1)
        self.assertAlmostEqual(planet.get_gravity((0,2), 1)[1], -1/4)
        self.assertAlmostEqual(planet.get_gravity((0,3), 1)[1], -1/9)

    def testAttractionForceIsProportionalToMassOfObject(self):
        planet = Planet() 
        self.assertEqual(planet.get_gravity((0,1),   1)[1],   -1)
        self.assertEqual(planet.get_gravity((0,1),  10)[1],  -10)
        self.assertEqual(planet.get_gravity((0,1), 100)[1], -100)

    def testAttractionForceIsProportionalToMassOfPlanet(self):
        planet = Planet(mass=5) 
        self.assertEqual(planet.get_gravity((0,1),   1)[1],   -5)

    def testPlanetAtNonZeroPosition(self):
        planet = Planet(position=(100, 100)) 
        self.assertEqual(planet.get_gravity((100,101),   1)[1],   -1)

    def testAttractionIsTowardsPlanetPosition(self):
        planet = Planet(position=(50, 50))
        self.assertEqual(planet.get_gravity((50, 51), 1), ( 0, -1))
        self.assertEqual(planet.get_gravity((50, 49), 1), ( 0,  1))
        self.assertEqual(planet.get_gravity((51, 50), 1), (-1,  0))
        self.assertEqual(planet.get_gravity((50, 51), 1), ( 0, -1))
        self.assertAlmostEqual(planet.get_gravity((51, 51), 1)[0], -1/4*sqrt(2))
        self.assertAlmostEqual(planet.get_gravity((51, 51), 1)[1], -1/4*sqrt(2))

    def testOrbitalVelocity(self):
        planet = Planet()
        self.assertAlmostEqual(planet.orbital_velocity(1), sqrt(1))
        self.assertAlmostEqual(planet.orbital_velocity(2), sqrt(1/2))
        self.assertAlmostEqual(planet.orbital_velocity(5), sqrt(1/5))
        planet = Planet(mass=10)
        self.assertAlmostEqual(planet.orbital_velocity(7), sqrt(10/7))
