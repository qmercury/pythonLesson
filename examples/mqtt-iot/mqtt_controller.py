"""MQTT 4~7차시: Tkinter로 다른 PC의 가상 로봇을 조종합니다.

실행 전: paho-mqtt 설치, 교실 MQTT 브로커 주소/계정 환경변수 설정
고정 길이의 짧은 동작 명령만 보냅니다(버튼을 누를 때 0.2초 동작).
실제 로봇에 연결하기 전에 수신 PC의 시뮬레이터로 테스트하세요.
"""
import json
import os
import queue
import tkinter as tk
from tkinter import ttk

import paho.mqtt.client as mqtt
from protocol import make_command, topic

HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
ROBOT = os.getenv("MQTT_ROBOT", "robot01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
CMD = topic(ROOM, ROBOT, "cmd")
STATUS = topic(ROOM, ROBOT, "status")
events = queue.Queue()
connected = False


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        events.put(("connected", False))
    else:
        client.subscribe(STATUS, qos=1)
        events.put(("connected", True))


def on_disconnect(client, userdata, flags, reason_code, properties):
    events.put(("connected", False))


def on_message(client, userdata, message):
    try:
        status = json.loads(message.payload)
        text = f"{status.get('state', '?')}: {status.get('detail', '')}"
    except (ValueError, UnicodeError):
        text = "상태 메시지 해석 실패"
    events.put(("status", text))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

root = tk.Tk()
root.title("학생 A - 로봇 조종기")
root.geometry("450x365")
connection = ttk.Label(root, text="MQTT 연결 중...")
connection.pack(pady=10)
ttk.Label(root, text=f"ROOM {ROOM} / {ROBOT}", font=("Arial", 14)).pack()
feedback = ttk.Label(root, text="상태를 기다리는 중...")
feedback.pack(pady=8)


def command(action):
    if not connected:
        feedback.config(text="MQTT에 연결되지 않았습니다.")
        return
    payload = json.dumps(make_command(action), ensure_ascii=False)
    info = client.publish(CMD, payload, qos=1, retain=False)
    feedback.config(text=f"{action} 송신 요청" if info.rc == mqtt.MQTT_ERR_SUCCESS
                    else "송신 요청 실패")


ttk.Button(root, text="↑ 전진(0.2초)", command=lambda: command("forward")).pack()
row = ttk.Frame(root)
row.pack(pady=8)
ttk.Button(row, text="← 왼쪽", command=lambda: command("left")).pack(side="left", padx=4)
ttk.Button(row, text="■ 정지", command=lambda: command("stop")).pack(side="left", padx=4)
ttk.Button(row, text="오른쪽 →", command=lambda: command("right")).pack(side="left", padx=4)
ttk.Button(root, text="↓ 후진(0.2초)", command=lambda: command("backward")).pack()


def process_events():
    global connected
    try:
        while True:
            kind, data = events.get_nowait()
            if kind == "connected":
                connected = data
                connection.config(text="MQTT 연결됨" if data else "MQTT 연결 끊김")
            else:
                feedback.config(text=data)
    except queue.Empty:
        pass
    root.after(50, process_events)


def close():
    client.disconnect()
    client.loop_stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)
client.connect_async(HOST, PORT, keepalive=30)
client.loop_start()
process_events()
root.mainloop()
