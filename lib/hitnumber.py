import pygame

class HitNumber:

    def __init__(self, core, parent, value):
        self.core = core
        self.parent = parent
        font = pygame.font.Font("data/assets/fonts/dogica.ttf", 24)
        if parent == self.core.player:
            color = [255, 0, 0]
        else:
            color = [255, 255, 255]
        self.text = font.render(str(value), True, color)
        self.x, self.y = self.parent.x, self.parent.y
        self.ticks = 0

    def loop(self):
        pygame.display.get_surface().blit(self.text, (self.x + (self.parent.w / 2), self.y))
        self.y -= 1
        self.ticks += 1
        if self.ticks >= 150:
            self.core.scene.remove(self)
