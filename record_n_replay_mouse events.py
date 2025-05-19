import tkinter as tk
from tkinter import messagebox
from pynput import mouse
from pynput.mouse import Button, Controller
import threading
import time
import os

# File to save click positions
file_path = "click_positions.txt"

# Global listener variable
listener = None

# Mouse controller for replay
mouse_controller = Controller()

def start_recording():
    global listener
    if listener is not None:
        messagebox.showinfo("Info", "Already recording!")
        return

    def on_click(x, y, button, pressed):
        if pressed:
            with open(file_path, "a") as f:
                f.write(f"{x},{y}\n")
            print(f"Recorded click at ({x}, {y})")

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    messagebox.showinfo("Recording", "Click recording started!\nPress 'Stop Recording' when done.")

def stop_recording():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
        messagebox.showinfo("Stopped", "Click recording stopped.")
    else:
        messagebox.showinfo("Info", "No recording session running.")

def replay_clicks():
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "No click positions recorded yet.")
        return

    def replay():
        with open(file_path, "r") as f:
            positions = [tuple(map(int, line.strip().split(","))) for line in f.readlines()]

        if len(positions) < 3:
            messagebox.showinfo("Info", "Not enough recorded positions to replay (need at least 3).")
            return

        # Remove first and last clicks
        positions = positions[1:-1]

        messagebox.showinfo("Replay Starting", "Replaying clicks in 3 seconds...\nSwitch to the target window.")
        time.sleep(3)

        for pos in positions:
            x, y = pos
            mouse_controller.position = (x, y)
            time.sleep(0.5)
            mouse_controller.click(Button.left, 1)
            print(f"Clicked at ({x}, {y})")

        messagebox.showinfo("Done", "Finished replaying recorded clicks.")

    threading.Thread(target=replay).start()

def clear_recording():
    if os.path.exists(file_path):
        os.remove(file_path)
        messagebox.showinfo("Cleared", "Recorded clicks cleared.")

# GUI setup
window = tk.Tk()
window.title("Mouse Click Recorder & Replayer")
window.geometry("350x250")
window.resizable(False, False)

# Buttons
btn_start = tk.Button(window, text="Start Recording", command=start_recording, height=2, width=20, bg="#4CAF50", fg="white")
btn_start.pack(pady=10)

btn_stop = tk.Button(window, text="Stop Recording", command=stop_recording, height=2, width=20, bg="#f44336", fg="white")
btn_stop.pack(pady=10)

btn_replay = tk.Button(window, text="Replay Clicks", command=replay_clicks, height=2, width=20, bg="#2196F3", fg="white")
btn_replay.pack(pady=10)

btn_clear = tk.Button(window, text="Clear Recorded Clicks", command=clear_recording, height=2, width=20, bg="#9E9E9E", fg="white")
btn_clear.pack(pady=10)

# Run GUI
window.mainloop()
