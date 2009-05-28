from Box2D import *

import pyglet.window.key as key

from adastra.material import *

_materials = {'metal': Metal()}

def parse_shapes(svg):
    shapes = []
    for path in svg.paths('shapes'):
        shape_def = b2PolygonDef()
        shape_def.vertices = path.points
        shape = _Shape()
        shape.shape_def = shape_def
        shape.color = path.fill
        if path.data and path.data.has_key('material'):
            material = _materials[path.data['material']]
            shape_def.density = material.density
            shape_def.friction = material.friction
            shape_def.restitution = material.restitution
        shapes.append(shape)
    return shapes

class _Shape(object):
    shape_def = None
    color = None

def parse_thrusters(svg):
    thrusters = []
    for path in svg.paths('thrusters'):
        if len(path.points) != 2:
            raise Exception()
        if not path.data.has_key('thrust'):
            raise Exception()
        if not path.data.has_key('thrust'):
            raise Exception()
        thruster = _Thruster()
        direction = b2Vec2(path.points[1]) - b2Vec2(path.points[0])
        direction.Normalize()
        thruster.direction = direction.tuple()
        thrusters.append(thruster)
        thruster.thrust = float(path.data['thrust'])
        thruster.position = path.points[1]
        thruster.keys = [getattr(key, k) for k in path.data['keys'].split(',')]
    return thrusters

class _Thruster(object):
    direction = None
    thrust = 0
    position = None
    keys = None
    firing = False