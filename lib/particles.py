import pygame, random

class Particle:
    def __init__(self, core, image, pos):
        self.core = core
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 1

    def loop(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image, (self.x, self.y))
        self.y += self.speed
        self.x += random.randint(-2, 2)
        if self.y > screen.get_height():
            self.core.scene.remove(self)

class Particles:

    def __init__(self, core, image=None):
        self.core = core
        if image is not None:
            self.image = image
        else:
            particlesurf = pygame.Surface((4, 4)).convert_alpha()
            pygame.draw.circle(particlesurf, [255, 255, 255], (2, 2), 2)
            self.image = particlesurf

    def loop(self):
        numparticles = 0
        for obj in self.core.scene.layers[4]:
            if isinstance(obj, Particle):
                numparticles += 1
        if numparticles < 100 and random.randint(0, 10) == 1:
            screen = pygame.display.get_surface()
            xpos = random.randint(0, screen.get_width() * 2)
            ypos = random.randint(0, 100)
            self.core.scene.add(
                Particle(
                    self.core, 
                    self.image, 
                    (xpos, ypos)))
