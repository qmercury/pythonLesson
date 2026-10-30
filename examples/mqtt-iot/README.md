# MQTT + Tkinter — 두 컴퓨터의 통신에서 LEGO 로봇 IoT까지

> 현재 제공 범위: **PC↔PC 실제 MQTT 통신 + Tkinter 양방향 제어 UI + Canvas 시뮬레이터**.
> 로봇 하드웨어를 움직이는 EV3·SPIKE 드라이버는 아직 구현하지 않았습니다.

## 준비물

- 교사 서버: 동일 교실 LAN의 Raspberry Pi 4 또는 PC에 설치한 MQTT 브로커(Mosquitto 추천)
- 학생 A, 학생 B: Thonny + 데스크톱 Python 3.10 이상 + paho-mqtt 2.x
- 공통 네트워크: 학생 두 컴퓨터에서 브로커 IP로 접속할 수 있어야 함
- 실제 로봇을 연결하는 단계에서는 별도로 Pybricks/ev3dev 통신 장치 준비

## 0. 교사 서버 설정 (Ubuntu 24.04/Raspberry Pi 예시)

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo mosquitto_passwd -c /etc/mosquitto/classroom-passwd classroom
```

비밀번호를 묻는 창이 나타나면 교실 전용 비밀번호를 설정합니다(소스 코드나 GitHub에 저장하지 않음). `-c`는 기존 파일을 덮어쓰므로 처음 만들 때에만 사용하세요.

다음 내용을 `/etc/mosquitto/conf.d/classroom.conf`에 저장합니다.

```conf
listener 1883
allow_anonymous false
password_file /etc/mosquitto/classroom-passwd
```

재시작 후 확인:

```bash
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

*중요:* Mosquitto 2.0 계열 설정 예시입니다. 다른 버전에서는 공식 인증 설정 문서와 사용 중인 배포판을 확인합니다. 포트 1883은 교실 전용 내부망으로만 허용하세요. 인터넷에 노출해서는 안 됩니다. 운영 시에는 계정별 ACL·TLS 등 접근 통제를 강화해야 합니다.

## 1. 학생 PC에 패키지 설치

Thonny **도구 → 패키지 관리 → paho-mqtt**를 설치합니다. 또는 Thonny가 선택한 Python에서:

```bash
python3 -m pip install "paho-mqtt>=2,<3"
```

Windows에서는 Python 명령이 다를 수 있으므로 Thonny의 패키지 관리자가 가장 간편합니다.

## 2. 공통 환경변수 설정

프로그램은 환경변수를 읽습니다. 예시:

- `MQTT_HOST` = 교사 서버 IP (예: `192.168.0.10` — **예시 주소**, 실주소로 수정)
- `MQTT_PORT` = `1883`
- `MQTT_USER` = `classroom`
- `MQTT_PASSWORD` = 교사가 설정한 값
- `MQTT_ROOM` = `class01`
- `MQTT_ROBOT` = `robot01`

실습 PC에서 다른 서버로 접속하려면 환경변수 설정이 필요합니다. 로컬 브로커가 같은 PC에 있을 때만 `MQTT_HOST`를 생략할 수 있습니다(`127.0.0.1` 기본값).

교사 예시(macOS/Linux, 터미널을 연 상태에서):

```bash
export MQTT_HOST=192.168.0.10
export MQTT_USER=classroom
export MQTT_PASSWORD='(교사가 정한 비밀번호)'
export MQTT_ROOM=class01
export MQTT_ROBOT=robot01
python3 mqtt_chat.py
```

> Thonny에서 F5로 실행하는 경우 터미널의 `export` 값이 자동 전달되지 않을 수 있습니다. 수업 전 **Thonny에서 실제 실행 환경변수를 지정하거나**, 교사가 별도 로컬 설정/런처 스크립트를 준비해야 합니다. 교실 비밀번호는 GitHub에 넣지 않습니다.

## 3. 두 학생 간 채팅부터 테스트

- 학생 A PC: `mqtt_chat.py` 실행
- 학생 B PC: `mqtt_chat.py` 실행
- 두 PC에서 같은 room과 브로커로 연결한 뒤, 서로 메시지를 보내 보세요.
- 대화 기록은 앱 실행 중에만 표시되며 브로커에 retained/persistent 메시지로 저장하지 않습니다.

## 4. PC A가 조종하고 PC B가 수신하기

