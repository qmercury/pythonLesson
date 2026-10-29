"""04 | Frame과 grid로 계산기 화면 설계 (기능은 다음 차시)."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Calculator Layout")
root.geometry("320x380")
frame = ttk.Frame(root, padding=16)
frame.pack(fill="both", expand=True)

display = ttk.Entry(frame, font=("Arial", 20), justify="right")
display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=10)

keys = [
    ["7", "8", "9", "+"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "×"],
    ["0", ".", "=", "÷"],
]
def press(key):
    display.insert("end", key)

for row, items in enumerate(keys, start=1):
    for col, key in enumerate(items):
        ttk.Button(frame, text=key, command=lambda k=key: press(k)).grid(
            row=row, column=col, sticky="nsew", padx=2, pady=2
        )
for col in range(4):
    frame.columnconfigure(col, weight=1)
for row in range(1, 5):
    frame.rowconfigure(row, weight=1)

# 미션: 화면 배치와 버튼 순서를 바꿔 보세요.
root.mainloop()
