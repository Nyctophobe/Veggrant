from . import Animated
from util import vec, magnitude, scale

class Mobile(Animated):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(0,0)
        self.maxVelocity = 200
    
    def update(self, seconds):
        super().update(seconds)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)
        self.position += self.velocity * seconds

    """
    def __init__(self, position, fileName="", offset=None, maxSpeed = 100):
        super().__init__(position, fileName, offset)
        self.velocity = vec(0,0)
        self.maxSpeed = maxSpeed
    
    def update(self, seconds):
        super().update(seconds)
        if magnitude(self.velocity) > self.maxSpeed:
            self.velocity = scale(self.velocity, self.maxSpeed)

        self.position += self.velocity * seconds



class Player(Mobile):
    def __init__(self, position, fileName="", offset=None, maxSpeed = 100):
        super().__init__(position, fileName, offset, maxSpeed)
        self.speed = maxSpeed

        self.keyMap = {
            K_w   : False,
            K_s : False,
            K_d : False,
            K_a  : False
        }

    
    def handleEvent(self, event):
        if event.type in (KEYDOWN, KEYUP) and event.key in self.keyMap.keys():
            self.keyMap[event.key] = event.type == KEYDOWN
    
    def update(self, seconds):
        if self.keyMap[K_a] or self.keyMap[K_d]:
            if self.keyMap[K_a]:
                self.velocity[0] = -self.speed
            else:
                self.velocity[0] = self.speed
        else:
            self.velocity[0] = 0
        if self.keyMap[K_w] or self.keyMap[K_s]:
            if self.keyMap[K_w]:
                self.velocity[1] = -self.speed
            else:
                self.velocity[1] = self.speed
        else:
            self.velocity[1] = 0
        
        super().update(seconds)
"""