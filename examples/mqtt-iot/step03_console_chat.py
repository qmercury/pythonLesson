"""MQTT 3차시: 두 컴퓨터에서 이 파일을 실행하면 콘솔 채팅을 할 수 있습니다.

실습 순서
1. 학생 A와 B의 PC를 같은 교실 MQTT 브로커에 연결합니다.
2. 각자의 Thonny에서 이 프로그램을 실행합니다.
3. 콘솔(Shell)에 메시지를 입력한 뒤 Enter를 누릅니다.
4. 서로의 콘솔에 '[받음]' 메시지가 표시되는지 확인합니다.
5. '종료'를 입력하면 통신을 끝냅니다.

준비: Thonny 패키지 관리에서 paho-mqtt 2.x 설치.
환경변수: MQTT_HOST(브로커 IP), MQTT_USER, MQTT_PASSWORD, MQTT_ROOM.
안전: 실물 로봇에 명령을 보내지 않는 채팅 실습입니다.
"""
import os
import threading

import paho.mqtt.client as mqtt

# ── 1. 교실 방송실(MQTT 브로커) 정보 ──
# A, B가 반드시 같은 브로커에 접속해야 합니다.
# 기본 127.0.0.1은 '이 컴퓨터'이므로 다른 PC에 브로커가 있으면 수정하세요.
HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")

# ── 2. 메시지를 구분하는 방송 채널(Topic) ──
# room을 class02로 바꾸면 class01 채널의 메시지는 보이지 않습니다.
TOPIC = f"robottagram/{ROOM}/chat"

# ── 3. 연결 성공 여부를 기억할 신호등 ──
# on_connect는 별도 MQTT 스레드에서 실행되므로 Event를 사용합니다.
connected = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):
    """[연결 콜백] 브로커의 연결 승인(CONNACK)을 받으면 자동 실행됩니다."""
    if reason_code.is_failure:
        print("접속 거부:", reason_code)
        connected.clear()
        return

    # 메시지를 받으려면 '이 채널을 구독한다'고 신청해야 합니다.
    client.subscribe(TOPIC, qos=1)
    connected.set()
    print("\n[연결됨] 구독 토픽:", TOPIC)


def on_disconnect(client, userdata, flags, reason_code, properties):
    """[연결 끊김] 끊긴 상태에서 계속 메시지를 보내지 않도록 표시합니다."""
    connected.clear()
    print("\n[연결 끊김] 브로커 상태를 확인하세요.")


def on_message(client, userdata, msg):
    """[수신 콜백] 다른 컴퓨터가 발행한 메시지가 도착하면 콘솔에 출력합니다."""
    # MQTT의 payload는 글자가 아닌 bytes이므로 UTF-8로 변환합니다.
    text = msg.payload.decode("utf-8", errors="replace")
    print("\n[받음]", text)

    # 이 함수는 '메시지를 받을 때' 자동 실행됩니다.
    # 학생이 아래의 input()에 글자를 입력하는 도중에도 출력될 수 있습니다.


# ── 4. 클라이언트를 만들고 콜백 함수를 등록 ──
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# ── 5. 브로커에 연결하고 수신 작업을 시작 ──
# connect(): 연결을 시작합니다.
# loop_start(): 네트워크 메시지를 백그라운드에서 받습니다.
# 입력(input)을 기다려도 MQTT 수신이 멈추지 않습니다.
print(f"[연결 시도] {HOST}:{PORT}")
try:
    client.connect(HOST, PORT, keepalive=30)
except OSError as error:
    print("[오류] 브로커 접속 실패:", error)
    raise SystemExit(1)

client.loop_start()

# 브로커 연결 승인과 구독 등록을 기다립니다.
# 기다리던 도중 실패하면 학생이 설정을 확인할 수 있게 안내합니다.
if not connected.wait(timeout=10):
    print("[오류] 접속이 확인되지 않았습니다. IP, 계정, 방화벽을 확인하세요.")
    client.disconnect()
    client.loop_stop()
    raise SystemExit(1)

print("\n채팅을 시작합니다! (끝내려면 '종료' 입력)")
nickname = input("나의 별명: ").strip()[:15] or "학생"

try:
    while True:
        # ── 6. 학생이 콘솔에 문장을 입력하면 메시지 발행 ──
        message = input("보낼 메시지: ").strip()

        if message == "종료":
            break
        if not message:
            continue
        if not connected.is_set():
            print("[안내] 현재 연결이 끊겨서 보내지 않습니다.")
            continue

        # 학생이 입력한 글자를 MQTT 메시지로 전달합니다.
        payload = f"{nickname}: {message[:120]}"
        result = client.publish(TOPIC, payload, qos=1, retain=False)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print("[오류] 메시지를 보내지 못했습니다.")

        # 같은 채널을 구독 중이므로 '내가 쓴 메시지'도 [받음]에 나타납니다.
        # 이것은 브로커가 구독한 모든 클라이언트에게 전달하기 때문입니다.
except (KeyboardInterrupt, EOFError):
    # Ctrl+C 또는 입력 종료 시에도 깨끗하게 닫습니다.
    pass
finally:
    # ── 7. 수업 종료: 브로커 연결과 백그라운드 수신 스레드 정리 ──
    client.disconnect()
    client.loop_stop()
    print("\n[종료] MQTT 채팅을 마쳤습니다.")
