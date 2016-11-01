import pymunk
import pyglet.graphics
import math

from cocos import cocosnode

from pyglet.gl import glColor3f, GL_LINES, GL_LINE_LOOP

class Box(cocosnode.CocosNode):
    def __init__(self, mass, size):
        super(Box, self).__init__()
        self.size = size
        inertia = pymunk.moment_for_box(mass, (size, size))
        self.body = pymunk.Body(mass, inertia)
        shape = pymunk.Poly.create_box(self.body, (size,size))
        shape.elasticity = 0.2
        shape.friction = 0.7
        space.add(self.body, shape)
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
            self.body.apply_impulse_at_local_point(self._scale_vector(dt, *force), pos)
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

    def draw(self):
        if draw_debug:
            glColor3f(1,1,1)
            self.vertex_list.draw(GL_LINE_LOOP)
            glColor3f(1,1,0)
            for j,r in self.forces:
                pyglet.graphics.draw(2, GL_LINES, ("v2f", (r[0], r[1], r[0] + j[0]/10, r[1] + j[1]/10)))

draw_debug = False
space = pymunk.Space()
"The singleton space"
    
