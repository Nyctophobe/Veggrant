import pygame
from . import Drawable, Egg, Human, Horse
from util import SoundManager, vec, RESOLUTION, FONT

class GameEngine3(object):
    def __init__(self):
        self.collidables = []
        self.winBox = pygame.Rect(16*19,16*2, 16, 16)
        self.gameWin = False

        self.standDelayA = 0
        self.standDelayB = 0

        #Main Character       
        self.egg = Egg((16*20,16*18))
        self.startPos = (16*20,16*18)
        self.size = vec(*RESOLUTION)

        #Enemies
        self.humanOne = Human("left", (16*29, 16*13), "Human.png")
        self.humanOne.flipImage[0] = True
        self.humanTwo = Human("left", (16*20, 16*13), "Human.png")
        self.humanTwo.flipImage[0] = True
        self.humanThree = Human("left", (16*29, 16*3), "Human.png", (pygame.Rect(16*29, 16*1, 5, 16*10), (16*31, 16*9)))
        self.humanThree.flipImage[0] = True
        self.horseOne = Horse((16*7, 16*14), "horse.png", True, 90)
        self.horseTwo = Horse((16*2, 16*14), "horse.png")

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
        
        #Level
        GameEngine3.readLevel(self, drawSurface)

        #Enemies
        self.humanOne.draw(drawSurface)
        self.humanTwo.draw(drawSurface)
        self.humanThree.draw(drawSurface)
        pygame.draw.rect(drawSurface, (150, 75, 0), self.humanThree.platform)

        self.horseOne.draw(drawSurface)
        self.horseTwo.draw(drawSurface)

        #Egg
        self.egg.draw(drawSurface)
        #pygame.draw.rect(drawSurface, (255, 0, 0),self.egg.getStandRect())
        if self.gameWin == True:
            drawSurface.blit(FONT.render("WINNN", True, (255,0,0)), (16*18,16*1))

        

    def handleEvent(self, event):
        self.egg.handleEvent(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.egg.setPosition(self.startPos)
            self.humanOne.position = (16*29, 16*13)
            self.humanTwo.position = (16*20, 16*13)
            self.humanThree.setMoveIt(False)
            self.humanThree.platform[0] = 16*29
            self.humanThree.platform[1] = 16*1
            self.humanThree.arrive = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.egg.grav.fall()
            self.egg.setPosition((pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2))
    
    def update(self, seconds):
        #Egg
        self.egg.update(self.collidables, seconds)
        Drawable.updateOffset(self.egg, self.size)
        if self.egg.position[1] > 16*20:
            self.egg.position = (16*14, 16*18)

        #Enemies
        self.horseOne.update(seconds)
        if self.horseOne.getReactCollid().clip(self.humanOne.getReactCollid()):
            self.horseOne.chill = True
            pass
        elif self.egg.getCollisionRect().clip(self.horseOne.getReactCollid()):
            self.horseOne.chill = False
            if self.egg.grav.hasGround == True and self.egg.getInteracted() == False:
                self.egg.position[1] = self.egg.position[1]- 3
            self.egg.grav.jump()
            self.egg.setInteracted(True)
            self.egg.setBypass(True)
            self.egg.grav.jumpSpeed = 400
            self.egg.velocity[0] = 300
        else:
            self.horseOne.chill = False

        self.horseTwo.update(seconds)
        if self.egg.getCollisionRect().clip(self.horseTwo.getReactCollid()):
            if self.egg.grav.hasGround == True and self.egg.getInteracted() == False:
                self.egg.position[1] = self.egg.position[1]- 3
            self.egg.grav.jump()
            self.egg.LR.stop_all()
            self.egg.setInteracted(True)
            self.egg.setBypass(True)
            self.egg.grav.jumpSpeed = 650
            self.egg.velocity[0] = -50

        self.humanOne.update(seconds)
        self.humanTwo.update(seconds)
        self.humanThree.update(seconds)
        if self.humanThree.arrive == True:
            if self.egg.getCollisionRect().clip(self.humanOne.getReactCollid()):
                if self.egg.grav.hasGround == False and self.egg.grav != "falling" and self.egg.getInteracted() == False:
                    self.humanOne.arrive = False
            if self.humanOne.arrive == False:
                self.humanOne.shuffle("special1", (16*8, 16*13))
            if self.humanOne.position[0] <= 16*8:
                self.standDelayA += 1
            if self.standDelayA >= 75:
                self.humanOne.shuffle("special2", (16*29, 16*13))
            if self.humanOne.position[0] == 16*29:
                        self.standDelayA = 0
        
        else:
            if (self.humanOne.position[0] <=16*26 and self.humanOne.position[0] >=16*25)  or self.humanTwo.position[0] >=16*26:
                if self.humanTwo.getCollisionRect().clip(self.humanThree.platform):
                    self.humanTwo.shuffle("rightup", (16*26, 16*4))
                    if self.humanOne.position[0] >= 16*26:
                        self.humanOne.shuffle("rightdown", (16*29, 16*13))
                    else: 
                        self.humanOne.shuffle("leftdown", (16*8, 16*13))
                        self.humanOne.arrive = False
                elif self.humanOne.getCollisionRect().clip(self.humanThree.platform):
                    self.humanOne.shuffle("leftup", (16*26, 16*4))
                    self.humanTwo.shuffle("leftdown", (16*20, 16*13))
                    if self.humanOne.position[1] == 16*4:
                        self.standDelayB = 1
                        self.humanThree.arrive = True
                        
                    
                
            else:
                if self.humanOne.position[0] >= 16*26:
                    self.humanOne.shuffle("leftup", (16*1, 16*4))
                else: 
                    self.humanOne.shuffle("rightup", (16*40, 16*4))
                self.humanTwo.shuffle("rightup", (16*40, 16*4))

        if self.standDelayB >= 1 and self.standDelayB <300:
            self.standDelayB += 1
        if self.standDelayB == 300:
            self.humanOne.shuffle("downright", (16*31, 16*13))
            if self.humanOne.position[0] == (16*29) and self.humanOne.position[1] == (16*13):
                self.humanThree.setMoveIt(True)
                self.standDelayB = 0
            


        self.humanTwo.update(seconds)
        if self.egg.getCollisionRect().clip(self.humanTwo.getReactCollid()):
            if self.egg.grav.hasGround == False and self.egg.grav != "falling" and self.egg.getInteracted() == False:
                self.egg.setInteracted(True)
                self.egg.setBypass(True)
                self.humanTwo.setKick(True)
                self.egg.grav.jumpSpeed = 600
                self.egg.velocity[0] = -250        
        
        if self.egg.getCollisionRect().clip(self.humanThree.getReactCollid()):
            if self.egg.grav.hasGround == False and self.egg.grav != "falling" and self.egg.getInteracted() == False:
                self.humanThree.setMoveIt(True)
        if self.humanThree.getMoveIt() == True:
            self.humanThree.moveRope()





        #Win Box
        if self.egg.getCollisionRect().clip(self.winBox):
            self.gameWin = True
        

    
    
    def readLevel(self, drawSurface):
        file_path = "Levels\\level3.txt"
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
        return False
    