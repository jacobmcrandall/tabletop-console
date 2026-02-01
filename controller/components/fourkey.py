from adafruit_neokey.neokey1x4 import NeoKey1x4

class FourKey():
    def __init__(self, playerIndex: int, bus, addr=0x30):
        self.playerIndex = playerIndex
        self.fourKey = NeoKey1x4(bus, addr=addr)
    
    def getActions(self):
        return []

    def setColor(self, index, color=0x0):
        self.fourKey.pixels[index] = color