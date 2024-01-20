from data.assets.enemies.Skeleton.skeleton import Skeleton
from data.scenes.glacialmountains.glacialmountains import GlacialMountains
from lib.background import Background
from lib.collidable import Collidable
from lib.scene import Scene
from lib.text import Text
import pygame, random

class Pit(Scene):

    def __init__(self, core):
        self.core = core
        super().__init__()
        self.initBackgrounds()
        self.initGround()
        self.initObjects()
        self.core.player.x = 100
        self.core.player.y = -100
        self.add(self.core.player) # add player to foremost layer
        self.initEnemy()

    def loop(self):
        self.checkBounds()
        pygame.display.get_surface().fill([255, 255, 255])
        self.applygravity() # this is where gravity is applied to every non-stationary object in the scene
        super().loop() # this is where every object in the scene has its loop() called

    def checkBounds(self):
        numskellys = 0
        for layer in self.layers:
            for obj in layer:
                if isinstance(obj, Skeleton):
                    numskellys += 1
        if numskellys < 1 and self.core.player.x > pygame.display.get_surface().get_width():
            self.core.scene = GlacialMountains(self.core)
        
    def initGround(self):
        self.initFloorTiles()
        self.add(Collidable(self.core, 50, 0, 20, 768, stationary=True, debug=False))
        self.add(Collidable(self.core, 0, 700, 128, 128, stationary=True, image=self.floortiles[0]))
        for x in range(25):
            self.add(Collidable(self.core, 128 * x, 700, 128, 128, stationary=True, image=self.floortiles[1]))

    def initObjects(self):
        pass

    def initEnemy(self):
        for x in range(1, 3):
            enemy = Skeleton(self.core)
            if x == 2:
                enemy.transforms = True
            enemy.x = 500 + (x * 50)
            enemy.y = 600
            self.add(enemy)

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
            pygame.transform.scale(ss.subsurface((64, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((0, 32, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((32, 32, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((64, 32, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((0, 64, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((32, 64, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((64, 64, 32, 32)), (128, 128))
        ]

    def applygravity(self):
        for layer in self.layers:
            for obj in layer:
                if hasattr(obj, "collider") and not \
                    obj.collider.stationary and not \
                    obj.collider.antigrav:
                    obj.y += 8