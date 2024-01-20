from lib.animation import Animation
from lib.collider import Collider
from lib.enemy import Enemy
from lib.healthbar import HealthBar
import pygame, random

class Mushroom(Enemy):

    def __init__(self, core, boss=False, transforms=False):
        self.core = core
        self.boss = boss
        self.transforms = transforms
        self.x = 800
        self.y = 200
        self.w = 160 if boss else 80
        self.h = self.w
        self.hp = 100 if boss else 15
        self.maxhp = self.hp
        if boss:
            self.healthbar = HealthBar(self, title="Shroomsy", rightside=True)
        self.mass = 10
        self.speed = 4
        self.dmg = 2
        self.collider = Collider(self, debug=False)
        self.initAnimations()
        self.currentanimation = self.walkLeftAnimation
        self.direction = "e"
        self.takinghit = False

    def loop(self):
        if self.hp <= 0:
            if self.direction == "e":
                self.currentanimation = self.dieRightAnimation
            elif self.direction == "w":
                self.currentanimation = self.dieLeftAnimation
        if self.hp <= 0 and not self.currentanimation.ended:
            self.currentanimation.play()
            return
        elif self.hp <= 0 and self.currentanimation.ended:
            self.core.scene.remove(self)
            if not self.boss and self.transforms:
                bossmusic = pygame.mixer.Sound("data/assets/sounds/music/boss.mp3")
                bossmusic.play()
                boss = Mushroom(self.core, True)
                boss.x = self.x
                boss.y = self.y
                self.core.scene.add(boss)
            return
        if random.randint(0, 300) == 1:
            self.playSound()
        super().moveToPlayer()
        super().checkWalking()
        if self.collider.colliding(self.core.player):
            super().attack()
        self.collider.update()
        self.currentanimation.play()
        if self.boss:
            self.healthbar.loop()

    def playSound(self):
        sounds = [
            "data/assets/sounds/grunts/mushrooms/attack-cannibal-beast-95140.mp3",
            "data/assets/sounds/grunts/mushrooms/monster-screech-94983.mp3",
            "data/assets/sounds/grunts/mushrooms/pterodactyl-85046.mp3"
        ]
        pygame.mixer.Sound(random.choice(sounds)).play()

    def initAnimations(self):
        ss = pygame.image.load("data/assets/enemies/Mushroom/Run.png").convert_alpha()
        walksprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.walkRightAnimation = Animation(walksprites, self)
        self.walkLeftAnimation = Animation(walksprites, self, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Mushroom/Attack.png").convert_alpha()
        atksprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.attackRightAnimation = Animation(atksprites, self, delay=10)
        self.attackLeftAnimation = Animation(atksprites, self, delay=10, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Mushroom/Death.png").convert_alpha()
        diesprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.dieRightAnimation = Animation(diesprites, self, delay=10)
        self.dieLeftAnimation = Animation(diesprites, self, delay=10, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Mushroom/Take Hit.png").convert_alpha()
        hitsprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.hitRightAnimation = Animation(hitsprites, self, delay=5)
        self.hitLeftAnimation = Animation(hitsprites, self, delay=5, flipx=True)