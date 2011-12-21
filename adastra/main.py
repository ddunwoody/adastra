from cocos.director import director
from cocos.text import Label
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite 

from adastra.systems import Throttle

import pyglet.resource as resource
import pyglet.window.key as pygkey

class Lander(Sprite):
    def __init__(self, image="lander.png", position=(0,0), rotation=0, scale=1):
        super(Lander, self).__init__("lander.png", position, rotation, scale)
        self.schedule(self.update)
        self.throttle = Throttle()
        self.systems = [self.throttle]

    def update(self, dt):
        pass
        

class LanderLayer(Layer):
    def __init__(self, lander):
        super(LanderLayer, self).__init__()
        self.add(lander)


class SystemsDisplay(Layer):
    is_event_handler = True
    
    def __init__(self, lander):
        super(SystemsDisplay, self).__init__()
        self.lander = lander
        self.text = Label('', (director.get_window_size()[0] - 10 ,10), anchor_x="right")
        self.value = 0
        self.add(self.text)

    def update_text(self):
        self.text.element.text = ",".join([str(s) for s in self.lander.systems])
    
    def on_key_press(self, key, modifiers):
        if key == pygkey.W:
            self.lander.throttle += 0.1
        if key == pygkey.S:
            self.lander.throttle -= 0.1

    def on_key_release(self, key, modifiers):
        pass

    def on_draw(self):
        self.update_text()


if __name__ == "__main__":
    resource.path = ['@adastra.resources']
    resource.reindex()

    director.init(caption="Ad Astra")

    x,y = director.get_window_size()
    lander = Lander(position=(x/2, y/2), scale=2)
    director.run(Scene(LanderLayer(lander), SystemsDisplay(lander)))
    
