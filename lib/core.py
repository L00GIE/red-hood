from data.scenes.test.test import Test
from lib.player import Player

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Test(self) # initialize scene

    def loop(self, events):
        self.events = events
        self.scene.loop()