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
    
    
class Engine(object):        
    def __init__(self, throttle=Throttle(), spool_time = 3):
        self.throttle = throttle
        self._thrust = 0
        self.spool_time = spool_time
        
    def step(self, dt):
        delta = self.throttle.value - self._thrust
        abs_move = dt / self.spool_time
        self._thrust += clip(delta, -abs_move, abs_move)
        
    @property
    def thrust(self):
        return self._thrust

    def __str__(self):
        return "Engine(%0.2f/%0.2f)" % (self._thrust, self.throttle.value)
        
    