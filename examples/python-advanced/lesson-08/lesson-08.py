import json
import paho.mqtt.client as mqtt

HOST = 'CHANGE_ME'
PORT = 1883
TOPIC = 'robottagram/class01/cleaner01/cmd'
USER = ''
PASSWORD = ''
state = 'stopped'

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe(TOPIC)
        print('연결 성공')
    else:
        print('연결 실패:', reason_code)

def on_message(client, userdata, msg):
    global state
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        if not isinstance(data, dict):
            return
    except (ValueError, UnicodeError):
        return

    command = data.get('cmd')

    # 여기에 코드를 작성하세요.

    print('현재 상태:', state)

if HOST == 'CHANGE_ME':
    print('HOST를 교실 MQTT 브로커 주소로 변경하세요.')
else:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    if USER:
        client.username_pw_set(USER, PASSWORD)
    client.connect(HOST, PORT, 60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
