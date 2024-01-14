import pygame

class StaticImage:

    def __init__(self, image, pos):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]

    def loop(self):
        pygame.display.get_surface().blit(self.image, (self.x, self.y))