from adastra.svg.Path import *

import copy

class Svg(object):
    def __init__(self):
        self.size = None
        self.reference_point = None
        self.paths = []
        self.scale = None
        self.translate = None
        self._translated_paths = None

    # subtracts reference_point from the points in the paths
    def translated_paths(self):
        if self._translated_paths is not None:
            return self._translated_paths
        
        self._translated_paths = copy.deepcopy(self.paths)
        for path in self._translated_paths:
            translated_points = []
            for x, y in path.points:
                translated_points.append((x - self.reference_point[0], y - self.reference_point[1]))
            path.points = translated_points
        
        return self._translated_paths