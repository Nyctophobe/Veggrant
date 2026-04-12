import pygame
from . import Drawable, Egg, Human
from util import SoundManager, vec, RESOLUTION, FONT

class GameEngine2(object):
    def __init__(self):
        self.collidables = []
        self.winBox = pygame.Rect(16*38,16*18, 16, 16)
        self.gameWin = False
        self.sticky = False
        self.stickyBox = pygame.Rect(16*2, 16*18, 16*3, 16)
        self.bouncy = False
        self.bouncyBox = pygame.Rect(16*6, 16*8, 16, 16)

        #Main Character       
        self.egg = Egg((16*15,16*18))
        self.startPos = (16*15,16*18)
        self.size = vec(*RESOLUTION)

        #Enemies
        self.humanOne = Human("right", (16*6,16*13), "Human.png", (pygame.Rect(16*3, 16*19, 45, 5), (16*17, 16*11)))
        self.kiteDelay = 0
        self.collidables.append(self.humanOne.platform)
        self.humanTwo = Human("right", (16*26, 16*6), "Human.png", (pygame.Rect(16*30, 16*18.7, 16*4, 5), (16*24, 16*11)))
        self.collidables.append(self.humanTwo.platform)

        #Blocks for building Levels
        self.BrownDecor = Drawable((0,0),"Blocks.png", (0,0))
        self.BrownBlock = Drawable((0,0),"Blocks.png", (1,0))
        self.GreenDecor = Drawable((0,0),"Blocks.png", (0,1))
        self.GreenBlock = Drawable((0,0),"Blocks.png", (1,1))
        self.BlueDecor = Drawable((0,0),"Blocks.png", (0,2))
        self.BlueBlock = Drawable((0,0),"Blocks.png", (1,2))
        self.BlackDecor = Drawable((0,0),"Blocks.png", (0,3))
        self.BlackBlock = Drawable((0,0),"Blocks.png", (1,3))
        self.YellowDecor = Drawable((0,0),"Blocks.png", (2,0))
        self.YellowBlock = Drawable((0,0),"Blocks.png", (3,0))
        self.RedDecor = Drawable((0,0),"Blocks.png", (2,1))
        self.RedBlock = Drawable((0,0),"Blocks.png", (3,1))
        self.nest = Drawable((0,0), "Blocks.png", (3,3))
        self.Cloud = Drawable((0,0), "could.png")

        #Others
        self.background = Drawable((0,0), "background.png")
        self.sm = SoundManager.getInstance()
    
    def draw(self, drawSurface):  
        drawSurface.fill(vec(0,200,255))

        #Enemies pt 1
        self.humanOne.draw(drawSurface)
        pygame.draw.rect(drawSurface, (255,255,255), self.humanOne.platform)
        

        #Level
        GameEngine2.readLevel(self, drawSurface)
        
        #Enemies pt 2
        self.humanTwo.draw(drawSurface)
        pygame.draw.rect(drawSurface, (150, 75, 0), self.humanTwo.platform)

        #Egg
        self.egg.draw(drawSurface)

        #other
        if self.bouncy == True:
            drawSurface.blit(FONT.render("Bouncing infront will ", True, (255,0,0)), (16*4,16*5))
            drawSurface.blit(FONT.render("activate Human", True, (255,0,0)), (16*4,16*6))
        if self.sticky == True:
            drawSurface.blit(FONT.render("Press C to Stick", True, (255,0,0)), (16*2,16*15))
            drawSurface.blit(FONT.render("to Solid Blocks", True, (255,0,0)), (16*2,16*16))
        #pygame.draw.rect(drawSurface, (255, 0, 0), self.winBox)

    def handleEvent(self, event):
        self.egg.handleEvent(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.egg.setPosition(self.startPos)
            self.humanOne.setMoveIt(False)
            self.humanOne.platform[0] = 16*3 
            self.humanOne.platform[1] = 16*19
            self.humanTwo.platform[0] = 16*30
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.egg.grav.fall()
            self.egg.setPosition((pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2))

    
    def update(self, seconds):
        #Egg
        self.egg.update(self.collidables, seconds)
        Drawable.updateOffset(self.egg, self.size)

        if self.egg.position[1] > 16*22:
            self.egg.setPosition(self.startPos)
            self.humanOne.setMoveIt(False)
            self.humanOne.platform[0] = 16*3 
            self.humanOne.platform[1] = 16*18.8

        #Enemies
        self.humanOne.update(seconds)
        if self.egg.getCollisionRect().clip(self.humanOne.getReactCollid()):
            if self.egg.grav.hasGround == False and self.egg.grav != "falling" and self.egg.getInteracted() == False:
                self.humanOne.setMoveIt(True)
        if self.humanOne.getMoveIt() == True:
            self.humanOne.moveKite()
        if self.humanOne.destination == self.humanOne.positionDown:
            self.kiteDelay += 1
            if self.kiteDelay >= 100:
                self.humanOne.setMoveIt(True)
        if self.humanOne.destination == self.humanOne.positionUp:
                    self.kiteDelay = 0
        
        self.humanTwo.update(seconds)
        if self.egg.getCollisionRect().clip(self.humanTwo.getReactCollid()):
            if self.egg.grav.hasGround == False and self.egg.grav != "falling" and self.egg.getInteracted() == False:
                self.humanTwo.setMoveIt(True)
        if self.humanTwo.getMoveIt() == True:
            self.humanTwo.moveBridge()

        #other
        if self.egg.getCollisionRect().clip(self.stickyBox):
            self.sticky = True
        else:
            self.sticky = False 
        
        if self.egg.getCollisionRect().clip(self.bouncyBox):
            self.bouncy = True
        else:
            self.bouncy = False   
        
        #Win Box
        if self.egg.getCollisionRect().clip(self.winBox):
            self.gameWin = True
        

    
    
    def readLevel(self, drawSurface):
        file_path = "Levels\\level2.txt"
        file = open(file_path, 'r')
        columnCount = 0
        lineCount = -1

        for line in file:
            lineCount += 1
            columnCount = 0
            for char in line:
                if not char:
                    break
                #Brown
                if char == "t":
                    self.BrownDecor.setPosition((16*columnCount, 16*lineCount))
                    self.BrownDecor.draw(drawSurface)
                elif char == "T":
                    self.BrownBlock.setPosition((16*columnCount, 16*lineCount))
                    self.BrownBlock.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)
                #Green
                elif char == "g":
                    self.GreenDecor.setPosition((16*columnCount, 16*lineCount))
                    self.GreenDecor.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                elif char == "G":
                    self.GreenBlock.setPosition((16*columnCount, 16*lineCount))
                    self.GreenBlock.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)
                #Blue
                elif char == "b":
                    self.BlueDecor.setPosition((16*columnCount, 16*lineCount))
                    self.BlueDecor.draw(drawSurface)
                elif char == "B":
                    self.BlueBlock.setPosition((16*columnCount, 16*lineCount))
                    self.BlueBlock.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)
                #Black
                elif char == "s":
                    self.BlackDecor.setPosition((16*columnCount, 16*lineCount))
                    self.BlackDecor.draw(drawSurface)
                elif char == "S":
                    self.BlackBlock.setPosition((16*columnCount, 16*lineCount))
                    self.BlackBlock.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)
                #Yellow
                elif char == "y":
                    self.YellowDecor.setPosition((16*columnCount, 16*lineCount))
                    self.YellowDecor.draw(drawSurface)
                elif char == "Y":
                    self.YellowBlock.setPosition((16*columnCount, 16*lineCount))
                    self.YellowBlock.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)
                elif char == "r":
                    self.RedDecor.setPosition((16*columnCount, 16*lineCount))
                    self.RedDecor.draw(drawSurface)
                elif char == "R":
                    self.RedBlock.setPosition((16*columnCount, 16*lineCount))
                    self.RedBlock.draw(drawSurface)
                    newRect = pygame.Rect(16*columnCount, 16*lineCount, 16, 16)
                    if newRect not in self.collidables:
                        self.collidables.append(newRect)
                elif char == "n":
                    self.nest.setPosition((16*columnCount, 16*lineCount))
                    self.nest.draw(drawSurface)
                elif char == "p":
                    self.Cloud.setPosition((16*columnCount, 16*lineCount))
                    self.Cloud.draw(drawSurface)
                else:
                    pass
                columnCount += 1
    

    def getWin(self):
        return False
    def getWin2(self):
        return self.gameWin
    