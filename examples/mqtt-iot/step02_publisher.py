"""MQTT 첫 실습 ② 메시지 보내기: step01_subscriber.py 다음에 실행하세요.

채팅처럼 긴 프로그램에 들어가기 전에 publish()를 한 번 체험합니다.
교실 서버의 IP·비밀번호와 토픽은 수신자와 동일해야 합니다.
"""
import os

import paho.mqtt.client as mqtt

# 1. 수신 프로그램과 똑같은 MQTT 브로커 주소를 입력합니다.
HOST = os.getenv("MQTT_HOST", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
ROOM = os.getenv("MQTT_ROOM", "class01")
USER = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")

# 2. 토픽: 같은 채널로 보내야 구독자가 받습니다.
TOPIC = f"robottagram/{ROOM}/chat"

# 3. 페이로드: 실제로 전송하고 싶은 말입니다.
PAYLOAD = "안녕하세요! Python으로 보낸 MQTT 메시지입니다."

# 4. MQTT 통신을 담당할 클라이언트를 만듭니다.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if USER and PASSWORD:
    client.username_pw_set(USER, PASSWORD)

# 5. 브로커에 연결한 뒤 네트워크 처리 스레드를 시작합니다.
# 서버 연결에 실패하거나 인증이 거부되면 송신도 실패할 수 있습니다.
print(f"{HOST}:{PORT}에 연결하는 중...")
client.connect(HOST, PORT, keepalive=30)
client.loop_start()

# 6. publish()로 메시지를 보냅니다.
# qos=1: 브로커의 전송 확인을 기다리는 방식을 사용합니다.
# retain=False: 마지막 메시지를 브로커에 저장하지 않습니다.
info = client.publish(TOPIC, PAYLOAD, qos=1, retain=False)

# 7. 브로커가 PUBACK를 반환할 때까지 기다립니다.
# '발행 확인'은 수신자의 화면 출력이나 실제 로봇 동작을 뜻하지 않습니다.
info.wait_for_publish(timeout=5)
if info.is_published():
    print("발행 확인됨:", TOPIC, "→", PAYLOAD)
else:
    print("시간 안에 발행이 확인되지 않았습니다.")

# 8. 메시지 송신 후 접속을 마칩니다.
client.disconnect()
client.loop_stop()
