from data.scenes.start.start import Start
from lib.camera import Camera
from lib.cursor import Cursor
from lib.particles import Particles
from lib.player import Player

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Start(self) # initialize start scene
        # self.cursor = Cursor(self)
        self.camera = Camera(self)
        self.particles = Particles(self)

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