"""10 | BFS로 격자 미로의 최단 경로를 찾아 애니메이션해요."""
from collections import deque
import turtle

screen = turtle.Screen()
screen.setup(600, 470)
screen.title("10 - Shortest Path")
screen.tracer(0)
width, height, unit = 8, 6, 45
walls = {(2, 0), (2, 1), (2, 2), (4, 2), (4, 3), (5, 3)}
start, goal = (0, 0), (7, 5)

def place(cell):
    x, y = cell
    return (-160 + x * unit, -110 + y * unit)

painter = turtle.Turtle()
painter.hideturtle()
painter.penup()
for x in range(width):
    for y in range(height):
        painter.goto(*place((x, y)))
        painter.dot(30, "firebrick" if (x, y) in walls else "lightgray")
painter.goto(*place(goal))
painter.dot(30, "green")

def shortest_path():
    queue = deque([start])
    previous = {start: None}
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for nxt in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            nx, ny = nxt
            if (0 <= nx < width and 0 <= ny < height
                    and nxt not in walls and nxt not in previous):
                previous[nxt] = (x, y)
                queue.append(nxt)
    if goal not in previous:
        return []
    path = []
    cursor = goal
    while cursor is not None:
        path.append(cursor)
        cursor = previous[cursor]
    return list(reversed(path))

route = shortest_path()
robot = turtle.Turtle(shape="turtle")
robot.color("blue")
robot.penup()
robot.goto(*place(start))
screen.update()

def animate(step=0):
    if step >= len(route):
        screen.title(f"Complete: {len(route)-1} moves")
        return
    robot.goto(*place(route[step]))
    screen.update()
    screen.ontimer(lambda: animate(step + 1), 300)

animate()
screen.mainloop()
