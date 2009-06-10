from __future__ import division

from Box2D import b2Vec2, b2Mat22

from math import sqrt, atan2

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

    # returns the orbital velocity vector required for a circular orbit through given position
    def orbital_velocity(self, position, clockwise=True):
        position_vector = b2Vec2(position) - self.position
        velocity_magnitude = sqrt(self.mass / position_vector.Length())
        angle = atan2(position_vector.x, position_vector.y)
        rotation = b2Mat22(angle)
        velocity = rotation.Solve((velocity_magnitude, 0))
        if not clockwise:
            velocity = velocity * -1
        return velocity.tuple()

    def __repr__(self):
        return "Planet(position=%s, radius=%s, mass=%s, color=%s)" % (self.position.tuple(), self.radius, self.mass, self.color)