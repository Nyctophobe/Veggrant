"""
Veggerant: My Game Design game
Will be a unique platformer designed to find ways to move the character.

Author: Simon Lopez-Trujillo, Elizabeth Matthews
"""
#Imports
import pygame
from gameObjects import GameEngine
from util import RESOLUTION, SCALE
UPSCALED = RESOLUTION * SCALE

#____________________________________________________________Game Setup____________________________________________________________
def main():

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(list(map(int, UPSCALED)))  
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    game = GameEngine()

    RUNNING = True
#____________________________________________________________Main Loop Start____________________________________________________________   
    while RUNNING:
    
        game.draw(drawSurface)
    
        pygame.transform.scale(drawSurface, list(map(int, UPSCALED)), screen)

        pygame.display.flip()
        gameClock = pygame.time.Clock()

        for event in pygame.event.get():
        #Quit Game
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
        #Other Events
            else:
                game.handleEvent(event)

    #Progresses & Tracks Clock
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        game.update(seconds)
#____________________________________________________________Main Loop End____________________________________________________________
         
#Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
