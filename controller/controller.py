from components.fourkey import FourKey
from components.rotary import Rotary

class Controller:
    def __init__(self, playerIndex, bus):
        self.rotary = Rotary(playerIndex, bus)
        self.fourkey = FourKey(playerIndex, bus)

    def getActions(self):
        return self.rotary.getActions() + self.fourkey.getActions()