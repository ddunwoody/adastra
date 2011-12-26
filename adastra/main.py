from cocos.cocosnode import CocosNode
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene

from pyglet.window import key

import setup

from glnode import Ground
from hud import HUDLayer
from systems import Lander
import physics    

class WorldLayer(Layer):
    "Renders the lander and the world"
    def __init__(self, lander):
        super(WorldLayer, self).__init__()
        self.add(Ground(lander.get_rect().bottom + 1))
        self.add(lander)


class ControlHandler(CocosNode):
    "Handles keyboard input directed to a vehicle"
    def __init__(self, vehicle):
        super(ControlHandler, self).__init__()
        self.keyboard = key.KeyStateHandler()
        self.vehicle = vehicle

    def update(self, dt):
        delta = 1
        if self.keyboard[key.X]:
            physics.draw_debug = not physics.draw_debug
        if self.keyboard[key.LSHIFT]:
            delta = 0.1
        self.vehicle.engine.throttle.value += dt * self.keyboard[key.W] * delta
        self.vehicle.engine.throttle.value -= dt * self.keyboard[key.S] * delta
        if self.keyboard[key.SPACE]:
            self.vehicle.engine.throttle.value = 0
        if self.keyboard[key.E]:
            self.vehicle.engine.throttle.value = 1
        if self.keyboard[key.A] or self.keyboard[key.D]:
            torque = 1000 * delta
            self.vehicle.box.body.torque = self.keyboard[key.A] * torque + self.keyboard[key.D] * -torque

def main():
    setup.resources()
    physics.space.gravity = (0, -10)
    director.init(caption="Ad Astra", resizable=True, width=1024, height=640)
    x,y = director.get_window_size()

    lander = Lander(position=(x/2, 50))
    control_handler = ControlHandler(lander)
    director.window.push_handlers(control_handler.keyboard)

    scene = Scene(control_handler, WorldLayer(lander), HUDLayer(lander, control_handler.keyboard))
    def update(dt):
        control_handler.update(dt)
        lander.update(dt)
        physics.space.step(dt)
    scene.schedule_interval(update, 1/60.0)
    director.run(scene)

if __name__ == "__main__":
    import cProfile
    cProfile.run('main()', 'mainprof')
