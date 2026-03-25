from pygame import Rect
from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM, GravityFSM
from util import vec, rectAdd, RESOLUTION

from pygame.locals import *
import numpy as np


class Egg(Mobile):
   def __init__(self, position):
      super().__init__(position, "kirby.png")
        
      # Animation variables specific to Egg
      
      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 4,
         "standing" : 2
      }
      
      self.rowList = {
         "moving"   : 1,
         "standing" : 0
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.grav = GravityFSM(self)

      self.standRect = rectAdd((self.position[0], self.position[1]+16), Rect(0,0,16,2))
      
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if self.grav.hasGround == True:
            if event.key == K_a:
               self.LR.decrease()
               
            elif event.key == K_d:
               self.LR.increase()

         if event.key == K_w and self.LR == 'not_moving':
            self.grav.jump()
            
      elif event.type == KEYUP:
         if self.grav.hasGround == True:
            if event.key == K_a:
               self.LR.stop_decrease()
               
            elif event.key == K_d:
               self.LR.stop_increase()
         if event.key == K_d:
            self.grav.fall()
   
   def update(self, seconds): 
      self.LR.update(seconds)
      self.grav.update(seconds)
      
      
      super().update(seconds)

   def getStandRect(self):
      return self.standRect
   
  