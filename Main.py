"""
Veggerant: My Game Design game
Will be a unique platformer designed to find ways to move the character.

Author: Simon Lopez-Trujillo
"""
#Imports
import pygame
from GameEngine import GameEngine

#____________________________________________________________Game Setup____________________________________________________________
def main():
#Initialize Pygame
    pygame.init()
    pygame.font.init()

#Set up display
    RESOLUTION = (400, 200)
    SCALE = 2
    UPSCALED = [int(x * SCALE) for x in RESOLUTION]
    
    screen = pygame.display.set_mode(list(UPSCALED))   
    drawSurface = pygame.Surface(list(RESOLUTION))

#Game Clock
    gameClock = pygame.time.Clock()

#Game Run Control
    RUNNING = True
    game = GameEngine()

#____________________________________________________________Main Loop Start____________________________________________________________   
    while RUNNING:

#------------------------------------------------------------Display World------------------------------------------------------------        
    
    
    #Upscale Images
        pygame.transform.scale(drawSurface, list(UPSCALED), screen)

    #draw game objects    
        game.draw(drawSurface)

    #Update the display
        pygame.display.flip()
#------------------------------------------------------------Event Keys------------------------------------------------------------
        for event in pygame.event.get():
        #Quit Game
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
        #Other Events
            else:
                game.handleEvent(event)

    #Progresses & Tracks Clock
        seconds = gameClock.get_time() / 1000
        gameClock.tick(60)

        game.update(seconds)

#____________________________________________________________Main Loop End____________________________________________________________
         


#Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
