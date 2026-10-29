"""04 | Row, Column, Container로 나의 소개 화면 꾸미기."""
import flet as ft

def main(page: ft.Page):
    page.title = "My Profile"
    page.add(
        ft.Column([
            ft.Text("나의 프로필", size=27),
            ft.Container(
                content=ft.Column([
                    ft.Text("별명: 코딩탐험가", size=18),
                    ft.Text("좋아하는 것: 로봇, 게임, 그림"),
                ]),
                padding=18,
                bgcolor=ft.Colors.BLUE_50,
            ),
            ft.Row([
                ft.Container(content=ft.Text("Python"), padding=12,
                             bgcolor=ft.Colors.GREEN_100),
                ft.Container(content=ft.Text("Robotics"), padding=12,
                             bgcolor=ft.Colors.AMBER_100),
            ]),
        ])
    )

if __name__ == "__main__":
    ft.run(main)
