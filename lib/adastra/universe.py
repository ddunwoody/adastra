from __future__ import with_statement
from contextlib import contextmanager

from Box2D import *
from adastra.agent import Agent


class Universe(object):
    def __init__(self, world):
        self.world = world
        self.agents = {}
        self.background_color = 0, 0, 0.1


class Planet(object):
    def __init__(self):
        self.fields = {}

    def __setattr__(self, attr, value):
        if attr == "fields":
            object.__setattr__(self, attr, value)
        else:
            self.fields[attr] = value

    def create(self, universe):
        body_def = b2BodyDef()
        body_def.position.Set(*self.fields['position'])
        body = universe.world.CreateBody(body_def)
        shape_def = b2CircleDef()
        shape_def.radius = self.fields['radius']
        shape = body.CreateShape(shape_def)
        shape.SetUserData({'color': self.fields['color']})


@contextmanager
def create_planet(universe):
    planet = Planet()
    yield planet
    planet.create(universe)

class Player(Planet):
    def create(self, universe):
        agent = Agent()
        agent.id = self.fields['id']
        universe.agents[agent.id] = agent
        body_def = b2BodyDef()
        body_def.position.Set(*self.fields['position'])
        body_def.angle = self.fields['angle']
        agent.body = universe.world.CreateBody(body_def)
        agent.body.SetLinearVelocity(self.fields['linear_velocity'])
        agent.body.SetAngularVelocity(self.fields['angular_velocity'])
        shape_def = b2PolygonDef()
        shape_def.SetAsBox(*self.fields['as_box'])
        shape_def.density = self.fields['density']
        shape_def.friction = self.fields['friction']
        shape_def.restitution = self.fields['restitution']
        shape = agent.body.CreateShape(shape_def)
        shape.SetUserData({'color': self.fields['color']})
        agent.body.SetMassFromShapes()

@contextmanager
def create_player(universe):
    player = Player()
    yield player
    player.create(universe)


def load_universe(width, height):
    aabb = b2AABB()
    aabb.lowerBound = width // -2, height // -2
    aabb.upperBound = width // 2, height // 2
    gravity = 0, 0
    doSleep = True

    world = b2World(aabb, gravity, doSleep)
    universe = Universe(world)

    # create ground
    with create_planet(universe) as p:
        p.position = 0, 0
        p.radius = 100
        p.color = 0, 0.4, 0

    with create_player(universe) as a:
        a.id = "player"
        a.position = 0, 105
        a.angle = 0.3
        a.linear_velocity = 17.5, 0
        a.angular_velocity = -2
        a.as_box = 1, 1
        a.density = 1
        a.friction = 0.7
        a.restitution = 0.3
        a.color = 0.5, 0.5, 0.5

    return universe
