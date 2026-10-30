# Python 네트워크·IoT 프로젝트 — Tkinter + MQTT + LEGO 로봇 (12차시)

> Python 문법 → GUI → **다른 컴퓨터와 통신** → **실제 로봇 제어**로 확장하는 로보타그램 심화 과정

## 목표와 전제

- 대상: SPIKE Prime Python 기초, Tkinter의 Label/Button/Entry/이벤트를 배운 학생
- 운영: 90분 × 12차시, 교사 통제하의 교실 전용 네트워크
- 실습: 학생 A의 Tkinter → MQTT broker → 학생 B의 Tkinter → 로봇 연결 브리지 → EV3 또는 SPIKE Prime
- 기본 예제: [MQTT PC↔PC 채팅](../../examples/mqtt-iot/mqtt_chat.py), [조종기](../../examples/mqtt-iot/mqtt_controller.py), [가상 로봇 수신기](../../examples/mqtt-iot/mqtt_gateway_simulator.py)
- **하드웨어 연결은 준비/검증 단계**: 저장소에는 현재 PC↔PC 통신과 시뮬레이터만 있으며 실제 EV3/SPIKE 모터를 자동으로 움직이는 완성 어댑터는 포함하지 않습니다.

## 시스템 구조

```text
학생 A PC                 교실 MQTT 브로커                  학생 B PC
Tkinter 조종기  --publish-->  [MQTT server]  --subscribe-->  Tkinter 수신 UI
      ^                 /                                   |
      |                /                                    v
      +--subscribe-- status <--publish------------------ 로봇 브리지
                                                            |
                                          +-----------------+-----------------+
                                          |                                   |
                                       EV3 (Pybricks Legendary)                    SPIKE Prime (Pybricks)
                                          |                                   |
                                     Bluetooth Classic RFCOMM           BLE Nordic UART / Pybricks
                                     검증된 Web Serial 방식           허브 프로그램
```

학생 두 명은 직접 TCP 연결을 만드는 것이 아니라 **같은 브로커를 통해 publish/subscribe**합니다. 교실에서는 교사 PC 또는 Raspberry Pi 4에 브로커를 두는 것을 권장합니다.

## 12차시 계획

| 차시 | 수업 주제 | 결과물 | 주요 개념 |
|---:|---|---|---|
| 01 | 네트워크와 IoT 이해 | 메시지 전달 구조도·토픽 설계 | IP, 서버/클라이언트, 브로커 |
| 02 | MQTT 송신 실습 | 문자열 메시지 송신 | publish, broker, topic |
| 03 | 두 컴퓨터 대화 | Tkinter 채팅 앱 | subscribe, callback, queue |
| 04 | 로봇 조종 UI 설계 | Tkinter 방향 버튼 패널 | 이벤트, 기능 분리 |
| 05 | 명령 메시지 만들기 | JSON 명령 보내기 | 프로토콜, 명령 코드 |
| 06 | 다른 PC에서 받아 실행하기 | Canvas 로봇 시뮬레이터 | 수신·검증·처리 |
| 07 | 결과를 다시 보내기 | 양방향 상태 표시 | cmd/status, 왕복 통신 |
| 08 | 통신 사고 예방 | 유효 시간, STOP, 중복 처리 | 안전, 재전송, fail-safe |
| 09 | EV3 Legendary 시리얼 브리지 | Web Serial과 pyserial 방식 비교 | MQTT와 직렬포트 연결 |
| 10 | EV3 Legendary 실제 연결 | 손 씻기 스테이션 v8 통신 활용, 저속 모터 실험 | Bluetooth Classic 직렬통신 *(명령 형식 검증)* |
| 11 | IoT 종합 프로젝트 | 원격 조종+상태 시각화 | 시스템 통합 |
| 12 | 다른 팀과 교차 테스트·발표 | 시연과 연구일지 | 테스트, 원인 분석, 개선 |

## 차시별 미션과 결과물

### 01. 네트워크·IoT 구조
- 질문: 두 컴퓨터가 서로 다른 자리에 있어도 메시지를 주고받으려면?
- 기본: IP / 브로커 / 발행자 / 구독자를 카드로 연결
- 응용: 학생별 room과 robot id 토픽 설계
- 도전: 명령(topic cmd)과 상태(topic status)를 분리하는 이유 설명
- 산출물: 전체 구조도

### 02. 메시지 송신
- 기본: MQTT 서버에 자신의 닉네임과 메시지 발행
- 응용: 토픽을 바꿔 교실별로 구분
- 도전: 브로커 접속 실패를 화면에 표시
- 참고: [mqtt_chat.py](../../examples/mqtt-iot/mqtt_chat.py)

### 03. 컴퓨터 A ↔ B 채팅
- 기본: 서로 다른 두 PC에서 같은 토픽 구독 후 채팅
- 응용: Enter 키로 송신, 닉네임 표시
- 도전: 중복 송신과 네트워크 단절 시 동작 관찰
- 중요: Paho 네트워크 콜백은 다른 스레드에서 실행되므로 Tkinter 위젯은 메인 스레드에서 업데이트
- 참고: [mqtt_chat.py](../../examples/mqtt-iot/mqtt_chat.py)

### 04. 원격조종 UI
- 기본: 전진/후진/좌회전/우회전/정지 버튼
- 응용: 연결 상태 라벨
- 도전: 다른 로봇 이름으로 토픽 바꾸기
- 참고: [mqtt_controller.py](../../examples/mqtt-iot/mqtt_controller.py)

