"""01 | 화면 속 거북이 로봇: 반복문으로 정다각형을 그려요."""
import turtle

screen = turtle.Screen()
screen.title("01 - Polygon Robot")
robot = turtle.Turtle()
robot.shape("turtle")
robot.color("royalblue")
robot.speed(3)

sides = 4       # 바꿔 보기: 3, 5, 6
length = 100
for _ in range(sides):
    robot.forward(length)
    robot.left(360 / sides)

screen.mainloop()
