"""MQTT 4~7차시: Tkinter로 다른 PC의 가상 로봇을 조종합니다.

실행 전: paho-mqtt 설치, 교실 MQTT 브로커 주소/계정 환경변수 설정
고정 길이의 짧은 동작 명령만 보냅니다(버튼을 누를 때 0.2초 동작).
실제 로봇에 연결하기 전에 수신 PC의 시뮬레이터로 테스트하세요.
"""
# [흐름] A에서 버튼 클릭 → JSON 명령 → MQTT cmd 토픽 발행
# B가 처리 결과를 status 토픽으로 보내면 A 화면에 다시 표시합니다.
# 주의: 조종기는 실제 EV3 모터에 직접 연결하지 않습니다.
import json
import os
import queue
import tkinter as tk
from tkinter import ttk

import paho.mqtt.client as mqtt
# 수업 전용 메시지 형식과 안전 범위 검사를 별도 파일에서 가져옵니다.
from protocol import make_command, topic

# [공통 설정] B 수신기와 동일한 브로커/방/로봇 ID를 사용하세요.
HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
ROBOT = os.getenv("MQTT_ROBOT", "robot01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
# 명령 송신 채널과 상태 수신 채널은 서로 다릅니다.
CMD = topic(ROOM, ROBOT, "cmd")
STATUS = topic(ROOM, ROBOT, "status")
# Paho의 네트워크 스레드 → Tkinter의 메인 스레드로 메시지 전달.
events = queue.Queue()
connected = False


# [콜백] 브로커 연결 응답을 받은 순간 호출합니다.
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        events.put(("connected", False))
    else:
        # A는 B가 알려 줄 '상태'를 듣습니다. cmd를 듣는 것은 B입니다.
        client.subscribe(STATUS, qos=1)
        events.put(("connected", True))


# 네트워크 연결이 끊기면 화면의 연결 표시를 바꾸도록 요청합니다.
def on_disconnect(client, userdata, flags, reason_code, properties):
    events.put(("connected", False))


# [상태 수신] B가 보낸 JSON을 화면에 표시할 한 줄로 바꿉니다.
def on_message(client, userdata, message):
    try:
        # bytes로 전달된 JSON 메시지를 Python dict로 해석합니다.
        status = json.loads(message.payload)
        text = f"{status.get('state', '?')}: {status.get('detail', '')}"
    except (ValueError, UnicodeError):
        text = "상태 메시지 해석 실패"
    events.put(("status", text))


# Paho 2.x 콜백 함수 형태를 사용합니다.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# [화면] 이 창은 '원격 조종기'입니다. 실제 그림 이동은 B PC에서 일어납니다.
root = tk.Tk()
root.title("학생 A - 로봇 조종기")
root.geometry("450x365")
connection = ttk.Label(root, text="MQTT 연결 중...")
connection.pack(pady=10)
ttk.Label(root, text=f"ROOM {ROOM} / {ROBOT}", font=("Arial", 14)).pack()
feedback = ttk.Label(root, text="상태를 기다리는 중...")
feedback.pack(pady=8)


# [송신 함수] 버튼에서 전달한 action으로 제한된 크기의 명령을 만듭니다.
def command(action):
    if not connected:
        feedback.config(text="MQTT에 연결되지 않았습니다.")
        return
    # make_command: action 외에 유효시간·명령 ID·속도·지속시간을 추가.
    # json.dumps: dict를 MQTT로 보내기 쉬운 문자열로 변환.
    payload = json.dumps(make_command(action), ensure_ascii=False)
    # 제어 명령은 retained로 저장하지 않습니다(재연결 후 오래된 명령 방지).
    # QoS 1은 중복 도착 가능! B에서 ID를 확인하여 중복 실행을 막습니다.
    info = client.publish(CMD, payload, qos=1, retain=False)
    # 여기서 확인하는 것은 '송신 요청' 상태뿐, 실제 모터 동작 성공이 아닙니다.
    feedback.config(text=f"{action} 송신 요청" if info.rc == mqtt.MQTT_ERR_SUCCESS
                    else "송신 요청 실패")


# [방향 버튼] lambda는 클릭했을 때 action 인자를 넣어 호출하게 해 줍니다.
ttk.Button(root, text="↑ 전진(0.2초)", command=lambda: command("forward")).pack()
row = ttk.Frame(root)
row.pack(pady=8)
ttk.Button(row, text="← 왼쪽", command=lambda: command("left")).pack(side="left", padx=4)
ttk.Button(row, text="■ 정지", command=lambda: command("stop")).pack(side="left", padx=4)
ttk.Button(row, text="오른쪽 →", command=lambda: command("right")).pack(side="left", padx=4)
ttk.Button(root, text="↓ 후진(0.2초)", command=lambda: command("backward")).pack()


# [UI 함수] MQTT 네트워크 콜백에서 바로 Label을 고치지 않습니다.
# queue에 기록한 상태만 Tkinter 메인 스레드에서 처리합니다.
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
    # 50ms 후 다시 상태 메모함을 확인합니다.
    root.after(50, process_events)


# 창을 닫을 때 브로커 연결과 백그라운드 루프를 종료합니다.
def close():
    client.disconnect()
    client.loop_stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)
# 실제 연결 성공은 on_connect가 알려 주므로 처음엔 '연결 중'을 표시합니다.
client.connect_async(HOST, PORT, keepalive=30)
# 네트워크 연결/메시지 처리를 GUI 밖의 별도 스레드에서 진행합니다.
client.loop_start()
process_events()
# 이 루프가 끝날 때까지 버튼 클릭과 화면 갱신이 동작합니다.
root.mainloop()
