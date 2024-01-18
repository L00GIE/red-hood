from lib.collider import Collider
import pygame

class Projectile:

    def __init__(self, parent, direction, image=None):
        self.parent = parent
        self.image = image
        self.direction = direction
        self.speed = 10
        if direction == "e":
            self.x = parent.x + parent.w
        else:
            self.x = parent.x
        self.y = parent.y + (parent.h / 2)
        self.w = 10
        self.h = 10
        self.mass = 0.5
        self.collider = Collider(self, antigrav=True)

    def loop(self):
        self.checkbounds()
        self.moveandblit()
        self.checkcollision()

    def checkcollision(self):
        for layer in self.parent.core.scene.layers:
            for obj in layer:
                if hasattr(obj, "collider") and \
                    self.collider.colliding(obj):
                    if hasattr(obj, "hp"):
                        if obj == self.parent: continue
                        obj.hp -= self.parent.dmg
                        self.parent.core.scene.remove(self)

    def checkbounds(self):
        if self.x < 0 or self.x > pygame.display.get_surface().get_width():
            self.parent.core.scene.remove(self)

    def moveandblit(self):
        if self.direction == "e":
            self.x += self.speed
        elif self.direction == "w":
            self.x -= self.speed
        self.collider.update()
        if self.image is not None:
            pygame.display.get_surface().blit(self.image, (self.x, self.y))