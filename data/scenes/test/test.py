from data.assets.enemies.Skeleton.skeleton import Skeleton
from lib.background import Background
from lib.collidable import Collidable
from lib.scene import Scene
import pygame

class Test(Scene):

    def __init__(self, core):
        self.core = core
        super().__init__()
        self.initBackgrounds()
        self.initGround()
        self.initEnemy()

    def loop(self):
        pygame.display.get_surface().fill([255, 255, 255])
        self.applygravity()
        super().loop()

    def initGround(self):
        self.initFloorTiles()
        ss = pygame.image.load("data/assets/objects/TX Village Props.png")
        boximg = pygame.transform.scale(ss.subsurface((41, 18, 47, 45)), (100, 100))
        wall = Collidable(self.core, 50, 0, 20, 768, stationary=True, debug=True)
        wall2 = Collidable(self.core, 800, 368, 800, 250, stationary=True, debug=True)
        box = Collidable(self.core, 400, 200, 100, 100, mass=1, image=boximg)
        self.add(Collidable(self.core, 0, 600, 128, 128, stationary=True, image=self.floortiles[0]))
        for x in range(10):
            self.add(Collidable(self.core, 128 * x, 600, 128, 128, stationary=True, image=self.floortiles[1], debug=True))
        self.add(Collidable(self.core, (128*x) + 32, 600, 128, 128, stationary=True, image=self.floortiles[2]))
        self.add(wall)
        self.add(wall2)
        self.add(box)

    def initEnemy(self):
        enemy = Skeleton(self.core)
        self.add(enemy)

    def initBackgrounds(self):
        bg1 = Background(self.core, pygame.transform.scale(pygame.image.load("data/assets/backgrounds/background_layer_1.png"), (1366,768)))
        bg2 = Background(self.core, pygame.transform.scale(pygame.image.load("data/assets/backgrounds/background_layer_2.png"), (1366,768)), scrollspeed=2)
        bg3 = Background(self.core, pygame.transform.scale(pygame.image.load("data/assets/backgrounds/background_layer_3.png"), (1366,768)), scrollspeed=4)
        self.add(bg1, 0)
        self.add(bg2, 1)
        self.add(bg3, 2)

    def initFloorTiles(self):
        ss = pygame.image.load("data/assets/objects/TX Tileset Ground.png")
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
                if hasattr(obj, "collider") and not obj.collider.stationary:
                    obj.y += 6