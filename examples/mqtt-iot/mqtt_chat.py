"""MQTT 1~3차시: 두 컴퓨터에서 같은 프로그램을 실행해 메시지를 교환합니다.

시작 전: python -m pip install "paho-mqtt>=2,<3"
환경변수: MQTT_HOST(교실 브로커 IP), MQTT_USER, MQTT_PASSWORD
두 PC는 같은 room을 사용합니다. 브로커는 사설 교실 네트워크에 둡니다.
"""
import os
import queue
import tkinter as tk
from tkinter import ttk

import paho.mqtt.client as mqtt

HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
TOPIC = f"robottagram/{ROOM}/chat"
events = queue.Queue()
connected = False


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        events.put(("system", f"연결 거부: {reason_code}"))
    else:
        client.subscribe(TOPIC, qos=1)
        events.put(("connected", True))


def on_disconnect(client, userdata, flags, reason_code, properties):
    events.put(("connected", False))


def on_message(client, userdata, message):
    events.put(("message", message.payload.decode("utf-8", errors="replace")[:200]))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

root = tk.Tk()
root.title("MQTT 메시지 교환")
root.geometry("480x400")
state = ttk.Label(root, text="연결 중...")
state.pack(pady=6)
history = tk.Text(root, width=55, height=15, state="disabled")
history.pack(padx=12, pady=8)
name = ttk.Entry(root)
name.insert(0, "학생")
name.pack(fill="x", padx=12)
message = ttk.Entry(root)
message.pack(fill="x", padx=12, pady=6)


def log(line):
    history.config(state="normal")
    history.insert("end", line + "\n")
    history.see("end")
    history.config(state="disabled")


def send():
    if not connected:
        log("서버가 연결되지 않았습니다.")
        return
    nickname = name.get().strip()[:15] or "학생"
    text = message.get().strip()[:120]
    if text:
        client.publish(TOPIC, f"{nickname}: {text}", qos=1, retain=False)
        message.delete(0, "end")


ttk.Button(root, text="보내기", command=send).pack(pady=4)
message.bind("<Return>", lambda event: send())


def process_events():
    global connected
    try:
        while True:
            kind, item = events.get_nowait()
            if kind == "connected":
                connected = item
                state.config(text="MQTT 연결됨" if connected else "MQTT 연결 끊김")
            elif kind == "message":
                log(item)
            else:
                log(item)
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
