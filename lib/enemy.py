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
        if self.currentanimation.ended:
            self.core.player.takehit(self.dmg)

    def takehit(self):
        self.takinghit = True
        if self.direction == "e":
            self.currentanimation = self.hitRightAnimation
        elif self.direction == "w":
            self.currentanimation = self.hitLeftAnimation
