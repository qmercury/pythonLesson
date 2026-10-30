"""MQTT 1~3차시: 두 컴퓨터에서 같은 프로그램을 실행해 메시지를 교환합니다.

시작 전: python -m pip install "paho-mqtt>=2,<3"
환경변수: MQTT_HOST(교실 브로커 IP), MQTT_USER, MQTT_PASSWORD
두 PC는 같은 room을 사용합니다. 브로커는 사설 교실 네트워크에 둡니다.
"""
# 교사가 먼저 알아야 할 큰 흐름:
# 연결 → subscribe(채널 구독) → on_message(메시지 도착) → queue → Tkinter 표시
# 버튼 클릭 → publish(메시지 전송) → 상대 프로그램에서 수신
import os
import queue
import tkinter as tk
from tkinter import ttk

import paho.mqtt.client as mqtt

# [설정] 컴퓨터 두 대는 같은 브로커 서버를 사용해야 합니다.
# MQTT_HOST를 지정하지 않으면 127.0.0.1(자기 PC)을 사용합니다.
# 설정값/계정 정보는 GitHub에 올리지 마세요.
HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
# [토픽] '방송 채널 이름'입니다. class01과 class02는 서로 다른 채널입니다.
TOPIC = f"robottagram/{ROOM}/chat"
# [queue] 네트워크 작업과 Tkinter 화면 갱신 사이의 안전한 메모함.
# MQTT는 별도 스레드에서 수신하므로 화면을 직접 만지지 않고 여기에 기록합니다.
events = queue.Queue()
connected = False


# [콜백] 브로커가 '연결되었어요/거절합니다'라고 응답하면 자동 호출합니다.
# Paho 2.x의 CallbackAPIVersion.VERSION2 인자 순서입니다.
def on_connect(client, userdata, flags, reason_code, properties):
    # 연결 거부와 성공을 구분해야 실제로 구독할 수 있습니다.
    if reason_code.is_failure:
        events.put(("system", f"연결 거부: {reason_code}"))
    else:
        # 연결/재연결 직후 구독: 재접속 시에도 채널을 다시 신청합니다.
        client.subscribe(TOPIC, qos=1)
        events.put(("connected", True))


# [콜백] 연결이 끊겼을 때 표시할 메시지를 메모함에 넣습니다.
def on_disconnect(client, userdata, flags, reason_code, properties):
    events.put(("connected", False))


# [콜백] 구독한 채널로 실제 메시지가 도착했을 때 실행됩니다.
def on_message(client, userdata, message):
    # MQTT payload는 bytes이므로 UTF-8 글자로 해석한 뒤 전달합니다.
    events.put(("message", message.payload.decode("utf-8", errors="replace")[:200]))


# [클라이언트] 네트워크 연결·발행·구독을 담당하는 객체입니다.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# 교실 브로커는 암호가 필요할 수 있습니다. 비밀번호를 코드에 적지 않습니다.
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# [GUI] 이제부터는 Tkinter 화면을 만듭니다.
# Tkinter의 mainloop와 MQTT loop_start는 서로 다른 일을 합니다.
root = tk.Tk()
root.title("MQTT 메시지 교환")
root.geometry("480x400")
state = ttk.Label(root, text="연결 중...")
state.pack(pady=6)
# 채팅 내용 창: 사용자가 직접 수정하지 못하도록 기본 상태를 disabled로 둡니다.
history = tk.Text(root, width=55, height=15, state="disabled")
history.pack(padx=12, pady=8)
# 송신할 별명과 메시지를 입력하는 두 개의 칸입니다.
name = ttk.Entry(root)
name.insert(0, "학생")
name.pack(fill="x", padx=12)
message = ttk.Entry(root)
message.pack(fill="x", padx=12, pady=6)


# [UI 함수] 받은 메시지 한 줄을 채팅창에 추가합니다.
# 이 함수는 Tkinter 메인 스레드에서만 호출합니다.
def log(line):
    # Text를 잠깐 편집 가능하게 만들고 글자를 추가한 뒤 다시 잠급니다.
    history.config(state="normal")
    history.insert("end", line + "\n")
    history.see("end")
    history.config(state="disabled")


# [버튼 이벤트] '보내기'를 눌렀을 때 호출되는 함수입니다.
def send():
    # 연결 상태가 아닌데 발행을 요청하면 화면에 안내만 합니다.
    if not connected:
        log("서버가 연결되지 않았습니다.")
        return
    # Entry.get()으로 사용자가 입력한 글자를 가져옵니다.
    # 너무 긴 메시지/별명은 연습용 화면에서 일부만 사용합니다.
    nickname = name.get().strip()[:15] or "학생"
    text = message.get().strip()[:120]
    if text:
        # qos=1: 중복 전달 가능성이 있는 '최소 한 번' 전달 방식.
        # retain=False: 브로커에 마지막 채팅을 retained 메시지로 저장하지 않음.
        # 이 호출 자체는 상대가 읽었음을 보장하지는 않습니다.
        client.publish(TOPIC, f"{nickname}: {text}", qos=1, retain=False)
        message.delete(0, "end")


ttk.Button(root, text="보내기", command=send).pack(pady=4)
# <Return>: 입력창에서 Enter를 눌러도 send()가 실행되도록 연결.
message.bind("<Return>", lambda event: send())


# [UI 반복 작업] queue에 쌓인 네트워크 알림을 Tkinter 메인 스레드로 전달합니다.
# after()는 창을 멈추지 않고 다음 실행을 예약합니다.
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
    # 약 50ms 뒤 다시 메모함 확인(무한 while로 창을 막지 않습니다).
    root.after(50, process_events)


# [종료] 네트워크 스레드를 정리하고 Tkinter 창을 닫습니다.
def close():
    client.disconnect()
    client.loop_stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)
# [연결] 네트워크 연결 시작. 실제 연결 완료는 on_connect()가 알려 줍니다.
client.connect_async(HOST, PORT, keepalive=30)
# MQTT 네트워크 작업을 별도 스레드에서 처리하여 창이 멈추지 않습니다.
client.loop_start()
process_events()
# [GUI 루프] 창의 버튼·입력·화면 갱신 이벤트를 처리합니다.
root.mainloop()
