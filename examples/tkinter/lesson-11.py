"""11 | 자유 프로젝트 시작 코드: 간단한 할 일 목록 앱."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("My Project - Tasks")
root.geometry("420x340")
title = ttk.Label(root, text="나의 할 일", font=("Arial", 18))
title.pack(pady=12)
entry = ttk.Entry(root, width=36)
entry.pack()
tasks = tk.Listbox(root, width=45, height=9)
tasks.pack(pady=10)
status = ttk.Label(root, text="할 일을 추가하세요.")
status.pack()

def add_task():
    value = entry.get().strip()
    if value:
        tasks.insert("end", value)
        entry.delete(0, "end")
        status.config(text="할 일을 추가했습니다.")
    else:
        status.config(text="내용을 먼저 입력하세요.")

ttk.Button(root, text="추가", command=add_task).pack()
# TODO 1: 선택한 항목 삭제 버튼 만들기
# TODO 2: 완료 표시 기능 만들기
# TODO 3: 프로그램 종료 후에도 남는 저장 기능 만들기
root.mainloop()
