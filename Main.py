"""
Veggerant: My Game Design game
Will be a unique platformer designed to find ways to move the character.

Author: Simon Lopez-Trujillo
"""

import os
import pygame

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()

    # Set up display
    RESOLUTION = (400, 200)
    SCALE = 2
    UPSCALED = [int(x * SCALE) for x in RESOLUTION]
    
    screen = pygame.display.set_mode(list(UPSCALED))   
    drawSurface = pygame.Surface(list(RESOLUTION))

    # Set up texts
    basicText = pygame.font.SysFont('Arial', 20)

#____________________________________________________________Main loop____________________________________________________________
    RUNNING = True
    while RUNNING:
#____________________________________________________________Display World____________________________________________________________


        # Fill the screen with a color (RGB)
        drawSurface.fill((0, 50, 255))
        """
        #Egg Sprite Sheet
        egg = pygame.image.load(os.path.join("Game Sprites.png")).convert()
        #drawSurface.blit(egg, (200, 100))
        egg.set_colorkey((0, 0, 0))
        drawSurface.blit(egg, (200, 100), pygame.Rect(0, 0, 16, 16))
        """
        #Game Text
        helloWorld = basicText.render("hello world", False, (255,0,0))
        drawSurface.blit(helloWorld, (0,0))

        #Upscale Text
        pygame.transform.scale(drawSurface,
                            list(UPSCALED),
                            screen)
        # Update the display
        pygame.display.flip()
#____________________________________________________________Event Keys____________________________________________________________

        for event in pygame.event.get():
            #Quit Event
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False

            #Other Events
            #else
#____________________________________________________________Update Objects____________________________________________________________
           


    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
