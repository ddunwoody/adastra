from cocos.cocosnode import CocosNode
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene

from pyglet.window import key

import setup

from glnode import Ground
from hud import HUDLayer
from systems import Lander
    

class WorldLayer(Layer):
    def __init__(self, lander):
        super(WorldLayer, self).__init__()
        self.add(lander)
        self.add(Ground(lander.get_rect().bottom + 1))


class ControlHandler(CocosNode):
    def __init__(self, lander):
        super(ControlHandler, self).__init__()
        self.keyboard = key.KeyStateHandler()
        self.lander = lander
        self.schedule(self.update)

    def update(self, dt):
        delta = 1
        self.lander.rvel = 0
        if self.keyboard[key.LSHIFT]:
            delta = 0.1
        self.lander.engine.throttle.value += dt * self.keyboard[key.W] * delta
        self.lander.engine.throttle.value -= dt * self.keyboard[key.S] * delta
        if self.keyboard[key.SPACE]:
            self.lander.engine.throttle.value = 0
        if self.keyboard[key.E]:
            self.lander.engine.throttle.value = 1
        if self.keyboard[key.A] or self.keyboard[key.D]:
            self.lander.rvel = self.keyboard[key.A] * -45 + self.keyboard[key.D] * 45
            self.lander.rvel *= delta 


if __name__ == "__main__":
    setup.resources()

    director.init(caption="Ad Astra", resizable=True, width=1024, height=640)
    x,y = director.get_window_size()

    lander = Lander(position=(x/2, 50))
    control_handler = ControlHandler(lander)
    director.window.push_handlers(control_handler.keyboard)

    scene = Scene(control_handler, WorldLayer(lander), HUDLayer(lander, control_handler.keyboard))
    director.run(scene)
    
