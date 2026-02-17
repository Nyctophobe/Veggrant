import pygame
from util import SpriteManager, SCALE, RESOLUTION, vec, rectAdd

class Drawable(object):

    CAMERA_OFFSET = vec(20,0)


    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None):
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
        
        self.position=vec(*position)
        self.imageName = fileName
    
    def draw(self, drawSurface):
      drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
         
    def getSize(self):
        return vec(*self.image.get_size())    
   
    def getWidth(self):
        return self.getSize()[0]
    
    def getHeight(self):
        return self.getSize()[1]

    def getPosition(self):
        return self.position
    
    def setPosition(self, newPosition):
        self.position = vec(*newPosition)

    def getCollisionRect(self):
        return rectAdd(self.getPosition(), self.image.get_rect())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
      
