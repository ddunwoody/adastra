import unittest

from adastra.svg_loader import load_svg

class SvgLoaderTest(unittest.TestCase):

    def testSize(self):
        size = load_svg('svg_loader/sized.svg').size
        self.assertEqual(size, (123,456))

    def testReferencePoint(self):
        reference_point = load_svg('svg_loader/reference_point.svg').reference_point
        self.assertEqual(reference_point, (100, 120))

    def testTrianglePath(self):
        path = load_svg('svg_loader/triangle_path.svg').paths[0]
        self.assertEqual(path.points, [(100,100), (50,150), (150,150)])
        
    def testPolygonPath(self):
        path = load_svg('svg_loader/polygon_path.svg').paths[0]
        self.assertEqual(path.points, [(88.55,89.4), (64,112), (73.01,143.97), (101.50,160.54), (134,151), (125,116), (88.70,89.455613)])

    def testFilledPath(self):
        path = load_svg('svg_loader/filled_path.svg').paths[0]
        self.assertEqual(path.fill, '#ABCDEF')

    def testStrokedPath(self):
        path = load_svg('svg_loader/stroked_path.svg').paths[0]
        self.assertEqual(path.stroke, '#998877')

    def testMultiplePaths(self):
        paths = load_svg('svg_loader/multiple_paths.svg').paths
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0].points, [(100,100), (50,150), (150,150)])
        self.assertEqual(paths[1].points, [(200,200), (50,250), (250,250)])
        
    def testInkscapeLabelledPath(self):
        path = load_svg('svg_loader/inkscape_labelled_path.svg').paths[0]
        self.assertEqual(path.label, 'foo')

    def testPathWithID(self):
        path = load_svg('svg_loader/path_with_id.svg').paths[0]
        self.assertEqual(path.id, 'id_value')