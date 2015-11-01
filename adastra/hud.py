from cocos.batch import BatchNode
from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.text import Label
import pkg_resources

from utils import load_image

from pyglet.image import ImageGrid
from pyglet.window import key

class HUDLayer(Layer):
    "Display HUD elements"
    def __init__(self, vehicle, keyboard):
        super(HUDLayer, self).__init__()
        x = director.get_window_size()[0]
        self.add(SystemsLabel(vehicle.systems, (x-5, 10), anchor_x="right", font_name="Press Start 2P", font_size=8))
        self.add(ThrusterLights(keyboard, (x-16, 64)))


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
    def __init__(self, keyboard, position, spread=3):
        super(ThrusterLights, self).__init__()
        self.keyboard = keyboard
        self.position = position

        self.images = ImageGrid(load_image(pkg_resources.resource_filename("adastra.resources", "lights.png")), 1, 2)

        self.sprites = {}
        self.sprites[key.W] = Sprite(self.images[0], (0, spread))
        self.sprites[key.S] = Sprite(self.images[0], (0, -spread))
        self.sprites[key.A] = Sprite(self.images[0], (-spread*2, 0))
        self.sprites[key.D] = Sprite(self.images[0], (spread*2, 0))

        for sprite in self.sprites.values():
            self.add(sprite)

        self.schedule(self.update)

    def update(self, dt):
        "Turns on/off the relevant light associated to each key"
        for k, sprite in self.sprites.iteritems():
            if self.keyboard[k]:
                sprite.image = self.images[1]
            else:
                sprite.image = self.images[0]
