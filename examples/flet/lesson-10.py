"""10 | 모바일 화면 크기에 따라 달라지는 반응형 카드."""
import flet as ft

def main(page: ft.Page):
    page.title = "Responsive Mobile Test"
    page.add(
        ft.Text("휴대폰에서 레이아웃 확인", size=24),
        ft.Text("창 폭을 줄이거나 휴대폰에서 실행해 보세요."),
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Text(f"미션 {i}", size=20),
                    padding=18,
                    bgcolor=ft.Colors.BLUE_100 if i % 2 else ft.Colors.GREEN_100,
                    col={"xs": 12, "md": 6},
                )
                for i in range(1, 5)
            ],
            spacing=10,
            run_spacing=10,
        ),
    )

if __name__ == "__main__":
    ft.run(main)
