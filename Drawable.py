import pygame
import os
import vector

class drawable(object):

    def __init__(self, image, position):
        pygame.init()
        #The image to draw on screenDisplay
        self.image = pygame.image.load(os.path.join(image)).convert()
        self.image.set_colorkey((0,0,0))
        #Where to draw the image
        self.position = position

    def draw(self, drawSurface):
        drawSurface.blit(self.image, vector.pyVec(self.position))
    
    def update(self, seconds):
        pass
