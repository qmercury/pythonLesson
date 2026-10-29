"""07 | 30초 동안 별(목표)을 모으며 점수를 얻어요."""
import random
import turtle

screen = turtle.Screen()
screen.setup(600, 450)
screen.title("07 - Timed Game")
robot = turtle.Turtle(shape="turtle")
robot.penup()
target = turtle.Turtle(shape="circle")
target.color("orange")
target.penup()
target.goto(100, 90)
status = turtle.Turtle()
status.hideturtle()
status.penup()
status.goto(-270, 180)
score = 0
remaining = 30

def draw_status():
    status.clear()
    status.write(f"Score: {score}     Time: {remaining}",
                 font=("Arial", 16, "bold"))

def move(distance):
    global score
    if remaining <= 0:
        return
    robot.forward(distance)
    if robot.distance(target) < 25:
        score += 1
        target.goto(random.randint(-240, 240),
                    random.randint(-150, 150))
    draw_status()

def tick():
    global remaining
    if remaining <= 0:
        screen.title(f"Game Over! Score: {score}")
        return
    remaining -= 1
    draw_status()
    screen.ontimer(tick, 1000)

draw_status()
screen.ontimer(tick, 1000)
screen.onkey(lambda: move(20), "Up")
screen.onkey(lambda: move(-20), "Down")
screen.onkey(lambda: robot.left(20), "Left")
screen.onkey(lambda: robot.right(20), "Right")
screen.listen()
screen.mainloop()
