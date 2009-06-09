from __future__ import division

import unittest

from adastra.Planet import *

from math import sqrt

# mocks a b2Body
class Body(object):
    def __init__(self, position, mass):
        self.position = position
        self.mass = mass

    def GetWorldCenter(self):
        return b2Vec2(self.position)

    def GetMass(self):
        return self.mass

class PlanetTest(unittest.TestCase):

    def testAttractionForceReducesWithDistanceSquared(self):
        planet = Planet() 
        self.assertAlmostEqual(planet.get_gravity(Body((0,1), 1)).y, -1)
        self.assertAlmostEqual(planet.get_gravity(Body((0,2), 1)).y, -1/4)
        self.assertAlmostEqual(planet.get_gravity(Body((0,3), 1)).y, -1/9)

    def testAttractionForceIsProportionalToMassOfObject(self):
        planet = Planet() 
        self.assertEqual(planet.get_gravity(Body((0,1),   1)).y,   -1)
        self.assertEqual(planet.get_gravity(Body((0,1),  10)).y,  -10)
        self.assertEqual(planet.get_gravity(Body((0,1), 100)).y, -100)

    def testAttractionForceIsProportionalToMassOfPlanet(self):
        planet = Planet(mass=5) 
        self.assertEqual(planet.get_gravity(Body((0,1),   1)).y,   -5)

    def testPlanetAtNonZeroPosition(self):
        planet = Planet(position=(100, 100)) 
        self.assertEqual(planet.get_gravity(Body((100,101),   1)).y,   -1)

    def testDirectionOfAttractionIsCorrect(self):
        planet = Planet(position=(50, 50))
        self.assertEqual(planet.get_gravity(Body((50, 51), 1)).tuple(), ( 0, -1))
        self.assertEqual(planet.get_gravity(Body((50, 49), 1)).tuple(), ( 0,  1))
        self.assertEqual(planet.get_gravity(Body((51, 50), 1)).tuple(), (-1,  0))
        self.assertEqual(planet.get_gravity(Body((50, 51), 1)).tuple(), ( 0, -1))
        self.assertAlmostEqual(planet.get_gravity(Body((51, 51), 1)).x, -1/4*sqrt(2))
        self.assertAlmostEqual(planet.get_gravity(Body((51, 51), 1)).y, -1/4*sqrt(2))

    def testOrbitalVelocity(self):
        planet = Planet()
        self.assertAlmostEqual(planet.orbital_velocity(1), sqrt(1))
        self.assertAlmostEqual(planet.orbital_velocity(2), sqrt(1/2))
        self.assertAlmostEqual(planet.orbital_velocity(5), sqrt(1/5))
        planet = Planet(mass=10)
        self.assertAlmostEqual(planet.orbital_velocity(7), sqrt(10/7))
