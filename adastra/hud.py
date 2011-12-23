from cocos.batch import BatchNode
from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.text import Label

from pyglet.resource import image 
from pyglet.window import key


class HUDLayer(Layer):
    "Display HUD elements"
    def __init__(self, systems, keyboard):
        super(HUDLayer, self).__init__()
        x = director.get_window_size()[0]
        self.add(SystemsLabel(systems, (x-10, 10), anchor_x="right"))
        self.add(ThrusterLights(keyboard, (x/2,13)))


class SystemsLabel(Label):
    "Displays a textual representation of the systems passed"
    def __init__(self, systems, position=(0,0), **kwargs):
        super(SystemsLabel, self).__init__("bar", position, **kwargs)
        self.systems = systems
        self.schedule(self.update)
        
    def update(self, dt):
        self.element.text = ",".join([str(s) for s in self.systems])

        
class ThrusterLights(BatchNode):
    "Displays a little light for each thruster pressed"
    def __init__(self, keyboard, position, scale=1, spread=3):
        super(ThrusterLights, self).__init__()
        self.keyboard = keyboard
        self.position = position

        self.images = [image("light_unlit.png"), image("light_green.png")]
        self.sprites = {}
        self.sprites[key.W] = Sprite(self.images[0], (0, spread), scale=scale)
        self.sprites[key.S] = Sprite(self.images[0], (0, -spread), scale=scale)
        self.sprites[key.A] = Sprite(self.images[0], (-spread*2, 0), scale=scale)
        self.sprites[key.D] = Sprite(self.images[0], (spread*2, 0), scale=scale)

        for sprite in self.sprites.values():
            self.add(sprite)

        self.schedule(self.update)

    def update(self, dt):
        for k, sprite in self.sprites.iteritems():
            if self.keyboard[k]:
                sprite.image = self.images[1]
            else:
                sprite.image = self.images[0]
