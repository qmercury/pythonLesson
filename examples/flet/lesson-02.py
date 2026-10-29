"""02 | 버튼 이벤트로 점수를 바꾸는 카운터."""
import flet as ft

def main(page: ft.Page):
    page.title = "Score Counter"
    count = 0
    score = ft.Text("0", size=42)

    def change(amount):
        nonlocal count
        count = max(0, count + amount)
        score.value = str(count)
        page.update()

    def reset(e):
        nonlocal count
        count = 0
        score.value = "0"
        page.update()

    page.add(
        ft.Text("점수판", size=25),
        score,
        ft.Row([
            ft.Button("+1", on_click=lambda e: change(1)),
            ft.Button("-1", on_click=lambda e: change(-1)),
            ft.Button("초기화", on_click=reset),
        ]),
    )

if __name__ == "__main__":
    ft.run(main)
