from data.scenes.start.start import Start
from lib.camera import Camera
from lib.cursor import Cursor
from lib.particles import Particles
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

    def loop(self, events):
        self.events = events
        self.particles.loop()
        self.scene.loop()
        self.camera.loop()
        # self.cursor.loop()

    def restart(self):
        self.player = Player(self)
        self.scene = Start(self)
        self.Camera = Camera(self)