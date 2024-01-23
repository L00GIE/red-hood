import pygame

class Text:

    def __init__(self, text, fontsize, color, pos=None):
        self.text = text
        self.font = pygame.font.Font("data/assets/fonts/dogica.ttf", fontsize)
        self.color = color
        if pos is not None:
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = None
            self.y = None
        self.surf = self.font.render(self.text, antialias=True, color=self.color)
        self.w = self.surf.get_width()
        self.h = self.surf.get_height()

    def loop(self):
        self.surf = self.font.render(self.text, antialias=True, color=self.color)
        if self.x is None and self.y is None:
            screen = pygame.display.get_surface()
            self.x = (screen.get_width() / 2) - (self.w / 2)
            self.y = (screen.get_height() / 2) - (self.h / 2)
        pygame.display.get_surface().blit(self.surf, (self.x, self.y))

    def get_height(self):
        return self.surf.get_height()
    
    def get_width(self):
        return self.surf.get_width()
