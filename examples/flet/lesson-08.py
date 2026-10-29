"""08 | 할 일을 추가하고 삭제하는 목록 앱."""
import flet as ft

def main(page: ft.Page):
    page.title = "My Tasks"
    tasks = []
    field = ft.TextField(label="할 일", width=240)
    area = ft.Column()
    summary = ft.Text()

    def render():
        area.controls = []
        for index, task in enumerate(tasks):
            area.controls.append(ft.Row([
                ft.Text(task),
                ft.Button("삭제", on_click=lambda e, i=index: remove(i)),
            ]))
        summary.value = f"할 일 {len(tasks)}개"
        page.update()

    def add(e):
        text = (field.value or "").strip()
        if text:
            tasks.append(text)
            field.value = ""
        render()

    def remove(index):
        tasks.pop(index)
        render()

    page.add(
        ft.Text("오늘의 할 일", size=25),
        ft.Row([field, ft.Button("추가", on_click=add)],
               wrap=True),
        summary,
        area,
    )
    render()

if __name__ == "__main__":
    ft.run(main)
