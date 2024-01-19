import pygame

class Cursor:

    def __init__(self, core):
        self.core = core
        self.initsprites()
        self.sprite = self.default

    def loop(self):
        pass

    def initsprites():
        ss = pygame.image.load("")