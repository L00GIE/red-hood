from data.assets.enemies.Flyingeye.flyingeye import FlyingEye
from data.scenes.grandmashouse.grandmas import Grandmas
from lib.background import Background
from lib.collidable import Collidable
from lib.damagedrop import DamageDrop
from lib.healthdrop import HealthDrop
from lib.scene import Scene
from lib.staticimg import StaticImage
from lib.text import Text
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
        self.healthdrop = HealthDrop(self.core, (600, 0))
        self.add(self.healthdrop)
        self.initText()
        self.grown = False
        self.shrunk = True

    def loop(self):
        self.checkBounds()
        self.checkClick()
        pygame.display.get_surface().fill([255, 255, 255])
        self.applygravity() # this is where gravity is applied to every non-stationary object in the scene
        super().loop() # this is where every object in the scene has its loop() called

    def initText(self):
        screen = pygame.display.get_surface()
        exchange = pygame.transform.scale_by(pygame.image.load("data/assets/objects/exchange.png").convert_alpha(), 0.75)
        imgx = (screen.get_width() / 2) - (exchange.get_width() / 2)
        imgy = (screen.get_height() / 2) - (exchange.get_height() / 2)
        text = Text("Wait... You can take this heart, or you can", "helvetica", 36, [255, 255, 255], (0, imgy - 41))
        text.x = (screen.get_width() / 2) - (text.get_width() / 2)
        self.exchimg = StaticImage(exchange, (imgx, imgy))
        text2 = Text("it for more damage... Which will it be?", "helvetica", 36, [255, 255, 255], (0, imgy + exchange.get_height() + 5))
        text2.x = (screen.get_width() / 2) - (text2.get_width() / 2)
        self.add(text)
        self.add(self.exchimg)
        self.add(text2)

    def checkClick(self):
        imgrect = pygame.Rect(
            self.exchimg.x, 
            self.exchimg.y,
            self.exchimg.image.get_width(),
            self.exchimg.image.get_height())
        if imgrect.collidepoint(pygame.mouse.get_pos()):
            if not self.grown:
                self.exchimg.image = pygame.transform.scale_by(self.exchimg.image, 1.5)
                self.exchimg.x = (pygame.display.get_surface().get_width() / 2) - (self.exchimg.image.get_width() / 2)
                self.exchimg.y = (pygame.display.get_surface().get_height() / 2) - (self.exchimg.image.get_height() / 2)
                self.grown = True
                self.shrunk = False
            for event in self.core.events:
                if event.type == pygame.MOUSEBUTTONDOWN and self.find(self.healthdrop):
                    if event.button == 1:
                        self.remove(self.healthdrop)
                        for obj in self.layers[4]:
                            if isinstance(obj, Text):
                                self.remove(obj)
                        self.remove(self.exchimg)
                        self.add(DamageDrop(self.core, (600, 0)))
                        self.add(Text("Interesting choice...", "helvetica", 36, [255, 255, 255]))
        else:
            if not self.shrunk:
                self.exchimg.image = pygame.transform.scale_by(self.exchimg.image, 0.6667)
                self.exchimg.x = (pygame.display.get_surface().get_width() / 2) - (self.exchimg.image.get_width() / 2)
                self.exchimg.y = (pygame.display.get_surface().get_height() / 2) - (self.exchimg.image.get_height() / 2)
                self.shrunk = True
                self.grown = False

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
        bgimg1 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/forest/background_layer_1.png").convert(), (1366,768))
        bgimg2 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/forest/background_layer_2.png").convert_alpha(), (1366,768))
        bgimg3 = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/forest/background_layer_3.png").convert_alpha(), (1366,768))
        bg1 = Background(self.core, bgimg1)
        bg2 = Background(self.core, bgimg2, scrollspeed=2)
        bg3 = Background(self.core, bgimg3, scrollspeed=4)
        self.add(bg1, 0)
        self.add(bg2, 1)
        self.add(bg3, 2)
        vignette = pygame.transform.scale(pygame.image.load("data/assets/backgrounds/Vignette.png").convert_alpha(), (1366,768))
        self.add(Background(self.core, vignette), 5)

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
