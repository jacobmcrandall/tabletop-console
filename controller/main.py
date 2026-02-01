import os
import json

# This must be set before import of board for the correct board to properly load
os.environ["BLINKA_MCP2221"]="1"

useEmulator = False
try:
    import board
    import adafruit_tca9548a # our multiplexer
    from controller import Controller
    i2c = board.I2C()  # uses board.SCL and board.SDA
    #i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    # Create the TCA9548A object and give it the I2C bus
    mplexer = adafruit_tca9548a.TCA9548A(i2c)
except Exception as e:
    print("Error importing board use emulator")
    from helpers.emulator import EmulatedController
    useEmulator = True

from sockethelper import SocketHelper

printInputsMode = True
controllers=[]

if (useEmulator):
    controllers.append(EmulatedController(0))
else:
    controllers.append(Controller(0, mplexer[0]))
    controllers.append(Controller(1, mplexer[7]))

if(not printInputsMode):
    socketHelper = SocketHelper()

while True:
    for i, controller in enumerate(controllers):
        inputs = controller.getActions()

        if len(inputs) == 0:
            continue

        if printInputsMode:
            print(inputs)
        else:
            socketHelper.sendMessage(json.dumps(inputs, default=lambda o: o.__dict__))