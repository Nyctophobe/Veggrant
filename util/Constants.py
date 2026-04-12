from . import vec
import pygame
pygame.font.init()

FIRSTPLAY = False
RESOLUTION = vec(640, 320)

WORLD_SIZE = (640, 320)
WORLD_SIZE_VEC = vec(WORLD_SIZE[0], WORLD_SIZE[1])

SCALE = 2

EPSILON = 0.01

FONT = pygame.font.SysFont("Aerial", 20)

FIRSTPLAY = False