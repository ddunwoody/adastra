from adastra.svg.Path import *

import copy

class Svg(object):
    def __init__(self):
        self.size = None
        self.paths = []
        self.scale = None
        self.translate = None
        self._transformed_paths = None

    # returns a copy of paths with scale and translate applied
    def transformed_paths(self):
        paths = copy.deepcopy(self.paths)

        for path in paths:
            transformed_points = []
            for x, y in path.points:
                if self.translate is not None:
                    x, y = x+self.translate[0], y+self.translate[1]
                if self.scale is not None:
                    x, y = x*self.scale, y*self.scale
                transformed_points.append((x, y))
            path.points = transformed_points
        
        return paths