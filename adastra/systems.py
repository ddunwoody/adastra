from cocos.cocosnode import CocosNode
from cocos.euclid import Point2
from cocos.particle import ParticleSystem, Color
from cocos.sprite import Sprite 

import numpy as np
import pkg_resources

from utils import load_image

import physics


class System(CocosNode):
    "Base class for items which update each frame and need a reference to the parent vehicle"
    def __init__(self):
        super(System, self).__init__()
        self.vehicle = None
        
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
        self._value = np.clip(value, self.min, self.max)
        
    def __str__(self):
        return "Throttle(%0.2f)" % self.value


class ValueAndRate(System):
    "Attribute indicator, including rate of change"
    def __init__(self, name, attr, offset=0, buffer=5):
        super(ValueAndRate, self).__init__()
        self.name = name
        self.attr = attr
        self.offset = offset
        self.buffer = buffer
        self.values = np.zeros(self.buffer)
        self.dts = np.zeros(self.buffer)
        self.idx = 0
        self.value = 0
        self.rate = 0

    def update(self, dt):
        #TODO: fix rate calculation
        self.value = getattr(self.vehicle, self.attr)
        self.values[self.idx] = self.value
        self.dts[self.idx] = dt
        self.rate = np.mean(self.values*self.dts*self.buffer)
        self.idx = 0 if self.idx == self.buffer-1 else self.idx + 1
        
    def __str__(self):
        return "%s(%+0.2f, %+0.2f)" % (self.name, self.value + self.offset, self.rate)


class Exhaust(ParticleSystem):
    "Flames from an engine"
    total_particles = 200
    duration = -1

    angle = 270.0
    angle_var = 10.0

    speed = 10.0
    speed_var = 2.0

    radial_accel = -2.0
    radial_accel_var = 0.5

    pos_var = Point2(3.0, 0.0)

    life = 3
    life_var = 0.5

    active = False
    emission_rate = 0

    # color of particles
    start_color = Color(0.75, 0.25, 0.12, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 0.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    size = 15.0
    size_var = 2.0

    blend_additive = True

    def __init__(self, engine):
        super(Exhaust, self).__init__()
        self.engine = engine
        
    def update(self, dt):
        if self.engine.thrust == 0:
            self.active = False
        else:
            self.active = True
            self.emission_rate = self.engine._power * self.total_particles / self.life


class Engine(System):
    def __init__(self, position, throttle=Throttle(), spool_time=3, max_thrust=1):
        super(Engine, self).__init__()
        self.position = position
        self.throttle = throttle
        self.spool_time = spool_time
        self.max_thrust = max_thrust
        self._power = 0
        self.exhaust = Exhaust(self)
        self.exhaust.position = (1, -2)
        self.add(self.exhaust)
      
    def update(self, dt):
        "Calculates power by lagging throttle according to spool_time"
        delta = self.throttle.value - self._power
        abs_move = dt / self.spool_time
        self._power += np.clip(delta, -abs_move, abs_move)
        if self.thrust > 0:
            self.vehicle.box.apply_force((0, self.thrust), self.position)
        self.exhaust.update(dt)
        
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
        self.systems.append(system)
        system.vehicle = self
        self.add(system)

    
class Lander(Vehicle):
    def __init__(self, image=pkg_resources.resource_filename("adastra.resources", "lander.png"), position=(0, 0), **kwargs):
        super(Lander, self).__init__(image, **kwargs)

        self.box = physics.Box(100, 15)
        self.add(self.box)
        self.position = self.box.body.position = position

        self.engine = Engine(position=(0, -4), max_thrust=1500)    
        self.add_system(self.engine)
        self.add_system(ValueAndRate("Alt", "y", -50))
        self.add_system(ValueAndRate("VVI", "vvel"))
        self.add_system(ValueAndRate("HVI", "hvel"))
        self.add_system(ValueAndRate("RVI", "rvel"))

    def update(self, dt):
        self.box.reset_forces()
        for system in self.systems:
            system.update(dt)
        self.box.update(dt)

        self.position = self.box.position
        self.rotation = self.box.rotation

    @property
    def vvel(self):
        return self.box.body.velocity[1]

    @property
    def hvel(self):
        return self.box.body.velocity[0]

    @property
    def rvel(self):
        return self.box.body.angular_velocity

