from __future__ import division

from Box2D import b2Vec2

from math import sqrt

class Planet(object):
    def __init__(self, position=(0,0), radius=1, mass=1, color=(1,1,1)):
        self.position = b2Vec2(position)
        self.radius = radius
        self.mass = mass
        self.color = color

    # returns a tuple which represents the force to be appled to the
    # centre of mass of the orbiting body
    def get_gravity(self, position, mass):
        vector = self.position - position
        distanceSq = vector.LengthSquared()
        vector.Normalize()
        return (vector * (mass * self.mass / distanceSq)).tuple()

    # returns the orbital velocity required for a circular orbit of a given radius
    def orbital_velocity(self, radius):
        return sqrt(self.mass / radius)

    def __repr__(self):
        return "Planet(position=%s, radius=%s, mass=%s, color=%s)" % (self.position.tuple(), self.radius, self.mass, self.color)