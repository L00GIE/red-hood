from lib.scenes.start import Start
from lib.camera import Camera
from lib.particles import Particles
from lib.text import Text
from lib.player import Player
import pygame, time, math

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Start(self) # initialize start scene
        self.camera = Camera(self)
        particleimg = pygame.transform.scale_by(pygame.image.load("data/assets/objects/particle.png").convert_alpha(), 0.5)
        self.particles = Particles(self, image=particleimg)
        self.paused = False
        self.pausetext = Text("Paused", 36, [255, 255, 255])
        self.initTimer()

    def loop(self, events):
        self.events = events
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    self.timer = time.time()
        if self.paused:
            self.pausetext.loop()
            return
        self.particles.loop()
        self.scene.loop()
        self.camera.loop()
        self.doTimer()

    def initTimer(self):
        timery = pygame.display.get_surface().get_height() - 36
        self.timertext = Text("0.0", 36, [255, 255, 255], (0, timery))
        self.timer = time.time()
        self.elapsed = 0.0

    def doTimer(self):
        t2 = time.time()
        deltat = t2 - self.timer
        self.timer = t2
        self.elapsed += deltat
        if self.elapsed >= 60.0:
            mins = math.floor(self.elapsed / 60)
            timetext = f"{mins}m {round(self.elapsed - (mins * 60), 2)}s"
        else:
            timetext = f"{round(self.elapsed, 2)}s"
        self.timertext.text = timetext
        self.timertext.loop()

    def restart(self):
        self.player = Player(self)
        self.scene = Start(self)
        self.Camera = Camera(self)