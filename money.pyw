import tkinter as tk
from tkinter import ttk
from pynput import mouse, keyboard
import threading
import time

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Auto Clicker")

        self.click_rate = 0.1
        #Just like OP Auto Clicker, it uses F6
        self.toggle_hotkey = "f6"  
        self.clicking = False
        self.spam_keys = []
        self.spamming = False
        self.mouse_button = mouse.Button.left

        #cleaned up UI buttons/grids
        self.rate_label = ttk.Label(root, text="Input Send Rate (seconds, can be less than 1):")
        #WARNING! Below 0.006, clicking may cause lag on your machine or diminishing returns
        self.rate_label.grid(row=0, column=0, sticky="w")
        self.rate_entry = ttk.Entry(root)
        self.rate_entry.grid(row=0, column=1)
        self.rate_entry.insert(0, str(self.click_rate))
        self.rate_entry.bind("<KeyRelease>", self.update_rate)

        self.mode_label = ttk.Label(root, text="Input type:")
        self.mode_label.grid(row=2, column=0, sticky="w")
        self.mode = tk.StringVar(value="click")
        self.click_radio = ttk.Radiobutton(root, text="Click", variable=self.mode, value="click")
        self.click_radio.grid(row=2, column=1, sticky="w")
        self.spam_radio = ttk.Radiobutton(root, text="Spam KB input:", variable=self.mode, value="spam")
        self.spam_radio.grid(row=2, column=2, sticky="w")

        self.spam_display = ttk.Label(root, text="None")
        self.spam_display.grid(row=3, column=1, sticky="w")
        self.spam_button = ttk.Button(root, text="Record KB inputs", command=self.set_spam_keys)
        self.spam_button.grid(row=3, column=2)

        self.mouse_label = ttk.Label(root, text="Mouse Button:")
        self.mouse_label.grid(row=4, column=0, sticky="w")
        self.mouse_var = tk.StringVar(value="left")
        self.left_radio = ttk.Radiobutton(root, text="Left", variable=self.mouse_var, value="left")
        self.left_radio.grid(row=4, column=1, sticky="w")
        self.right_radio = ttk.Radiobutton(root, text="Right", variable=self.mouse_var, value="right")
        self.right_radio.grid(row=4, column=2, sticky="w")
        self.middle_radio = ttk.Radiobutton(root, text="Scroll", variable=self.mouse_var, value="middle")
        self.middle_radio.grid(row=5, column=1, sticky="w")
        self.mouse_var.trace("w", self.update_mouse_button)

        self.status_label = ttk.Label(root, text="Off")
        self.status_label.grid(row=6, column=0, columnspan=3)

        self.toggle_button = ttk.Button(root, text="Toggle", command=self.toggle)
        self.toggle_button.grid(row=7, column=0, columnspan=3)

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.action_thread = None

    def update_rate(self, event):
        try:
            rate = float(self.rate_entry.get())
            if rate <= 0:
                raise ValueSet
            self.click_rate = rate
        except ValueSet:
            self.click_rate = 0.1
            self.status_label.config(text="Custom rate set.")

    def set_spam_keys(self):
        self.status_label.config(text="Press keys (Esc to finish combo)...")
        self.spam_keys = []
        self.root.bind("<KeyPress>", self.record_spam_keys)

    def record_spam_keys(self, event):
        if event.keysym == "Escape":
            self.spam_display.config(text="+".join(self.spam_keys))
            self.status_label.config(text="Combo recorded")
            self.root.unbind("<KeyPress>")
        else:
            if event.keysym == "space":
                self.spam_keys.append(" ")
            # We're treating Shift_L and Shift_R as "Shift" so that it works, not in all games though for some reason
            elif event.keysym == "Shift_L" or event.keysym == "Shift_R":
                self.spam_keys.append("Shift")
            else:
                if event.keysym not in self.spam_keys:
                    self.spam_keys.append(event.keysym)

    def update_mouse_button(self, *args):
        self.mouse_button = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle
        }.get(self.mouse_var.get(), mouse.Button.left)

    def on_press(self, key):
        try:
            key_str = getattr(key, 'char', None) or getattr(key, 'name', None) or str(key).strip('Key.')
            if key_str.lower() == self.toggle_hotkey:
                self.root.after(0, self.toggle)
        except Exception as e:
            print(f"There was an error that occured when we tried starting to spam: {e}")

    def click_action(self):
        controller = mouse.Controller()
        while self.clicking:
            controller.click(self.mouse_button)
            time.sleep(self.click_rate)

    def spam_action(self):
        controller = keyboard.Controller()
        while self.spamming and self.spam_keys:
            for key_name in self.spam_keys:
                try:
                    if key_name == " ":
                        controller.press(keyboard.Key.space)
                        controller.release(keyboard.Key.space)
                    elif key_name == "Shift":
                        controller.press(keyboard.Key.shift)
                        controller.release(keyboard.Key.shift)
                    elif hasattr(keyboard.Key, key_name.lower()):
                        controller.press(getattr(keyboard.Key, key_name.lower()))
                        controller.release(getattr(keyboard.Key, key_name.lower()))
                    else:
                        controller.press(key_name)
                        controller.release(key_name)
                except Exception as e:
                    print(f"Failed to press {key_name}: {e}")
            time.sleep(self.click_rate)

    def toggle(self):
        #Block originally for error handling, was kinda fucked up, now just tells if it's a "safe" method or not, not helpful at all
        if self.mode.get() == "click":
            self.clicking = not self.clicking
            if self.clicking:
                self.status_label.config(text="Active with generally stable input method")
                self.action_thread = threading.Thread(target=self.click_action)
                self.action_thread.start()
            else:
                self.status_label.config(text="Off")
        elif self.mode.get() == "spam":
            self.spamming = not self.spamming
            if self.spamming and self.spam_keys:
                self.status_label.config(text="Active with possible unstable performance")
                self.action_thread = threading.Thread(target=self.spam_action)
                self.action_thread.start()
            else:
                self.status_label.config(text="Off")

    def on_close(self):
        self.clicking = False
        self.spamming = False
        if self.listener:
            self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
