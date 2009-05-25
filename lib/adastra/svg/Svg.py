from adastra.svg.Path import *

class Svg(object):
    def __init__(self):
        self.size = None
        self.reference_point = None
        self.paths = []

    def translated_paths(self):
       paths = []
       for path in self.paths:
           points = []
           for x, y in path.points:
               points.append((x - self.reference_point[0], y - self.reference_point[1]))
           paths.append(Path(points=points))
       return paths
