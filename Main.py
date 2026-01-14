"""
Veggerant: My Game Design game

Author: Simon Lopez-Trujillo
"""

import pygame

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()

    # Set up display
    screen = pygame.display.set_mode((800, 600))

    # Set up texts
    basicText = pygame.font.SysFont('Arial', 20)

#____________________________________________________________Main loop____________________________________________________________
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color (RGB)
        screen.fill((0, 50, 255))

        #Game Text
        helloWorld = basicText.render("hello world", False, (255,0,0))
        screen.blit(helloWorld, (0,0))

        #Egg Sprite Sheet
        #starSurf = pygame.Surface((10, 10))
        #rect = pygame.Rect(10*2, 0, 10, 10)
        #starSurf.blit(star.png, (0,0), rect)

        # Update the display
        pygame.display.flip()


    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()