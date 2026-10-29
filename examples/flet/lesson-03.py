"""03 | 입력창에 입력한 이름으로 인사하는 앱."""
import flet as ft

def main(page: ft.Page):
    page.title = "Greeting App"
    name = ft.TextField(label="별명", width=260)
    result = ft.Text("이름을 입력해 보세요.", size=18)

    def greet(e):
        text = (name.value or "").strip()
        result.value = f"안녕하세요, {text}님!" if text else "별명을 입력하세요."
        page.update()

    page.add(
        ft.Text("인사말 생성기", size=24),
        name,
        ft.Button("인사하기", on_click=greet),
        result,
    )

if __name__ == "__main__":
    ft.run(main)
