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
        

if __name__ == "__main__":
    setup.resources()

    director.init(caption="Ad Astra", resizable=True, width=1024, height=640)
    x,y = director.get_window_size()

    lander = Lander(position=(x/2, 50))

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def update(dt):
        delta = 1
        lander.rvel = 0
        if keyboard[key.LSHIFT]:
            delta = 0.1
        lander.engine.throttle.value += dt * keyboard[key.W] * delta
        lander.engine.throttle.value -= dt * keyboard[key.S] * delta
        if keyboard[key.SPACE]:
            lander.engine.throttle.value = 0
        if keyboard[key.E]:
            lander.engine.throttle.value = 1
        if keyboard[key.A] or keyboard[key.D]:
            lander.rvel = keyboard[key.A] * -45 + keyboard[key.D] * 45
            lander.rvel *= delta 

    layer = Layer()
    layer.add(lander)

    scene = Scene(WorldLayer(lander), HUDLayer(lander, keyboard))
    scene.schedule(update)

    
    director.run(scene)
    
