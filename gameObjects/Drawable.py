import pygame
from util import SpriteManager, SCALE, RESOLUTION, vec, rectAdd, pyVec

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
    
    def __init__(self, position=vec(0,0), fileName="", offset=None, rotate = False, angle = 0):
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
        self.position=vec(*position)
        self.imageName = fileName
        self.flipImage = [False, False]
        self.rotate = rotate
        self.angle = angle
        self.original = self.image
    
    def setDrawPosition(self):
        if self.rotate:
            self.image = pygame.transform.rotate(self.original, self.angle)
            center = vec(*self.original.get_rect().center)
            rotatedCenter = vec(*self.image.get_rect().center)
            self.drawPosition = self.position + center - rotatedCenter
                
        else:
            self.drawPosition = self.position
    
    def draw(self, drawSurface):
        self.setDrawPosition()
        blitImage = pygame.transform.flip(self.image, *self.flipImage)
        
        drawSurface.blit(blitImage,
                         pyVec(self.drawPosition - Drawable.CAMERA_OFFSET)) 

         
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
      
