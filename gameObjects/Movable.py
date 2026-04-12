from . import Animated
from util import vec, magnitude, scale

class Movable(Animated):
    def __init__(self, position, fileName="", rotate = False, angle = 0):
        super().__init__(position, fileName, rotate,  angle)

        self.velocity = vec(0,0)
        self.maxVelocity = 250
        self.trackMaxVel = 250
        self.bypass = False
    
    def update(self, seconds):
        super().update(seconds)
        if (magnitude(self.velocity) > self.maxVelocity and self.bypass == False):
            self.velocity = scale(self.velocity, self.maxVelocity)
        self.position += self.velocity * seconds
        

    def setBypass(self, bypassToggle):
        self.bypass = bypassToggle
    
    def getBypass(self):
        return self.bypass
