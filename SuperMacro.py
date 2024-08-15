import time
import pandas as pd
import ctypes
from pynput import keyboard
import threading

# Virtual Key Codes
VK_CODES = {
    'enter': 0x0D,
    'tab': 0x09,
    # Add more special keys as needed
}

def press_key(hex_key_code):
    """ Simulate a key press using ctypes """
    ctypes.windll.user32.keybd_event(hex_key_code, 0, 0, 0)  # Key down
    time.sleep(0.05)  # Small delay to simulate real key press
    ctypes.windll.user32.keybd_event(hex_key_code, 0, 2, 0)  # Key up

# Load the recorded actions from the CSV file
df = pd.read_csv("keylog.csv")

# Global flag to control the macro execution
macro_running = False
macro_thread = None
macro_lock = threading.Lock()  # Add a lock for safe access to macro_running

def run_macro():
    global macro_running

    for index, row in df.iterrows():
        with macro_lock:
            if not macro_running:
                print("Macro stopped.")
                break  # Stop the loop if macro_running is False

        # Simulate the action
        action_name = row["Action Name"]
        delay = row["Delay to Next Action (ms)"] / 1000  # Convert delay to seconds

        # Simulate typing the key
        try:
            if len(action_name) == 1:  # Regular character
                hex_key_code = ord(action_name.upper())
                press_key(hex_key_code)
            else:  # Special keys
                if action_name == 'Key.enter':
                    hex_key_code = VK_CODES['enter']
                elif action_name == 'Key.tab':
                    hex_key_code = VK_CODES['tab']
                else:
                    # Add more special keys as needed
                    continue
                press_key(hex_key_code)
            print(f"Executed: {action_name}")
        except Exception as e:
            print(f"Failed to execute key: {action_name} with error {e}")

        # Wait for the specified delay before the next action
        time.sleep(delay)

def on_press(key):
    global macro_running, macro_thread

    if key == keyboard.Key.f1:
        with macro_lock:
            if not macro_running:
                print("F1 pressed. Starting macro.")
                macro_running = True
                macro_thread = threading.Thread(target=run_macro)
                macro_thread.start()

    elif key == keyboard.Key.f2:
        with macro_lock:
            if macro_running:
                print("F2 pressed. Stopping macro.")
                macro_running = False

    if key == keyboard.Key.esc:
        print("Esc key pressed. Exiting.")
        with macro_lock:
            macro_running = False
        if macro_thread is not None:
            macro_thread.join()  # Ensure the macro thread has finished
        return False  # Stop listener

# Start the listener to monitor F1 and F2 keys
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Script exited.")
