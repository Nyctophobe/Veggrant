import pygame
import os
from . import Drawable, Egg, Human, Dog
from util import SoundManager, vec, rectAdd, RESOLUTION

class GameEngine(object):
    def __init__(self):
        #Main Character       
        self.egg = Egg((0,0))
        self.size = vec(*RESOLUTION)

        #Obstacles
        self.dog = Dog((0,0), "Dog.png", (0,0))
        self.human = Human((0,0))

        #Blocks for building Levels
        self.QBBlack = Drawable((0,0),"QuadBlock.png", (0,0))
        self.QBBlue = Drawable((0,0), "QuadBlock.png", (1,0))
        self.QBGreen = Drawable((0,0), "QuadBlock.png", (0,1))
        self.QBBrown = Drawable((0,0), "QuadBlock.png", (1,1))
        self.collidables = []

        #Others
        self.background = Drawable((0,0), "background.png")
        self.sm = SoundManager.getInstance()
    
    def draw(self, drawSurface):  
        drawSurface.fill(vec(0,200,255))
        self.egg.draw(drawSurface)
        """
        self.dog.draw(drawSurface)
        self.human.draw(drawSurface)"""
        GameEngine.readLevel(self, drawSurface)

    def handleEvent(self, event):
        self.egg.handleEvent(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sm.playSFX("Blowing Wind.wav")
    
    def update(self, seconds):
        self.egg.update(seconds)
        for collid in self.collidables:
            if self.egg.getCollisionRect().clip(collid):
                
                self.egg.grav.hasGround = True
        
        Drawable.updateOffset(self.egg, self.size)
    
    def readLevel(self, drawSurface):
        file_path = "C:\\Users\\simon\\My Games\\vEggrant\\gameObjects\\level1.txt"
        file = open(file_path, 'r')
        columnCount = 0
        lineCount = -1

        for line in file:
            lineCount += 1
            columnCount = 0
            for char in line:
                if not char:
                    
                    break
                #Stone
                if char == "s":
                    self.QBBlack.setPosition((16*columnCount, 16*lineCount))
                    self.QBBlack.draw(drawSurface)
                #Green
                elif char == "g":
                    self.QBGreen.setPosition((16*columnCount, 16*lineCount))
                    self.QBGreen.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)

                #Blue
                elif char == "b":
                    self.QBBlue.setPosition((16*columnCount, 16*lineCount))
                    self.QBBlue.draw(drawSurface)
                #Tree
                elif char == "t":
                    self.QBBrown.setPosition((16*columnCount, 16*lineCount))
                    self.QBBrown.draw(drawSurface)
                elif char == "d":
                    self.dog.setPosition((16*columnCount, 16*lineCount))
                    self.dog.draw(drawSurface)
                elif char == "h":
                    self.human.setPosition((16*columnCount, 16*lineCount))
                    self.human.draw(drawSurface)
                else:
                    pass
                columnCount += 1
    