"""MQTT 4~9차시: 수신 PC의 로봇 게이트웨이 시뮬레이터.

실제 모터는 제어하지 않습니다. Tkinter Canvas의 파란 로봇만 움직입니다.
수신 메시지는 MQTT 네트워크 스레드에서 UI 스레드로 안전하게 전달합니다.
실제 EV3/SPIKE 연결은 별도 하드웨어 어댑터 구현/검증 후 사용하세요.
"""
from collections import deque
import math
import json
import os
import queue
import tkinter as tk
from tkinter import ttk

import paho.mqtt.client as mqtt
from protocol import parse_command, status_payload, topic

HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
ROBOT = os.getenv("MQTT_ROBOT", "robot01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
CMD = topic(ROOM, ROBOT, "cmd")
STATUS = topic(ROOM, ROBOT, "status")
events = queue.Queue()
seen = deque(maxlen=128)
connected = False


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        events.put(("connected", False))
    else:
        client.subscribe(CMD, qos=1)
        events.put(("connected", True))


def on_disconnect(client, userdata, flags, reason_code, properties):
    events.put(("connected", False))


def on_message(client, userdata, message):
    events.put(("command", message.payload))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

root = tk.Tk()
root.title("학생 B - MQTT 로봇 수신 시뮬레이터")
root.geometry("550x425")
connection = ttk.Label(root, text="MQTT 연결 중...")
connection.pack(pady=6)
canvas = tk.Canvas(root, width=500, height=300, bg="white")
canvas.pack(pady=8)
canvas.create_rectangle(10, 10, 490, 290, outline="gray", width=2)
robot_id = canvas.create_polygon(250, 130, 239, 162, 261, 162,
                                 fill="royalblue")
robot_x, robot_y, heading = 250.0, 150.0, 90.0  # 처음에는 화면 위를 바라봄

def redraw_robot():
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


def publish_status(state, detail):
    if connected:
        client.publish(STATUS, status_payload(state, detail),
                       qos=0, retain=False)


def simulate(message):
    global robot_x, robot_y, heading
    try:
        data = parse_command(message)
        if data["id"] in seen:
            return  # QoS 1 중복 전달을 무시
        seen.append(data["id"])
    except ValueError as exc:
        last.config(text=f"거부됨: {exc}")
        publish_status("rejected", str(exc))
        return

    action = data["action"]
    if action in ("left", "right"):
        heading += 30 if action == "left" else -30
    elif action in ("forward", "backward"):
        direction = 1 if action == "forward" else -1
        angle = math.radians(heading)
        new_x = robot_x + direction * 20 * math.cos(angle)
        new_y = robot_y - direction * 20 * math.sin(angle)
        if 30 <= new_x <= 470 and 30 <= new_y <= 270:
            robot_x, robot_y = new_x, new_y
    redraw_robot()
    last.config(text=f"시뮬레이션: {action} / {data['duration_ms']}ms")
    publish_status("simulated", action)


def process_events():
    global connected
    try:
        while True:
            kind, data = events.get_nowait()
            if kind == "connected":
                connected = data
                connection.config(text="MQTT 연결됨" if data else "MQTT 연결 끊김")
                if data:
                    publish_status("ready", "simulation gateway online")
            elif kind == "command":
                simulate(data)
    except queue.Empty:
        pass
    root.after(50, process_events)


def close():
    publish_status("offline", "gateway closing")
    client.disconnect()
    client.loop_stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)
client.connect_async(HOST, PORT, keepalive=30)
client.loop_start()
process_events()
root.mainloop()
