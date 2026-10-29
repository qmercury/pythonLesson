"""05 | 입력 검증과 예외 처리가 있는 사칙연산 계산기."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Mini Calculator")
root.geometry("360x290")
outer = ttk.Frame(root, padding=20)
outer.pack(fill="both", expand=True)

ttk.Label(outer, text="첫 번째 숫자").pack()
first = ttk.Entry(outer)
first.pack(fill="x")
ttk.Label(outer, text="두 번째 숫자").pack(pady=(10, 0))
second = ttk.Entry(outer)
second.pack(fill="x")
answer = ttk.Label(outer, text="결과가 여기에 나타납니다.")
answer.pack(pady=16)

def calculate(operator):
    try:
        a, b = float(first.get()), float(second.get())
        if operator == "+":
            value = a + b
        elif operator == "-":
            value = a - b
        elif operator == "×":
            value = a * b
        else:
            if b == 0:
                raise ZeroDivisionError
            value = a / b
        answer.config(text=f"결과: {value:g}")
    except ValueError:
        answer.config(text="숫자를 정확히 입력하세요.")
    except ZeroDivisionError:
        answer.config(text="0으로 나눌 수 없습니다.")

buttons = ttk.Frame(outer)
buttons.pack()
for op in ["+", "-", "×", "÷"]:
    ttk.Button(buttons, text=op, width=5,
               command=lambda choice=op: calculate(choice)).pack(
                   side="left", padx=3
               )
root.mainloop()
