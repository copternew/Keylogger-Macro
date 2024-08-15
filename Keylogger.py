import time
import pandas as pd
from pynput import keyboard
from pynput.keyboard import Controller
import threading

# Load the recorded actions from the CSV file
df = pd.read_csv("keylog.csv")

# Initialize the keyboard controller to simulate key presses
kb = Controller()

# Global flag to control the macro execution
macro_running = False
macro_thread = None

def run_macro():
    global macro_running

    for index, row in df.iterrows():
        if not macro_running:
            print("Macro stopped.")
            break  # Stop the loop if macro_running is False

        # Simulate the action
        action_name = row["Action Name"]
        delay = row["Delay to Next Action (ms)"] / 1000  # Convert delay to seconds

        # Simulate typing the key
        try:
            if len(action_name) == 1:  # Regular character
                kb.press(action_name)
                kb.release(action_name)
            else:  # Special keys (e.g., 'Key.enter')
                key = getattr(keyboard.Key, action_name.split(".")[1])
                kb.press(key)
                kb.release(key)
        except AttributeError:
            print(f"Unknown key: {action_name}")

        # Wait for the specified delay before the next action
        time.sleep(delay)

def on_press(key):
    global macro_running, macro_thread

    if key == keyboard.Key.f1:
        if not macro_running:
            print("F1 pressed. Starting macro.")
            macro_running = True
            macro_thread = threading.Thread(target=run_macro)
            macro_thread.start()

    elif key == keyboard.Key.f2:
        if macro_running:
            print("F2 pressed. Stopping macro.")
            macro_running = False
            if macro_thread is not None:
                macro_thread.join()  # Ensure the macro thread has finished

    if key == keyboard.Key.esc:
        print("Esc key pressed. Exiting.")
        macro_running = False
        if macro_thread is not None:
            macro_thread.join()  # Ensure the macro thread has finished
        return False  # Stop listener

# Start the listener to monitor F1 and F2 keys
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Script exited.")
