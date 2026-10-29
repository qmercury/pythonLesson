"""03 | 이름과 점수를 입력받아 결과를 보여줘요."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Input Practice")
root.geometry("380x280")

ttk.Label(root, text="이름(별명)").pack(pady=(20, 0))
name = ttk.Entry(root)
name.pack()
ttk.Label(root, text="목표 점수").pack(pady=(12, 0))
target = ttk.Entry(root)
target.pack()
result = ttk.Label(root, text="값을 입력하고 확인을 누르세요.")
result.pack(pady=18)

def show():
    nickname = name.get().strip()
    try:
        value = int(target.get())
        if not nickname or value < 0:
            raise ValueError
        result.config(text=f"{nickname}님의 목표는 {value}점!")
    except ValueError:
        result.config(text="이름과 0 이상의 정수를 입력하세요.")

ttk.Button(root, text="확인", command=show).pack()
root.mainloop()
