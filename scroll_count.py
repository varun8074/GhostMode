from pynput.mouse import Listener

# Initialize the count for the scroll wheel
scroll_up_count = 0
scroll_down_count = 0

# Define the function to handle mouse scroll events
def on_scroll(x, y, dx, dy):
    global scroll_up_count, scroll_down_count
    
    if dy > 0:
        scroll_up_count += 1
        print(f"Scroll wheel moved up {scroll_up_count} times")
    elif dy < 0:
        scroll_down_count += 1
        print(f"Scroll wheel moved down {scroll_down_count} times")

# Set up the listener to monitor mouse input
with Listener(on_scroll=on_scroll) as listener:
    listener.join()
