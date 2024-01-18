import pygame

class Text:

    def __init__(self, text, font, fontsize, color):
        self.text = text
        self.font = pygame.font.SysFont(font, fontsize)
        self.color = color

    def loop(self):
        screen = pygame.display.get_surface()
        surf = self.font.render(self.text, antialias=True, color=self.color)
        xpos = (screen.get_width() / 2) - (surf.get_width() / 2)
        ypos = (screen.get_height() / 2) - (surf.get_height() / 2)
        screen.blit(surf, (xpos, ypos))