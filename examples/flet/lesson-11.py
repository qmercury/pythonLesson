"""11 | 자유 프로젝트 시작 코드: 로봇축구 점수판."""
import flet as ft

def main(page: ft.Page):
    page.title = "Robot Soccer Scoreboard"
    scores = {"Blue": 0, "Red": 0}
    blue = ft.Text("0", size=36)
    red = ft.Text("0", size=36)

    def add(team):
        scores[team] += 1
        blue.value = str(scores["Blue"])
        red.value = str(scores["Red"])
        page.update()

    def reset(e):
        scores["Blue"] = 0
        scores["Red"] = 0
        blue.value, red.value = "0", "0"
        page.update()

    page.add(
        ft.Text("로봇축구 점수판", size=26),
        ft.Row([
            ft.Column([ft.Text("BLUE"), blue,
                       ft.Button("+1", on_click=lambda e: add("Blue"))]),
            ft.Column([ft.Text("RED"), red,
                       ft.Button("+1", on_click=lambda e: add("Red"))]),
        ]),
        ft.Button("초기화", on_click=reset),
    )
    # TODO: 팀 이름 입력, 경기 타이머, 결과 저장 중 1개 추가하기

if __name__ == "__main__":
    ft.run(main)
