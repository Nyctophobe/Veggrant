from pygame import Rect
from . import Movable
from FSMs import WalkingFSM, AccelerationFSM, GravityFSM
from util import vec, rectAdd, RESOLUTION

from pygame.locals import *
import numpy as np


class Egg(Movable):
   def __init__(self, position, rotate = False):
      super().__init__(position, "Egg.png", rotate)
      self.standRect = Rect(0,0,0,0)
      self.climbRect = Rect(self.getPosition()[0]-1, self.getPosition()[1]+self.getHeight(), self.getWidth()+1, 16)
      self.lockDown = False
      self.interact = False
      self.boil = False
      self.crack = False
        
      # Animation variables specific to Egg
      
      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 1,
         "standing" : 1
      }
      
      self.rowList = {
         "moving"   : 0,
         "standing" : 0
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.grav = GravityFSM(self)      
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if not self.getLockDown():
            if self.grav.hasGround == True or self.boil == True:
               if event.key == K_SPACE:
                  self.grav.bounceCount = 5
               if event.key == K_a:
                  self.LR.decrease()
                  
               elif event.key == K_d:
                  self.LR.increase()
               elif event.key == K_b:
                  if self.boil == False:
                     self.boil = True
                     self.crack = False
                     self.grav.gravity = 6000
                     self.maxVelocity = 400
                     self.trackMaxVel = 400
                  else:
                     self.boil = False
                     self.grav.gravity = 3000
                     self.maxVelocity = 250
                     self.trackMaxVel = 250
               elif event.key == K_c:
                  if self.crack == True:
                     self.crack = False
                  else:
                     self.crack = True
                     self.boil = False
                     self.grav.gravity = 3000
                     self.maxVelocity = 250
                     self.trackMaxVel = 250
               elif event.key == K_LSHIFT:
                  if self.boil == True:
                     self.crack = True
                     self.boil = False
                     self.grav.gravity = 3000
                     self.maxVelocity = 250
                     self.trackMaxVel = 250
                  else:
                     self.boil = True
                     self.crack = False
                     self.grav.gravity = 6000
                     self.maxVelocity = 400
                     self.trackMaxVel = 400
                  

            if event.key == K_SPACE and self.LR == 'not_moving' and self.grav.hasGround == True and self.boil == False:
               self.grav.jump()
         
      elif event.type == KEYUP:
         if not self.getLockDown():
            if event.key == K_a and self.getInteracted() == False:
               self.LR.stop_decrease()
               
            elif event.key == K_d and self.getInteracted() == False:
               self.LR.stop_increase()
      elif self.getInteracted() == True:
         self.LR.stop_all()
   
   def update(self, collidables, seconds):
      self.LR.update(seconds)
      self.grav.update(collidables, seconds)
      if self.boil == True:
         if self.grav == "falling":
            self.grav.gravity = 6000
         if self.grav == "jumping":
            self.grav.gravity == 1000
      else:
         self.grav.gravity = 3000 
      if self.grav.jumpTimer < 0:
         self.grav.fall()
      self.standRect = Rect(self.getPosition()[0], self.getPosition()[1]+self.getHeight(), self.getWidth(), 1)
      if self.grav.hasGround == False and self.getInteracted() == False and self.boil == False:
         self.LR.stop_all()
      super().update(seconds)

   def getStandRect(self):
      return self.standRect
   
   def getEgg(self):
      return self
   
   def setLockDown(self, lockToggle):
      self.lockDown = lockToggle

   def getLockDown(self):
      return self.lockDown

   def setInteracted(self, interactToggle):
      self.interact = interactToggle
   
   def getInteracted(self):
      return self.interact

      
   
  