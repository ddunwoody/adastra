from __future__ import division

from Box2D import b2Vec2

from math import sqrt

class Planet(object):
    def __init__(self, position=(0,0), radius=1, mass=1, color=(1,1,1)):
        self.position = b2Vec2(position)
        self.radius = radius
        self.mass = mass
        self.color = color

    # returns a b2Vec2 which is the force to be applied to the body
    def get_gravity(self, body):
        vector = self.position - body.GetWorldCenter()
        distanceSq = vector.LengthSquared()
        vector.Normalize()
        return vector * (body.GetMass() * self.mass / distanceSq)

    # returns the orbital velocity required for a circular orbit of a given radius
    def orbital_velocity(self, radius):
        return sqrt(self.mass / radius)

    def __repr__(self):
        return "Planet(position=%s, radius=%s, mass=%s, color=%s)" % (self.position.tuple(), self.radius, self.mass, self.color)