"""09 | 명령 목록을 읽어 자동으로 이동하는 가상 로봇."""
import turtle

screen = turtle.Screen()
screen.title("09 - Auto Drive")
robot = turtle.Turtle(shape="turtle")
robot.color("blue")
robot.speed(3)

# (이동 거리, 회전 각도): 왼쪽 회전은 양수
commands = [(100, 90), (100, -90), (80, -90),
            (60, 90), (70, 0)]
index = 0

def next_command():
    global index
    if index >= len(commands):
        screen.title("09 - Mission Complete")
        return
    distance, angle = commands[index]
    robot.forward(distance)
    robot.left(angle)
    index += 1
    screen.ontimer(next_command, 400)

screen.ontimer(next_command, 500)
screen.mainloop()
