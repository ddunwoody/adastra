from cocos.cocosnode import CocosNode
from cocos.sprite import Sprite 

from numpy import clip
from math import radians, sin, cos

from utils import load_image

class System(CocosNode):
    def __init__(self):
        super(System, self).__init__()
        self.vehicle = None
        self.schedule(self._update)

    def _update(self, dt):
        if not self.vehicle:
            self.vehicle = self.get_ancestor(Vehicle)
        self.update(dt)

    def update(self, dt):
        pass

    
class Throttle(object):
    "Convenient class for constraining a value to a range"
    def __init__(self, min_value=0, max_value=1, value=0):
        self.min = min_value
        self.max = max_value
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = clip(value, self.min, self.max)
        
    def __str__(self):
        return "Throttle(%0.2f)" % self.value


class ValueAndRate(System):
    "Attribute indicator, including rate of change"
    def __init__(self, name, attr, offset=0):
        super(ValueAndRate, self).__init__()
        self.name = name
        self.attr = attr
        self.offset = offset
        self.value = 0
        self.rate = 0

    def update(self, dt):
        value = getattr(self.vehicle, self.attr)
        if dt == 0:
            self.rate = 0
        else:
            self.rate =  (value - self.value) / dt
        self.value = value
        
    def __str__(self):
        return "%s(%+0.2f, %+0.2f)" % (self.name, self.value+self.offset, self.rate)


class Engine(System):
    def __init__(self, position, throttle=Throttle(), spool_time=3, max_thrust=1):
        super(Engine, self).__init__()
        self.position = position
        self.throttle = throttle
        self.spool_time = spool_time
        self.max_thrust = max_thrust
        self._power = 0
        self.schedule(self.update)
      
    def update(self, dt):
        "Calculates power by lagging throttle according to spool_time"
        delta = self.throttle.value - self._power
        abs_move = dt / self.spool_time
        self._power += clip(delta, -abs_move, abs_move)
        
    @property
    def thrust(self):
        return self._power * self.max_thrust

    def __str__(self):
        return "Engine(%0.2f/%0.2f)" % (self._power, self.throttle.value)


class Vehicle(Sprite):
    "A player's vehicle"
    def __init__(self, image, **kwargs):
        super(Vehicle, self).__init__(load_image(image), **kwargs)
        self.systems = []

    def add_system(self, system):
        self.add(system)
        self.systems.append(system)

    
class Lander(Vehicle):
    def __init__(self, image="lander.png", **kwargs):
        super(Lander, self).__init__(image, **kwargs)
        self.vvel = 0
        self.hvel = 0
        self.rvel = 0
        self.vaccel = 0
        self.haccel = 0
        self.schedule(self.update)
        self.engine = Engine(position=(0,-4), max_thrust=15)
        self.add_system(self.engine)
        self.add_system(ValueAndRate("Alt", "y", -50))
        self.add_system(ValueAndRate("VVI", "vvel"))
        self.add_system(ValueAndRate("HVI", "hvel"))
        self.add_system(ValueAndRate("RVI", "rvel"))
        self.landed = True

    def update(self, dt):
        self.vaccel = -10 + self.engine.thrust * cos(radians(self.rotation))
        self.haccel = self.engine.thrust * sin(radians(self.rotation))
        self.vvel += self.vaccel * dt
        self.hvel += self.haccel * dt
        self.y += self.vvel * dt
        self.x += self.hvel * dt
        self.rotation += self.rvel * dt

        if self.y < 50:
            self.y = 50
            self.vvel = 0
            self.hvel = 0
            self.rvel = 0
            self.rotation = 0
            if not self.landed:
                self.engine.throttle.value = 0
                self.landed = True
        else:
            self.landed = False
