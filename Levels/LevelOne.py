import pygame
from gameObjects import Drawable
from util import WORLD_SIZE

class LevelOne(object):
    def __init__(self):
        self.QBBlack = Drawable((0,0),"QuadBlock.png", (0,0))
        self.QBBlue = Drawable((0,0), "QuadBlock.png", (1,0))
        self.QBGreen = Drawable((0,0), "QuadBlock.png", (0,1))
        self.QBBrown = Drawable((0,0), "QuadBlock.png", (1,1))
        pass

    def readLevel(self, drawSurface):
        file = open('level1.txt', 'r')
        columnCount = 0
        lineCount = 0
        for line in file:
            for char in line:
                if not char:
                    columnCount = 0
                    lineCount += 1
                    break
                #Stone
                if char == "s":
                    self.QBBlack.setPosition((16*columnCount, 16*lineCount))
                    self.QBBlack.draw()
                #Green
                elif char == "g":
                    self.QBGreen.setPosition((16*columnCount, 16*lineCount))
                    self.QBGreen.draw()
                #Blue
                elif char == "b":
                    self.QBBlue.setPosition((16*columnCount, 16*lineCount))
                    self.QBBlue.draw()
                #Tree
                elif char == "t":
                    self.QBBrown.setPosition((16*columnCount, 16*lineCount))
                    self.QBBrown.draw()
                else:
                    pass
                columnCount += 1

        file.close()
    
            
