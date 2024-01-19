from data.assets.enemies.Skeleton.skeleton import Skeleton
from data.scenes.pit.pit import Pit
from lib.background import Background
from lib.collidable import Collidable
from lib.scene import Scene
import pygame

from lib.staticimg import StaticImage

class Start(Scene):

    def __init__(self, core):
        self.core = core
        super().__init__()
        self.initBackgrounds()
        self.initGround()
        self.initObjects()
        self.add(self.core.player) # add player to foremost layer
        pygame.mixer.music.load("data/assets/sounds/music/dance-with-fate.mp3")
        pygame.mixer.music.play(loops=-1)

    def loop(self):
        if self.core.player.x > pygame.display.get_surface().get_width():
            self.core.scene = Pit(self.core)
        pygame.display.get_surface().fill([255, 255, 255])
        self.applygravity() # this is where gravity is applied to every non-stationary object in the scene
        super().loop() # this is where every object in the scene has its loop() called
        
    def initGround(self):
        self.initFloorTiles()
        wall = Collidable(self.core, 50, 0, 20, 768, stationary=True, debug=False)
        self.add(Collidable(self.core, 0, 700, 128, 128, stationary=True, image=self.floortiles[0]))
        for x in range(10):
            self.add(Collidable(self.core, 128 * x, 700, 128, 128, stationary=True, image=self.floortiles[1]))
        self.add(Collidable(self.core, (128*x) + 32, 700, 128, 128, stationary=True, image=self.floortiles[2]))
        self.add(wall)

    def initObjects(self):
        ss = pygame.image.load("data/assets/objects/TX Village Props.png").convert_alpha()
        signimg = pygame.transform.scale_by(pygame.image.load("data/assets/objects/donotentersign.png").convert_alpha(), 0.8)
        boximg = pygame.transform.scale(ss.subsurface((41, 18, 47, 45)), (100, 100))
        scaffoldimg = pygame.transform.scale(ss.subsurface((187, 162, 72, 64)), (216, 192))
        box = Collidable(self.core, 400, -200, 100, 100, mass=1, image=boximg)
        scaffold = Collidable(self.core, 800, 520, scaffoldimg.get_width(), scaffoldimg.get_height(), stationary=True, image=scaffoldimg)
        scaffold1 = Collidable(self.core, 800 + scaffoldimg.get_width() - 20, 520, scaffoldimg.get_width(), scaffoldimg.get_height(), stationary=True, image=scaffoldimg)
        signtext = StaticImage(signimg, (scaffold.x + 50, scaffold.y + 20))
        signtext1 = StaticImage(signimg, (scaffold1.x + 50, scaffold1.y + 20))
        self.add(box)
        self.add(scaffold)
        self.add(scaffold1)
        self.add(signtext)
        self.add(signtext1)

    def initBackgrounds(self):
        bgimg1 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/forest/background_layer_1.png").convert(), (1366,768))
        bgimg2 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/forest/background_layer_2.png").convert_alpha(), (1366,768))
        bgimg3 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/forest/background_layer_3.png").convert_alpha(), (1366,768))
        bg1 = Background(self.core, bgimg1)
        bg2 = Background(self.core, bgimg2, scrollspeed=2)
        bg3 = Background(self.core, bgimg3, scrollspeed=4)
        self.add(bg1, 0)
        self.add(bg2, 1)
        self.add(bg3, 2)

    def initFloorTiles(self):
        ss = pygame.image.load("data/assets/objects/TX Tileset Ground.png").convert_alpha()
        self.floortiles = [
            pygame.transform.scale(ss.subsurface((0, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((32, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((64, 0, 32, 32)), (128, 128))
        ]

    def applygravity(self):
        for layer in self.layers:
            for obj in layer:
                if hasattr(obj, "collider") and not \
                    obj.collider.stationary and not \
                    obj.collider.antigrav:
                    obj.y += 8