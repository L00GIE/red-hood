from lib.animation import Animation
from lib.collider import Collider
from lib.enemy import Enemy
import pygame

class Skeleton(Enemy):

    def __init__(self, core):
        self.core = core
        self.x = 600
        self.y = 200
        self.w = 150
        self.h = 150
        self.hp = 10
        self.mass = 10
        self.speed = 3
        self.collider = Collider(self, debug=True)
        self.initAnimations()
        self.currentanimation = self.walkLeftAnimation
        self.direction = "e"

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
            return
        super().moveToPlayer()
        self.checkWalking()
        if self.collider.colliding(self.core.player):
            self.attack()
        self.collider.update(self.x + 40, self.y + 45, 60, 60)
        self.currentanimation.play()

    def checkWalking(self):
        if self.direction == "e":
            self.currentanimation = self.walkRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.walkLeftAnimation

    def attack(self):
        if self.direction == "e":
            self.currentanimation = self.attackRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.attackLeftAnimation

    def initAnimations(self):
        ss = pygame.image.load("data/assets/enemies/Skeleton/Walk.png")
        walksprites = []
        for x in range(4):
            walksprites.append(ss.subsurface(self.w * x, 0, self.w, self.h))
        self.walkRightAnimation = Animation(walksprites, self)
        self.walkLeftAnimation = Animation(walksprites, self, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Skeleton/Attack.png")
        atksprites = []
        for x in range(8):
            atksprites.append(ss.subsurface(self.w * x, 0, self.w, self.h))
        self.attackRightAnimation = Animation(atksprites, self)
        self.attackLeftAnimation = Animation(atksprites, self, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Skeleton/Death.png")
        diesprites = []
        for x in range(4):
            diesprites.append(ss.subsurface(self.w * x, 0, self.w, self.h))
        self.dieRightAnimation = Animation(diesprites, self, delay=10)
        self.dieLeftAnimation = Animation(diesprites, self, delay=10, flipx=True)
