from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from cleaner_core import load_room, start_position

room = load_room(level=1)
robot = start_position(room)
cleaned = {robot}
CELL = 55
root = tk.Tk()
root.title('로보타그램 청소 로봇 관제')
canvas = tk.Canvas(root, width=len(room[0]) * CELL, height=len(room) * CELL)
canvas.pack(padx=12, pady=12)
status = tk.Label(root, text='청소 지도')
status.pack(pady=(0, 12))

# 여기에 코드를 작성하세요.

root.mainloop()
