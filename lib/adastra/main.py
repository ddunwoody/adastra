from __future__ import division

import pyglet, math
from pyglet.gl import *
from Box2D import *
from adastra.universe import load_universe

class AdAstraWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, fullscreen=False,
                                      caption="Ad Astra")
        self.set_mouse_visible(False)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.circle_display_list = glGenLists(1)
        glNewList(self.circle_display_list, GL_COMPILE)
        self.draw_circle(256)
        glEndList()

        self.camera_pos = 0, 0
        self.camera_height = 100
        self.min_camera_height = 1
        self.max_camera_height = 10000
        self.zoom_in = self.zoom_out = False

        self.universe = load_universe(self.width, self.height)
        self.world = self.universe.world

        pyglet.clock.schedule_interval(self.step, 1 / 60)

    def step(self, dt):
        player = self.universe.agents['player']

        if player:
            player_pos = player.body.position
            self.camera_pos = player_pos.tuple()
            distance_sq = player_pos.LengthSquared()
            force = player_pos.copy()
            force.mul_float(-1000 / distance_sq)
            player.body.ApplyForce(force, player_pos)

        if self.zoom_in:
            self.camera_height /= 10 ** dt
        if self.zoom_out:
            self.camera_height *= 10 ** dt
        self.camera_height = max(self.min_camera_height, self.camera_height)
        self.camera_height = min(self.max_camera_height, self.camera_height)
        velocityIterations = 10
        positionIterations = 8
        self.world.Step(dt, velocityIterations, positionIterations)

    def on_draw(self):
        r, g, b = self.universe.background_color
        glClearColor(r, g, b, 1)
        self.clear()

        camera_x, camera_y = self.camera_pos
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        height = self.camera_height
        aspect_ratio = self.width / self.height
        width = aspect_ratio * height
        min_x = camera_x - width / 2
        min_y = camera_y - height / 2
        max_x = camera_x + width / 2
        max_y = camera_y + height / 2
        glOrtho(min_x, max_x, min_y, max_y, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        aabb = b2AABB()
        aabb.lowerBound = min_x, min_y
        aabb.upperBound = max_x, max_y
        count, shapes = self.world.Query(aabb, 1000)

        def key(shape):
            return id(shape.GetBody())

        glPushMatrix()
        for shape in sorted(shapes, key=key):
            self.draw_shape(shape)
        glPopMatrix()

    def draw_shape(self, shape):
        glPushMatrix()
        p = shape.GetBody().GetPosition()
        a = shape.GetBody().GetAngle()
        glTranslated(p.x, p.y, 0)
        glRotated(a * 180 / math.pi, 0, 0, 1)
        data = shape.GetUserData() or {}
        color = data.get('color', (1, 1, 1))
        glColor3f(*color)
        polygon = shape.asPolygon()
        circle = shape.asCircle()
        if polygon:
            self.draw_polygon(polygon)
        elif circle:
            p = circle.localPosition
            glTranslated(p.x, p.y, 0)
            glScaled(circle.radius, circle.radius, 1)
            glCallList(self.circle_display_list)
        glPopMatrix()

    def draw_polygon(self, polygon):
        vertices = list(polygon.vertices)
        vertices.append(vertices[0])
        glBegin(GL_POLYGON)
        for x, y in vertices:
            glVertex2d(x, y)
        glEnd()
        glBegin(GL_LINE_STRIP)
        for x, y in vertices:
            glVertex2d(x, y)
        glEnd()

    def draw_circle(self, triangle_count):
        glBegin(GL_POLYGON)
        for i in xrange(triangle_count + 1):
            a = 2 * math.pi * i / triangle_count
            glVertex2d(math.cos(a), math.sin(a))
        glEnd()
        glBegin(GL_LINE_STRIP)
        for i in xrange(triangle_count + 1):
            a = 2 * math.pi * i / triangle_count
            glVertex2d(math.cos(a), math.sin(a))
        glEnd()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close();
        if symbol == pyglet.window.key.MINUS:
            self.zoom_out = True
        if symbol == pyglet.window.key.EQUAL:
            self.zoom_in = True
        if symbol == pyglet.window.key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.MINUS:
            self.zoom_out = False
        if symbol == pyglet.window.key.EQUAL:
            self.zoom_in = False

def main():
    window = AdAstraWindow()
    pyglet.app.run()

if __name__ == "__main__":
    main()
