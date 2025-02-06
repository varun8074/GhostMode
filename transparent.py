import ctypes
import pygetwindow as gw
from pywinauto import Application
import time

def set_window_transparency(window_title, transparency):
    try:
        # Ensure the exact window title is found
        all_titles = gw.getAllTitles()
        if window_title not in all_titles:
            print(f"Window with title '{window_title}' not found. Available titles: {all_titles}")
            return

        print(f"Found window with title: {window_title}")

        # Connect to the application using the 'win32' backend
        app = Application(backend="win32").connect(title=window_title)

        # Get the window object
        window = app.window(title=window_title)

        # Bring the window to the foreground and restore if minimized
        if window.is_minimized():
            window.restore()
        window.set_focus()  # Make sure the window is active

        # Get the window handle (HWND)
        hwnd = window.handle

        # Set the window to be a layered window with transparency support
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x80000 | 0x20)  # Enable WS_EX_LAYERED and WS_EX_TOPMOST

        # Set transparency (0.0 = fully transparent, 1.0 = fully opaque)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, int(transparency * 255), 2)

        print(f"Transparency of '{window_title}' set to {transparency * 100}%")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
window_title = "Blocked In"  # Update with your desired window title
set_window_transparency(window_title, 0.1)  # Set transparency to 50%

# Wait for a moment to observe the result
time.sleep(5)
