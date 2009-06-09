from __future__ import division

from Box2D import b2Vec2

class Planet(object):
    def __init__(self, position=(0,0), radius=1, mass=1, color=(1,1,1)):
        self.position = b2Vec2(position)
        self.radius = radius
        self.mass = mass
        self.color = color
        
    def attract(self, position, mass):
        vector = self.position - position
        distanceSq = vector.LengthSquared()
        vector.Normalize()
        return vector * (mass * self.mass / distanceSq)

    def __repr__(self):
        return "Planet(position=%s, radius=%s, mass=%s, color=%s)" % (self.position.tuple(), self.radius, self.mass, self.color)