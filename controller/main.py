import os
import json
import time

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

printInputsMode = False
controllers=[]

if (useEmulator):
    controllers.append(EmulatedController(0))
else:
    controllers.append(Controller(0, i2c)) # If passive multiplexer
    # controllers.append(Controller(0, mplexer[0])) # If active multiplexer
    # controllers.append(Controller(1, mplexer[7]))

if(not printInputsMode):
    socketHelper = SocketHelper()

while True:
    for i, controller in enumerate(controllers):
        inputs = controller.getActions()

        if len(inputs) == 0:
            time.sleep(0.01)
            continue

        if printInputsMode:
            print(inputs)
        else:
            socketHelper.sendMessage(json.dumps(inputs, default=lambda o: o.__dict__))

            if not useEmulator:
                componentsMessages = socketHelper.getMessage()
                for message in componentsMessages:
                    #TODO: Prolly just parse the message to a class and pass messages entirely to components to handle
                    hexColor = (int(message["R"]), int(message["B"]), int(message["G"]))
                    brightness = float(message["Brightness"])
                    index = int(message["Index"])

                    if(message["KeyType"] == 'r'):
                        controller.rotary.setColor(hexColor, brightness)
                    elif(message["KeyType"] == 'f'):
                        controller.fourkey.setColor(index, hexColor)