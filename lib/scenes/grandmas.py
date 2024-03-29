from lib.enemies.grandma import Grandma
from lib.background import Background
from lib.collidable import Collidable
from lib.scene import Scene
from lib.staticimg import StaticImage
import pygame

class Grandmas(Scene):

    def __init__(self, core):
        self.core = core
        super().__init__()
        self.initBackgrounds()
        self.initGround()
        self.initObjects()
        self.core.player.x = 100
        self.add(self.core.player) # add player to foremost layer
        pygame.mixer.music.load("data/assets/sounds/music/this-is-epic.mp3")
        pygame.mixer.music.play(loops=-1)
        self.add(Grandma(self.core))

    def loop(self):
        numenemies = 0
        for x in self.layers[4]:
            if isinstance(x, Grandma):
                numenemies += 1
        if numenemies < 1:
            self.remove(self.wall)
        pygame.display.get_surface().fill([255, 255, 255])
        self.applygravity() # this is where gravity is applied to every non-stationary object in the scene
        super().loop() # this is where every object in the scene has its loop() called
        
    def initGround(self):
        self.wall = Collidable(self.core, 2500, 0, 50, 768, stationary=True, debug=False)
        self.add(self.wall)
        self.initFloorTiles()
        wall = Collidable(self.core, 50, 0, 20, 768, stationary=True, debug=False)
        self.add(Collidable(self.core, 0, 700, 128, 128, stationary=True, image=self.floortiles[0]))
        for x in range(25):
            self.add(Collidable(self.core, 128 * x, 700, 128, 128, stationary=True, image=self.floortiles[1]))
        self.add(Collidable(self.core, (128*x) + 32, 700, 128, 128, stationary=True, image=self.floortiles[2]))
        self.add(wall)

    def initObjects(self):
        ss = pygame.image.load("data/assets/objects/TX Village Props.png").convert_alpha()
        signimg = pygame.transform.scale_by(pygame.image.load("data/assets/objects/donotentersign.png").convert_alpha(), 0.8)
        boximg = pygame.transform.scale(ss.subsurface((41, 18, 47, 45)), (100, 100))
        scaffoldimg = pygame.transform.scale(ss.subsurface((187, 162, 72, 64)), (216, 192))
        scaffold = StaticImage(scaffoldimg, (800, 520))
        signtext = StaticImage(signimg, (scaffold.x + 50, scaffold.y + 20))
        """box = Collidable(self.core, 400, -200, 100, 100, mass=1, image=boximg)
        box2 = Collidable(self.core, 800, pygame.display.get_surface().get_height() - 250, 100, 100, mass=10, image=boximg, stationary=True)
        box3 = Collidable(self.core, 900, pygame.display.get_surface().get_height() - 350, 100, 100, mass=10, image=boximg, stationary=True)
        box4 = Collidable(self.core, 1000, pygame.display.get_surface().get_height() - 450, 100, 100, mass=10, image=boximg, stationary=True)
        box5 = Collidable(self.core, 1100, pygame.display.get_surface().get_height() - 450, 100, 100, mass=10, image=boximg, stationary=True)
        box6 = Collidable(self.core, 1200, pygame.display.get_surface().get_height() - 450, 100, 100, mass=10, image=boximg, stationary=True)"""
        self.add(scaffold)
        self.add(signtext)
        """self.addAll([
            box, box2, box3, box4, box5, box6
        ])"""

    def initBackgrounds(self):
        bgimg1 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/dawn/2.png").convert(), (1366,768))
        bgimg2 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/dawn/3.png").convert_alpha(), (1366,768))
        bgimg3 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/dawn/4.png").convert_alpha(), (1366,768))
        bgimg4 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/dawn/5.png").convert_alpha(), (1366,768))
        bgimg5 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/dawn/7.png").convert_alpha(), (1366,768))
        bg1 = Background(self.core, bgimg1)
        bg2 = Background(self.core, bgimg2, scrollspeed=1)
        bg3 = Background(self.core, bgimg3, scrollspeed=2)
        bg4 = Background(self.core, bgimg4, scrollspeed=3)
        bg5 = Background(self.core, bgimg5, scrollspeed=3)
        self.add(bg1, 0)
        self.add(bg2, 1)
        self.add(bg3, 2)
        self.add(bg4, 3)
        self.add(bg5, 3)
        vignette = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/Vignette.png").convert_alpha(), (1366,768))
        self.add(Background(self.core, vignette), 5)

    def initFloorTiles(self):
        ss = pygame.image.load("data/assets/objects/TX Tileset Ground.png").convert_alpha()
        self.floortiles = [
            pygame.transform.scale(ss.subsurface((0, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((32, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((64, 0, 32, 32)), (128, 128))
        ]
