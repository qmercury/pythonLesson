"""12 | 최종 앱: 이름 입력, 점수판, 승리 팀 판정."""
import flet as ft

def main(page: ft.Page):
    page.title = "Final Soccer App"
    blue_score, red_score = 0, 0
    blue_name = ft.TextField(label="파란 팀", value="Blue", width=140)
    red_name = ft.TextField(label="빨간 팀", value="Red", width=140)
    board = ft.Text(size=23)
    result = ft.Text(size=18)

    def refresh():
        board.value = (f"{blue_name.value or 'Blue'} {blue_score} : "
                       f"{red_score} {red_name.value or 'Red'}")
        if blue_score > red_score:
            result.value = "파란 팀이 앞서고 있습니다."
        elif red_score > blue_score:
            result.value = "빨간 팀이 앞서고 있습니다."
        else:
            result.value = "현재 동점입니다."
        page.update()

    def add(team):
        nonlocal blue_score, red_score
        if team == "blue":
            blue_score += 1
        else:
            red_score += 1
        refresh()

    def reset(e):
        nonlocal blue_score, red_score
        blue_score = red_score = 0
        refresh()

    page.add(
        ft.Text("로봇축구 경기 관리", size=26),
        ft.Row([blue_name, red_name], wrap=True),
        board,
        ft.Row([
            ft.Button("파란 팀 +1", on_click=lambda e: add("blue")),
            ft.Button("빨간 팀 +1", on_click=lambda e: add("red")),
        ], wrap=True),
        ft.Button("점수 초기화", on_click=reset),
        result,
    )
    blue_name.on_change = lambda e: refresh()
    red_name.on_change = lambda e: refresh()
    refresh()

if __name__ == "__main__":
    ft.run(main)
