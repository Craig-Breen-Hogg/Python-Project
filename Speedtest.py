
import tkinter as tk
import time
import random

# Sample texts
texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing speed tests are a great way to improve your skills.",
    "Practice makes perfect when it comes to typing fast and accurately."
]

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("600x400")
        
        self.sample_text = random.choice(texts)
        self.start_time = None
        
        # Widgets
        self.label_text = tk.Label(root, text=self.sample_text, wraplength=500, font=("Arial", 14))
        self.label_text.pack(pady=20)
        
        self.entry = tk.Entry(root, width=60, font=("Arial", 14))
        self.entry.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start Test", command=self.start_test, font=("Arial", 12))
        self.start_button.pack(pady=10)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
    def start_test(self):
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.start_time = time.time()
        self.start_button.config(text="Finish Test", command=self.finish_test)
        
    def finish_test(self):
        end_time = time.time()
        typed_text = self.entry.get()
        elapsed_time = end_time - self.start_time
        
        word_count = len(typed_text.split())
        wpm = round((word_count / elapsed_time) * 60)
        
        self.result_label.config(text=f"Your typing speed: {wpm} WPM")
        self.start_button.config(text="Start Test", command=self.start_test)

# Run the app
root = tk.Tk()
app = TypingSpeedTest(root)
root.mainloop()
