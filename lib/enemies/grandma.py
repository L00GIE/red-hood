from lib.animation import Animation
from lib.collider import Collider
from lib.enemy import Enemy
from lib.healthbar import HealthBar
from lib.projectile import Projectile
import pygame, random

class Grandma(Enemy):

    def __init__(self, core):
        self.core = core
        self.x = 800
        self.y = 200
        self.w = 160
        self.h = self.w
        self.hp = 500
        self.maxhp = self.hp
        self.healthbar = HealthBar(self, title="Grandma", rightside=True)
        self.mass = 10
        self.speed = 5
        self.dmg = 4
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
            return
        if random.randint(0, 400) == 1:
            self.playSound()
        if random.randint(0, 200) == 1:
            self.throwSlipper()
        super().moveToPlayer()
        super().checkWalking()
        if self.collider.colliding(self.core.player):
            super().attack()
        self.collider.update()
        self.currentanimation.play()
        if not self.core.scene.find(self.healthbar):
            self.core.scene.add(self.healthbar, 6)

    def throwSlipper(self):
        self.core.scene.add(Slipper(self))

    def playSound(self):
        sounds = [
            "data/assets/sounds/grunts/grandma/laugh-1.wav",
            "data/assets/sounds/grunts/grandma/laugh-2.wav",
            "data/assets/sounds/grunts/grandma/laugh-3.wav",
            "data/assets/sounds/grunts/grandma/laugh-4.wav",
            "data/assets/sounds/grunts/grandma/laugh-5.wav",
            "data/assets/sounds/grunts/grandma/laugh-6.wav"
        ]
        pygame.mixer.Sound(random.choice(sounds)).play()

    def initAnimations(self):
        ss = pygame.image.load("data/assets/enemies/Grandma/$Elderly Inn Keeper.png")
        walksprites = []
        for x in range(3):
            walksprites.append(ss.subsurface((48 * x, 50, 48, 50)))
        self.walkRightAnimation = Animation(walksprites, self, flipx=True)
        self.walkLeftAnimation = Animation(walksprites, self)
        ss = pygame.image.load("data/assets/enemies/Grandma/Elderly Inn Keeper SV Battler.png")
        atksprites = []
        for x in range(5):
            atksprites.append(ss.subsurface(64 * x, 0, 64, 64))
        self.attackRightAnimation = Animation(atksprites, self, delay=10, flipx=True)
        self.attackLeftAnimation = Animation(atksprites, self, delay=10)
        diesprites = []
        for x in range(5):
            diesprites.append(ss.subsurface(384, 64 + (64 * x), 64, 64))
        self.dieRightAnimation = Animation(diesprites, self, delay=10, flipx=True)
        self.dieLeftAnimation = Animation(diesprites, self, delay=10)
        hitsprites = []
        for x in range(3):
            hitsprites.append(ss.subsurface(384 + (64 * x), 0, 64, 64))
        self.hitRightAnimation = Animation(hitsprites, self, delay=5, flipx=True)
        self.hitLeftAnimation = Animation(hitsprites, self, delay=5)


class Slipper:

    def __init__(self, parent):
        self.parent = parent
        self.direction = parent.direction
        self.x, self.y = parent.x, parent.y + (parent.h / 2)
        self.speed = 10
        slipperimg = pygame.transform.scale_by(pygame.image.load("data/assets/objects/slipper.png"), 0.2)
        self.slipperimgs = [slipperimg]
        for x in range(36):
            self.slipperimgs.append(pygame.transform.rotate(slipperimg, 10 * x))
        self.slipperindex = 0
        self.h = slipperimg.get_height()
        self.w = slipperimg.get_width()
        self.mass = 0.1
        self.collider = Collider(self, antigrav=True)
        self.angle = 0

    def loop(self):
        img = self.slipperimgs[self.slipperindex]
        self.slipperindex += 1
        if self.slipperindex >= len(self.slipperimgs):
            self.slipperindex = 0
        if self.direction == "e":
            self.x += self.speed
        elif self.direction == "w":
            self.x -= self.speed
        if self.parent.core.player.y > self.y:
            self.y += 1
        self.collider.update()
        if self.collider.colliding(self.parent.core.player):
            self.parent.core.player.takehit(self.parent.dmg)
            self.parent.core.scene.remove(self)
        pygame.display.get_surface().blit(img, (self.x, self.y))
        

