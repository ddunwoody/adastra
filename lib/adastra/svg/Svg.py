from adastra.svg.Path import *

import copy

class Svg(object):
    def __init__(self):
        self.size = None
        self.paths = []
        self.scale = None
        self.translate = None
        self._transformed_paths = None

    # subtracts reference_point from the points in the paths
    def transformed_paths(self):
        if self._transformed_paths is not None:
            return self._transformed_paths
        
        self._transformed_paths = copy.deepcopy(self.paths)
        for path in self._transformed_paths:
            transformed_points = []
            for x, y in path.points:
                transformed_points.append((x - self.translate[0], y - self.translate[1]))
            path.points = transformed_points
        
        return self._transformed_paths