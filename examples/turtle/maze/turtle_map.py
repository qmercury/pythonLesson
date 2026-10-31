import math
import random
import time
import turtle

LEVELS = {
    1: {"cols": 5, "rows": 4, "cell": 86, "seed": 7},
    2: {"cols": 7, "rows": 5, "cell": 70, "seed": 11},
    3: {"cols": 9, "rows": 6, "cell": 62, "seed": 55},
}
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 690
WORLD = (-400, -300, 400, 300)
BODY_RADIUS = 8
WALL_WIDTH = 6
COLLISION_DISTANCE = BODY_RADIUS + WALL_WIDTH / 2
MOVE_UNIT = 3

_screen = None
_player = None
_status_pen = None
_walls = None
_segments = []
_left = _bottom = 0.0
_cols = _rows = _cell = 0
_goal = (0.0, 0.0)
_finished = False

_DIRS = (
    ("N", 0, 1, "S"),
    ("E", 1, 0, "W"),
    ("S", 0, -1, "N"),
    ("W", -1, 0, "E"),
)


def _create_maze(cols, rows, seed):
    walls = {(x, y): set("NESW") for x in range(cols) for y in range(rows)}
    rng = random.Random(seed)
    visited = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        neighbors = []
        for direction, dx, dy, reverse in _DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                neighbors.append((direction, reverse, nx, ny))
        if not neighbors:
            stack.pop()
            continue
        direction, reverse, nx, ny = rng.choice(neighbors)
        walls[(x, y)].remove(direction)
        walls[(nx, ny)].remove(reverse)
        visited.add((nx, ny))
        stack.append((nx, ny))
    return walls


def _pen(color, width=2):
    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.pencolor(color)
    pen.pensize(width)
    return pen


def _line(pen, x1, y1, x2, y2):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.goto(x2, y2)
    pen.penup()
    _segments.append((x1, y1, x2, y2))


def _show_status(message, color="#456e64"):
    _status_pen.clear()
    _status_pen.pencolor(color)
    _status_pen.goto(0, 246)
    _status_pen.write(message, align="center", font=("Arial", 14, "bold"))
    _screen.update()


def start(level=1):
    global _screen, _player, _status_pen, _walls, _segments
    global _left, _bottom, _cols, _rows, _cell, _goal, _finished

    if _screen is not None:
        raise RuntimeError("한 프로그램에서는 maze.start()를 한 번만 호출하세요.")
    if level not in LEVELS:
        raise ValueError("level은 1(쉬움), 2(보통), 3(도전) 중 하나입니다.")

    cfg = LEVELS[level]
    _cols, _rows, _cell = cfg["cols"], cfg["rows"], cfg["cell"]
    _walls = _create_maze(_cols, _rows, cfg["seed"])
    _segments = []
    _finished = False

    _screen = turtle.Screen()
    _screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    _screen.title("로보타그램 | Turtle Maze Mission")
    _screen.setworldcoordinates(*WORLD)
    _screen.bgcolor("#fbf8f1")
    _screen.tracer(0)

    _left = -_cols * _cell / 2
    _bottom = -_rows * _cell / 2
    right_edge = -_left
    top_edge = -_bottom

    background = _pen("#ece5d7")
    background.goto(_left, _bottom)
    background.pendown()
    background.fillcolor("#fffefb")
    background.begin_fill()
    for pt in ((right_edge, _bottom), (right_edge, top_edge),
               (_left, top_edge), (_left, _bottom)):
        background.goto(*pt)
    background.end_fill()
    background.penup()

    pen = _pen("#627589", WALL_WIDTH)
    for y in range(_rows):
        for x in range(_cols):
            x0, y0 = _left + x * _cell, _bottom + y * _cell
            x1, y1 = x0 + _cell, y0 + _cell
            closed = _walls[(x, y)]
            if "N" in closed:
                _line(pen, x0, y1, x1, y1)
            if "E" in closed:
                _line(pen, x1, y0, x1, y1)
            if y == 0 and "S" in closed:
                _line(pen, x0, y0, x1, y0)
            if x == 0 and "W" in closed:
                _line(pen, x0, y0, x0, y1)

    start_x, start_y = _left + _cell / 2, _bottom + _cell / 2
    _goal = (_left + (_cols - 0.5) * _cell,
             _bottom + (_rows - 0.5) * _cell)

    decoration = _pen("#568275")
    decoration.goto(start_x, start_y)
    decoration.dot(35, "#bce0ce")
    decoration.goto(start_x, start_y - 22)
    decoration.write("START", align="center", font=("Arial", 9, "bold"))
    decoration.goto(*_goal)
    decoration.dot(40, "#ffe3a0")
    decoration.goto(_goal[0], _goal[1] - 5)
    decoration.write("GOAL", align="center", font=("Arial", 10, "bold"))
    decoration.goto(0, -250)
    decoration.pencolor("#63707a")
    decoration.write(
        "전진 / 후진 / 왼쪽 / 오른쪽으로 길을 찾으세요. 벽은 통과할 수 없어요!",
        align="center", font=("Arial", 12, "normal"))
    decoration.goto(0, 274)
    decoration.write("ROBOTTagram  •  Turtle Maze", align="center",
                     font=("Arial", 15, "bold"))

    _status_pen = _pen("#456e64")
    _player = turtle.Turtle(shape="turtle")
    _player.color("#298c79")
    _player.shape("turtle")
    _player.shapesize(1.0)
    _player.speed(0)
    _player.pensize(3)
    _player.penup()
    _player.goto(start_x, start_y)
    _player.setheading(0)
    _player.pendown()

    _show_status(f"LEVEL {level} · START에서 GOAL까지 이동하세요!")
    print(f"[Turtle Maze] {level}단계 시작 / 한 칸 = {_cell}")
    print("벽을 만나면 더 움직이지 않습니다. 게임 창은 코드 실행 중 열려 있습니다.")
    return _cell


