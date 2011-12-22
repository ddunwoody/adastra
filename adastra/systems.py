from cocos.sprite import Sprite 

from numpy import clip

class Throttle(object):
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


class Engine(Sprite):        
    def __init__(self, image="engine.png", position=(0,0), rotation=0, scale=1, throttle=Throttle(), spool_time=3, max_thrust=1):
        super(Engine, self).__init__(image, position, rotation, scale)
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
    def __init__(self, image="lander.png", position=(0,0), rotation=0, scale=1):
        super(Lander, self).__init__(image, position, rotation, scale)
        self.schedule(self.update)
        self.engine = Engine(position=(0,-4))
        self.add(self.engine)
        self.systems = [self.engine]

    def update(self, dt):
        for system in self.systems:
            system.update(dt)
