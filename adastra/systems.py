from cocos.sprite import Sprite 

from numpy import clip
from math import radians, sin, cos

from utils import load_image

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
        
    def __iadd__(self, other):
        self.value += other
        return self

    def __isub__(self, other):
        self.value -= other
        return self

    def __str__(self):
        return "Throttle(%0.2f)" % self.value

class VVI(object):
    def __init__(self, lander):
        self.lander = lander
        self.vvel = self.lander.vvel
        self.vaccel = None

    def update(self, dt):
        vvel = self.lander.vvel
        if dt == 0:
            self.vaccel = 0
        else:
            self.vaccel =  (vvel - self.vvel) / dt
        self.vvel = vvel
        
    def __str__(self):
        return "VVI(%0.2f, %+0.2f)" % (self.vvel, self.vaccel)

class HSI(object):
    def __init__(self, lander):
        self.lander = lander

    def __str__(self):
        return "HSI(%0.2f, %+0.2f)" % (self.lander.rotation, self.lander.rvel)


#TODO: refactor to separate rendering and engine modelling
class Engine(Sprite):
    "Renders a sprite and lags the thrust demanded by a throttle"        
    def __init__(self, image="engine.png", position=(0,0), rotation=0, scale=1, throttle=Throttle(), spool_time=3, max_thrust=1):
        super(Engine, self).__init__(load_image(image), position, rotation, scale)
        self.throttle = throttle
        self.max_thrust = max_thrust
        self._power = 0
        self.spool_time = spool_time
        
    def update(self, dt):
        delta = self.throttle.value - self._power
        abs_move = dt / self.spool_time
        self._power += clip(delta, -abs_move, abs_move)
        
    @property
    def thrust(self):
        return self._power * self.max_thrust

    def __str__(self):
        return "Engine(%0.2f/%0.2f)" % (self._power, self.throttle.value)

    
class Lander(Sprite):
    "A player's ship"
    def __init__(self, image="lander.png", position=(0,0), rotation=0, scale=1):
        super(Lander, self).__init__(load_image(image), position, rotation, scale)
        self.vvel = 0
        self.hvel = 0
        self.rvel = 0
        self.vaccel = 0
        self.haccel = 0
        self.schedule(self.update)
        self.engine = Engine(position=(0,-4), max_thrust=12)
        self.add(self.engine)
        self.systems = [self.engine, VVI(self), HSI(self)]
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
            
        for system in self.systems:
            if hasattr(system, 'update'):
                system.update(dt)
