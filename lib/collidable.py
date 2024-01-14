import pygame
from lib.collider import Collider

class Collidable:
    
    def __init__(self, core, x, y, w, h, mass=0, layer=4, stationary=False, image=None, debug=False):
        self.core = core
        self.x, self.y, self.w, self.h = x, y, w, h
        self.mass = mass
        self.layer = layer
        self.speed = 1
        self.image = image
        self.collider = Collider(self, debug=debug, stationary=stationary)

    def loop(self):
        self.checkCollision()
        self.collider.update()
        if self.image is not None:
            pygame.display.get_surface().blit(self.image, (self.x, self.y))

    def checkCollision(self):
        for obj in self.core.scene.layers[self.layer]:
            if obj == self: continue
            if hasattr(obj, "collider"):
                if obj.collider.colliding(self) and not obj.collider.stationary:
                    if obj.collider.rect.top <= self.collider.rect.top: # object coming from above
                        obj.y = self.y - obj.h + 1
                    elif obj.collider.rect.center >= self.collider.rect.center: # object coming from right
                        obj.x = self.collider.rect.right
                        if obj.mass > self.mass and not self.collider.stationary:
                            self.x -= self.core.player.speed / 2
                    elif obj.collider.rect.center <= self.collider.rect.center:  # object coming from left
                        obj.x = self.collider.rect.left - obj.w
                        if obj.mass > self.mass and not self.collider.stationary:
                            self.x += self.core.player.speed / 2
