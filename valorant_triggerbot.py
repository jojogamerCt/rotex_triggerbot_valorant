import time
import win32api
import win32con
import keyboard
import numpy as np
import os
from mss import mss
import winsound

def get_pixel_color(x, y):
    screen_image = mss().grab({"left": x, "top": y, "width": 1, "height": 1})
    pixel = screen_image.pixel(0, 0)
    return pixel[0], pixel[1], pixel[2]

def is_purple_color(rgb, purple_min, purple_max):
    r, g, b = rgb
    return (purple_min[0] <= r <= purple_max[0]) and (purple_min[1] <= g <= purple_max[1]) and (purple_min[2] <= b <= purple_max[2])

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def play_sound(freq=440, duration=100):
    try:
        winsound.Beep(freq, duration)
    except Exception as e:
        print(f"Error playing sound: {e}")

def save_config(config_file, toggle_key, delay):
    with open(config_file, "w") as file:
        file.write(f"{toggle_key}\n")
        file.write(f"{delay}\n")

def load_config(config_file):
    default_toggle_key = "t"
    default_delay = 0.1
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                toggle_key = lines[0].strip()
                delay = float(lines[1].strip())
                return toggle_key, delay
    return default_toggle_key, default_delay

def triggerbot(toggle_key='t', delay=0.1):
    toggle_flag = False

    # Define the range for detecting purple color (adjust these values as needed)
    purple_min = (60, 0, 60)  # Minimum threshold for purple color (R, G, B)
    purple_max = (255, 100, 255)  # Maximum threshold for purple color (R, G, B)

    while True:
        if keyboard.is_pressed(toggle_key):
            toggle_flag = not toggle_flag
            play_sound(500 if toggle_flag else 300)  # Play different frequencies for activate/deactivate
            time.sleep(0.2)  # Debounce delay to prevent multiple toggles in quick succession

        if toggle_flag:
            try:
                cursor_x, cursor_y = win32api.GetCursorPos()
                pixel_color = get_pixel_color(cursor_x, cursor_y)

                if is_purple_color(pixel_color, purple_min, purple_max):
                    left_click()

            except Exception as e:
                print(f"Error during triggerbot execution: {e}")

        time.sleep(delay)

if __name__ == "__main__":
    print(r'''
       ____        __          
      / __ \____ _/ /____  _  __
     / /_/ / __ `/ __/ _ \| |/_/
    / _, _/ /_/ / /_/  __/>  <  
   /_/ |_|\__,_/\__/\___/_/|_|  
                                
    ''')

    print("Welcome to the Rotex TriggerBot!")
    print("The TriggerBot will automatically shoot when the cursor is near a purple character in the game.")
    
    config_file = "config.txt"
    toggle_key, delay = load_config(config_file)

    print(f"Loaded config: Toggle key: {toggle_key}, Delay: {delay}")

    update_config = input("Do you want to update the settings? (y/n): ")
    if update_config.lower() == "y":
        toggle_key = input("Enter the key to toggle the Rotex TriggerBot (default is 't'): ")
        delay = float(input("Enter the delay for the Rotex TriggerBot (in seconds, default is 0.1): "))
        save_config(config_file, toggle_key, delay)

    print(f"Press the toggle key '{toggle_key.upper()}' to start the Rotex TriggerBot.")
    time.sleep(2)  # Pause for a moment before starting

    triggerbot(toggle_key, delay)
