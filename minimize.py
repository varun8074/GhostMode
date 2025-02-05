import pygetwindow as gw
import keyboard
import pythoncom  # Import for COM initialization
import psutil
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Applications to keep open (case-insensitive)
EXCLUDED_APPS = ["Google Chrome", "Visual Studio Code", "Code"]
# Applications to close (case-insensitive)
CLOSE_APPS = ["BlockedIn"]

def minimize_all_windows():
    windows = gw.getWindowsWithTitle("")
    for window in windows:
        if not window.isMinimized and not any(app.lower() in window.title.lower() for app in EXCLUDED_APPS):
            window.minimize()
    mute_system_volume()  # Mute the sound
    close_specified_apps()  # Close specific apps

def mute_system_volume():
    pythoncom.CoInitialize()  # Initialize COM before using pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)  # Mute the sound

def close_specified_apps():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if any(app.lower() in process.info['name'].lower() for app in CLOSE_APPS):
                os.kill(process.info['pid'], 9)  # Forcefully terminate the process
                print(f"Closed {process.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Set a hotkey (change 'numlock' to any key you prefer)
keyboard.add_hotkey("numlock", minimize_all_windows)

print("Press Num Lock to minimize all windows (except Chrome & VS Code), mute sound, and close specified apps. Press ESC to exit.")
keyboard.wait("esc")  # Keeps the script running until ESC is pressed
