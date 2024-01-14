import pygame

class Background:

    def __init__(self, core, image, scrollspeed=0):
        self.core = core
        self.image = image
        self.scrollspeed = scrollspeed
        self.x = 0
        self.y = 0
        self.lastplayerx = core.player.x

    def loop(self):
        if self.scrollspeed > 0:
            self.scroll()
        pygame.display.get_surface().blit(self.image, (self.x - self.image.get_width(), self.y))
        pygame.display.get_surface().blit(self.image, (self.x, self.y))
        pygame.display.get_surface().blit(self.image, (self.x + self.image.get_width(), self.y))

    def scroll(self):
        delta = self.lastplayerx - self.core.player.x
        self.x += (delta / 10) * self.scrollspeed
        self.lastplayerx = self.core.player.x