"""09 | 방향키로 장애물을 피해 초록 목표까지 이동하기."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Maze Game")
canvas = tk.Canvas(root, width=480, height=320, bg="white")
canvas.pack(padx=10, pady=10)
wall = canvas.create_rectangle(200, 80, 280, 250, fill="tomato")
goal = canvas.create_oval(405, 255, 445, 295, fill="limegreen")
player = canvas.create_oval(35, 35, 65, 65, fill="royalblue")
message = ttk.Label(root, text="방향키로 목표에 도착하세요!")
message.pack()
finished = False

def overlap(a, b):
    return not (a[2] <= b[0] or a[0] >= b[2]
                or a[3] <= b[1] or a[1] >= b[3])

def move(event):
    global finished
    if finished:
        return
    moves = {"Up": (0, -15), "Down": (0, 15),
             "Left": (-15, 0), "Right": (15, 0)}
    dx, dy = moves[event.keysym]
    before = canvas.coords(player)
    canvas.move(player, dx, dy)
    now = canvas.coords(player)
    blocked = (now[0] < 0 or now[1] < 0 or
               now[2] > 480 or now[3] > 320 or
               overlap(now, canvas.coords(wall)))
    if blocked:
        canvas.coords(player, *before)
    elif overlap(now, canvas.coords(goal)):
        finished = True
        message.config(text="MISSION SUCCESS!")

for key in ("Up", "Down", "Left", "Right"):
    root.bind(f"<{key}>", move)
root.mainloop()
