from lib.enemies.mushroom import Mushroom
from lib.scenes.industrial import Industrial
from lib.background import Background
from lib.collidable import Collidable
from lib.scene import Scene
import pygame, random

class Church(Scene):

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
                if isinstance(obj, Mushroom):
                    numskellys += 1 
        if numskellys < 1:
            self.remove(self.wall)
        if numskellys < 1 and self.core.player.x > pygame.display.get_surface().get_width():
            self.core.scene = Industrial(self.core)
        
    def initGround(self):
        self.wall = Collidable(self.core, 2500, 0, 50, 768, stationary=True, debug=False)
        self.add(self.wall)
        self.initFloorTiles()
        self.add(Collidable(self.core, 50, 0, 20, 768, stationary=True, debug=False))
        self.add(Collidable(self.core, 0, 700, 128, 128, stationary=True, image=self.floortiles[0]))
        for x in range(25):
            self.add(Collidable(self.core, 128 * x, 700, 128, 128, stationary=True, image=self.floortiles[1]))

    def initObjects(self):
        pass

    def initEnemy(self):
        for x in range(1, 3):
            enemy = Mushroom(self.core)
            if x == 2:
                enemy.transforms = True
            enemy.x = 500 * x
            enemy.y = 600
            self.add(enemy)

    def initBackgrounds(self):
        bgimg1 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/church/Background_0.png").convert(), (1366,768))
        bgimg2 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/church/Background_1.png").convert_alpha(), (1366,768))
        bg1 = Background(self.core, bgimg1)
        bg2 = Background(self.core, bgimg2, scrollspeed=2)
        self.add(bg1, 0)
        self.add(bg2, 1)
        vignette = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/Vignette.png").convert_alpha(), (1366,768))
        self.add(Background(self.core, vignette), 5)

    def initFloorTiles(self):
        ss = pygame.image.load("data/assets/objects/TX Tileset Ground.png").convert_alpha()
        self.floortiles = [
            pygame.transform.scale(ss.subsurface((0, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((32, 0, 32, 32)), (128, 128)),
            pygame.transform.scale(ss.subsurface((64, 0, 32, 32)), (128, 128))
        ]
