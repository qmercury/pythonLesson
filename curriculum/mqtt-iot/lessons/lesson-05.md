# 05차시 — Tkinter 버튼과 JSON 로봇 명령

> 교사용 설명 + 학생용 실습 / 90분 / **실제 모터는 연결하지 않음**

## 수업 목표

1. Tkinter 버튼 클릭을 MQTT 메시지 발행과 연결한다.
2. 메시지 내용이 일반 채팅 글자에서 `action` 등의 키를 가진 JSON 명령으로 바뀌는 이유를 이해한다.
3. 로봇 동작 명령을 보내는 토픽과 실행 결과를 받는 토픽을 구분한다.

## 도입 (0~10분)

**질문:** "채팅으로 '앞으로 가'라고 말하는 대신 버튼을 누르면 로봇이 알아들을 수 있는 명령을 만들려면?"

```text
[전진 버튼] → {"action":"forward"} → MQTT cmd 토픽
                                      ↓
                                 [수신 프로그램]
```

실제 예제의 JSON에는 `v`, `id`, `sent_at`, `duration_ms`, `speed_pct`도 포함된다.

## 교사가 설명할 핵심 (10~25분)

- `Button(command=...)`: 클릭하면 함수 호출.
- `lambda`: 버튼마다 다른 action 문자열을 넘기기.
- `make_command("forward")`: 허용된 명령과 기본 제한값을 적용해 명령 생성.
- `json.dumps()`: Python dict를 JSON 문자열로 변환.
- `client.publish(CMD, payload)`: 명령 채널로 발행.
- `status` 채널: 수신 PC가 결과를 돌려줌. **송신 요청과 실제 동작 성공은 다름**.

## 학생 실습 (25~55분)

교사가 제공한 [mqtt_controller.py](../../../examples/mqtt-iot/mqtt_controller.py)와 [protocol.py](../../../examples/mqtt-iot/protocol.py)를 같은 폴더에 저장하고, 송신 프로그램에서 아래 개념을 찾는다.

```python
def command(action):
    payload = json.dumps(make_command(action))
    client.publish(CMD, payload, qos=1, retain=False)
```

이는 원리 설명을 위한 축약 코드다. 실제 실행 파일에는 연결 상태 점검 등이 추가된다.

- **기본:** 전진/후진/회전/정지 버튼과 명령 action을 대응시킨다.
- **기본:** `make_command("forward")`가 만드는 JSON 키를 찾아 기능을 설명한다.
- **응용:** UI의 버튼 문구·배치 변경.
- **도전:** 오래된 명령이나 100% 속도 요청을 거부하는 이유 설명.

## 평가·정리 (55~90분)

- 다른 PC 수신 시뮬레이터를 미리 준비했다면 6차시의 가상 로봇으로 시험해 볼 수 있다.
- 다른 PC가 준비되지 않았다면 브로커에 명령이 발행되는지 확인하고 6차시에서 실제 수신·처리를 학습한다.
- 확인 질문: "브로커가 메시지를 받아 줬다면 EV3도 반드시 움직였나요?" → 아니다.
- 포트폴리오: 내가 설계한 버튼 1개와 실제 발행한 MQTT 메시지의 action 설명.

## 교사 지도 포인트

- EV3 Legendary 실제 모터는 아직 연결하지 않는다. 먼저 가상 로봇으로 MQTT 통신을 확인한다.
- `retained=False`는 오래된 움직임 명령이 새 구독자에게 전달되는 것을 줄인다.
- 실제 EV3에서 명령이 끊겼을 때 자동 정지하는 watchdog이 있어야 하므로 MQTT 명령 자체만으로 로봇 안전을 보장하지 않는다.

[04차시 — Tkinter 채팅](lesson-04.md) · [06차시 — 가상 로봇 수신](lesson-06.md)
