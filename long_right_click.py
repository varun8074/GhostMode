import time
from pynput import mouse, keyboard
import threading

# Time threshold for long press
HOLD_DURATION = 0.5

# Controllers
keyboard_controller = keyboard.Controller()
mouse_controller = mouse.Controller()

# Track press time and state
press_time = None
action_triggered = False

def monitor_hold():
    global press_time, action_triggered
    while True:
        if press_time and not action_triggered:
            if time.time() - press_time >= HOLD_DURATION:
                print("Hold time exceeded, performing Shift + Right-Click")
                action_triggered = True
                keyboard_controller.press(keyboard.Key.shift)
                time.sleep(0.05)
                mouse_controller.press(mouse.Button.right)
                mouse_controller.release(mouse.Button.right)
                time.sleep(0.05)
                keyboard_controller.release(keyboard.Key.shift)
        time.sleep(0.01)

def on_click(x, y, button, pressed):
    global press_time, action_triggered
    if button == mouse.Button.right:
        if pressed:
            press_time = time.time()
            action_triggered = False
        else:
            press_time = None
            action_triggered = False

# Start monitoring in a background thread
threading.Thread(target=monitor_hold, daemon=True).start()

# Start mouse listener
with mouse.Listener(on_click=on_click) as listener:
    print("Hold right-click to auto-perform Shift + Right-Click after 1 second...")
    listener.join()
