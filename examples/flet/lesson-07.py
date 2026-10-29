"""07 | 메뉴와 두 화면을 오가는 퀴즈 앱."""
import flet as ft

def main(page: ft.Page):
    page.title = "Two Screens"
    score = 0

    def home():
        page.controls.clear()
        page.add(
            ft.Text("나의 게임 메뉴", size=28),
            ft.Text(f"현재 점수: {score}"),
            ft.Button("퀴즈 시작", on_click=lambda e: quiz()),
        )

    def quiz():
        page.controls.clear()
        page.add(
            ft.Text("문제: 3 + 4 = ?", size=24),
            ft.Button("7", on_click=lambda e: answer(True)),
            ft.Button("8", on_click=lambda e: answer(False)),
            ft.Button("메뉴로", on_click=lambda e: home()),
        )

    def answer(correct):
        nonlocal score
        if correct:
            score += 1
        page.controls.clear()
        page.add(
            ft.Text("정답입니다!" if correct else "다시 도전해 보세요!", size=23),
            ft.Text(f"점수: {score}"),
            ft.Button("메뉴로 돌아가기", on_click=lambda e: home()),
        )

    home()

if __name__ == "__main__":
    ft.run(main)
