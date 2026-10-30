"""MQTT 4~9차시: 수신 PC의 로봇 게이트웨이 시뮬레이터.

실제 모터는 제어하지 않습니다. Tkinter Canvas의 파란 로봇만 움직입니다.
수신 메시지는 MQTT 네트워크 스레드에서 UI 스레드로 안전하게 전달합니다.
실제 EV3/SPIKE 연결은 별도 하드웨어 어댑터 구현/검증 후 사용하세요.
"""
# [데이터 흐름] MQTT cmd 구독 → 메시지 검사 → Canvas 이동 → MQTT status 발행
# 실제 EV3/SPIKE 모터는 연결하지 않는 교육용 가상 로봇입니다.
from collections import deque
import math
import json
import os
import queue
import tkinter as tk
from tkinter import ttk

import paho.mqtt.client as mqtt
# '명령 생성'이 아니라 '명령 해석과 검증'을 담당하는 수신 측입니다.
from protocol import parse_command, status_payload, topic

# 조종기 A와 동일한 HOST/ROOM/ROBOT 설정을 사용합니다.
HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
ROBOT = os.getenv("MQTT_ROBOT", "robot01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
# cmd: B가 듣는 채널 / status: B가 처리 결과를 보내는 채널.
CMD = topic(ROOM, ROBOT, "cmd")
STATUS = topic(ROOM, ROBOT, "status")
# Paho callback은 UI가 아닌 네트워크 스레드에서 실행됩니다.
# Tkinter UI 작업은 메인 스레드로 전달합니다.
events = queue.Queue()
# MQTT QoS 1은 동일 메시지가 다시 올 수 있습니다.
# 최근 128개의 id를 보관해 중복 실행을 막습니다(교육용 메모리 목록).
seen = deque(maxlen=128)
connected = False


# 연결/재연결 때마다 cmd 토픽을 다시 구독합니다.
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        events.put(("connected", False))
    else:
        client.subscribe(CMD, qos=1)
        events.put(("connected", True))


def on_disconnect(client, userdata, flags, reason_code, properties):
    events.put(("connected", False))


# 받은 데이터는 여기에서 곧바로 Canvas에 그리지 않습니다.
# 메인 스레드의 process_events()가 해석하도록 메모함에 넣습니다.
def on_message(client, userdata, message):
    events.put(("command", message.payload))


# Paho 2.x VERSION2: 콜백 인자 형식이 일관됩니다.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# [가상 로봇 GUI] Tkinter로 좌표 평면을 만듭니다.
root = tk.Tk()
root.title("학생 B - MQTT 로봇 수신 시뮬레이터")
root.geometry("550x425")
connection = ttk.Label(root, text="MQTT 연결 중...")
connection.pack(pady=6)
canvas = tk.Canvas(root, width=500, height=300, bg="white")
canvas.pack(pady=8)
canvas.create_rectangle(10, 10, 490, 290, outline="gray", width=2)
# 파란 삼각형이 가상 로봇입니다. 방향을 알 수 있도록 삼각형 사용.
robot_id = canvas.create_polygon(250, 130, 239, 162, 261, 162,
                                 fill="royalblue")
# 실제 EV3의 센티미터와 무관한 'Canvas 픽셀 좌표'입니다.
robot_x, robot_y, heading = 250.0, 150.0, 90.0  # 처음에는 화면 위를 바라봄

# [그래픽 함수] 위치와 각도를 이용해 삼각형 꼭짓점 좌표를 계산합니다.
# Canvas에서는 y가 아래쪽으로 커지므로 sin 부분에 -가 붙습니다.
def redraw_robot():
    # math.sin/cos는 라디안 각도를 받으므로 degrees → radians 변환.
    angle = math.radians(heading)
    tip = (robot_x + 18 * math.cos(angle),
           robot_y - 18 * math.sin(angle))
    left = (robot_x + 13 * math.cos(angle + 2.5),
            robot_y - 13 * math.sin(angle + 2.5))
    right = (robot_x + 13 * math.cos(angle - 2.5),
             robot_y - 13 * math.sin(angle - 2.5))
    canvas.coords(robot_id, *(tip + left + right))
last = ttk.Label(root, text="명령 대기 중")
last.pack()
ttk.Label(root, text="로봇이 실제로 움직이지 않는 안전한 연습입니다.").pack()


# [왕복 통신] 명령 처리 결과를 status 채널로 알려줍니다.
def publish_status(state, detail):
    if connected:
        client.publish(STATUS, status_payload(state, detail),
                       qos=0, retain=False)


# [핵심 함수] MQTT에서 전달한 메시지를 검사하고 '가상 로봇'에 적용.
def simulate(message):
    global robot_x, robot_y, heading
    try:
        # JSON 형식·허용 동작·시간·속도를 검사. 유효하지 않으면 오류 발생.
        data = parse_command(message)
        # 이전에 처리한 id라면 로봇이 중복으로 움직이지 않도록 건너뜁니다.
        if data["id"] in seen:
            return  # QoS 1 중복 전달을 무시
        seen.append(data["id"])
    except ValueError as exc:
        last.config(text=f"거부됨: {exc}")
        publish_status("rejected", str(exc))
        return

    # 여기까지 왔다면 검증을 통과한 명령입니다.
    action = data["action"]
    # 회전은 현재 방향(heading)을 바꾸고, 이동은 위치(x, y)를 바꿉니다.
    if action in ("left", "right"):
        heading += 30 if action == "left" else -30
    elif action in ("forward", "backward"):
        direction = 1 if action == "forward" else -1
        angle = math.radians(heading)
        new_x = robot_x + direction * 20 * math.cos(angle)
        new_y = robot_y - direction * 20 * math.sin(angle)
        # 화면 밖으로 나가지 않도록 간단한 경계 검사를 합니다.
        if 30 <= new_x <= 470 and 30 <= new_y <= 270:
            robot_x, robot_y = new_x, new_y
    # 변경된 방향/좌표로 파란 삼각형을 다시 그립니다.
    redraw_robot()
    last.config(text=f"시뮬레이션: {action} / {data['duration_ms']}ms")
    # '실제 모터 완료'가 아니라 '시뮬레이션 처리'라고 회신합니다.
    publish_status("simulated", action)


# [UI 이벤트 루프] queue의 수신 자료를 Tkinter 메인 스레드에서 처리.
def process_events():
    global connected
    try:
        while True:
            kind, data = events.get_nowait()
            if kind == "connected":
                connected = data
                connection.config(text="MQTT 연결됨" if data else "MQTT 연결 끊김")
                # 송신 측에 시뮬레이터가 준비되었음을 알립니다.
                if data:
                    publish_status("ready", "simulation gateway online")
            elif kind == "command":
                simulate(data)
    except queue.Empty:
        pass
    # 창을 막지 않고 50ms 뒤 다시 확인합니다.
    root.after(50, process_events)


# 수신기 종료 후 브로커 연결을 정상적으로 정리합니다.
def close():
    publish_status("offline", "gateway closing")
    client.disconnect()
    client.loop_stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)
# Paho 네트워크 연결 시작. 실제 접속 완료는 on_connect 콜백에서 확인.
client.connect_async(HOST, PORT, keepalive=30)
client.loop_start()
process_events()
# 화면이 열린 동안 Tkinter 버튼/화면 이벤트가 작동합니다.
root.mainloop()
