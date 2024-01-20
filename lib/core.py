from data.scenes.start.start import Start
from lib.camera import Camera
from lib.cursor import Cursor
from lib.particles import Particles
from lib.text import Text
from lib.player import Player
import pygame

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Start(self) # initialize start scene
        # self.cursor = Cursor(self)
        self.camera = Camera(self)
        particleimg = pygame.transform.scale_by(pygame.image.load("data/assets/objects/particle.png").convert_alpha(), 0.5)
        self.particles = Particles(self, image=particleimg)
        self.paused = False
        self.pausetext = Text("Paused", "helvetica", 36, [255, 255, 255])

    def loop(self, events):
        self.events = events
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
        if self.paused:
            self.pausetext.loop()
            return
        self.particles.loop()
        self.scene.loop()
        self.camera.loop()
        # self.cursor.loop()

    def restart(self):
        self.player = Player(self)
        self.scene = Start(self)
        self.Camera = Camera(self)