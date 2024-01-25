from lib.healthbar import HealthBar
from lib.scenes.grandmas import Grandmas
from lib.scenes.start import Start
from lib.camera import Camera
from lib.particles import Particles
from lib.text import Text
from lib.player import Player
import pygame, time, math

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Grandmas(self) # initialize start scene
        self.camera = Camera(self)
        particleimg = pygame.transform.scale_by(pygame.image.load("data/assets/objects/particle.png").convert_alpha(), 0.5)
        self.particles = Particles(self, image=particleimg)
        self.paused, self.shownbg = False, False
        self.pausetext = Text("Paused", 36, [255, 255, 255])
        self.restarttext = Text("Restart?", 26, [255, 0, 0])
        self.initTimer()

    def loop(self, events):
        self.events = events
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    self.timer = time.time()
        if self.paused:
            self.dopause()
            return
        self.shownbg = False
        self.particles.loop()
        self.scene.loop()
        self.camera.loop()
        self.doTimer()

    def dopause(self):
        screen = pygame.display.get_surface()
        if not self.shownbg:
            self.bg = pygame.Surface(screen.get_size())
            self.bg.set_alpha(150)
            self.bg.fill((0,0,0))
            screen.blit(self.bg, (0,0))
            self.shownbg = True
        self.pausetext.loop()
        self.restarttext.x = (pygame.display.get_surface().get_width() / 2) - (self.restarttext.surf.get_width() / 2)
        self.restarttext.y = (pygame.display.get_surface().get_height() / 2) - (self.restarttext.surf.get_height() / 2) + 36
        textrect = pygame.Rect(self.restarttext.x, self.restarttext.y, self.restarttext.get_width(), self.restarttext.get_height())
        if textrect.collidepoint(pygame.mouse.get_pos()):
            self.restarttext.color = [255, 255, 255]
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.restart()
        else:
            self.restarttext.color = [255, 0, 0]
        self.restarttext.loop()

    def initTimer(self):
        if hasattr(self, "timertext"):
            self.scene.remove(self.timertext)
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
        for obj in self.scene.layers[6]:
            if isinstance(obj, HealthBar) and \
                obj.parent is not self.player:
                self.scene.remove(obj)
        self.player = Player(self)
        self.scene = Start(self)
        self.Camera = Camera(self)
        self.initTimer()
        self.paused = False