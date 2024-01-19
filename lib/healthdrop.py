import pygame
from lib.collider import Collider

class HealthDrop:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.w, self.h = 64, 64
        self.collider = Collider(self, antigrav=True)
        self.initSprite()

    def loop(self):
        pygame.display.get_surface().blit(self.sprite, (self.x, self.y))

    def initSprite(self):
        ss = pygame.image.load("data/assets/ui/icons.png").convert_alpha()
        self.sprite = pygame.transform.scale(ss.subsurface(0, 0, 16, 16), (64, 64))