"""
Veggerant: My Game Design game
Will be a unique platformer designed to find ways to move the character.

Author: Simon Lopez-Trujillo, Elizabeth Matthews
"""
#Imports
import pygame
from gameObjects import GameEngine, GameEngine2, GameEngine3
from util import SoundManager, RESOLUTION, SCALE, FONT
UPSCALED = RESOLUTION * SCALE
FIRSTPLAY = True
CURRENTGAME = 0
#____________________________________________________________Game Setup____________________________________________________________
def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
    game = GameEngine()

    RUNNING = True
    keyMap = False

    sm = SoundManager.getInstance()
    sm.playBGM("Evening.mp3")

    gameClock = pygame.time.Clock()
#____________________________________________________________Main Loop Start____________________________________________________________   
    while RUNNING:
    
        game.draw(drawSurface)
        if keyMap == True:
            drawSurface.blit(FONT.render("Left: A", True, (255,0,0)), (16*32,16*0))
            drawSurface.blit(FONT.render("Right: D", True, (255,0,0)), (16*32,16*1))
            drawSurface.blit(FONT.render("Jump: Space", True, (255,0,0)), (16*32,16*2))
            drawSurface.blit(FONT.render("Crack: C", True, (255,0,0)), (16*32,16*3))
            drawSurface.blit(FONT.render("Boil: B", True, (255,0,0)), (16*32,16*4))
            drawSurface.blit(FONT.render("Swap state: LShift", True, (255,0,0)), (16*32,16*5))
            drawSurface.blit(FONT.render("Restart: R", True, (255,0,0)), (16*32,16*6))

        pygame.transform.scale(drawSurface, list(map(int, UPSCALED)), screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
        #Quit Game
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                main()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                if keyMap == False:
                    keyMap = True
                else:
                    keyMap = False
        #Other Events
            else:
                game.handleEvent(event)

    #Progresses & Tracks Clock
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        game.update(seconds)

        if game.getWin() == True:
            game = GameEngine2()
            CURRENTGAME = GameEngine2()
        if game.getWin2() == True:
            game = GameEngine3()
            CURRENTGAME = GameEngine3()
#____________________________________________________________Main Loop End____________________________________________________________
         
#Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()