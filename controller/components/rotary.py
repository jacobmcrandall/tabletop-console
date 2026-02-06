from adafruit_seesaw import digitalio, neopixel, rotaryio, seesaw

class Rotary():
    def __init__(self, playerIndex: int, bus, addr=0x36):
        adaRotary = seesaw.Seesaw(bus, addr=0x36)
        seesaw_product = (adaRotary.get_version() >> 16) & 0xFFFF
        print(f"Controller {playerIndex} : Found product {seesaw_product}")
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        # Configure seesaw pin used to read knob button presses
        # The internal pull up is enabled to prevent floating input
        adaRotary.pin_mode(24, adaRotary.INPUT_PULLUP)
        adaRotary.button = digitalio.DigitalIO(adaRotary, 24)
        adaRotary.button_held = False
        adaRotary.encoder = rotaryio.IncrementalEncoder(adaRotary)
        adaRotary.last_position = None

        self.playerIndex = playerIndex
        self.rotary = adaRotary
        self.pixel = neopixel.NeoPixel(adaRotary, 6, 1)

    def getActions(self):
        # negate the position to make clockwise rotation positive
        position = -self.rotary.encoder.position
        inputs = []

        if position != self.rotary.last_position:
            self.rotary.last_position = position
            inputs.append({"Action": f"{self.playerIndex}_rotary_moved", "Strength": position })

        if not self.rotary.button.value and not self.rotary.button_held:
            self.rotary.button_held = True
            inputs.append({ "Action": f"{self.playerIndex}_rotary_pressed", "Pressed": True })

        if self.rotary.button.value and self.rotary.button_held:
            self.rotary.button_held = False
            inputs.append({ "Action": f"{self.playerIndex}_rotary_released", "Pressed": True })
        
        return inputs

    def setColor(self, color=(0,0,0), brightness=1.0):
        self.pixel.brightness = brightness
        self.pixel.fill(color)