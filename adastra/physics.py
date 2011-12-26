from cocos import director, layer, scene

import glnode
import pymunk
import pyglet.graphics
import math

from pyglet.gl import glColor3f, GL_LINES, GL_LINE_LOOP

class Box(glnode.GLNode):
    def __init__(self, mass, size):
        super(Box, self).__init__()
        self.size = size
        inertia = pymunk.moment_for_box(mass, size, size)
        self.body = pymunk.Body(mass, inertia)
        shape = pymunk.Poly.create_box(self.body, (size,size))
        shape.elasticity = 0.2
        shape.friction = 0.7
        space.add(self.body, shape)
        self.schedule(self.update)
        p = self.size / 2
        self.vertex_list = pyglet.graphics.vertex_list(4, ("v2f\static", (-p,p, p,p, p,-p, -p,-p)))
        
        self.forces = []
    
    def apply_force(self, f, r=(0, 0)):
        self.forces.append((f,r))
    
    def reset_forces(self):
        del self.forces[:]
    
    def update(self, dt):
        for f,r in self.forces:
            force = self._rotate_vector(self.body.angle, *f)
            pos = self._rotate_vector(self.body.angle, *r)
            self.body.apply_impulse(self._scale_vector(dt, *force), pos)
        space.step(dt)
        self.position = self.body.position
        self.rotation = math.degrees(-self.body.angle)

    def _rotate_vector(self, angle_radians, x, y):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        rx = x*cos - y*sin
        ry = x*sin + y*cos
        return rx,ry

    def _scale_vector(self, factor, x, y):
        return x*factor, y*factor

    def drawGl(self):
        self.vertex_list.draw(GL_LINE_LOOP)
        glColor3f(1,1,0)
        for j,r in self.forces:
            pyglet.graphics.draw(2, GL_LINES, ("v2f", (r[0], r[1], r[0] + j[0], r[1] + j[1])))
        glColor3f(1,1,1)

class Slope(glnode.GLNode):
    def __init__(self, a, b, radius):
        super(Slope, self).__init__()
        body = pymunk.Body()
        l1 = pymunk.Segment(body, a, b, radius)
        l1.elasticity = 0.2
        l1.friction = 0.7
        space.add_static(l1)
        self.vertex_list = pyglet.graphics.vertex_list(2, ("v2f\static", (a[0], a[1], b[0], b[1])))
    
    def drawGl(self):
        self.vertex_list.draw(GL_LINES)

space = pymunk.Space()
"The singleton space"


if __name__ == "__main__":
    director.director.init(caption="Physics Spike", resizable=True, width=1024, height=640)
    space.gravity = (0.0, -10.0)

    physics_layer = layer.Layer()
    b = Box(10, 10)
    s = Slope((400,300), (600,280), 0)
    b.body.position = (512,350)
    b.apply_force((0,100), (1,0))
    physics_layer.add(s)
    physics_layer.add(b)

    director.director.run(scene.Scene(physics_layer))
    