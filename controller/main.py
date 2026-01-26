# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9548A to perform a simple scan for connected devices

import os
import json

os.environ["BLINKA_MCP2221"]="1"

import board
#our multiplexer
import adafruit_tca9548a
from rainbowio import colorwheel

from adafruit_seesaw import digitalio, neopixel, rotaryio, seesaw
from adafruit_neokey.neokey1x4 import NeoKey1x4

from controller import Controller
from sockethelper import SocketHelper

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
mplexer = adafruit_tca9548a.TCA9548A(i2c)

#neokey = NeoKey1x4(i2c_bus, addr=0x30)
#seesaw = seesaw.Seesaw(i2c, 0x36)

# for channel in range(8):
#     if mplexer[channel].try_lock():
#         print(f"Channel {channel}:", end="")
#         addresses = mplexer[channel].scan()
#         print([hex(address) for address in addresses if address != 0x70])
#         mplexer[channel].unlock()

controllers=[]
controllers.append(Controller(seesaw.Seesaw(mplexer[0], addr=0x36), NeoKey1x4(mplexer[0], addr=0x30)))
controllers.append(Controller(seesaw.Seesaw(mplexer[7], addr=0x36), NeoKey1x4(mplexer[7], addr=0x30)))

for i, controller in enumerate(controllers):
    
    ### TODO: Breakout to function or class but here is "init rotary"
    seesaw_product = (controller.rotary.get_version() >> 16) & 0xFFFF
    print(f"Controller {i} : Found product {seesaw_product}")
    if seesaw_product != 4991:
        print("Wrong firmware loaded?  Expected 4991")

    # Configure seesaw pin used to read knob button presses
    # The internal pull up is enabled to prevent floating input
    controller.rotary.pin_mode(24, controller.rotary.INPUT_PULLUP)
    controller.rotary.button = digitalio.DigitalIO(controller.rotary, 24)
    controller.rotary.button_held = False
    controller.rotary.encoder = rotaryio.IncrementalEncoder(controller.rotary)
    controller.rotary.last_position = None


# socketHelper = SocketHelper()

while True:
    for i, controller in enumerate(controllers):
        # negate the position to make clockwise rotation positive
        position = -controller.rotary.encoder.position
        # TODO: Should be an interface or class that represents godots input event action (action, pressed and strength)
        # https://docs.godotengine.org/en/stable/classes/class_inputeventaction.html
        inputs = []

        if position != controller.rotary.last_position:
            shouldSend = True
            controller.rotary.last_position = position
            inputs.append({"Action": f"{i}_rotary_moved", "Strength": position })

        if not controller.rotary.button.value and not controller.rotary.button_held:
            shouldSend = True
            controller.rotary.button_held = True
            controller.neokey.pixels[0] = 0xFF0000
            inputs.append({ "Action": f"{i}_rotary_pressed", "Pressed": True })

        if controller.rotary.button.value and controller.rotary.button_held:
            shouldSend = True
            controller.rotary.button_held = False
            controller.neokey.pixels[0] = 0x0
            inputs.append({ "Action": f"{i}_rotary_released", "Pressed": True })
        
        if len(inputs) > 0:
            # socketHelper.sendMessage(json.dumps(inputs, default=lambda o: o.__dict__))
            print(inputs)

