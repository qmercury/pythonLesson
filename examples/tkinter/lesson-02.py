"""02 | 버튼 클릭 카운터: 함수와 이벤트 연결."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Click Counter")
root.geometry("320x260")
score = tk.IntVar(value=0)

def add():
    score.set(score.get() + 1)

def subtract():
    score.set(max(0, score.get() - 1))

def reset():
    score.set(0)

ttk.Label(root, text="클릭 카운터", font=("Arial", 18)).pack(pady=15)
ttk.Label(root, textvariable=score, font=("Arial", 35)).pack()
ttk.Button(root, text="+1", command=add).pack(pady=3)
ttk.Button(root, text="-1", command=subtract).pack(pady=3)
ttk.Button(root, text="초기화", command=reset).pack(pady=3)
root.mainloop()
