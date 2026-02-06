from adafruit_neokey.neokey1x4 import NeoKey1x4

class FourKey():
    def __init__(self, playerIndex: int, bus, addr=0x30):
        self.playerIndex = playerIndex
        self.fourKey = NeoKey1x4(bus, addr=addr)
        self.lastState = [False, False, False, False]
    
    def getActions(self):
        inputs = []
        keyRange = range(4)
        for i in keyRange:
            if not self.lastState[i] == self.fourKey[i]:
                inputs.append({"Action": f"{self.playerIndex}_k{i}_pressed", "Pressed": self.fourKey[i] })
                self.lastState[i] = self.fourKey[i]

        return inputs

    def setColor(self, index, color=(0,0,0)):
        self.fourKey.pixels[index] = color