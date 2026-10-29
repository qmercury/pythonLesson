"""04 | 방향키로 조종하는 거북이 로봇."""
import turtle

screen = turtle.Screen()
screen.setup(600, 450)
screen.title("04 - Keyboard Robot")
robot = turtle.Turtle()
robot.shape("turtle")
robot.color("blue")
robot.penup()

def move(distance):
    before = robot.position()
    robot.forward(distance)
    if abs(robot.xcor()) > 270 or abs(robot.ycor()) > 190:
        robot.goto(before)  # 화면 밖이면 이동 취소

screen.onkey(lambda: move(20), "Up")
screen.onkey(lambda: move(-20), "Down")
screen.onkey(lambda: robot.left(15), "Left")
screen.onkey(lambda: robot.right(15), "Right")
screen.listen()
screen.mainloop()
