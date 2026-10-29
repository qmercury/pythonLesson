"""05 | 보물에 가까이 가면 점수가 올라가는 게임."""
import random
import turtle

screen = turtle.Screen()
screen.setup(600, 450)
screen.title("05 - Treasure Hunt")
robot = turtle.Turtle(shape="turtle")
robot.penup()
robot.color("blue")
treasure = turtle.Turtle(shape="circle")
treasure.penup()
treasure.color("gold")
treasure.goto(150, 100)
score = 0
board = turtle.Turtle()
board.hideturtle()
board.penup()
board.goto(-270, 175)

def move(distance):
    global score
    robot.forward(distance)
    if robot.distance(treasure) < 25:
        score += 1
        treasure.goto(random.randint(-220, 220),
                      random.randint(-150, 150))
    board.clear()
    board.write(f"Score: {score}", font=("Arial", 17, "bold"))

move(0)
screen.onkey(lambda: move(20), "Up")
screen.onkey(lambda: move(-20), "Down")
screen.onkey(lambda: robot.left(20), "Left")
screen.onkey(lambda: robot.right(20), "Right")
screen.listen()
screen.mainloop()
