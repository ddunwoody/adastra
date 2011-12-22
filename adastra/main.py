from cocos.director import director
from cocos.text import Label
from cocos.layer import Layer
from cocos.scene import Scene

import pyglet.resource as resource
from pyglet.window import key

from adastra.systems import Lander

from pyglet.gl import glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST

class SystemsLayer(Layer):
    def __init__(self, systems):
        super(SystemsLayer, self).__init__()
        self.systems = systems
        self.text = Label('', (director.get_window_size()[0] - 10 ,10), anchor_x="right")
        self.value = 0
        self.add(self.text)

    def draw(self):
        self.text.element.text = ",".join([str(s) for s in self.systems])
    

if __name__ == "__main__":
    resource.path.append('@adastra.resources')
    resource.reindex()

    director.init(caption="Ad Astra")
    x,y = director.get_window_size()

    lander = Lander(position=(x/2, y/2), scale=2)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def update(dt):
        lander.engine.throttle += dt * keyboard[key.W]
        lander.engine.throttle -= dt * keyboard[key.S]

    layer = Layer()
    layer.add(lander)

    scene = Scene(layer, SystemsLayer(lander.systems))
    scene.schedule(update)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    director.run(scene)
    
