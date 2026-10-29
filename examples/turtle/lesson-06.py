"""06 | 빨간 벽에 들어가면 이전 위치로 되돌아가요."""
import turtle

screen = turtle.Screen()
screen.setup(650, 450)
screen.title("06 - Maze")
walls = [(-60, -40, 60, 40), (110, 30, 160, 160)]

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
for x1, y1, x2, y2 in walls:
    drawer.penup()
    drawer.goto(x1, y1)
    drawer.color("red")
    drawer.begin_fill()
    for x, y in [(x2, y1), (x2, y2), (x1, y2), (x1, y1)]:
        drawer.goto(x, y)
    drawer.end_fill()

robot = turtle.Turtle(shape="turtle")
robot.color("blue")
robot.penup()
robot.goto(-230, -130)

def move(distance):
    before = robot.position()
    robot.forward(distance)
    x, y = robot.position()
    hit = any(x1 <= x <= x2 and y1 <= y <= y2
              for x1, y1, x2, y2 in walls)
    if hit or abs(x) > 290 or abs(y) > 190:
        robot.goto(before)

screen.onkey(lambda: move(15), "Up")
screen.onkey(lambda: move(-15), "Down")
screen.onkey(lambda: robot.left(15), "Left")
screen.onkey(lambda: robot.right(15), "Right")
screen.listen()
screen.mainloop()
