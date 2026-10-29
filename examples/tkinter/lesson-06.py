"""06 | Radiobutton으로 선택하는 3문제 퀴즈."""
import tkinter as tk
from tkinter import ttk

questions = [
    ("Python의 반복문은?", ["for", "print", "def"], 0),
    ("조건을 검사하는 명령은?", ["while", "if", "return"], 1),
    ("함수를 만들 때 쓰는 키워드는?", ["class", "def", "import"], 1),
]
root = tk.Tk()
root.title("Python Quiz")
root.geometry("430x320")
current = 0
score = 0
choice = tk.IntVar(value=-1)
title = ttk.Label(root, font=("Arial", 16), wraplength=390)
title.pack(pady=18)
options = ttk.Frame(root)
options.pack()
result = ttk.Label(root)
result.pack(pady=12)

def show_question():
    choice.set(-1)
    for child in options.winfo_children():
        child.destroy()
    question, answers, _ = questions[current]
    title.config(text=f"{current+1}. {question}")
    for number, answer in enumerate(answers):
        ttk.Radiobutton(options, text=answer, variable=choice,
                        value=number).pack(anchor="w")

def submit():
    global current, score
    if choice.get() == -1:
        result.config(text="답을 먼저 선택하세요.")
        return
    if choice.get() == questions[current][2]:
        score += 1
    current += 1
    if current == len(questions):
        title.config(text=f"퀴즈 끝! {score} / {len(questions)}점")
        for child in options.winfo_children():
            child.destroy()
        submit_button.config(state="disabled")
        result.config(text="수고했어요!")
    else:
        result.config(text=f"현재 점수: {score}")
        show_question()

submit_button = ttk.Button(root, text="정답 제출", command=submit)
submit_button.pack()
show_question()
root.mainloop()
