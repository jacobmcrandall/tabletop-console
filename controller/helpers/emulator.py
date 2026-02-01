from pynput import mouse
from pynput import keyboard

class EmulatedController:
    def __init__(self, playerIndex):
        self.actions = []
        self.scrollPosition = 0
        self.playerIndex = playerIndex
    
        klistener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        klistener.start()

        mlistener = mouse.Listener(
            on_scroll=self.on_scroll)
        mlistener.start()

    def getActions(self):
        retActions = self.actions.copy()
        self.actions = []
        return retActions

    def on_scroll(self, x, y, dx, dy, injected):
        self.scrollPosition = self.scrollPosition + dy
        self.actions.append({"Action": f"{self.playerIndex}_rotary_moved", "Strength": self.scrollPosition })

    def on_press(self, key, injected):
        if(key == keyboard.KeyCode.from_char('a')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_0_pressed", "Pressed": True })
        elif(key == keyboard.KeyCode.from_char('s')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_1_pressed", "Pressed": True })
        elif(key == keyboard.KeyCode.from_char('d')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_2_pressed", "Pressed": True })
        elif(key == keyboard.KeyCode.from_char('f')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_3_pressed", "Pressed": True })

    def on_release(self, key, injected):
        if(key == keyboard.KeyCode.from_char('a')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_0_pressed", "Pressed": False })
        elif(key == keyboard.KeyCode.from_char('s')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_1_pressed", "Pressed": False })
        elif(key == keyboard.KeyCode.from_char('d')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_2_pressed", "Pressed": False })
        elif(key == keyboard.KeyCode.from_char('f')):
            self.actions.append({"Action": f"{self.playerIndex}_fourkey_3_pressed", "Pressed": False })
