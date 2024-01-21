import pygame, random
from lib.animation import Animation
from lib.collider import Collider
from lib.healthbar import HealthBar
from lib.projectile import Projectile
from lib.text import Text

class Player:
    def __init__(self, core):
        self.core = core
        self.w, self.h = 64, 64
        self.x, self.y = 200, 200
        self.maxy = 0
        self.mass = 10
        self.speed, self.minspeed, self.maxspeed = 3, 3, 6
        self.dmg = 2
        self.maxdmg = 5
        self.hp, self.maxhp = 100, 100
        self.healthbar = HealthBar(self)
        self.initAnimations()
        self.currentanimation = self.idleRightAnimation
        self.direction = "e"
        self.attacking, self.shooting, self.jumping, self.died = False, False, False, False
        self.collider = Collider(self, debug=False)
        self.makingsound = False
        self.runningsound = pygame.mixer.Sound("data/assets/sounds/movement/player/running-in-grass.mp3")
        self.bowsound = pygame.mixer.Sound("data/assets/sounds/arrow/bow-loading.mp3")
        self.shotarrow = False

    def loop(self):
        if not self.core.scene.find(self.healthbar):
            self.core.scene.add(self.healthbar, 6)
        if self.checkDead():
            return
        self.checkInput()
        self.collider.update()
        self.currentanimation.play()

    def checkDead(self):
        if self.hp <= 0 and not self.died:
            text = Text("You didn't make it to grandma's house.", "helvetica", 36, [255, 0, 0])
            self.core.scene.add(text)
            self.core.scene.remove(self)
            self.died = True
            return True
        else:
            return False

    def checkInput(self):
        self.checkAttack()
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
        if not keys[pygame.K_d] and not keys[pygame.K_a] and not \
            self.jumping and not self.shooting and not self.attacking:
            if self.direction == "e":
                self.currentanimation = self.idleRightAnimation
            elif self.direction == "w":
                self.currentanimation = self.idleLeftAnimation
            self.runningsound.stop()
            self.makingsound = False
            

    def checkAttack(self):
        for event in self.core.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.attacking:
                    self.attack()
                elif event.button == 3 and not self.attacking:
                    self.shootArrow()
                    return
        if self.attacking:
            self.doSwordAttack()
        elif self.shooting:
            self.doShoot()

    def doShoot(self):
        if self.direction == "e":
            self.currentanimation = self.shootRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.shootLeftAnimation
        if self.currentanimation.currentframe == len(self.currentanimation.sprites) - int(len(self.currentanimation.sprites) / 3):
            if self.direction == "e":
                arrow = Projectile(self, self.direction, self.arrowimg)
            elif self.direction == "w":
                arrow = Projectile(self, self.direction, self.arrowimgleft)
            if not self.shotarrow:
                self.core.scene.add(arrow)
                self.shotarrow = True
        if self.currentanimation.ended:
            self.shooting = False

    def shootArrow(self):
        self.shotarrow = False
        if self.direction == "e":
            self.currentanimation = self.shootRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.shootLeftAnimation
        self.shooting = True
        self.bowsound.play()

    def dodamage(self):
        for obj in self.core.scene.layers[4]:
            if self.collider.colliding(obj) and hasattr(obj, "hp") and obj != self.core.player:
                obj.hp -= self.dmg
                if hasattr(obj, "takehit"):
                    obj.takehit()

    def doSwordAttack(self):
        if self.currentanimation.currentframe == int(len(self.currentanimation.sprites) / 3):
            self.dodamage()
        elif self.currentanimation.currentframe == int((len(self.currentanimation.sprites) / 3) * 2):
            self.dodamage()
        elif self.currentanimation.ended:
            self.dodamage()
            self.atkRightAnimation.reset()
            self.atkLeftAnimation.reset()
            self.attacking = False

    def attack(self):
        grunts = [
            "data/assets/sounds/grunts/player/grunting.wav", 
            "data/assets/sounds/grunts/player/grunting_2.wav", 
            "data/assets/sounds/grunts/player/grunting_3.wav",
            "data/assets/sounds/grunts/player/grunting_4.wav"
        ]
        grunt = pygame.mixer.Sound(random.choice(grunts))
        grunt.play()
        if self.direction == "e":
            self.currentanimation = self.atkRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.atkLeftAnimation
        self.attacking = True

    def checkJump(self):
        for event in self.core.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.jumping:
                    if self.direction == "e":
                        self.currentanimation = self.jumpRightAnimation
                    elif self.direction == "w":
                        self.currentanimation = self.jumpLeftAnimation
                    self.jumping = True
                    jumpsound = pygame.mixer.Sound("data/assets/sounds/grunts/player/grunting_4.wav")
                    jumpsound.play()
        if self.jumping and not self.currentanimation.ended:
            if self.currentanimation.currentframe < len(self.currentanimation.sprites) / 2:
                self.y -= 12
        if self.jumping and self.currentanimation.ended:
            self.jumpRightAnimation.reset()
            self.jumpLeftAnimation.reset()
            self.jumping = False
            
    def move(self, direction):
        self.bowsound.stop()
        if not self.jumping and not self.makingsound:
            self.runningsound.play(loops=-1)
            self.makingsound = True
        if direction == "e":
            self.x += self.speed
            if not self.jumping and not self.attacking:
                self.currentanimation = self.runRightAnimation
        else:
            self.x -= self.speed
            if not self.jumping and not self.attacking:
                self.currentanimation = self.runLeftAnimation
        self.direction = direction

    def takehit(self, damage):
        self.hp -= damage
        hurtsounds = [
            "data/assets/sounds/grunts/player/hurt/damage_1.wav",
            "data/assets/sounds/grunts/player/hurt/damage_2.wav",
            "data/assets/sounds/grunts/player/hurt/damage_3.wav"
        ]
        pygame.mixer.Sound(random.choice(hurtsounds)).play()

    def initAnimations(self):
        spritesize = 40
        ss = pygame.image.load("data/assets/player/idle sheet-Sheet.png").convert_alpha()
        idlesprites = []
        for x in range(35):
            idlesprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        idlesprites = idlesprites[::2]
        self.idleRightAnimation = Animation(idlesprites, self)
        self.idleLeftAnimation = Animation(idlesprites, self, flipx=True)
        ss = pygame.image.load("data/assets/player/itch run-Sheet sheet.png").convert_alpha()
        runsprites = []
        for x in range(47):
            runsprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        runsprites = runsprites[::2]
        self.runRightAnimation = Animation(runsprites, self)
        self.runLeftAnimation = Animation(runsprites, self, flipx=True)
        ss = pygame.image.load("data/assets/player/itch light atk sheet-Sheet.png").convert_alpha()
        atksprites = []
        for x in range(51):
            atksprites.append(ss.subsurface(((spritesize * x) + 10, 20, 60, spritesize)))
        atksprites = atksprites[::2]
        self.atkRightAnimation = Animation(atksprites, self, delay=2)
        self.atkLeftAnimation = Animation(atksprites, self, flipx=True, delay=2)
        ss = pygame.image.load("data/assets/player/itch jump sheet-Sheet.png").convert_alpha()
        jumpsprites = []
        for x in range(37):
            jumpsprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        jumpsprites = jumpsprites[::2]
        self.jumpRightAnimation = Animation(jumpsprites, self, delay=2)
        self.jumpLeftAnimation = Animation(jumpsprites, self, delay=2, flipx=True)
        ss = pygame.image.load("data/assets/player/shoot sheet.png").convert_alpha()
        shootsprites = []
        for x in range(24):
            shootsprites.append(ss.subsurface(((spritesize * x) + 10, 20, spritesize, spritesize)))
        shootsprites = shootsprites[::2]
        self.shootLeftAnimation = Animation(shootsprites, self, delay=2)
        self.shootRightAnimation = Animation(shootsprites, self, delay=2, flipx=True)

        ss = pygame.image.load("data/assets/objects/TX Village Props.png").convert_alpha()
        self.arrowimg = ss.subsurface(714, 3, 41, 15)
        self.arrowimgleft = pygame.transform.flip(self.arrowimg, True, False)
    