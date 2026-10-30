"""MQTT 첫 실습 ① 메시지 받기: 이 파일을 먼저 실행하세요.

교실 MQTT 브로커에 '채널 구독'을 신청하고 메시지가 오면 화면에 출력합니다.
준비: Thonny 패키지 관리자에서 paho-mqtt(2.x) 설치.
서버 설정: MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_ROOM 환경변수.

동작 순서:
  1) PC B에서 이 파일을 실행한다.
  2) 콘솔에 '브로커 연결됨 / 구독 시작' 표시를 확인한다.
  3) PC A에서 step02_publisher.py를 실행한다.
  4) PC B 콘솔에서 메시지가 도착했는지 확인한다.

종료: Thonny의 중지 버튼 또는 Ctrl+C. 로봇 모터는 제어하지 않습니다.
"""
import os

import paho.mqtt.client as mqtt

# ── 1. '어느 방송실에 연결할까?' 환경변수에서 서버 주소와 계정 읽기 ──
# 127.0.0.1은 자기 컴퓨터입니다. 다른 컴퓨터의 브로커를 쓰면 IP를 바꿔야 합니다.
HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")

# ── 2. '어느 방송 채널을 들을까?' 구독할 토픽 지정 ──
TOPIC = f"robottagram/{ROOM}/chat"


# ── 3. 브로커 접속 응답이 오면 자동으로 실행되는 함수(콜백) ──
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:  # 인증/접속이 거부됨
        print("브로커 연결 거부:", reason_code)
        return
    print("브로커 연결됨! 구독 시작:", TOPIC)
    client.subscribe(TOPIC, qos=1)  # 이 채널 메시지를 보내 달라고 신청


# ── 4. 구독한 채널로 메시지가 도착하면 자동 실행되는 함수 ──
def on_message(client, userdata, msg):
    # msg.topic: 어느 채널에서 왔나?
    # msg.payload: 실제 메시지 바이트(UTF-8로 텍스트 변환)
    text = msg.payload.decode("utf-8", errors="replace")
    print("받음:", msg.topic, "→", text)


# ── 5. MQTT 클라이언트(프로그램) 만들고 이벤트 함수를 등록 ──
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# ── 6. 브로커에 접속하고 메시지가 올 때까지 기다리기 ──
# loop_forever(): 이 프로그램은 메시지를 계속 기다리며 처리합니다.
# 재접속 처리는 Paho가 담당하지만, 첫 네트워크 연결 실패는 오류로 보일 수 있습니다.
print(f"브로커 접속 시도: {HOST}:{PORT}")
client.connect(HOST, PORT, keepalive=30)
client.loop_forever()
