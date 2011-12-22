from cocos.sprite import Sprite 

from adastra.systems import Engine

class Lander(Sprite):
    def __init__(self, image="lander.png", position=(0,0), rotation=0, scale=1):
        super(Lander, self).__init__("lander.png", position, rotation, scale)
        self.schedule(self.update)
        self.engine = Engine()
        self.systems = [self.engine]

    def update(self, dt):
        for system in self.systems:
            system.update(dt)
