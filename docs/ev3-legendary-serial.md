# EV3 Pybricks Legendary ↔ Tkinter + MQTT 연결 설계

## 확인된 사실 (2026-10-29 실습)

- 로보타그램 **손 씻기 스테이션 v8**에서 **EV3 Pybricks Legendary ↔ 컴퓨터**를 **Bluetooth Classic 기반 직렬통신**으로 연결하는 데 성공.
- 사용 인터페이스는 **Chrome Web Serial API**. EV3 모터 회전 방향에 따라 손 씻기 안내 영상을 재생하거나 종료하는 연동을 확인.
- 2026-10-30 기준 이번 채팅에서는 v8의 실제 소스/직렬 프레임/COM 또는 tty 포트 이름이 제공되지 않았으므로 그 내용을 추측하지 않음.
- v8의 Python `main.py`는 UI/서버 실행 및 Chrome 표시를 다루며, 실제 시리얼 접근은 브라우저 쪽 코드에 있을 수 있음.

## 목표

```text
학생 A (Tkinter 송신 UI)
         │ MQTT pub/sub
         ▼
교실 로컬 MQTT 브로커
         │
         ▼
학생 B (Tkinter 수신·상태 UI / 명령 검증)
         │
         ├─ 경로 A: Python pyserial (OS에 COM/tty가 노출되는 경우)
         │
         └─ 경로 B: 로컬 브리지 → 기존 Chrome Web Serial 연결 (v8 재사용)
         │
         ▼
EV3 (Pybricks Legendary, 사용자 프로그램)
         │
         ├─ 허용된 짧은 동작 명령만 수행, watchdog으로 자동 정지
         └─ 동작 결과/센서값을 역방향으로 송신 → MQTT 상태 메시지
```

## 첫 번째 작업: 기존 연결을 재사용

1. 손 씻기 스테이션 v8의 실제 Web Serial 통신 코드에서 `requestPort()`, `open()`, `readable`, `writable`, 메시지 프레이밍과 장치 응답 코드를 확인.
2. **브라우저에서 직렬포트 연결 성공은 이미 확인**되었으므로 재연구보다 프로토콜 재사용을 우선.
3. Tkinter에서 같은 직렬장치를 사용하려면 Python `pyserial`의 `serial.tools.list_ports`로 후보 COM/tty를 확인. [조회 전용 코드](../examples/mqtt-iot/ev3_serial_ports.py).
4. Python에서 연결할 수 없으면 로컬 웹서버/WebSocket 등으로 **MQTT 수신기 → Web Serial 브라우저**만 이어주는 브리지 구성 검토.
5. v8의 EV3 수신/송신 바이트가 확인될 때까지 새 임의 명령을 하드웨어에 전송하지 않음.

## 구분해야 할 두 경로

| 항목 | 기존 v8 검증 | 신규 Tkinter 통합 |
|---|---|---|
| EV3 펌웨어 | Pybricks Legendary | 그대로 유지 |
| 블루투스 | Classic 직렬 | 그대로 유지 |
| PC 측 연결 | Chrome Web Serial | Python pyserial 또는 기존 브라우저 브리지 |
| 애플리케이션 | 모터 회전 → 영상 재생/종료 | MQTT 명령 → EV3 동작, EV3 센서 → MQTT |
| 완료 상태 | v8에서 직렬 연결 및 영상 연동 확인 | 통신 어댑터와 로봇 명령 프로토콜은 미구현 |

## 교육 목표

- 학생은 MQTT의 발행/구독 역할과 Bluetooth 직렬 프레임의 역할을 구분한다.
- EV3를 직접 MQTT에 연결하지 않고 수신 PC가 **MQTT ↔ Bluetooth** 변환을 담당한다.
- 통신 실패 시 자동 정지, 메시지 만료, 중복 명령 차단, 팀별 토픽 분리를 배운다.

## 기술 검토

- Pybricks 4.1.1 (2026-10-22)에서는 EV3 USB/RFCOMM의 **호스트 명령 응답** 관련 수정이 있음. 이것이 사용자 임의 문자열 채널과 동일함을 뜻하지는 않음.
- Pybricks 공식 문서에는 EV3용 HubNetwork 등 다른 블루투스 통신 API도 있으나, **이번 교육과정에서는 이미 성공한 Web Serial 경로를 우선 재사용**.
- 브라우저 포트 사용 중 Python에서 동시에 같은 포트를 열 수 있다고 가정하지 않음.

참고:
- https://github.com/pybricks/pybricks-micropython/blob/master/CHANGELOG.md
- https://docs.pybricks.com/en/v4.1.1/messaging/index.html
