"""Turtle 미로용 로봇 모양 (위에서 내려다본 2륜 로봇).

기본 Turtle 기능만 사용하므로 별도 이미지 파일이 필요하지 않습니다.
로봇의 앞쪽은 오른쪽(0도)이며, 회전하면 그림도 함께 회전합니다.
"""
import turtle


def register_robot_shape(screen, name="maze_robot"):
    """Turtle 화면에 로봇 모양을 등록하고 모양 이름을 반환합니다."""
    shape = turtle.Shape("compound")

    # 몸체 위/아래에 있는 바퀴
    upper_wheel = [(-10, 9), (10, 9), (10, 14), (-10, 14)]
    lower_wheel = [(-10, -14), (10, -14), (10, -9), (-10, -9)]
    shape.addcomponent(upper_wheel, "#334355", "#334355")
    shape.addcomponent(lower_wheel, "#334355", "#334355")

    # 로봇 몸체
    body = [(-13, -9), (13, -9), (13, 9), (-13, 9)]
    shape.addcomponent(body, "#74b4de", "#305675")

    # 주황색 부분이 앞쪽
    front = [(13, -5), (19, -5), (19, 5), (13, 5)]
    shape.addcomponent(front, "#f5a66b", "#ae643c")

    screen.register_shape(name, shape)
    return name
