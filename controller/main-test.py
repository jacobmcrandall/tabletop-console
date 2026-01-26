# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9548A to perform a simple scan for connected devices

import os
import json
import time

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

rotaries=[]
r1 = seesaw.Seesaw(mplexer[0], addr=0x36)
r2 = seesaw.Seesaw(mplexer[7], addr=0x36)
rotaries.append(r1)
rotaries.append(r2)

for i, rotary in enumerate(rotaries):
    
    ### TODO: Breakout to function or class but here is "init rotary"
    seesaw_product = (rotary.get_version() >> 16) & 0xFFFF
    print(f"Controller {i} : Found product {seesaw_product}")
    if seesaw_product != 4991:
        print("Wrong firmware loaded?  Expected 4991")

    # Configure seesaw pin used to read knob button presses
    # The internal pull up is enabled to prevent floating input
    rotary.pin_mode(24, rotary.INPUT_PULLUP)
    rotary.button = digitalio.DigitalIO(rotary, 24)
    rotary.button_held = False
    rotary.encoder = rotaryio.IncrementalEncoder(rotary)
    rotary.last_position = None

while True:
    # negate the position to make clockwise rotation positive
    position = -r1.encoder.position
    # TODO: Should be an interface or class that represents godots input event action (action, pressed and strength)
    # https://docs.godotengine.org/en/stable/classes/class_inputeventaction.html
    inputs = []

    if position != r1.last_position:
        shouldSend = True
        r1.last_position = position
        inputs.append({"Action": f"{i}_rotary_moved", "Strength": position })

    if not r1.button.value and not r1.button_held:
        shouldSend = True
        r1.button_held = True
        inputs.append({ "Action": f"{i}_rotary_pressed", "Pressed": True })

    if r1.button.value and r1.button_held:
        shouldSend = True
        r1.button_held = False
        inputs.append({ "Action": f"{i}_rotary_released", "Pressed": True })
    
    if len(inputs) > 0:
        print(inputs)
    # time.sleep(0.01)

mplexer[0].unlock();
