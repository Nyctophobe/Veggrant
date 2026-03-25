from statemachine import State
from . import AbstractGameFSM

class GravityFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj) 
        self.jumpTimer = 0
        self.gravity = 200
        self.jumpSpeed = 100
        self.jumpTime = 0.2
        self.hasGround = False

    grounded = State(initial=True)
    jumping = State()
    falling = State()

    updateState = falling.to(grounded, cond="canLand") | \
                  grounded.to(falling, cond="canFall") | \
                  jumping.to(falling, cond="canFall") | \
                  jumping.to.itself(internal=True) | \
                  grounded.to.itself(internal=True) | \
                  falling.to.itself(internal=True)


    jump = grounded.to(jumping, cond = 'canJump') | \
           jumping.to.itself(internal=True) | \
           falling.to.itself(internal=True) | \
           grounded.to.itself(internal=True)
    
    fall = jumping.to(falling) | \
           falling.to.itself(internal=True) | \
           grounded.to.itself(internal=True)

    
    def canFall(self):
        return self.jumpTimer <= 0 and not self.hasGround

    def canJump(self):
        return self.hasGround

    def canLand(self):
        return self.hasGround

    def on_enter_jumping(self):
        self.jumpTimer = self.jumpTime
        self.hasGround = False
    
    def on_enter_falling(self):
        self.jumpTimer = 0
    
    def on_enter_grounded(self):
        self.jumpTimer = 0


    #Add Collision
    def update(self, seconds=0):
        self.updateState()
        super().update(seconds)
        if self == "falling":
            self.obj.velocity[1] += self.gravity * seconds
        elif self == "jumping":
            self.obj.velocity[1] = -self.jumpSpeed
            self.jumpTimer -= seconds
        else:
            self.obj.velocity[1] = 0
        
        


