from pynput import keyboard

class MyListener(keyboard.Listener):
    def __init__(self, state: dict[str, int], debug=False):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.state = state
        self._current_keys = set()
        self._debug = debug

    def on_press(self, key):
        self._current_keys.add(key)

        if key == keyboard.Key.left:
            self.state["direction"] = -1
        elif key == keyboard.Key.right:
            self.state["direction"] = 1

        if key == keyboard.Key.down:
            self.state["speed"] = 0
        elif key == keyboard.Key.up:
            self.state["speed"] = 1

        if self._debug:
            print(self.state, self._current_keys)

        if key == keyboard.Key.esc or self._current_keys.issuperset([keyboard.Key.ctrl_l, keyboard.KeyCode(char='c')]) or any([hasattr(key, 'char') and key.char == '\x03' for key in self._current_keys]):
            # Stop listener
            return False
        
    def on_release(self, key):
        self._current_keys.remove(key)

if __name__ == "__main__":
    state = {"direction": 1, "speed": 0}
    print("Running keyboard listener...") 
    with MyListener(state, debug=True) as listener:
        listener.join()

    
