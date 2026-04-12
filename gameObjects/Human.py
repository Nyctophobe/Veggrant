from pygame import Rect, transform

from FSMs import KickingFSM
from . import Movable
from util import vec


class Human(Movable):
   def __init__(self, directionFace, position, fileName, platform = False):
      super().__init__(position, fileName)
      self.direction = directionFace
      self.reactCollid = Rect(0,0,0,0)
      self.kick = False
      self.kickTime = 0.5
      self.kicking = 0
      if platform != False:
         self.platform = platform[0]
         self.positionDown = self.platform[0:2]
         self.positionUp = [platform[1][0], platform[1][1]]
         self.destination = [platform[1][0], platform[1][1]]
         self.moveIt = False
      
      self.arrive = True
      self.ogPos = self.position
      self.tick = 0

      self.framesPerSecond = 2 
      self.nFrames = 2

      self.nFramesList = {
         "kicking"   : 1,
         "standing" : 1
      }

      self.rowList = {
         "kicking"   : 1,
         "standing" : 0
      }

      self.framesPerSecondList = {
         "kicking"   : 4,
         "standing" : 8
      }
            
      self.FSManimated = KickingFSM(self)

   def update(self, seconds):
      if self.getKick() == True and self.kicking == 0:
         self.kicking = self.kickTime
      if self.kicking != 0:
         self.kicking -= 0.02
         if self.kicking <= 0:
            self.kicking = 0
            self.setKick(False)
            self.FSManimated.stand()

      if self.direction == "right":
         self.reactCollid = Rect(self.position[0]+self.getWidth()-50, self.position[1]+self.getHeight()/1.5, 24, 40)
      elif self.direction == "left":
         self.reactCollid = Rect(self.position[0]+23, self.position[1]+self.getHeight()/1.5, 24, 40)
      
      if self.tick >= 1:
         self.tick += 1
      if self.tick == 40:
         self.tick == 0

      super().update(seconds)

   def getReactCollid(self):
      return self.reactCollid

   def setKick(self, kickToggle):
      self.kick = kickToggle

   def getKick(self):
      return self.kick
   
   def setMoveIt(self, moveToggle):
      self.moveIt = moveToggle

   def getMoveIt(self):
      return self.moveIt

   def movePlatform(self):
      
      #Platform has reached Up
      if self.platform[1] <= self.positionUp[1] and self.destination[1] == self.positionUp[1]:
         self.setMoveIt(False)
         self.destination[1] = self.positionDown[1]
         return
      #Platform has reached Down
      if self.platform[1] >= self.positionDown[1] and self.destination[1] == self.positionDown[1]:
         self.setMoveIt(False)
         self.destination[1] = self.positionUp[1]
         return
      #Move platform to destination up
      if self.destination[1] == self.positionUp[1]:
         self.platform[1] -= self.positionUp[1]/150
      #Move platform to destination down
      elif self.destination[1] == self.positionDown[1]:
         self.platform[1] += 10
   
   def moveKite(self):
      #Platform has reached up
      if (self.platform[0] >= self.positionUp[0] and self.platform[1] <= self.positionUp[1]) and self.destination == self.positionUp:
         self.setMoveIt(False)
         self.destination = self.positionDown
         return
      #Platform has reached Down
      if (self.platform[0] <= self.positionDown[0] and self.platform[1] >= self.positionDown[1])  and self.destination == self.positionDown:
         self.setMoveIt(False)
         self.destination = self.positionUp
         return
      
      #Move platform to destination up
      if self.destination == self.positionUp:
         if self.platform[1] <= self.positionUp[1]:
            if self.platform[0] >= self.positionUp[0]:
               pass
            else:
               self.platform[0] += 1
         else:
            self.platform[1] -= 2
      elif self.destination == self.positionDown:
         if self.platform[1] >= self.positionDown[1]:
            if self.platform[0] <= self.positionDown[0]:
               pass
            else:
               self.platform[0] -= 2
         else:
            self.platform[1] += 3
         
      
   def moveBridge(self):
      #Platform has reached up
      if (self.platform[0] <= self.positionUp[0]) and self.destination == self.positionUp:
         self.setMoveIt(False)
         return
      
      #Move platform to destination up
      if self.destination == self.positionUp:
         self.platform[0] -= self.positionUp[0]/150
      
   def shuffle(self, moveDirect, location):
      if moveDirect == "special1":
         if self.position[0] <= location[0]:
            if self.position[1] <= location[1]:
               self.arrive = True
            else:
               self.position[1] -= 1
         else:
            self.position[0] -= 2.5
      elif moveDirect == "special2":
         if self.position[0] >= location[0]:
            if self.position[1] >= location[1]:
               self.arrive = True
            else:
               self.position[1] += 1
         else:
            self.position[0] += 0.13
      elif moveDirect == "downright":
         if self.position[1] >= location[1]:
            if self.position[0] >= location[0]:
               self.arrive = True
            else:
               self.position[0] += 1
         else:
            self.position[1] += 1
      
      if moveDirect == "leftup":
         if self.position[0] <= location[0]:
            if self.position[1] <= location[1]:
               self.arrive = True
            else:
               self.position[1] -= 1
         else:
            self.position[0] -= 1
      elif moveDirect == "leftdown":
         if self.position[0] <= location[0]:
            if self.position[1] >= location[1]:
               self.arrive = True
            else:
               self.position[1] += 1
         else:
            self.position[0] -= 1
         
      elif moveDirect == "rightup":
         if self.position[0] >= location[0]:
            if self.position[1] <= location[1]:
               self.arrive = True
            else:
               self.position[1] -= 1
         else:
            self.position[0] += 0.7
      elif moveDirect == "rightdown":
         if self.position[0] >= location[0]:
            if self.position[1] >= location[1]:
               self.arrive = True
            else:
               self.position[1] += 1
         else:
            self.position[0] += 1

   def moveRope(self):
      #Platform has reached Up
      if self.platform[1] >= self.positionUp[1] and self.destination[1] == self.positionUp[1]:
         self.setMoveIt(False)
         self.destination[1] = self.positionDown[1]
         self.arrive = False
         return
      #Platform has reached Down
      if self.platform[1] <= self.positionDown[1] and self.destination[1] == self.positionDown[1]:
         self.setMoveIt(False)
         self.destination[1] = self.positionUp[1]
         return
      #Move platform to destination up
      if self.destination[1] == self.positionUp[1]:
         self.platform[1] += 1
      #Move platform to destination down
      elif self.destination[1] == self.positionDown[1]:
         self.platform[1] -= 1