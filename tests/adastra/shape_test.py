import fudge
import unittest

import adastra.shape as shape

class ShapeTest(unittest.TestCase):
    
    def testSetsMassFromShapes(self):
        svg = None
        body = fudge.Fake('body')
        body.expects('SetMassFromShapes')
        shape.add(svg, body)
        fudge.verify()
