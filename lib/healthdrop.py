import pygame
from lib.collider import Collider

class HealthDrop:
    def __init__(self, core, pos):
        self.core = core
        self.x = pos[0]
        self.y = pos[1]
        self.w, self.h = 64, 64
        self.collider = Collider(self)
        self.initSprite()

    def loop(self):
        self.collider.update()
        self.checkCollision()
        pygame.display.get_surface().blit(self.sprite, (self.x, self.y))

    def checkCollision(self):
        if self.collider.colliding(self.core.player):
            self.core.scene.remove(self)
            self.core.player.hp = self.core.player.maxhp

    def initSprite(self):
        ss = pygame.image.load("data/assets/ui/icons.png").convert_alpha()
        self.sprite = pygame.transform.scale(ss.subsurface(0, 0, 16, 16), (64, 64))