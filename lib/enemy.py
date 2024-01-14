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
