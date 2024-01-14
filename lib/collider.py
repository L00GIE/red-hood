import pygame

class Collider:

    def __init__(self, parent, stationary=False, point=False, debug=False):
        self.parent = parent
        self.stationary = stationary
        self.rect = pygame.Rect((self.parent.x, self.parent.y, self.parent.w, self.parent.h))
        self.point = point
        self.debug = debug

    def update(self, x=None, y=None, w=None, h=None):
        if x is not None: self.rect.x = x
        else: self.rect.x = self.parent.x
        if y is not None: self.rect.y = y
        else: self.rect.y = self.parent.y
        if w is not None: self.rect.w = w
        else: self.rect.w = self.parent.w
        if h is not None: self.rect.h = h
        else: self.rect.h = self.parent.h
        if self.debug:
            colliderrect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, self.rect.w + 4, self.rect.h + 4)
            pygame.draw.rect(pygame.display.get_surface(), [255, 0, 0], colliderrect, width=2) # draw red rectangle around collider

    def colliding(self, obj):
        if hasattr(obj, "collider"):
            if self.point:
                if obj.collider.rect.collidepoint((self.rect.x, self.rect.y)):
                    return True
            else:
                if self.rect.colliderect(obj.collider.rect):
                    return True
        return False