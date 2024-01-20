import pygame

class Text:

    def __init__(self, text, font, fontsize, color, pos=None):
        self.text = text
        self.font = pygame.font.SysFont(font, fontsize)
        self.color = color
        self.pos = pos

    def loop(self):
        self.surf = self.font.render(self.text, antialias=True, color=self.color)
        if self.pos is None:
            screen = pygame.display.get_surface()
            self.x = (screen.get_width() / 2) - (self.surf.get_width() / 2)
            self.y = (screen.get_height() / 2) - (self.surf.get_height() / 2)
        else:
            self.x = self.pos[0]
            self.y = self.pos[1]
        pygame.display.get_surface().blit(self.surf, (self.x, self.y))
