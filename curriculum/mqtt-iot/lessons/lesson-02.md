# 02차시 — 콘솔에서 MQTT 메시지 보내고 받기

> 교사용 설명 + 학생용 실습 / 90분 / **Tkinter 사용하지 않음**

## 수업 목표

1. 발행자(Publisher)와 구독자(Subscriber)의 차이를 설명한다.
2. 학생 A에서 보낸 메시지가 학생 B의 **Thonny 콘솔(Shell)**에 출력되는 것을 직접 확인한다.
3. `Topic`과 `Payload`의 의미를 구분한다.

## 도입 (0~10분)

교사 질문: **"내 컴퓨터에서 '안녕'이라고 보내면 다른 컴퓨터의 Python 콘솔에는 어떤 일이 일어날까요?"**

칠판에 아래 구조를 그린다.

```text
학생 A 컴퓨터 (발행자)
  │ publish("class01/chat", "안녕")
  ▼
교실 MQTT 브로커 (메시지 전달)
  │
  ▼
학생 B 컴퓨터 (구독자)
  └─ Shell: [받음] 안녕
```

이 단계는 실제 로봇도 Tkinter도 사용하지 않는다.

## 교사 시연 (10~25분)

**교사가 미리 준비할 것:** 교실 내부 Mosquitto 브로커, 인증 계정, 두 학생 PC에 동일한 MQTT 접속 정보, Thonny에 `paho-mqtt` 2.x 설치. [교사 준비 안내](../TEACHER-PRACTICE.md)를 참조한다.

- 학생 B PC에서 [step01_subscriber.py](../../../examples/mqtt-iot/step01_subscriber.py)를 먼저 실행한다.
- Shell에 `브로커 연결됨! 구독 시작: robottagram/class01/chat` 메시지를 확인한다.
- 학생 A PC에서 [step02_publisher.py](../../../examples/mqtt-iot/step02_publisher.py)를 실행한다.
- B 콘솔에 다음처럼 표시되는지 확인한다.

```text
브로커 연결됨! 구독 시작: robottagram/class01/chat
받음: robottagram/class01/chat → 안녕하세요! Python으로 보낸 MQTT 메시지입니다.
```

이것은 **예상 출력 예시**이며, 실제 접속 성공을 의미하는 기록은 아니다.

## 아이들이 이해해야 할 핵심 코드

수신 프로그램:

```python
def on_message(client, userdata, msg):
    text = msg.payload.decode("utf-8")
    print("받은 메시지:", text)
```

발신 프로그램:

```python
client.publish(TOPIC, "안녕하세요!", qos=1, retain=False)
```

위 코드는 **전체 실행 파일이 아니라 학습할 핵심 부분**이다. 실제 연결 및 구독 코드는 제공된 파일을 실행한다.

## 학생 실습 (25~55분)

- **기본:** A에서 발행 / B에서 수신. 메시지가 B의 Shell에 나타나는지 확인한다.
- **기본:** 송신 파일의 `PAYLOAD` 문자열을 자신의 문장으로 바꾸고 다시 전송한다.
- **응용:** 메시지를 3번 바꾸어 전송하고 B가 받은 내용을 기록한다.
- **도전:** A에서 `class01`, B에서 `class02`를 선택해 왜 전달되지 않는지 설명한다.

## 학생 관찰 기록 (55~75분)

| 내가 변경한 항목 | 예상 결과 | 실제 결과 |
|---|---|---|
| Payload를 "안녕"으로 변경 | B가 "안녕" 출력 | |
| Topic을 다른 반으로 변경 | B에서 수신하지 않음 | |
| 원래 Topic으로 되돌리기 | 다시 수신 | |

## 발표·정리 (75~90분)

- **출구 질문:** "브로커가 없어도 A에서 B로 MQTT 메시지를 직접 전달할 수 있을까요?"
- **교사용 답:** 일반적인 MQTT 발행/구독 모델에서는 브로커가 필요하다.
- **성취 기준:** 송신과 수신 파일의 역할을 구분하고, B 콘솔에서 받은 메시지를 확인한다.
- **포트폴리오:** 오늘 보낸 메시지 / 메시지가 어떤 길을 지나 도착했는지 2문장 작성.

## 교사 지도 시 주의

- 학생이 `ModuleNotFoundError: paho`를 만나면 **Thonny가 사용하는 Python에 설치**됐는지 확인한다.
- 각 PC에서 `127.0.0.1`은 자기 PC다. 교실 브로커가 다른 PC에 있으면 실제 사설 IP를 설정한다.
- B가 수신 대기 중인데 학생이 Thonny 중지 버튼을 누르면 더 이상 수신되지 않는다.
- 수업 초반에는 모든 MQTT 내부 코드를 타이핑하게 하지 않는다. 학생이 `TOPIC`과 `PAYLOAD`를 바꾸며 결과를 이해하는 데 집중한다.

[03차시 — 콘솔 양방향 채팅](lesson-03.md) · [전체 IoT 과정](../README.md)
