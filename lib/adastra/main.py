import pyglet
from pyglet.gl import *
from Box2D import *

class AdAstraWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, fullscreen=True,
                                      caption="Ad Astra")
        self.set_mouse_visible(False)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.camera_pos = 0, 0

        aabb = b2AABB()
        aabb.lowerBound = 0, 0
        aabb.upperBound = self.width, self.height
        gravity = 0, -10
        doSleep = True
        self.world = b2World(aabb, gravity, doSleep)

        pyglet.clock.schedule_interval(self.step, 1 / 60)

    def step(self, dt):
        velocityIterations = 10
        positionIterations = 8
        self.world.Step(dt, velocityIterations, positionIterations)

    def on_draw(self):
        glClearColor(0, 0, 0.1, 1)
        self.clear()

        camera_x, camera_y = self.camera_pos
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = self.width / self.height
        height = 30
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
        print "Would draw %s" % shape


def main():
    window = AdAstraWindow()
    pyglet.app.run()

if __name__ == "__main__":
    main()
