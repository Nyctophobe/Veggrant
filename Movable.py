import pygame
import vector
from Drawable import drawable

class movable(drawable):
    def __init__(self, image, position, velocity):
        super().__init__(image, position)
        self.velocity = velocity

    def update(self, seconds):
        self.position = self.position + self.velocity * seconds * 100
        pass
