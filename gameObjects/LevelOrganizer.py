import pygame
from . import GameEngine


class LevelOrganizer():
    def __init__(self):
        self.currentLevel = GameEngine
    
    def setGame(self, level):
        self.currentLevel = level
    
    def getGame(self):
        return self.currentLevel