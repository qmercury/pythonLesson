"""01 | 나의 첫 GUI 자기소개 앱."""
import tkinter as tk

root = tk.Tk()
root.title("My First App")
root.geometry("480x320")
root.configure(bg="#EAF4FF")

tk.Label(root, text="안녕하세요!", font=("Arial", 25, "bold"),
         fg="#1455A0", bg="#EAF4FF").pack(pady=30)
tk.Label(root, text="로보타그램 Python 수업입니다.",
         font=("Arial", 15), bg="#EAF4FF").pack(pady=10)
tk.Label(root, text="좋아하는 것: 로봇, 게임, 코딩",
         font=("Arial", 13), bg="#EAF4FF").pack(pady=10)

# 미션: 제목, 색상, 소개 문구를 나만의 내용으로 바꿔 보세요.
root.mainloop()
