# 08차시 — MQTT로 원격 명령 주고받기

**시간:** 90분  
**선행:** SPIKE Prime Python 기초, Turtle 미로 탈출, 리스트 기초

## 학습 목표
- 핵심 개념을 설명할 수 있다.
- 제공된 데이터를 바탕으로 알고리즘을 직접 작성한다.
- 결과를 검증하고 개선할 수 있다.

## 이론 (20분)

MQTT는 발행자(Publisher)가 브로커에 메시지를 보내고 구독자(Subscriber)가 토픽을 구독해 메시지를 받는 구조다. PC A는 `start/pause/stop` 명령을 보내고 PC B는 가상 청소기의 상태만 바꾼다. Paho MQTT 2.x는 CallbackAPIVersion.VERSION2와 맞는 콜백 시그니처를 사용한다. 실물 로봇 모터를 제어하지 않는다.

## 짧은 예시

`client.publish(TOPIC, json.dumps({"cmd":"start"}), retain=False)`로 문자열 메시지를 보내고, 수신 쪽은 JSON을 해석한 뒤 허용된 명령만 처리한다.

## 교사 시연 (15분)

두 PC가 같은 내부망 브로커에 연결한 뒤 메시지를 보내고 받은 상태를 출력한다. 교사가 HOST/계정을 교실 환경에 맞게 설정해야 한다.

## 학생 실습 (30분)

**미션:** PC A에서 보낸 시작·일시정지·정지 명령으로 PC B 가상 청소기 상태를 바꿔라.

학생은 [실습 템플릿](../../../examples/python-advanced/lesson-08/lesson-08.py)을 열어 같은 폴더에 `main.py`로 저장한 후 `# 여기에 코드를 작성하세요.` 아래에 코드를 작성한다.

## 도전·검증 (15분)

- 토픽과 브로커 주소가 양쪽에서 같은가? / 비밀번호가 공개 GitHub에 저장되지 않았는가?
- **도전:** Tkinter 대시보드와 메시지를 연결하되 네트워크 콜백에서 GUI를 직접 변경하지 않고 queue로 전달하라.

## 도입·정리 운영

- 도입 및 지난 수업 연결: 10분
- 이론: 20분
- 교사 시연: 15분
- 학생 실습: 30분
- 검증·정리: 15분

### 8차시 사전 준비

Thonny에서 `paho-mqtt` 2.x 설치. 교실 내 Mosquitto 등의 브로커가 있어야 합니다. 공개 저장소에는 계정 비밀번호를 올리지 않습니다. `HOST = "192.168.0.10"`은 예시이며 실제 교사 서버 IP로 변경합니다. 실물 SPIKE Prime 제어는 포함되지 않습니다.

- PC A: `lesson-08-sender.py`를 `sender.py`로 복사해 실행합니다.
- PC B: `lesson-08.py`를 `main.py`로 복사하여 명령별 상태 변경 코드를 작성합니다.
- 브로커 주소를 두 PC에 동일하게 설정해야 합니다.

## 보충 이론: MQTT로 두 프로그램 연결

MQTT는 **보내는 프로그램 → 브로커 → 받는 프로그램**으로 작동한다.

| 용어 | 의미 | 예시 |
|---|---|---|
| Broker | 메시지를 중개하는 서버 | 교실 Raspberry Pi Mosquitto |
| Topic | 메시지를 분류하는 주소 | `robottagram/class01/cleaner01/cmd` |
| Publisher | 토픽에 메시지를 보냄 | PC A의 명령 입력 프로그램 |
| Subscriber | 토픽을 구독해 메시지를 받음 | PC B의 가상 청소기 |

### 명령 형식

```json
{"cmd":"start"}
```

받는 프로그램에서 메시지가 올바른 JSON인지 확인한 뒤 `start`, `pause`, `stop` 중 하나일 때만 상태를 변경한다.

Paho MQTT 2.x의 VERSION2 기준 연결 콜백은 `on_connect(client, userdata, flags, reason_code, properties)`, 메시지 콜백은 `on_message(client, userdata, msg)` 형태다. `loop_forever()`는 네트워크 처리로 실행 흐름을 점유하므로 Tkinter와 한 스레드에서 동시에 사용하지 않는다. Tkinter 확장에서는 MQTT `loop_start()`와 `queue.Queue` 및 `root.after()`를 활용할 수 있다.

### 안전·준비 사항

- 두 PC 모두 동일 브로커 주소·포트·토픽으로 설정
- 교실 내부망에서만 접근 가능하도록 구성
- 브로커의 실제 비밀번호는 개인 `main.py`와 `sender.py`에만 입력하고 공개 GitHub에는 올리지 않기
- 실습의 수신기는 **가상 상태 변경**만 처리. 실제 로봇 모터 연결 금지

**도전:** 받는 PC가 자신의 상태를 다른 토픽으로 돌려보내도록 양방향 통신을 설계한다.
