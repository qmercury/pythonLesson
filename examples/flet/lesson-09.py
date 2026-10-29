"""09 | SharedPreferences에 텍스트를 저장하고 다시 읽어요."""
import flet as ft

KEY = "robottagram.pythonlesson.note"

async def main(page: ft.Page):
    page.title = "Save and Load"
    note = ft.TextField(label="메모", multiline=True, min_lines=3, width=300)
    result = ft.Text("임의의 학습 메모만 사용하세요.")
    store = ft.SharedPreferences()

    async def save(e):
        await store.set(KEY, note.value or "")
        result.value = "기기에 저장했습니다."
        page.update()

    async def load(e):
        value = await store.get(KEY)
        note.value = value or ""
        result.value = "저장된 메모를 불러왔습니다."
        page.update()

    page.add(
        ft.Text("나의 메모 앱", size=25),
        note,
        ft.Row([
            ft.Button("저장", on_click=save),
            ft.Button("불러오기", on_click=load),
        ]),
        result,
    )

if __name__ == "__main__":
    ft.run(main)
