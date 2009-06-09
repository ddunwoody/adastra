from __future__ import division

from Box2D import b2Vec2

class Planet(object):
    def __init__(self, position=(0,0), radius=1, mass=1, color=(1,1,1)):
        self.position = b2Vec2(position)
        self.mass = mass
        self.radius = radius
        self.color = color
        
    def attract(self, position, mass):
        vector = self.position - position
        distanceSq = vector.LengthSquared()
        vector.Normalize()
        return vector * (mass * self.mass / distanceSq)