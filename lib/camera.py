class Camera:

    def __init__(self, core):
        self.core = core
        self.lastplayerx = self.core.player.x

    def loop(self):
        deltax = self.core.player.x - self.lastplayerx
        if deltax > 10 or deltax < -10:
            self.lastplayerx = self.core.player.x
            return
        for obj in self.core.scene.layers[4]:
            if obj == self.core.player: continue
            obj.x -= deltax
        self.lastplayerx = self.core.player.x