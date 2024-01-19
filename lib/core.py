from data.scenes.industrial.industrial import Industrial
from data.scenes.start.start import Start
from lib.camera import Camera
from lib.cursor import Cursor
from lib.player import Player

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Industrial(self) # initialize start scene
        # self.cursor = Cursor(self)
        self.camera = Camera(self)

    def loop(self, events):
        self.events = events
        self.scene.loop()
        self.camera.loop()
        # self.cursor.loop()