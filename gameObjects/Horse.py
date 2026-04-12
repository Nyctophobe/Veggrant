from pygame import Rect

from FSMs import DocileFSM
from . import Movable
from util import vec

class Horse(Movable):
    def __init__(self, position, fileName, rotate = False, angle = 0):
        super().__init__(position, fileName, rotate, angle)
        self.velocity = vec(0,0)
        self.reactCollid = Rect(0,0,0,0)
        self.chill = False

        self.framesPerSecond = 1
        self.nFrames = 2
        
        self.nFramesList = {
         "chilling"   : 1,
         "standing" : 1
        }

        self.rowList = {
         "chilling"   : 1,
         "standing" : 0
        }

        self.framesPerSecondList = {
         "chilling"   : 1,
         "standing" : 8
        }
            
        self.FSManimated = DocileFSM(self)

    def update(self, seconds):
        self.reactCollid = Rect(self.position[0]+self.getWidth()/4, self.position[1]+self.getHeight(),self.getWidth()/2, 15)

        super().update(seconds)
        pass

    def getReactCollid(self):
        return self.reactCollid
