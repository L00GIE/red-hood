import pygame
from lib.collider import Collider
from lib.hitnumber import HitNumber

class DamageDrop:
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
            self.core.player.dmg += 1
            self.core.scene.add(HitNumber(self.core, self.core.player, "+1 Damage", colorval=[255, 255, 255]))

    def initSprite(self):
        sprite = pygame.image.load("data/assets/objects/14 - Twin serrated swords.png").convert_alpha()
        self.sprite = pygame.transform.scale(sprite, (64, 64))