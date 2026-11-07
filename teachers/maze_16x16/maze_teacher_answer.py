"""교사용 정답 예시 - 16x16 Turtle 미로 만들기.

학생용 qmercury/pyClass와 분리된 qmercury/pythonLesson의 교사용 예시.
주의: pythonLesson은 공개 저장소이므로 이 파일도 GitHub에서 누구나 열람할 수 있습니다.

학생 미션 정답 예시
1. 40x40 검은 벽 그리기
2. 벽의 '왼쪽 위 픽셀 좌표'를 set에 저장하기
3. for / if로 미로 만들기
4. STEP=40으로 로봇 이동하기
5. 이동 전에 벽과 경계 검사하기
"""

import turtle
from robot_shape import register_robot_shape

# ===== 기본 환경 (학생용과 동일) =====
GRID_SIZE = 16
CELL_SIZE = 40
STEP = CELL_SIZE
START_X = 0
START_Y = 0
MAZE_PIXELS = GRID_SIZE * CELL_SIZE  # 640

screen = turtle.Screen()
screen.setup(800, 800)
screen.title("16 x 16 Maze - TEACHER ANSWER")
screen.bgcolor("white")
screen.setworldcoordinates(0, 800, 800, 0)
screen.tracer(0)

grid = turtle.Turtle()
grid.hideturtle()
grid.speed(0)
grid.pencolor("lightgray")

for i in range(GRID_SIZE + 1):
    px = i * CELL_SIZE
    py = i * CELL_SIZE

    grid.penup()
    grid.goto(px, 0)
    grid.pendown()
    grid.goto(px, MAZE_PIXELS)

    grid.penup()
    grid.goto(0, py)
    grid.pendown()
    grid.goto(MAZE_PIXELS, py)

grid.penup()

register_robot_shape(screen)
robot = turtle.Turtle()
robot.shape("maze_robot")
robot.penup()
robot.speed(3)
robot.setheading(0)
robot.goto(20, 20)  # 시작 칸의 중앙

# 도착점 표시 (학생용에는 선택 사항)
goal = turtle.Turtle()
goal.hideturtle()
goal.penup()
goal.goto(620, 620)  # 마지막 칸의 중앙
goal.dot(18, "gold")

# ===== 미션 1, 2: 벽 그리기 + 벽 위치 저장 =====
wall_pen = turtle.Turtle()
wall_pen.hideturtle()
wall_pen.speed(0)
wall_pen.pencolor("black")
wall_pen.fillcolor("black")

# 격자 좌표가 아닌 '픽셀 좌표'를 저장합니다.
# 예: (120, 200)은 왼쪽 위가 (120, 200)인 40x40 벽을 뜻합니다.
walls = set()


def draw_wall(x, y):
    """픽셀 (x, y)를 왼쪽 위 모서리로 하는 40x40 벽을 그립니다."""
    if x % STEP != 0 or y % STEP != 0:
        raise ValueError("벽 좌표는 40픽셀의 배수여야 합니다.")
    if not (0 <= x < MAZE_PIXELS and 0 <= y < MAZE_PIXELS):
        raise ValueError("벽 좌표는 0~600픽셀 범위여야 합니다.")
    if (x, y) in ((0, 0), (600, 600)):
        raise ValueError("시작점과 도착점은 벽으로 만들 수 없습니다.")
    if (x, y) in walls:
        return  # 이미 벽이 있다면 중복으로 그리지 않음

    wall_pen.penup()
    wall_pen.goto(x, y)
    wall_pen.setheading(0)  # 오른쪽을 바라봄
    wall_pen.pendown()
    wall_pen.begin_fill()

    for _ in range(4):
        wall_pen.forward(CELL_SIZE)
        # Y가 아래쪽으로 증가하므로 화면상 시계방향으로 회전
        wall_pen.left(90)

    wall_pen.end_fill()
    wall_pen.penup()
    walls.add((x, y))


# ===== 미션 3: 반복문/조건문으로 미로 만들기 =====
# 세로 벽: x=120, y=0~480. 단, (120,240)은 통로로 남김
for row in range(13):
    if row != 6:
        draw_wall(120, row * STEP)

# 가로 벽: y=360, x=160~520. 단, (320,360)은 통로
for col in range(4, 14):
    if col != 8:
        draw_wall(col * STEP, 360)

# ===== 미션 4, 5: 40픽셀 이동 + 벽 충돌 검사 =====
def forward(step):
    """바라보는 방향으로 한 칸씩 이동. 벽/경계에서 멈추면 False."""
    if not isinstance(step, int) or step <= 0 or step % STEP != 0:
        raise ValueError("이동 거리는 STEP(40)의 양의 정수배여야 합니다.")

    # 현재 픽셀 좌표계에서 0=오른쪽, 90=아래, 180=왼쪽, 270=위
    vectors = {
        0: (1, 0),
        90: (0, 1),
        180: (-1, 0),
        270: (0, -1),
    }
    heading = round(robot.heading()) % 360
    if heading not in vectors:
        print("방향을 90도 단위로 맞추세요.")
        return False

    dx, dy = vectors[heading]

    for _ in range(step // STEP):
        next_x = round(robot.xcor()) + dx * STEP
        next_y = round(robot.ycor()) + dy * STEP

        # 로봇이 다음 칸의 중심을 벗어나는지 확인
        if not (20 <= next_x <= 620 and 20 <= next_y <= 620):
            print("이동 불가: 미로 바깥입니다.")
            return False

        # 다음 칸 중앙을 칸 왼쪽 위의 픽셀 좌표로 바꾸어 조회
        next_wall = (next_x - CELL_SIZE // 2, next_y - CELL_SIZE // 2)
        if next_wall in walls:
            print("이동 불가: 앞에 벽이 있습니다.", next_wall)
            return False

        robot.forward(STEP)

    return True


screen.update()
screen.tracer(1, 0)

# ===== 교사용 실행 예시 =====
# 현재 위치 (20,20)에서 오른쪽 두 칸 -> (100,20)
forward(STEP)
forward(STEP)

# 오른쪽 세 번째 칸은 (120,0) 벽이라 이동하지 않음
blocked = forward(STEP)
assert blocked is False

# 벽의 틈 (120,240), (320,360)을 통과해 도착점까지 이동
# Y가 아래로 증가하므로 left(90)은 화면에서 아래 방향 회전
robot.left(90)
for _ in range(6):
    assert forward(STEP)  # (100,260)으로 이동

robot.right(90)
for _ in range(6):
    assert forward(STEP)  # (340,260), 첫 번째 통로 통과

robot.left(90)
for _ in range(9):
    assert forward(STEP)  # (340,620), 두 번째 통로 통과

robot.right(90)
for _ in range(7):
    assert forward(STEP)  # (620,620), 도착

print("완료! 로봇 최종 픽셀 좌표:", robot.position())
print("저장된 벽 개수:", len(walls))
assert (round(robot.xcor()), round(robot.ycor())) == (620, 620)
assert len(walls) == 21

screen.mainloop()
