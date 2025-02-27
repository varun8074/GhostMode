from pynput.keyboard import Listener

# Initialize the count for the 'a' key
key_count = 0

# Define the function to handle key press events
def on_press(key):
    global key_count
    try:
        # Check if the pressed key is 'a'
        if key.char == 'a':
            key_count += 1
            print(f"'a' key pressed {key_count} times")
    except AttributeError:
        # Handle special keys (like shift, control, etc.)
        pass

# Define the function to handle key release events (optional)
def on_release(key):
    if key == 'esc':  # Stop listener if 'esc' is pressed
        return False

# Set up the listener to monitor keyboard input
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
