# 04차시 — 콘솔 채팅을 Tkinter 화면으로 바꾸기

> 교사용 설명 + 학생용 실습 / 90분

## 수업 목표

1. 이전 차시 콘솔 채팅의 `input()`과 `print()`를 Tkinter UI와 비교한다.
2. `Entry`, `Button`, `Text` 위젯으로 채팅 화면을 구성한다.
3. 동일한 MQTT 통신을 GUI에 연결하는 방법을 설명한다.

## 도입 (0~10분)

**질문:** "3차시에는 Shell에 메시지를 입력했는데, 이제 진짜 채팅 앱처럼 보이게 하려면 무엇이 필요할까요?"

| 콘솔 채팅 | Tkinter 채팅 |
|---|---|
| `input()` | `Entry.get()` |
| `print()` | `Text.insert()` |
| Enter 키 | 보내기 Button |
| `on_message()` | `on_message()` + `queue` + `after()` |

**중요:** MQTT의 Publisher·Subscriber·Topic 구조는 변하지 않는다. 사용자 인터페이스만 바뀌는 것이다.

## 교사 시연 (10~25분)

- B/A 두 PC에 [mqtt_chat.py](../../../examples/mqtt-iot/mqtt_chat.py)를 실행한다.
- 별명을 입력하고 채팅을 주고받는다.
- 학생과 함께 코드에서 `send()`, `client.publish()`, `on_message()`, `process_events()`를 찾아본다.

## 이해할 핵심 부분

```python
def send():
    text = message.get().strip()
    if text:
        client.publish(TOPIC, text)

def process_events():
    # 실제 예제에서는 queue에서 받은 데이터를 UI 위젯에 표시
    ...
    root.after(50, process_events)
```

위 코드는 **원리 설명용 축약 코드**이며 실행용 완성 코드가 아니다. 완전한 소스는 `mqtt_chat.py`를 사용한다.

**왜 queue가 필요할까?** MQTT 메시지 수신은 Paho의 네트워크 스레드에서 일어난다. Tkinter 위젯은 메인 스레드에서 갱신하도록 `queue.Queue()`와 `root.after()`를 활용한다.

## 학생 실습 (25~55분)

- **기본:** 실제 메시지가 콘솔 대신 Tkinter 채팅 화면에 나타나는지 확인.
- **기본:** 화면 제목과 안내 문구 변경.
- **응용:** 채팅 입력창, 별명 입력창, 보내기 버튼 배치를 직접 수정.
- **도전:** 메시지 없을 때는 버튼을 눌러도 빈 문장을 보내지 않는 이유 설명.

## 테스트·발표 (55~90분)

- 두 PC의 GUI에서 A→B, B→A 채팅에 성공했는지 확인.
- 토픽이 달라지면 수신이 중단되는지 관찰.
- **정리 질문:** "콘솔 채팅과 Tkinter 채팅에서 변하지 않는 통신 코드는?"
  - 답: MQTT 연결, 토픽 구독, 메시지 발행, 수신 콜백 등의 기본 흐름.
- 포트폴리오: 콘솔과 GUI 차이 한 가지 / 직접 바꾼 UI 속성 한 가지.

## 교사 지도 포인트

- `root.mainloop()`와 `client.loop_start()`는 별개의 이벤트/네트워크 처리 루프.
- GUI가 멈추면 콜백에서 `sleep()` 또는 오래 걸리는 네트워크 동작을 하는지 점검.
- 이 차시는 채팅 화면에 집중한다. JSON 명령·EV3 모터 제어는 다음 차시 이후에 다룬다.

[03차시 — 콘솔 채팅](lesson-03.md) · [05차시 — 로봇 명령](lesson-05.md)
