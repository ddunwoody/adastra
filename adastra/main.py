from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene

from pyglet.gl import GL_LINES, glColor3f
from pyglet.graphics import draw
from pyglet.window import key

import adastra.setup as setup
from adastra.systems import Lander
from adastra.hud import HUDLayer

class WorldLayer(Layer):
    def __init__(self, lander):
        super(WorldLayer, self).__init__()
        self.width = director.get_window_size()[0]
        self.ground_height = lander.get_rect().bottom
        self.add(lander)
        
    def draw(self, *args, **kwargs):
        glColor3f(0,255,0)
        draw(2, GL_LINES, ('v2i', (0, self.ground_height, self.width, self.ground_height)))
        Layer.draw(self, *args, **kwargs)

if __name__ == "__main__":
    setup.resources()

    director.init(caption="Ad Astra", resizable=True)
    x,y = director.get_window_size()

    lander = Lander(position=(x/2, 50))

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def update(dt):
        delta = 1
        if keyboard[key.LSHIFT]:
            delta = 0.1
        lander.engine.throttle += dt * keyboard[key.W] * delta
        lander.engine.throttle -= dt * keyboard[key.S] * delta
        lander.rvel += dt * keyboard[key.D] * delta * 10
        lander.rvel -= dt * keyboard[key.A] * delta * 10

    layer = Layer()
    layer.add(lander)

    scene = Scene(WorldLayer(lander), HUDLayer(lander.systems, keyboard))
    scene.schedule(update)

    
    director.run(scene)
    
