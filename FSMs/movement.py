from . import AbstractGameFSM
from util import vec, magnitude, EPSILON, scale, RESOLUTION

from statemachine import State

class MovementFSM(AbstractGameFSM):
    
    def __init__(self, obj):
        super().__init__(obj)
    
    def update(self, seconds):
        super().update(seconds)
        
        pass # Add out of bounds checks here
        


class AccelerationFSM(MovementFSM):
    """Axis-based speederation with gradual stopping."""
    not_moving = State(initial=True)
    
    negative = State()
    positive = State()
    
    stalemate = State()
    
    decrease  = not_moving.to(negative) | positive.to(stalemate) | negative.to.itself(internal=True)
    
    increase = not_moving.to(positive) | negative.to(stalemate) | positive.to.itself(internal=True)
    
    stop_decrease = negative.to(not_moving) | stalemate.to(positive) | not_moving.to.itself(internal=True) | positive.to.itself(internal=True)
    
    stop_increase = positive.to(not_moving) | stalemate.to(negative) | not_moving.to.itself(internal=True)
    
    stop_all      = not_moving.to.itself(internal=True) | negative.to(not_moving) | \
                    positive.to(not_moving) | stalemate.to(not_moving)
    
    def __init__(self, obj, axis=0):
        self.axis      = axis
        self.direction = vec(0,0)
        self.direction[self.axis] = 1
        self.speed = 50
        
        super().__init__(obj)

    def update(self, seconds=0):
        if self == "positive":
            self.obj.velocity[0] = self.direction[0] * self.speed  * seconds
        elif self == "negative":
            self.obj.velocity[0] = -self.direction[0] * self.speed * seconds
                
        elif self == "stalemate":
            pass
        else:
            if self.obj.velocity[self.axis] > self.speed * seconds *100:
                self.obj.velocity[self.axis] = self.speed * seconds * 100
            elif self.obj.velocity[self.axis] < -self.speed * seconds *100:
                self.obj.velocity[self.axis] = -self.speed * seconds *100
            elif self.obj.getInteracted() == False:
                self.obj.velocity[self.axis] = 0
        
        
    
        super().update(seconds)