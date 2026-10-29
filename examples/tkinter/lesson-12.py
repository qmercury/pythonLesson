"""12 | 최종 앱: 추가·삭제·저장·불러오기 되는 할 일 목록."""
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

FILE = Path(__file__).with_name("lesson-12-tasks.json")
root = tk.Tk()
root.title("My Tasks")
root.geometry("430x390")
ttk.Label(root, text="나의 할 일 관리", font=("Arial", 19, "bold")).pack(pady=13)
entry = ttk.Entry(root, width=40)
entry.pack(pady=3)
items = tk.Listbox(root, width=45, height=11)
items.pack(pady=10)
tasks = []

def refresh():
    items.delete(0, "end")
    for task in tasks:
        items.insert("end", task)

def add():
    value = entry.get().strip()
    if value:
        tasks.append(value)
        entry.delete(0, "end")
        refresh()

def remove():
    selected = items.curselection()
    if selected:
        tasks.pop(selected[0])
        refresh()

def save():
    try:
        FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2),
                        encoding="utf-8")
        messagebox.showinfo("저장", "할 일 목록을 저장했습니다.")
    except OSError:
        messagebox.showerror("오류", "파일을 저장할 수 없습니다.")

def load():
    if not FILE.exists():
        messagebox.showinfo("안내", "저장된 목록이 없습니다.")
        return
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
            raise ValueError
    except (OSError, ValueError, json.JSONDecodeError):
        messagebox.showerror("오류", "목록 파일을 읽을 수 없습니다.")
        return
    tasks[:] = data
    refresh()

buttons = ttk.Frame(root)
buttons.pack()
for title, action in [("추가", add), ("삭제", remove),
                      ("저장", save), ("불러오기", load)]:
    ttk.Button(buttons, text=title, command=action).pack(side="left", padx=3)
root.mainloop()
