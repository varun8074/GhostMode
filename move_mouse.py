import pyautogui
import time

def move_mouse():
    # Move the mouse 10 pixels to the right and 10 pixels down from its current position
    pyautogui.move(1, 1)

while True:
    move_mouse()  # Move the mouse by a small amount
    time.sleep(2)  # Wait for 50 seconds before moving again
