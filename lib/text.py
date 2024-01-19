import pygame

class Text:

    def __init__(self, text, font, fontsize, color, pos=None):
        self.font = pygame.font.SysFont(font, fontsize)
        self.color = color
        self.surf = self.font.render(text, antialias=True, color=self.color)
        if pos is None:
            screen = pygame.display.get_surface()
            self.x = (screen.get_width() / 2) - (surf.get_width() / 2)
            self.y = (screen.get_height() / 2) - (surf.get_height() / 2)
        else:
            self.x = pos[0]
            self.y = pos[1]

    def loop(self):
        pygame.display.get_surface().blit(self.surf, (self.x, self.y))
