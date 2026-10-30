# 학생용: MQTT 예제 코드를 읽는 순서

**코드를 처음부터 전부 외우려고 하지 마세요.** 단계별로 '한 줄을 바꾸면 어떻게 될까?'를 확인합니다.

## 단계 1. 보내는 사람과 듣는 사람

1. [step01_subscriber.py](step01_subscriber.py) — 듣는 프로그램
2. [step02_publisher.py](step02_publisher.py) — 보내는 프로그램

**코드에서 찾아볼 명령어:**
- `client.connect(HOST, PORT)`: 브로커 연결
- `client.subscribe(TOPIC)`: 특정 채널 구독
- `client.publish(TOPIC, PAYLOAD)`: 메시지 발행
- `def on_message(...)`: 메시지 수신 시 자동 실행

**질문:** 구독자와 발행자의 `ROOM`이 서로 다르면 어떻게 될까요?

## 단계 2. 콘솔에서 양방향 채팅

3. [step03_console_chat.py](step03_console_chat.py) — 두 PC에서 **같은 프로그램**을 실행하고 직접 입력/출력하기

**코드에서 찾아볼 명령어:**
- `input("보낼 메시지: ")`: Thonny Shell에서 문자열 입력
- `client.publish(TOPIC, ...)`: MQTT 브로커로 전송
- `on_message(...)`: 메시지를 받으면 자동 호출
- `print(...)`: 받은 메시지를 Shell에 출력

**질문:** 한 컴퓨터가 보내기와 받기를 동시에 할 수 있을까요? 왜 자기 메시지도 표시될까요?

## 단계 3. Tkinter로 채팅

4. [mqtt_chat.py](mqtt_chat.py) — 콘솔 대신 Tkinter 화면에서 채팅

**코드에서 찾아볼 명령어:**
- `ttk.Entry(...)`: 사용자 입력
- `command=send`: 버튼 누를 때 실행
- `queue.Queue()`: MQTT 스레드에서 UI로 정보를 넘기는 안전한 메모함
- `root.after(50, process_events)`: 약 50ms 후 화면 갱신 작업을 예약

**질문:** 왜 `on_message`에서 바로 라벨을 바꾸지 않을까요?

## 단계 4. 메시지로 로봇 조종

5. [protocol.py](protocol.py) — 명령 카드 형식과 검사
6. [mqtt_controller.py](mqtt_controller.py) — 전진·후진·회전 버튼
7. [mqtt_gateway_simulator.py](mqtt_gateway_simulator.py) — PC B의 가상 로봇

**코드에서 찾아볼 명령어:**
- `make_command("forward")`: 정해진 형식의 명령 카드 만들기
- `json.dumps(...)`: Python 데이터를 JSON 문자열로 만들기
- `parse_command(...)`: 잘못된 명령 거부하기
- `canvas.coords(...)`: 화면 속 로봇 위치 업데이트
- `client.publish(STATUS, ...)`: 실행 결과를 다시 보내기

**질문:** A에서 송신 요청을 확인한 것과 B에서 실제 명령을 실행했다는 것은 왜 다를까요?

## 단계 5. EV3 Legendary 실물 연결

- [ev3_serial_ports.py](ev3_serial_ports.py): 어떤 직렬포트가 보이는지 **조회만** 한다.
- [EV3 시리얼 설계](../../docs/ev3-legendary-serial.md): 기존 손 씻기 스테이션 v8과 연결.
- 실제 EV3 제어 코드는 아직 구현·시험되지 않았으므로 임의 송신을 하지 않는다.

수업 지도안: [12차시 목록](../../curriculum/mqtt-iot/README.md) · [교사용 입문 교재](../../curriculum/mqtt-iot/TEACHER-HANDBOOK.md).
