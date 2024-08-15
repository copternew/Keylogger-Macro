import time
import pandas as pd
import pydirectinput
from pynput import keyboard
import threading

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
                pydirectinput.press(action_name)
            else:  # Special keys (e.g., 'enter', 'tab')
                if action_name == 'Key.enter':
                    pydirectinput.press('enter')
                elif action_name == 'Key.tab':
                    pydirectinput.press('tab')
                # Add more special keys as needed
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