- **학생 A:** `mqtt_controller.py` 실행
- **학생 B:** `mqtt_gateway_simulator.py` 실행
- 같은 room과 robot을 선택해 두 앱 모두 "MQTT 연결됨"을 확인합니다.
- 학생 A가 버튼을 누르면 학생 B의 Canvas 가상 로봇이 반응합니다.
- 학생 B는 `status` 토픽으로 실행 결과를 보내고 학생 A의 화면에 표시됩니다.

## 5. 메시지 예시 및 토픽

```text
robottagram/class01/robot01/cmd
robottagram/class01/robot01/status
robottagram/class01/chat
```

JSON 명령은 예를 들어 다음과 같은 형태입니다:

```json
{"v":1,"id":"<매 요청마다 다른 32자리 hex>","sent_at":1793000000.0,"action":"forward","duration_ms":200,"speed_pct":20}
```

- 허용 동작: `forward`, `backward`, `left`, `right`, `stop`
- 명령 1개는 최대 300ms 동작을 **요청**하는 짧은 명령입니다.
- 2초보다 오래된 명령, 잘못된 형식, 허용 범위 밖의 속도/시간, 중복 메시지를 거부합니다.
- 명령은 **retained=False**. 구독 재연결 뒤 오래된 명령이 되살아나 움직이지 않도록 합니다.
- MQTT QoS 1은 중복 배달 가능성이 있으므로 메시지 ID로 중복 실행을 막습니다.
- 송신 GUI의 "송신 요청" 표시는 로봇이 실제로 동작했다는 뜻이 아닙니다. status 응답을 확인합니다.

## 6. 하드웨어 연결 시 필수 조건

**지금 예제는 실제 모터를 전혀 제어하지 않습니다.** 실제 로봇 어댑터는 다음 방식으로 별도 구현해야 합니다.

### EV3 (ev3dev 계열)
- PC B와 EV3를 같은 로컬 네트워크에 연결하고 SSH/EV3 측 에이전트를 통해 제어
- EV3의 Python 버전 및 기존 상주 서비스, 모터 포트를 확인해야 함
- 네트워크 명령이 실종되더라도 EV3 내부에서 **짧은 시간 후 자동 정지**하도록 설계
- 예: 미리 시작한 EV3 프로그램이 안전한 명령만 허용하는 별도의 제어 프로토콜을 사용
- 참고: https://ev3dev-lang-python.readthedocs.io/en/latest/

### SPIKE Prime (Pybricks 계열)
- PC B에서 Pybricks BLE/Nordic UART 채널을 통해 허브에 명령 전달
- 허브에는 **미리 다운로드해 실행하는 입력 처리 프로그램**이 필요
- Pybricks Code 연결과 BLE 제어 프로그램 연결을 동시에 사용할 수 있는지 사전 확인
- 버전에 따라 API 차이가 있으므로 아래 공식 예제 기반으로 먼저 단일 모터 실습
- 참고: https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/

### 안전 원칙
1. 교실 로컬 네트워크에만 브로커 노출. 실제 장치 제어에는 인증·ACL, 필요 시 TLS 적용.
2. **실제 모터를 제어하는 장치 쪽**에 독립적인 timeout watchdog과 물리/소프트웨어 STOP 필수.
3. 저속·저출력·짧은 동작부터 시작. 처음에는 바퀴를 바닥에서 띄우고 테스트.
4. 로봇이 이동 중 끊기면 자동 정지. 네트워크 메시지의 도착·순서를 안전 정지 수단으로 의존하지 않음.
5. 외부에서 받은 코드를 eval/exec하거나 임의 쉘 명령으로 전달하지 않음.
6. 학생별 room/robot을 분리하고 실제 수업에서 교사 허가 없이는 다른 팀 로봇을 제어하지 못하게 ACL 구성.

## 코드

| 파일 | 학습 목표 |
|---|---|
| [mqtt_chat.py](mqtt_chat.py) | 두 컴퓨터 간 Tkinter 채팅 |
| [mqtt_controller.py](mqtt_controller.py) | MQTT 명령 발행·상태 구독 |
| [mqtt_gateway_simulator.py](mqtt_gateway_simulator.py) | 명령 검증·수신·시뮬레이터·상태 발행 |
| [protocol.py](protocol.py) | JSON 명령 형식·안전 검사 |
| [test_mqtt_protocol.py](../../tests/test_mqtt_protocol.py) | 명령 허용/거부 자동 테스트 |

[12차시 커리큘럼](../../curriculum/mqtt-iot/README.md)
