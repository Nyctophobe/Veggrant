import pygame
from math import floor
from statemachine import State
from . import AbstractGameFSM
from gameObjects import Movable

class GravityFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj) 
        self.jumpTimer = 0
        self.gravity = 3000
        self.jumpSpeed = 3000
        self.jumpTime = 0.1
        self.hasGround = True
        self.bonked = False
        self.standRect = pygame.Rect(self.obj.getPosition()[0], self.obj.getPosition()[1]+self.obj.getHeight(), self.obj.getWidth(), 1)

        self.fallStart = 0
        self.bounceCount = 0
        self.gravToggle = False
        self.count = 0
        self.groundTime = 0
        self.collided = (0,0)

        self.climbTouch = 0

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
        return self.bonked or (self.jumpTimer <= 0 and not self.hasGround)

    def canJump(self):
        return self.hasGround and self.jumpTimer >= 0

    def canLand(self):
        return self.hasGround

    def on_enter_jumping(self):
        self.jumpTimer = self.jumpTime
        self.hasGround = False
    
    def on_enter_falling(self):
        self.jumpTimer = 0
        self.bonked = False
    
    def on_enter_grounded(self):
        self.jumpTimer = 0
        self.hasGround = True
        self.obj.setLockDown(False)
        self.obj.setInteracted(False)
        self.obj.maxVelocity = self.obj.trackMaxVel
        self.obj.LR.speed = 5000
        self.obj.setBypass(False)

    def update(self, collidables, seconds=0):
        self.updateState()
        super().update(seconds)
        stand = 0
        #Checks if ground time should be updated
        if self.groundTime <= 10 and self == "grounded":
            self.groundTime+= 1
        else:
            self.groundTime = 0
        if self.groundTime == 10:
            self.bounceCount = 0
            self.fallStart = self.obj.position[1]

        #Checking collision with objects and for Ground Below
        for collid in collidables:
            if self.obj.getCollisionRect().clip(collid):
                #Normal Collision
                if self.obj.crack == False:
                    #Left & Right Collision
                    if self.obj.velocity[1] == 0 and self.obj.velocity[0] != 0:
                        if self.obj.position[0] > collid[0]:
                            self.obj.position[0] = (self.obj.position[0]+self.obj.getCollisionRect().clip(collid)[2]+1)
                        else:
                            self.obj.position[0] = (self.obj.position[0]-self.obj.getCollisionRect().clip(collid)[2]-1)
                        self.obj.velocity[0] = 0
                    #Head Collision
                    elif self.obj.position[1] > collid[1] and floor(self.obj.position[1]) != collid[1]:
                        self.bonked = True
                        self.fall()
                        self.obj.setPosition((self.obj.position[0], self.obj.position[1]+self.obj.getCollisionRect().clip(collid)[3]))
                    #Feet Collision
                    elif (self == "falling" or "grounded") and floor(self.obj.position[1]) != collid[1]:
                        self.collided = (collid[0], collid[1])
                        self.obj.setPosition((self.obj.position[0], self.obj.position[1]-self.obj.getCollisionRect().clip(collid)[3]))
                        if self.obj.boil == True:
                            if self.bounceCount < 4:
                                self.gravToggle = True
                                self.obj.velocity[1] = self.obj.velocity[1]*-2
                                self.bounceCount += 1
                            else:
                                self.obj.velocity[1] = 0
                                self.obj.setPosition((self.obj.position[0], self.obj.position[1]-self.obj.getCollisionRect().clip(collid)[3]))
                
                #Cracked Physics
                else:
                    #Head Collision
                    if self.obj.position[1] > collid[1] and floor(self.obj.position[1]) != collid[1] and self.climbTouch == 0:
                        stand = 3
                        self.obj.setPosition((self.obj.position[0], self.obj.position[1]+self.obj.getCollisionRect().clip(collid)[3]))
                    #Left & Right Collision
                    elif self.obj.velocity[0] != 0:
                        self.climbTouch = 1
                        stand = 1
                        if self.obj.position[0] > collid[0]:
                            self.obj.position[0] = (self.obj.position[0]+self.obj.getCollisionRect().clip(collid)[2]-2)
                            self.obj.position[1] = (self.obj.position[1]-1)
                        else:
                            self.obj.position[0] = (self.obj.position[0]-self.obj.getCollisionRect().clip(collid)[2]+2)
                            self.obj.position[1] = (self.obj.position[1]-1)
                        self.obj.velocity[0] = 0
                    #Feet Collision
                    elif (self == "falling" or "grounded") and floor(self.obj.position[1]) != collid[1] and self.climbTouch == 0:
                        stand = 1
                        self.collided = (collid[0], collid[1])
                        self.obj.setPosition((self.obj.position[0], self.obj.position[1]-self.obj.getCollisionRect().clip(collid)[3]))
                        if self.obj.boil == True:
                            if self.bounceCount < 4:
                                self.gravToggle = True
                                self.obj.velocity[1] = self.obj.velocity[1]*-2
                                self.bounceCount += 1
                            else:
                                self.obj.velocity[1] = 0
                                self.obj.setPosition((self.obj.position[0], self.obj.position[1]-self.obj.getCollisionRect().clip(collid)[3]))

            if stand == 3:
                pass
            elif self.obj.standRect.clip(collid):
                stand = 1
        if stand == 1 and self.obj.crack == False:
            self.hasGround = True
        elif stand == 1 and self.obj.crack == True:
            self.hasGround = True
        elif stand == 3:
            self.hasGround = True
        else:
            self.hasGround = False
            self.climbTouch = 0
        if self == "falling" and self.gravToggle == False and self.obj.crack == False:
            self.obj.velocity[1] += self.gravity*seconds
            self.count = 0
        elif self == "jumping":
            self.obj.velocity[1] = -self.jumpSpeed
            self.jumpTimer -= seconds
        elif self.gravToggle == True:
            self.count += 1
            if self.count >= ((self.collided[1]-self.fallStart)/10):
                self.count = 0
                self.gravToggle = False
            
        elif self.obj.crack == True:
            if stand == 1:
                self.obj.velocity[1] = 0
                self.hasGround = True
            elif stand == 3:
                self.hasGround = True
            else:
                self.obj.velocity[1] += self.gravity*seconds
                self.count = 0
        else:
            self.obj.velocity[1] = 0
        
