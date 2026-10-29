"""08 | 가상 전방 거리센서: 물체가 앞에 있으면 경고해요."""
import turtle

screen = turtle.Screen()
screen.setup(650, 480)
screen.title("08 - Virtual Sensor")
robot = turtle.Turtle(shape="turtle")
robot.color("blue")
robot.penup()
obstacles = [(130, 80), (-130, 80), (50, -130)]
for x, y in obstacles:
    obj = turtle.Turtle(shape="circle")
    obj.penup()
    obj.color("red")
    obj.shapesize(2)
    obj.goto(x, y)

message = turtle.Turtle()
message.hideturtle()
message.penup()
message.goto(-290, 190)

def scan():
    nearest = None
    for x, y in obstacles:
        distance = robot.distance(x, y)
        direction = robot.towards(x, y)
        diff = (direction - robot.heading() + 180) % 360 - 180
        if abs(diff) <= 30 and (nearest is None or distance < nearest):
            nearest = distance
    message.clear()
    if nearest is not None and nearest < 130:
        message.write(f"WARNING! {nearest:.0f} px",
                      font=("Arial", 18, "bold"))
    else:
        message.write("No obstacle ahead", font=("Arial", 16, "normal"))

def move(distance):
    robot.forward(distance)
    scan()

def turn(angle):
    robot.left(angle)
    scan()

screen.onkey(lambda: move(15), "Up")
screen.onkey(lambda: move(-15), "Down")
screen.onkey(lambda: turn(15), "Left")
screen.onkey(lambda: turn(-15), "Right")
scan()
screen.listen()
screen.mainloop()
