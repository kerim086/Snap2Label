from mss import mss
import keyboard

with mss() as sct:
    while True:
        if keyboard.is_pressed('ESC'):
            break

        screenshot = sct.grab(sct.monitors[0])