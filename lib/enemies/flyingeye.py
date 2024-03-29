from lib.animation import Animation
from lib.collider import Collider
from lib.enemy import Enemy
import pygame, random

from lib.healthbar import HealthBar

class FlyingEye(Enemy):
    def __init__(self, core, boss=False, transforms=False):
        self.core = core
        self.boss = boss
        self.transforms = transforms
        self.x = 800
        self.y = 200
        self.w = 160 if boss else 80
        self.h = self.w
        self.hp = 150 if boss else 30
        self.maxhp = self.hp
        if boss:
            self.healthbar = HealthBar(self, title="Big Flyball", rightside=True)
        self.mass = 10
        self.speed = 3
        self.dmg = 1.5
        self.collider = Collider(self, debug=False)
        self.initAnimations()
        self.currentanimation = self.walkLeftAnimation
        self.direction = "e"
        self.takinghit, self.diving = False, False
        self.dropped = False

    def loop(self):
        self.checkcollision()
        self.divebomb()
        if self.hp <= 0:
            if self.direction == "e":
                self.currentanimation = self.dieRightAnimation
            elif self.direction == "w":
                self.currentanimation = self.dieLeftAnimation
        if self.hp <= 0 and self.boss and not self.dropped:
            self.doDrop()
            self.dropped = True
        if self.hp <= 0 and not self.currentanimation.ended:
            self.currentanimation.play()
            return
        elif self.hp <= 0 and self.currentanimation.ended:
            self.core.scene.remove(self)
            if not self.boss and self.transforms:
                bossmusic = pygame.mixer.Sound("data/assets/sounds/music/boss.mp3")
                bossmusic.play()
                boss = FlyingEye(self.core, True)
                boss.x = self.x
                boss.y = self.y
                self.core.scene.add(boss)
            return
        if random.randint(0, 300) == 1:
            self.playSound()
        self.moveToPlayer()
        self.checkWalking()
        if self.collider.colliding(self.core.player):
            self.attack()
        self.collider.update()
        self.currentanimation.play()
        if self.boss and not self.core.scene.find(self.healthbar):
            self.core.scene.add(self.healthbar, 6)

    def divebomb(self):
        if not self.diving:
            self.y -= 10
            if self.y <= 500:
                self.diving = True
        else:
            self.y += 2
            if self.y >= 600:
                self.diving = False

    def playSound(self):
        sounds = [
            "data/assets/sounds/grunts/flyingeyes/dragon-roar-96996.mp3",
            "data/assets/sounds/grunts/flyingeyes/monster-howl-85304.mp3",
            "data/assets/sounds/grunts/flyingeyes/angry-beast-6172.mp3"
        ]
        pygame.mixer.Sound(random.choice(sounds)).play()

    def initAnimations(self):
        ss = pygame.image.load("data/assets/enemies/Flyingeye/Flight.png").convert_alpha()
        walksprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.walkRightAnimation = Animation(walksprites, self)
        self.walkLeftAnimation = Animation(walksprites, self, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Flyingeye/Attack.png").convert_alpha()
        atksprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.attackRightAnimation = Animation(atksprites, self, delay=10)
        self.attackLeftAnimation = Animation(atksprites, self, delay=10, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Flyingeye/Death.png").convert_alpha()
        diesprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.dieRightAnimation = Animation(diesprites, self, delay=10)
        self.dieLeftAnimation = Animation(diesprites, self, delay=10, flipx=True)
        ss = pygame.image.load("data/assets/enemies/Flyingeye/Take Hit.png").convert_alpha()
        hitsprites = [
            ss.subsurface(57, 48, 50, 55),
            ss.subsurface(206, 48, 50, 55),
            ss.subsurface(356, 48, 50, 55),
            ss.subsurface(506, 48, 50, 55)
        ]
        self.hitRightAnimation = Animation(hitsprites, self, delay=5)
        self.hitLeftAnimation = Animation(hitsprites, self, delay=5, flipx=True)
