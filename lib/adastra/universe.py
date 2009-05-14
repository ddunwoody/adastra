from Box2D import *
from adastra.agent import Agent

class Universe(object):
    def __init__(self, world):
        self.world = world
        self.agents = {}
        self.background_color = 0, 0, 0.1

def load_universe(width, height):
    aabb = b2AABB()
    aabb.lowerBound = width // -2, height // -2
    aabb.upperBound = width // 2, height // 2
    gravity = 0, 0
    doSleep = True

    world = b2World(aabb, gravity, doSleep)
    universe = Universe(world)

    # create ground
    body_def = b2BodyDef()
    body_def.position.Set(0, 0)
    ground_body = world.CreateBody(body_def)
    shape_def = b2CircleDef()
    shape_def.radius = 100
    shape = ground_body.CreateShape(shape_def)
    shape.SetUserData({'color': (0, 0.4, 0)})

    # create box
    agent = Agent()
    agent.id = 'player'
    universe.agents[agent.id] = agent
    body_def.position.Set(0, 105)
    body_def.angle = 0.3
    agent.body = world.CreateBody(body_def)
    agent.body.SetLinearVelocity((17.5, 0))
    agent.body.SetAngularVelocity(-2)
    shape_def = b2PolygonDef()
    shape_def.SetAsBox(1, 1)
    shape_def.density = 1
    shape_def.friction = 0.7
    shape_def.restitution = 0.3
    shape = agent.body.CreateShape(shape_def)
    shape.SetUserData({'color': (0.5, 0.5, 0.5)})
    agent.body.SetMassFromShapes()

    return universe
