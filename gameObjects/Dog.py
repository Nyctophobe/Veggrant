from pygame import Rect

from FSMs import WalkingFSM
from . import Movable
from util import vec

class Dog(Movable):
   def __init__(self, leftBounding, rightBounding, dragDrop, position, fileName, rotate = False):
      super().__init__(position, fileName, rotate)
      self.leftBounding = leftBounding*16
      self.rightBouding = rightBounding*16
      self.dragDrop = dragDrop*16

      self.velocity = vec(0,0)
      self.reactCollid = Rect(0,0,0,0)
      self.chillout = 0

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
         "standing" : 8
      }
            
      self.FSManimated = WalkingFSM(self)

   def update(self, seconds):
      if self.chillout == 0:
         self.reactCollid = Rect(self.position[0]+self.getWidth()-5, self.position[1]+13, 10, self.getHeight())
      elif self.chillout == 30:
         self.chillout = 0
      elif self.chillout > 0:
         self.chillout += 1



      if self.position[0] >= self.rightBouding:
         self.velocity = self.velocity*-1
      if self.position[0] <= self.leftBounding:
         self.velocity = self.velocity*-1

      super().update(seconds)
      pass

   def getReactCollid(self):
      return self.reactCollid

   def fetch(self):
      self.velocity = vec(50,0)
      #if negative
      if self.velocity[0] < 0:
         if self.position[0] > self.dragDrop:
            pass
         elif self.position[0] < self.dragDrop:
            self.velocity = self.velocity*-1
         if self.position[0] < self.dragDrop and self.position[0] > self.dragDrop-16:
            self.noAggro()

      #if positive
      if self.velocity[0] > 0:
         if self.position[0] < self.dragDrop:
            pass
         elif self.position[0] > self.dragDrop:
            self.velocity = self.velocity*-1
         if self.position[0] > self.dragDrop-16 and self.position[0] < self.dragDrop:
            self.noAggro()
   
   def noAggro(self):
      self.reactCollid = Rect(0,0,0,0)
      self.chillout = 1
