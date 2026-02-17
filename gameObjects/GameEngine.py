import pygame
from . import Drawable, Egg
from gameObjects import Mobile, Player
from util import vec, RESOLUTION


class GameEngine(object):
    def __init__(self):       
        self.egg = Egg((0,0))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.egg.draw(drawSurface)
            
    def handleEvent(self, event):
        self.egg.handleEvent(event)
    
    def update(self, seconds):
        self.egg.update(seconds)
        
        Drawable.updateOffset(self.egg, self.size)
    """
    def __init__(self):
        #self.egg = Player((0,0), "kirby.png", (0,1))
        self.egg = Player((0,0), "Game Sprites.png", (0, 0, 16, 16), maxSpeed = 1000)
        self.egg.animate = False
        self.x = Drawable((randint(50, 50), randint(20, 20)), "Game Sprites.png", (0,0, 16, 16))
        self.y = Drawable((randint(50, WORLD_SIZE[0]-50), randint(20, WORLD_SIZE[1]-20)), "Game Sprites.png", (0,0, 16, 16))
        self.z = Drawable((randint(50, WORLD_SIZE[0]-50), randint(20, WORLD_SIZE[1]-20)), "Game Sprites.png", (0,0, 16, 16))
        self.background = Drawable((0,0), "background.png")
        self.dragged = None

        self.collidables = [self.x, self.y, self.z]

    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.egg.draw(drawSurface)
        self.x.draw(drawSurface)
        self.y.draw(drawSurface)
        self.z.draw(drawSurface)
    
    def handleEvent(self,event):
        self.egg.handleEvent(event)
         #Future movement
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
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = vec(*event.pos)//SCALE
            position += Drawable.CAMERA_OFFSET
            if self.x.getCollisionRect().collidepoint(position):
                self.dragged = self.x
                self.mouseOffset = self.x.getPosition() - position
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragged = None
        elif event.type == pygame.MOUSEMOTION:
            position = vec(*event.pos)//SCALE
            position += Drawable.CAMERA_OFFSET

            if self.dragged != None:
                self.dragged.position = position + self.mouseOffset

    def update(self, seconds):
        self.egg.update(seconds)
        #Prevents Egg from escaping Window
        if self.egg.getPosition()[0] <= 0:
            self.egg.position[0] = 0
        if self.egg.getPosition()[0] + self.egg.getWidth() >= WORLD_SIZE_VEC[0]:
            self.egg.position[0] = WORLD_SIZE_VEC[0]-16   
        if self.egg.getPosition()[1] <= 0:
            self.egg.position[1] = 0
        if self.egg.getPosition()[1] + self.egg.getWidth() >= WORLD_SIZE_VEC[1]:
            self.egg.velocity[1] = 0
            self.egg.position[1] = WORLD_SIZE_VEC[1]-16
            
        for c in self.collidables:
            collision = self.egg.getCollisionRect().clip(c.getCollisionRect())
            if collision.width != 0 and collision.height != 0:
                if collision.width < collision.height:
                    self.egg.velocity[0] = 0
                    if self.egg.getPosition()[0] < c.getPosition()[0]:
                        self.egg.position[0] -= collision.width
                    else:
                        self.egg.position[0] += collision.width
                else: 
                    self.egg.velocity[1] = 0
                    if self.egg.getPosition()[1] < c.getPosition()[1]:
                        self.egg.position[1] -= collision.height
                    else:
                        self.egg.position[1] += collision.height
        
        Drawable.CAMERA_OFFSET = self.egg.getPosition() + self.egg.getSize()/2 - RESOLUTION / 2

        for i in range(2):
            Drawable.CAMERA_OFFSET[i] = max(0, min(Drawable.CAMERA_OFFSET[i], WORLD_SIZE[i] - RESOLUTION[i]))

"""













            
            
