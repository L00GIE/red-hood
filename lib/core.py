from data.scenes.city.city import City
from data.scenes.industrial.industrial import Industrial
from data.scenes.start.start import Start
from data.scenes.pit.pit import Pit
from lib.cursor import Cursor
from lib.player import Player

class Core:

    def __init__(self):
        self.player = Player(self) # initialize player
        self.scene = Start(self) # initialize start scene
        # self.cursor = Cursor(self)

    def loop(self, events):
        self.events = events
        self.scene.loop()
        # self.cursor.loop()