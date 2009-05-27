from adastra.svg.Path import *

import copy

class Svg(object):
    def __init__(self):
        self.size = None
        self.groups = {}
        self.scale = 1
        self.translate = (0, 0)

    # returns a copy of paths in group with scale and translate applied
    # flips y-axis to convert from SVG to Box2D coordinate system
    def paths(self, group):
        paths = copy.deepcopy(self.groups[group].paths)

        for path in paths:
            transformed_points = []
            for x, y in path.points:
                x, y = x+self.translate[0], y+self.translate[1]
                x, y = x*self.scale, y*-self.scale
                transformed_points.append((x, y))
            path.points = transformed_points
        
        return paths
