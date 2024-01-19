from data.assets.enemies.Flyingeye.flyingeye import FlyingEye
from data.scenes.grandmashouse.grandmas import Grandmas
from lib.background import Background
from lib.collidable import Collidable
from lib.scene import Scene
import pygame

class Dawn(Scene):

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
        if self.core.player.x > pygame.display.get_surface().get_width():
            self.core.scene = Grandmas(self.core)
        
    def initGround(self):
        self.initFloorTiles()
        self.add(Collidable(self.core, 50, 0, 20, 768, stationary=True, debug=False))
        self.add(Collidable(self.core, 0, 700, 128, 128, stationary=True, image=self.floortiles[0]))
        for x in range(25):
            self.add(Collidable(self.core, 128 * x, 700, 128, 128, stationary=True, image=self.floortiles[1]))

    def initObjects(self):
        pass

    def initEnemy(self):
        pass

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