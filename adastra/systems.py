from numpy import clip

class Throttle(object):
    """
    """
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