import json
import paho.mqtt.client as mqtt

HOST = 'CHANGE_ME'
PORT = 1883
TOPIC = 'robottagram/class01/cleaner01/cmd'
USER = ''
PASSWORD = ''

if HOST == 'CHANGE_ME':
    print('HOST를 교실 MQTT 브로커 주소로 변경하세요.')
else:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if USER:
        client.username_pw_set(USER, PASSWORD)
    client.connect(HOST, PORT, 60)
    client.loop_start()
    try:
        while True:
            cmd = input('명령 (start/pause/stop/quit)> ').strip().lower()
            if cmd == 'quit':
                break
            if cmd not in {'start','pause','stop'}:
                print('알 수 없는 명령')
                continue
            result = client.publish(TOPIC, json.dumps({'cmd':cmd}), qos=1, retain=False)
            result.wait_for_publish()
    finally:
        client.loop_stop()
        client.disconnect()
