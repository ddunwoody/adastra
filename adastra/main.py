from cocos.director import director
from cocos.text import Label
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite 

from adastra.systems import Engine

import pyglet.resource as resource
from pyglet.window import key

class Lander(Sprite):
    def __init__(self, image="lander.png", position=(0,0), rotation=0, scale=1):
        super(Lander, self).__init__("lander.png", position, rotation, scale)
        self.schedule(self.update)
        self.engine = Engine()
        self.systems = [self.engine]

    def update(self, dt):
        for system in self.systems:
            system.update(dt)


class LanderLayer(Layer):
    def __init__(self, lander):
        super(LanderLayer, self).__init__()
        self.add(lander)


class SystemsDisplay(Layer):
    def __init__(self, lander):
        super(SystemsDisplay, self).__init__()
        self.lander = lander
        self.text = Label('', (director.get_window_size()[0] - 10 ,10), anchor_x="right")
        self.value = 0
        self.add(self.text)
        self.schedule(self.update)

    def update(self, dt):
        self.text.element.text = ",".join([str(s) for s in self.lander.systems])
    

if __name__ == "__main__":
    resource.path = ['@adastra.resources']
    resource.reindex()

    director.init(caption="Ad Astra")
    x,y = director.get_window_size()
    lander = Lander(position=(x/2, y/2), scale=2)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def update(dt):
        lander.engine.throttle += dt * keyboard[key.W]
        lander.engine.throttle -= dt * keyboard[key.S]

    scene = Scene(LanderLayer(lander), SystemsDisplay(lander))
    scene.schedule(update)
    director.run(scene)
    
