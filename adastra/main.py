from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene

from pyglet.window import key

import adastra.setup as setup
from adastra.systems import Lander
from adastra.hud import HUDLayer

if __name__ == "__main__":
    setup.resources()

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

    setup.gl()
    scene = Scene(layer, HUDLayer(lander.systems, keyboard))
    scene.schedule(update)

    
    director.run(scene)
    
