from lib.animation import Animation
from lib.collider import Collider
from lib.enemy import Enemy
from lib.healthbar import HealthBar
import pygame


class Skeleton(Enemy):

    def __init__(self, core, boss=False):
        self.core = core
        self.boss = boss
        self.x = 800
        self.y = 200
        self.w = 160 if boss else 80
        self.h = self.w
        self.hp = 100 if boss else 15
        self.maxhp = self.hp
        if boss:
            self.healthbar = HealthBar(self, rightside=True)
        self.mass = 10
        self.speed = 3
        self.dmg = 1
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
            if not self.boss:
                boss = Skeleton(self.core, True)
                boss.x = self.x
                boss.y = self.y
                self.core.scene.add(boss)
            return
        super().moveToPlayer()
        self.checkWalking()
        if self.collider.colliding(self.core.player):
            self.attack()
        self.collider.update()
        self.currentanimation.play()
        if self.boss:
            self.healthbar.loop()

    def checkWalking(self):
        if self.direction == "e":
            self.currentanimation = self.walkRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.walkLeftAnimation

    def attack(self):
        if self.takinghit and not self.currentanimation.ended: return
        else: self.takinghit = False
        if self.direction == "e":
            self.currentanimation = self.attackRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.attackLeftAnimation
        if self.currentanimation.ended:
            self.core.player.hp -= self.dmg

    def takehit(self):
        self.takinghit = True
        if self.direction == "e":
            self.currentanimation = self.hitRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.hitLeftAnimation

    def initAnimations(self):
        ss = pygame.image.load("data/assets/enemies/Skeleton/Walk.png")
        walksprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.walkRightAnimation = Animation(walksprites, self)
        self.walkLeftAnimation = Animation(walksprites, self, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Skeleton/Attack.png")
        atksprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.attackRightAnimation = Animation(atksprites, self, delay=10)
        self.attackLeftAnimation = Animation(atksprites, self, delay=10, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Skeleton/Death.png")
        diesprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.dieRightAnimation = Animation(diesprites, self, delay=10)
        self.dieLeftAnimation = Animation(diesprites, self, delay=10, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Skeleton/Take Hit.png")
        hitsprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.hitRightAnimation = Animation(hitsprites, self, delay=5)
        self.hitLeftAnimation = Animation(hitsprites, self, delay=5, flipx=True)
