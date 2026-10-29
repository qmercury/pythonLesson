"""02 | 같은 도형을 반복 회전하여 패턴 아트를 만들어요."""
import turtle

screen = turtle.Screen()
screen.title("02 - Pattern Art")
pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)
colors = ["red", "orange", "green", "blue", "purple"]

for step in range(36):
    pen.pencolor(colors[step % len(colors)])
    for _ in range(4):
        pen.forward(110)
        pen.left(90)
    pen.left(10)  # 도전: 10을 15나 20으로 바꿔 보세요.

pen.hideturtle()
screen.mainloop()
