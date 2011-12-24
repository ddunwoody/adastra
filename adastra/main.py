from cocos.cocosnode import CocosNode
from cocos.director import director
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.scene import Scene
from cocos import tiles

from pyglet.window import key

import setup

from glnode import Ground
from hud import HUDLayer
from systems import Lander
    

class WorldLayer(ScrollableLayer):
    "Renders the lander and the world"
    def __init__(self, lander):
        super(WorldLayer, self).__init__()
        self.add(lander)


class ControlHandler(CocosNode):
    "Handles keyboard input directed to a vehicle"
    def __init__(self, vehicle):
        super(ControlHandler, self).__init__()
        self.keyboard = key.KeyStateHandler()
        self.vehicle = vehicle
        self.schedule(self.update)

    def update(self, dt):
        delta = 1
        self.vehicle.rvel = 0
        if self.keyboard[key.LSHIFT]:
            delta = 0.1
        self.vehicle.engine.throttle.value += dt * self.keyboard[key.W] * delta
        self.vehicle.engine.throttle.value -= dt * self.keyboard[key.S] * delta
        if self.keyboard[key.SPACE]:
            self.vehicle.engine.throttle.value = 0
        if self.keyboard[key.E]:
            self.vehicle.engine.throttle.value = 1
        if self.keyboard[key.A] or self.keyboard[key.D]:
            self.vehicle.rvel = self.keyboard[key.A] * -45 + self.keyboard[key.D] * 45
            self.vehicle.rvel *= delta 


if __name__ == "__main__":
    setup.resources()

    director.init(caption="Ad Astra", resizable=True, width=1024, height=640)
    x,y = director.get_window_size()

    lander = Lander(position=(x/2, 50))
    control_handler = ControlHandler(lander)
    director.window.push_handlers(control_handler.keyboard)

    scroller = ScrollingManager()
    map_layer = tiles.load('maps.xml')['map0']
    scroller.add(map_layer)
    scroller.add(WorldLayer(lander))

    scene = Scene(control_handler, scroller, HUDLayer(lander, control_handler.keyboard))
    director.run(scene)
    
