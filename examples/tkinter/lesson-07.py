"""07 | after()로 화면이 멈추지 않는 스톱워치 만들기."""
import time
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Stopwatch")
root.geometry("350x250")
label = ttk.Label(root, text="0.0 s", font=("Arial", 36, "bold"))
label.pack(pady=30)
running = False
elapsed = 0.0
started_at = 0.0

def refresh():
    if running:
        label.config(text=f"{elapsed + time.monotonic() - started_at:.1f} s")
    root.after(100, refresh)

def start():
    global running, started_at
    if not running:
        running = True
        started_at = time.monotonic()

def pause():
    global running, elapsed
    if running:
        elapsed += time.monotonic() - started_at
        running = False

def reset():
    global elapsed, running
    running = False
    elapsed = 0.0
    label.config(text="0.0 s")

buttons = ttk.Frame(root)
buttons.pack()
for text, action in [("시작", start), ("일시정지", pause), ("초기화", reset)]:
    ttk.Button(buttons, text=text, command=action).pack(side="left", padx=4)
refresh()
root.mainloop()
