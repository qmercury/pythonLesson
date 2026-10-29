"""06 | 라디오 버튼으로 답하는 Python 퀴즈 앱."""
import flet as ft

questions = [
    ("반복문에 사용하는 키워드는?", ["for", "def", "print"], "for"),
    ("함수를 선언하는 키워드는?", ["if", "def", "else"], "def"),
    ("조건문에 사용하는 키워드는?", ["return", "if", "import"], "if"),
]

def main(page: ft.Page):
    page.title = "Python Quiz"
    index = 0
    score = 0
    title = ft.Text(size=22)
    feedback = ft.Text()
    choices = ft.RadioGroup(content=ft.Column())

    def render():
        question, answers, _ = questions[index]
        title.value = f"{index+1}. {question}"
        choices.value = None
        choices.content.controls = [
            ft.Radio(value=answer, label=answer) for answer in answers
        ]
        page.update()

    def submit(e):
        nonlocal index, score
        if not choices.value:
            feedback.value = "답을 선택하세요."
            page.update()
            return
        score += int(choices.value == questions[index][2])
        index += 1
        if index == len(questions):
            title.value = f"완료! {score} / {len(questions)}점"
            choices.visible = False
            button.disabled = True
            feedback.value = "잘했어요!"
            page.update()
            return
        feedback.value = f"현재 점수: {score}"
        render()

    button = ft.Button("제출", on_click=submit)
    page.add(title, choices, button, feedback)
    render()

if __name__ == "__main__":
    ft.run(main)
