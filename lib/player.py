import pygame
from lib.animation import Animation
from lib.collider import Collider

class Player:
    def __init__(self, core):
        self.core = core
        self.w = 64
        self.h = 64
        self.x = 200
        self.y = 200
        self.mass = 10
        self.maxy = 0
        self.speed = 3
        self.minspeed = 3
        self.maxspeed = 6
        self.initAnimations()
        self.currentanimation = self.idleRightAnimation
        self.direction = "e"
        self.attacking = False
        self.jumping = False
        self.collider = Collider(self, debug=True)

    def loop(self):
        self.checkInput()
        self.collider.update()
        self.currentanimation.play()

    def checkInput(self):
        self.checkAttack()
        if self.attacking: return
        self.checkJump()
        self.checkMove()

    def checkMove(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed = self.maxspeed
            self.runLeftAnimation.delay = 1
            self.runRightAnimation.delay = 1
        else:
            self.speed = self.minspeed
            self.runLeftAnimation.delay = 3
            self.runRightAnimation.delay = 3
        if keys[pygame.K_d]:
            self.move("e")
        if keys[pygame.K_a]:
            self.move("w")
        if not keys[pygame.K_d] and not keys[pygame.K_a] and not self.jumping:
            if self.direction == "e":
                self.currentanimation = self.idleRightAnimation
            elif self.direction == "w":
                self.currentanimation = self.idleLeftAnimation

    def checkAttack(self):
        for event in self.core.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.attacking:
                    if self.direction == "e":
                        self.currentanimation = self.atkRightAnimation
                    elif self.direction == "w":
                        self.currentanimation = self.atkLeftAnimation
                    self.attacking = True
        if self.attacking and self.currentanimation.ended:
            for obj in self.core.scene.layers[4]:
                if self.collider.colliding(obj) and hasattr(obj, "hp") and obj != self.core.player:
                    obj.hp -= 100
            self.atkRightAnimation.reset()
            self.atkLeftAnimation.reset()
            self.attacking = False

    def checkJump(self):
        for event in self.core.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.jumping:
                    if self.direction == "e":
                        self.currentanimation = self.jumpRightAnimation
                    elif self.direction == "w":
                        self.currentanimation = self.jumpLeftAnimation
                    self.jumping = True
        if self.jumping and not self.currentanimation.ended:
            if self.currentanimation.currentframe < len(self.currentanimation.sprites) / 2:
                self.y -= 12
        if self.jumping and self.currentanimation.ended:
            self.jumpRightAnimation.reset()
            self.jumpLeftAnimation.reset()
            self.jumping = False
            
    def move(self, direction):
        if direction == "e":
            self.x += self.speed
            if not self.jumping:
                self.currentanimation = self.runRightAnimation
        else:
            self.x -= self.speed
            if not self.jumping:
                self.currentanimation = self.runLeftAnimation
        self.direction = direction

    def initAnimations(self):
        spritesize = 40
        ss = pygame.image.load("data/assets/player/idle sheet-Sheet.png")
        idlesprites = []
        for x in range(35):
            idlesprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        idlesprites = idlesprites[::2]
        self.idleRightAnimation = Animation(idlesprites, self)
        self.idleLeftAnimation = Animation(idlesprites, self, flipx=True)
        ss = pygame.image.load("data/assets/player/itch run-Sheet sheet.png")
        runsprites = []
        for x in range(24):
            runsprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        runsprites = runsprites[::2]
        self.runRightAnimation = Animation(runsprites, self)
        self.runLeftAnimation = Animation(runsprites, self, flipx=True)
        ss = pygame.image.load("data/assets/player/itch light atk sheet-Sheet.png")
        atksprites = []
        for x in range(26):
            atksprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        atksprites = atksprites[::2]
        self.atkRightAnimation = Animation(atksprites, self, delay=2)
        self.atkLeftAnimation = Animation(atksprites, self, flipx=True, delay=2)
        ss = pygame.image.load("data/assets/player/itch jump sheet-Sheet.png")
        jumpsprites = []
        for x in range(19):
            jumpsprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        jumpsprites = jumpsprites[::2]
        self.jumpRightAnimation = Animation(jumpsprites, self, delay=2)
        self.jumpLeftAnimation = Animation(jumpsprites, self, delay=2, flipx=True)
    