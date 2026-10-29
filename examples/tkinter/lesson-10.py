"""10 | 경기 기록을 CSV 파일에 저장하고 다시 불러와요."""
import csv
from pathlib import Path
import tkinter as tk
from tkinter import ttk

FILE = Path(__file__).with_name("lesson-10-records.csv")
root = tk.Tk()
root.title("Match Records")
root.geometry("480x400")
entry_frame = ttk.Frame(root, padding=12)
entry_frame.pack()
name = ttk.Entry(entry_frame, width=16)
name.insert(0, "Team A")
name.pack(side="left", padx=4)
record = ttk.Entry(entry_frame, width=12)
record.insert(0, "12.5")
record.pack(side="left", padx=4)
status = ttk.Label(root, text="가상의 팀 이름과 기록만 사용하세요.")
status.pack()
table = ttk.Treeview(root, columns=("team", "time"), show="headings")
table.heading("team", text="팀")
table.heading("time", text="기록(초)")
table.pack(fill="both", expand=True, padx=12, pady=10)
records = []

def refresh():
    for item in table.get_children():
        table.delete(item)
    for team, seconds in records:
        table.insert("", "end", values=(team, seconds))

def add():
    team = name.get().strip()
    try:
        seconds = float(record.get())
        if not team or seconds < 0:
            raise ValueError
    except ValueError:
        status.config(text="팀 이름과 0 이상의 숫자를 입력하세요.")
        return
    records.append((team, f"{seconds:.2f}"))
    status.config(text=f"{team} 기록 추가 완료")
    refresh()

def save():
    with FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["team", "seconds"])
        writer.writerows(records)
    status.config(text=f"저장: {FILE.name}")

def load():
    if not FILE.exists():
        status.config(text="저장된 파일이 없습니다.")
        return
    try:
        with FILE.open(newline="", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))
        loaded = [(row[0], row[1]) for row in rows[1:] if len(row) >= 2]
    except (OSError, UnicodeError, csv.Error):
        status.config(text="CSV 파일을 읽지 못했습니다.")
        return
    records[:] = loaded
    refresh()
    status.config(text="불러오기 완료")

buttons = ttk.Frame(root)
buttons.pack(pady=10)
for caption, action in [("추가", add), ("저장", save), ("불러오기", load)]:
    ttk.Button(buttons, text=caption, command=action).pack(side="left", padx=5)
root.mainloop()
