import pygame
from lib.damagedrop import DamageDrop
from lib.healthdrop import HealthDrop
from lib.hitnumber import HitNumber
import random

class Enemy:

    def moveToPlayer(self):
        if self.collider.colliding(self.core.player):
            return
        if self.core.player.x > self.x:
            self.x += self.speed
            self.direction = "e"
        if self.core.player.x < self.x:
            self.x -= self.speed
            self.direction = "w"

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
        if self.currentanimation.ended and self.core.player.hp > 0:
            self.core.player.takehit(self.dmg)

    def takehit(self, damage):
        self.hp -= damage
        self.core.scene.add(HitNumber(self.core, self, damage))
        self.takinghit = True
        if self.direction == "e":
            self.currentanimation = self.hitRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.hitLeftAnimation

    def doDrop(self):
        if random.randint(1, 2) == 1:
            self.core.scene.add(HealthDrop(self.core, (self.x, self.y - 1000)))
        else:
            self.core.scene.add(DamageDrop(self.core, (self.x, self.y - 1000)))

    def checkcollision(self):
        for obj in self.core.scene.layers[4]:
            if isinstance(obj, Enemy):
                if self.collider.colliding(obj):
                    if self.x > obj.x:
                        self.x = obj.x + obj.w
                    elif self.x < obj.x:
                        obj.x = self.x + self.y
