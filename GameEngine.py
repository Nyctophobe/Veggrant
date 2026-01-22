import pygame
import os
import vector
from Drawable import drawable
from Movable import movable

class GameEngine(object):
    def __init__(self):
#---------------------------------------------------------------Objects----------------------------------------------------------------
    #Egg 
        self.egg = movable("Game Sprites.png", vector.vec(200, 100), vector.vec(0,0))


    def draw(self, drawSurface):
    #Fill Entire Screen to reset display
        drawSurface.fill((0, 50, 255))
    #Draw Egg
        self.egg.draw(drawSurface)

    
    def handleEvent(self,event):
        """ #Future movement
                Egg movement will not be like this in the final game. The egg on its own will have very limited movement.
                The egg will be able to
                                - Jump (Cannot move while in the air)
                                - Roll (Each button press rolls a fixed distance)
                This movement may be altered by other abilities, such as chaning weight or cracking your shell,
                but all personal movement is tied to those two actions. Any additional movement is due to enviromental factors and how your 
                abilities interact with it

                Jumping on its own will need movement, gravity and collision
                Jumping will also be changed based on the weight of the egg, changing how effective gravity is on the egg.
                It will also be effected by if the egg is cracked or not, increacing gravity once it reaches its expected height.

                Rolling on its own will require movement, gravity and collision
                Rolling will also be changed based on the weight of the egg, changing how fast it can move.
                Rolling will also be effected by if the egg is cracked or not, preventing it from falling off edges and instead hang from the yoke

                Cracking will require movement, gravity and collision
                When the egg hits a surface fast enough, its shell will crack. The speed neede is based off the eggs weight.
                While the egg is cracked, all movement is altered.
                Yoke will stick to surfaces, allowing the egg to climb walls, hang under ledges, and prevent exterior methods of movement.

                Boiling will change the hardness & weight of the egg
                The egg starts out the level completely raw. It is at its lightest, frailest, and stickiest in this state. 
                The egg can boil itself twice, with its weight and strength increasing, but its stickiness decreasing.
                
                These will be my 4 main goals of movement, though they may not be fully implemented in all their interactions
                """
    #Egg Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.egg.velocity[1] = -1
            elif event.key == pygame.K_s:
                self.egg.velocity[1] = 1
            elif event.key == pygame.K_a:
                self.egg.velocity[0] = -1
            elif event.key == pygame.K_d:
                self.egg.velocity[0] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.egg.velocity[1] = 0
            elif event.key == pygame.K_s:
                self.egg.velocity[1] = 0
            elif event.key == pygame.K_a:
                self.egg.velocity[0] = 0
            elif event.key == pygame.K_d:
                self.egg.velocity[0] = 0
    #More Key Events
        if event.type == pygame.KEYUP:
            pass

    def update(self, seconds):
    #Move Egg
        self.egg.update(seconds)
    
