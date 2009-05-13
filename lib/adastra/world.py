from Box2D import *

def load_world(width, height):
    aabb = b2AABB()
    aabb.lowerBound = width // -2, height // -2
    aabb.upperBound = width // 2, height // 2
    gravity = 0, -10
    doSleep = True

    world = b2World(aabb, gravity, doSleep)

    # create ground
    body_def = b2BodyDef()
    body_def.position.Set(0, -10)
    ground_body = world.CreateBody(body_def)
    shape_def = b2PolygonDef()
    shape_def.SetAsBox(50, 10)
    shape = ground_body.CreateShape(shape_def)
    shape.SetUserData({'color': (0, 0.4, 0)})

    # create box
    body_def.position.Set(0, 4)
    body_def.angle = 0.3
    box_body = world.CreateBody(body_def)
    shape_def.SetAsBox(1, 1)
    shape_def.density = 1
    shape_def.friction = 0.3
    shape_def.restitution = 0.7
    shape = box_body.CreateShape(shape_def)
    shape.SetUserData({'color': (0, 0, 0.7)})
    box_body.SetMassFromShapes()

    return world


