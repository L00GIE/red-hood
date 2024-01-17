import pygame

class HealthBar:

    def __init__(self, parent, title=None, rightside=False):
        self.parent = parent
        self.title = title
        self.rightside = rightside
        self.initsprites()
        self.font = pygame.font.SysFont("Helvetica", 26)

    def loop(self):
        self.showHearts()
        if self.title is not None:
            self.showTitle()

    def showTitle(self):
        screen = pygame.display.get_surface()
        titletext = self.font.render(self.title, True, [255, 255, 255])
        xpos = screen.get_width() - titletext.get_width() - 10
        ypos = self.fullheart.get_height() + 10
        pygame.display.get_surface().blit(titletext, (xpos, ypos))

    def showHearts(self):
        screen = pygame.display.get_surface()
        percent = (self.parent.hp / self.parent.maxhp) * 100
        if not self.rightside:
            xpos = 10
        else:
            xpos = screen.get_width() - (self.fullheart.get_width() * 5) - 10
        ypos = 10
        if percent >= 90:
            for x in range(5):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
        elif percent < 90 and percent >= 80:
            for x in range(4):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
            screen.blit(self.halfheart, (xpos + (self.fullheart.get_width() * (x + 1)), ypos))
        elif percent < 80 and percent >= 70:
            for x in range(4):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
            screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * (x + 1)), ypos))
        elif percent < 70 and percent >= 60:
            for x in range(3):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
            screen.blit(self.halfheart, (xpos + (self.fullheart.get_width() * (x + 1)), ypos))
            screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * (x + 2)), ypos))
        elif percent < 60 and percent >= 50:
            for x in range(3):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
            for x in range(3, 5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))
        elif percent < 50 and percent >= 40:
            for x in range(2):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
            screen.blit(self.halfheart, (xpos + (self.fullheart.get_width() * 2), ypos))
            for x in range(3, 5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))
        elif percent < 40 and percent >= 30:
            for x in range(2):
                screen.blit(self.fullheart, (xpos + (self.fullheart.get_width() * x), ypos))
            for x in range(2, 5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))
        elif percent < 30 and percent >= 20:
            screen.blit(self.fullheart, (xpos , ypos))
            screen.blit(self.halfheart, (xpos + (self.fullheart.get_width()), ypos))
            for x in range(2, 5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))
        elif percent < 20 and percent > 10:
            screen.blit(self.fullheart, (xpos, ypos))
            for x in range(1, 5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))
        elif percent < 10 and percent > 0:
            screen.blit(self.halfheart, (xpos, ypos))
            for x in range(1, 5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))
        else:
            for x in range(5):
                screen.blit(self.emptyheart, (xpos + (self.fullheart.get_width() * x), ypos))

    def initsprites(self):
        ss = pygame.image.load("data/assets/ui/icons.png").convert_alpha()
        self.fullheart = pygame.transform.scale_by(ss.subsurface(0, 16, 16, 16), 3)
        self.halfheart = pygame.transform.scale_by(ss.subsurface(16, 16, 16, 16), 3)
        self.emptyheart = pygame.transform.scale_by(ss.subsurface(32, 16, 16, 16), 3)