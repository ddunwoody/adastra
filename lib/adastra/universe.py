from __future__ import with_statement
from contextlib import contextmanager

from Box2D import *
from adastra.agent import Agent
from adastra.loader import load_svg


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
        shapes = load_svg(self.fields['svg'])
        for s in shapes:
            shape_def = b2PolygonDef()
            shape_def.setVertices(s['path'])
            shape_def.density = 1
            shape_def.friction = 0.7
            shape_def.restitution = 0.3
            shape = agent.body.CreateShape(shape_def)
            shape.SetUserData({'color': s['color']})
        agent.body.SetMassFromShapes()

@contextmanager
def create_player(universe):
    player = Player()
    yield player
    player.create(universe)


def load_universe(width, height):
    aabb = b2AABB()
    bound = 100000
    aabb.lowerBound = -bound, -bound
    aabb.upperBound = bound, bound
    gravity = 0, 0
    doSleep = True

    world = b2World(aabb, gravity, doSleep)
    universe = Universe(world)

    # create ground
    with create_planet(universe) as p:
        p.position = 0, 0
        p.radius = 10000
        p.color = 0, 0.4, 0, 1

    with create_player(universe) as a:
        a.id = "player"
        a.position = 0, 10004
        a.angle = 0
        a.linear_velocity = 0, 0
        a.angular_velocity = 0
        a.svg = "content/ships/basic.svg"

    return universe
