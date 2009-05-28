from Box2D import *

def parse_shapes(svg):
    shapes = []
    for path in svg.paths('shapes'):
        shape_def = b2PolygonDef()
        shape_def.vertices = path.points
        shape_def.density = 1
        shape_def.friction = 0.7
        shape_def.restitution = 0.3
        shapes.append(_Shape(shape_def, path.fill))
    return shapes

class _Shape(object):
    def __init__(self, shape_def, color):
        self.shape_def = shape_def
        self.color = color