### 05. JSON 명령
- 기본: action, id, sent_at, duration_ms, speed_pct의 역할 설명
- 응용: 메시지를 파싱해서 허용 명령인지 확인
- 도전: 오래된 명령·위험 속도 값을 거부
- 참고: [protocol.py](../../examples/mqtt-iot/protocol.py)

### 06. 수신 PC 가상 로봇
- 기본: 송신 PC에서 버튼 누르면 수신 PC의 Canvas 도형 이동
- 응용: 두 명이 교대로 송신기와 수신기 역할 바꾸기
- 도전: 다른 토픽의 명령은 실행되지 않는지 검증
- 참고: [mqtt_gateway_simulator.py](../../examples/mqtt-iot/mqtt_gateway_simulator.py)

### 07. 왕복 통신
- 기본: 수신 게이트웨이가 명령 처리 후 status 토픽으로 결과 발행
- 응용: 송신 GUI에 상태 표시
- 도전: ready, simulated, rejected 상태 구분
- 참고: [mqtt_controller.py](../../examples/mqtt-iot/mqtt_controller.py) / [mqtt_gateway_simulator.py](../../examples/mqtt-iot/mqtt_gateway_simulator.py)

### 08. 안전한 로봇 명령
- 기본: 0.2초 단발 이동, 별도 STOP 버튼
- 응용: 2초 지난 메시지와 허용되지 않은 명령 거부
- 도전: 같은 메시지 ID가 두 번 올 때 중복 실행 방지
- 참고: [protocol.py](../../examples/mqtt-iot/protocol.py)
- 실제 로봇 제어 시 장치 자체에 **독립 watchdog, STOP, 연결 끊김 정지** 구현이 필수. MQTT 전송 보장(QoS)은 안전 정지를 보증하지 않습니다.

### 09. 로봇 브리지 설계
- 기본: `execute(action, duration_ms, speed_pct)` 형태의 어댑터 인터페이스 설계
- 응용: 손 씻기 스테이션 v8에서 성공한 Web Serial 방식과 Python pyserial 차이 설명
- 도전: MQTT와 Bluetooth 통신 코드를 독립된 모듈로 분리
- 참고: [EV3 Legendary 연결 조사](../../docs/ev3-legendary-serial.md), [PC 시리얼 장치 목록 확인](../../examples/mqtt-iot/ev3_serial_ports.py)
- 이 차시는 실제 구동 없이 인터페이스 설계와 모의 실험으로 진행

### 10. 실제 장치 연결
- EV3는 **Pybricks Legendary + Bluetooth Classic 직렬통신**으로 진행한다. 기존 ev3dev Wi-Fi/SSH 설명은 적용하지 않는다.
- **2026-10-29 사용자 실습 확인:** 로보타그램 손 씻기 스테이션 v8에서 EV3 Legendary의 Bluetooth Classic 연결을 Chrome Web Serial로 확인했다. 모터의 방향을 판단하여 영상 재생/종료 동작을 구현했다.
- **남은 과제:** 브라우저 Web Serial 연결의 실제 프레이밍/메시지 형식과 PC Python의 pyserial 접근 가능 여부는 별도로 확인한다. 기존 v8 소스 분석 전에는 일반 텍스트를 EV3에 임의 송신하지 않는다.
- SPIKE Prime(Pybricks): **공식 BLE Nordic UART 통신 사례** 기반으로 허브 입력을 받아 미리 지정된 동작만 실행. 허브 펌웨어와 통신 API 확인 필수.
- **기본** 모터 하나를 저속·짧은 시간 움직였다가 자동 정지
- **응용** 센서 상태를 PC에 전달
- **도전** 로봇 상태를 status 토픽으로 발행
- 안전: 바닥에 로봇을 두기보다 바퀴를 공중에 띄운 상태에서 교사 감독하에 먼저 시험

### 11. 종합 프로젝트
- 선택: 원격 조명/표시기, 원격 로봇 방향 조종, 센서 모니터링, 로봇 경기 점수판 연동
- 필수 기능: 송신 GUI, 수신 GUI, 명령 검사, 상태 피드백, 안전 정지
- 확장: 학생별 토픽, 팀별 브로커 접근 제어

### 12. 교차 테스트·발표
- 다른 팀 컴퓨터와 역할 교체 후 통신 재시험
- 인터넷이 끊기거나 브로커를 멈췄을 때 어떻게 되는지 관찰(시뮬레이터 우선)
- 학생 발표: 네트워크 구조, 오류 상황, 안전 대책, 고친 내용
- 결과물: 코드, 구조도, 화면 캡처, 포트폴리오

## 학습 평가

| 항목 | 성취 기준 |
|---|---|
| GUI | 버튼으로 송신/상태 표시 |
| 통신 | 브로커·발행·구독·토픽 구조 설명 |
| 프로토콜 | JSON 명령과 상태를 구분 |
| 안전 | 미승인/오래된 명령을 거부하고 STOP을 구현 |
| 로봇 | 로봇별 연결 계층 차이를 이해하고 검증된 한 가지 장치를 실험 |
| 협력 | 송신 PC와 수신 PC 역할을 바꾸어 시연 |

## 참고

- [설치 및 실행 안내](../../examples/mqtt-iot/README.md)
- [Paho MQTT Python 공식 문서](https://eclipse.dev/paho/clients/python/)
- [Mosquitto 인증 설정](https://mosquitto.org/documentation/authentication-methods/)
- [Pybricks 공식 허브↔PC 통신](https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/)

[상위 README](../../README.md)
