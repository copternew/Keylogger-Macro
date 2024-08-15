import csv
import time
from pynput import keyboard

# Initialize the previous press time
previous_press_time = None

# Open or create a CSV file and write the header
with open("keylog.csv", "w", newline="") as csvfile:
    fieldnames = ["Action Name", "Press Time (ms)", "Delay to Next Action (ms)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

def on_press(key):
    global previous_press_time

    # Get the current time in milliseconds when the key is pressed
    press_time = time.time() * 1000

    # Calculate the delay in milliseconds since the last key press
    if previous_press_time is not None:
        delay = press_time - previous_press_time
    else:
        delay = 0

    # Update previous_press_time to the current press time
    previous_press_time = press_time

    # Determine the action name
    try:
        action_name = key.char
    except AttributeError:
        action_name = str(key)

    # Write the action name, press time, and delay to the CSV file
    with open("keylog.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Action Name", "Press Time (ms)", "Delay to Next Action (ms)"])
        writer.writerow({"Action Name": action_name, "Press Time (ms)": int(press_time), "Delay to Next Action (ms)": int(delay)})

def on_release(key):
    if key == keyboard.Key.esc:
        print("Esc key pressed. Stopping the keylogger.")
        return False  # Stop the listener

# Start the keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("Keylogger stopped. CSV log file saved.")
