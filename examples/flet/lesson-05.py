"""05 | 입력 검증이 있는 두 숫자 계산기."""
import flet as ft

def main(page: ft.Page):
    page.title = "Mini Calculator"
    a = ft.TextField(label="첫 번째 숫자", width=230)
    b = ft.TextField(label="두 번째 숫자", width=230)
    result = ft.Text("두 수를 입력하세요.", size=17)

    def calculate(op):
        try:
            x, y = float(a.value), float(b.value)
            if op == "+":
                value = x + y
            elif op == "-":
                value = x - y
            elif op == "×":
                value = x * y
            else:
                if y == 0:
                    raise ZeroDivisionError
                value = x / y
            result.value = f"결과: {value:g}"
        except (ValueError, TypeError):
            result.value = "숫자를 정확하게 입력하세요."
        except ZeroDivisionError:
            result.value = "0으로 나눌 수 없습니다."
        page.update()

    page.add(
        ft.Text("사칙연산 계산기", size=24),
        a, b,
        ft.Row([
            ft.Button(op, on_click=lambda e, choice=op: calculate(choice))
            for op in ["+", "-", "×", "÷"]
        ]),
        result,
    )

if __name__ == "__main__":
    ft.run(main)
