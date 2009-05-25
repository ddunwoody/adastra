from adastra.svg.Path import *

import copy

class Svg(object):
    def __init__(self):
        self.size = None
        self.paths = []
        self.scale = 1
        self.translate = (0, 0)
        self._transformed_paths = None

    # returns a copy of paths with scale and translate applied
    # flips y-axis to convert from SVG to Box2D coordinate system
    def transformed_paths(self):
        paths = copy.deepcopy(self.paths)

        for path in paths:
            transformed_points = []
            for x, y in path.points:
                x, y = x+self.translate[0], y+self.translate[1]
                x, y = x*self.scale, y*-self.scale
                transformed_points.append((x, y))
            path.points = transformed_points
        
        return paths