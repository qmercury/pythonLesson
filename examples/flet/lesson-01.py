"""01 | 첫 Flet 앱: Python으로 화면에 글자를 표시해요."""
import flet as ft

def main(page: ft.Page):
    page.title = "My First Flet App"
    page.add(
        ft.Text("안녕하세요!", size=30),
        ft.Text("로보타그램 Python 앱 수업입니다."),
        ft.Text("미션: 글자와 크기를 변경해 보세요.", size=15),
    )

if __name__ == "__main__":
    ft.run(main)
