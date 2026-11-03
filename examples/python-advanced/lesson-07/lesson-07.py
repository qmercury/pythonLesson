from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from cleaner_core import load_room, start_position, floor_cells

room = load_room(level=1)
route = sorted(floor_cells(room), key=lambda p: (p[1], p[0]))
index = 0
running = False
root = tk.Tk()
root.title('자동 청소 상태 제어')
label = tk.Label(root, text='대기 중', font=('Arial', 17))
label.pack(padx=25, pady=20)

# 여기에 코드를 작성하세요.

root.mainloop()
