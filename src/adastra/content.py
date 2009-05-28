from Box2D import *

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