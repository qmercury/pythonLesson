"""11 | 자유 프로젝트 출발 코드: 목적지에 도착하면 성공!"""
import turtle

screen = turtle.Screen()
screen.setup(600, 450)
screen.title("11 - My Robot Project")
robot = turtle.Turtle(shape="turtle")
robot.color("blue")
robot.penup()
robot.goto(-200, -100)
goal = turtle.Turtle(shape="circle")
goal.color("green")
goal.penup()
goal.goto(180, 100)
finished = False

def move(distance):
    global finished
    if finished:
        return
    robot.forward(distance)
    if robot.distance(goal) < 25:
        finished = True
        screen.title("MISSION SUCCESS!")

screen.onkey(lambda: move(20), "Up")
screen.onkey(lambda: move(-20), "Down")
screen.onkey(lambda: robot.left(15), "Left")
screen.onkey(lambda: robot.right(15), "Right")
screen.listen()

# TODO 1: 장애물을 추가하세요.
# TODO 2: 점수나 제한 시간을 추가하세요.
# TODO 3: 직접 생각한 새로운 기능을 만드세요.
screen.mainloop()