def _ensure_started():
    if _screen is None:
        raise RuntimeError("먼저 STEP = maze.start(level=1)을 실행하세요.")


def _distance_to_wall(x, y, seg):
    x1, y1, x2, y2 = seg
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(x - x1, y - y1)
    t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    px, py = x1 + t * dx, y1 + t * dy
    return math.hypot(x - px, y - py)


def _blocked(x, y):
    return any(_distance_to_wall(x, y, seg) <= COLLISION_DISTANCE
               for seg in _segments)


def _move(distance):
    _ensure_started()
    global _finished
    if _finished:
        return False
    if not isinstance(distance, (int, float)) or not math.isfinite(distance):
        raise ValueError("이동 거리는 숫자로 입력해야 합니다.")
    if abs(distance) > 1200:
        raise ValueError("한 번에 이동할 수 있는 거리는 최대 1200입니다.")

    remaining = abs(distance)
    sign = 1 if distance >= 0 else -1
    moved = False
    while remaining > 0:
        step = min(MOVE_UNIT, remaining)
        rad = math.radians(_player.heading())
        nx = _player.xcor() + sign * step * math.cos(rad)
        ny = _player.ycor() + sign * step * math.sin(rad)
        if _blocked(nx, ny):
            _show_status("벽에 닿았어요! 다른 길로 이동해 보세요.", "#b06c5f")
            print("[벽 충돌] 방향을 바꾸거나 다른 길을 찾아보세요.")
            return False
        _player.goto(nx, ny)
        _screen.update()
        time.sleep(0.004)
        moved = True
        remaining -= step
        if math.dist((nx, ny), _goal) < 13:
            _player.goto(*_goal)
            _finished = True
            _player.color("#e6a545")
            _show_status("미션 성공! GOAL에 도착했습니다!", "#347b68")
            print("[성공] 목표 지점에 도착했습니다!")
            return True

    if moved:
        _show_status("이동 중... GOAL을 찾아보세요.")
    return True


def wall_ahead(distance=None):
    _ensure_started()
    if distance is None:
        distance = _cell
    if (not isinstance(distance, (int, float)) or
            not math.isfinite(distance) or distance <= 0 or distance > 1200):
        raise ValueError("검사 거리는 0보다 크고 1200 이하인 숫자여야 합니다.")

    angle = math.radians(_player.heading())
    dx, dy = math.cos(angle), math.sin(angle)
    x, y = _player.xcor(), _player.ycor()
    steps = math.ceil(distance / MOVE_UNIT)
    for i in range(1, steps + 1):
        look = min(i * MOVE_UNIT, distance)
        if _blocked(x + look * dx, y + look * dy):
            return True
    return False


def heading():
    _ensure_started()
    return _player.heading()


def forward(distance):
    return _move(distance)


def backward(distance):
    return _move(-distance)


def left(angle):
    _ensure_started()
    if not _finished:
        _player.left(angle)
        _screen.update()


def right(angle):
    _ensure_started()
    if not _finished:
        _player.right(angle)
        _screen.update()


def position():
    _ensure_started()
    return (round(_player.xcor(), 1), round(_player.ycor(), 1))


def is_finished():
    _ensure_started()
    return _finished


def done():
    _ensure_started()
    _screen.mainloop()
