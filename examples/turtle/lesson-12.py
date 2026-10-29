"""12 | 최종 작품: 보물 3개를 모으는 게임 (R 키로 재시작)."""
import random
import turtle

screen = turtle.Screen()
screen.setup(650, 480)
screen.title("12 - Final Treasure Game")
robot = turtle.Turtle(shape="turtle")
robot.color("blue")
robot.penup()
target = turtle.Turtle(shape="circle")
target.color("orange")
target.penup()
status = turtle.Turtle()
status.hideturtle()
status.penup()
status.goto(-280, 195)
score = 0
finished = False

def place_target():
    target.goto(random.randint(-240, 240),
                random.randint(-150, 150))

def draw_status():
    status.clear()
    status.write(f"Treasures: {score} / 3  (R: Restart)",
                 font=("Arial", 17, "bold"))

def restart():
    global score, finished
    score = 0
    finished = False
    robot.home()
    target.showturtle()
    place_target()
    screen.title("12 - Final Treasure Game")
    draw_status()

def move(distance):
    global score, finished
    if finished:
        return
    previous = robot.position()
    robot.forward(distance)
    if abs(robot.xcor()) > 285 or abs(robot.ycor()) > 195:
        robot.goto(previous)
    if robot.distance(target) < 25:
        score += 1
        if score >= 3:
            finished = True
            target.hideturtle()
            screen.title("YOU WIN!")
        else:
            place_target()
        draw_status()

screen.onkey(lambda: move(20), "Up")
screen.onkey(lambda: move(-20), "Down")
screen.onkey(lambda: robot.left(15), "Left")
screen.onkey(lambda: robot.right(15), "Right")
screen.onkey(restart, "r")
screen.listen()
target.showturtle()
restart()
screen.mainloop()
