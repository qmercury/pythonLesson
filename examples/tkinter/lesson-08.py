"""08 | Canvas의 원을 버튼으로 움직여 가상 로봇 만들기."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Canvas Robot")
canvas = tk.Canvas(root, width=440, height=280, bg="white")
canvas.pack(padx=12, pady=12)
robot = canvas.create_oval(195, 115, 245, 165, fill="royalblue")
position = ttk.Label(root)
position.pack()

def move(dx, dy):
    x1, y1, x2, y2 = canvas.coords(robot)
    if 0 <= x1 + dx and x2 + dx <= 440 and 0 <= y1 + dy and y2 + dy <= 280:
        canvas.move(robot, dx, dy)
    x1, y1, x2, y2 = canvas.coords(robot)
    position.config(text=f"중심 좌표: ({(x1+x2)/2:.0f}, {(y1+y2)/2:.0f})")

buttons = ttk.Frame(root)
buttons.pack(pady=8)
for label, dx, dy in [("←", -20, 0), ("→", 20, 0),
                      ("↑", 0, -20), ("↓", 0, 20)]:
    ttk.Button(buttons, text=label,
               command=lambda a=dx, b=dy: move(a, b)).pack(side="left", padx=2)
move(0, 0)
root.mainloop()
