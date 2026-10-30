# Thonny·Python 개발 환경 안내

문서 기준: 2026-10-29. 운영체제 및 라이브러리 버전에 따라 설치 절차가 바뀔 수 있다.

## 공통 원칙

- 학생 PC는 Thonny를 기본 편집기로 사용한다.
- **Tools → Options → Interpreter**에서 로봇 전용 인터프리터가 아닌 일반 데스크톱 Python을 선택한다.
- 각 차시별 폴더와 파일을 나누고 실행 후 화면이 생성되는지 확인한다.
- 기본 실습은 네트워크 없이 진행 가능하도록 구성한다(Turtle/Tkinter).
- Flet 모바일 테스트는 별도의 네트워크·패키지 설치 준비가 필요하다.

## Turtle

~~~python
import turtle

screen = turtle.Screen()
screen.title("Turtle Test")
turtle.forward(100)
screen.mainloop()
~~~

- 일반 Python 표준 라이브러리이므로 별도 pip 설치가 보통 필요하지 않다.
- Turtle/Tkinter 창 실행이 가능한 그래픽 데스크톱 환경이 필요하다.
- 키보드 이벤트 사용 시 Turtle 창에 포커스를 준다.

## Tkinter

~~~python
import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
tk.Label(root, text="Hello, GUI!").pack(padx=20, pady=20)
root.mainloop()
~~~

- 표준 라이브러리 tkinter가 포함된 Python 배포 환경에서 별도 설치 없이 동작한다.
- 일반 Thonny Python 설치를 우선 사용하고, 그래픽/Tk 구성 누락 시 설치 환경을 확인한다.

## Flet

- 공식 문서상 Python 3.10 이상 요구. Windows는 지원되는 64-bit Windows 10/11 사용.
- Thonny의 현재 인터프리터와 Flet을 설치한 인터프리터가 같아야 한다.
- Thonny의 **Tools → Manage packages**에서 flet 검색·설치 후 다음 코드로 PC 앱 실행을 먼저 확인한다.

~~~python
import flet as ft

def main(page: ft.Page):
    page.title = "Flet Test"
    page.add(ft.Text("Hello, Flet!"))

ft.run(main)
~~~

- 터미널에서 동일 환경으로 실행: flet run [script] (앱 개발 시 CLI 사용 권장).
- 휴대폰 개발 테스트: Android 또는 iOS용 Flet 앱 설치 → 같은 Wi-Fi → flet run --android [script] 또는 flet run --ios [script] → QR코드 스캔.
- **미리보기와 APK/IPA 빌드는 다르다.** 빌드 도구, 앱 서명, 장치별 제약은 별도 준비해야 한다.
- Android APK: flet build apk. iOS: macOS에서 iOS 빌드/서명 관련 별도 조건 확인.
- 인터넷 연결이 제한된 교실에서는 패키지·클라이언트 다운로드를 교사가 미리 검증한다.

## 문제 발생 시

| 현상 | 확인 |
|---|---|
| import 오류 | Thonny 선택 Python과 패키지 설치 위치가 같은가? |
| Turtle/Tkinter 창 미표시 | 그래픽 데스크톱 환경인가? 창이 뒤에 숨지 않았는가? |
| Flet PC 앱이 실행되지 않음 | 지원 Python/OS인지? 필요 클라이언트 다운로드 및 방화벽 제한 확인 |
| 휴대폰에서 QR 연결 불가 | 동일 네트워크, 방화벽/네트워크 격리, PC 개발 서버 실행 여부 |
| Flet API 오류 | 공식 문서와 설치 버전이 일치하는지 확인 |

## 공식 자료

- Thonny: https://thonny.org/
- Python turtle: https://docs.python.org/ko/3/library/turtle.html
- Python tkinter: https://docs.python.org/ko/3/library/tkinter.html
- Flet 설치: https://flet.dev/docs/getting-started/installation/
- Flet 실행: https://flet.dev/docs/getting-started/running-app/
- Flet 모바일 테스트: https://flet.dev/docs/getting-started/testing-on-mobile/
- Flet 패키징: https://flet.dev/docs/publish/

## Tkinter + MQTT IoT 심화 실습

- Tkinter 자체는 데스크톱 Python 표준 라이브러리입니다. MQTT 통신은 `paho-mqtt>=2,<3` 패키지를 추가 설치합니다.
- 학생 PC의 브로커 주소 `MQTT_HOST`에는 교실 서버의 실제 사설 IP를 입력해야 합니다. `127.0.0.1`은 해당 PC 자신을 뜻합니다.
- MQTT 사용자명/비밀번호는 교사가 관리하고 GitHub에 넣지 않습니다. 공개 인터넷의 인증 없는 브로커는 실물 로봇 제어용으로 사용하지 않습니다.
- [IoT 예제 실행 방법](../examples/mqtt-iot/README.md)에서 채팅 → 원격조종 → 가상 로봇 순서로 실습합니다.
- MQTT 통신용 백그라운드 스레드에서 Tkinter 위젯을 직접 수정하지 말고 `queue.Queue` + `root.after()`로 메인 스레드에 전달합니다.
- 실제 EV3/SPIKE Prime 하드웨어를 움직이는 브리지는 기종·펌웨어·포트별로 개발 및 안전 검증이 필요합니다. 예제의 시뮬레이터는 실제 모터를 제어하지 않습니다.

## EV3 Legendary Bluetooth 직렬통신

- 2026-10-29 로보타그램 손 씻기 스테이션 v8에서 **EV3 Legendary ↔ Chrome Web Serial 연결 성공**이 확인되었습니다.
- 이번 IoT 심화과정에서는 EV3에 ev3dev Wi-Fi/SSH를 설치하지 않고 **Pybricks Legendary**를 유지합니다.
- 브라우저 Web Serial은 이미 실습한 경로입니다. Tkinter의 Python `pyserial` 연결은 PC OS에서 실제 COM/tty 시리얼 장치가 보이는지 별도로 확인합니다.
- Thonny의 패키지 관리자에서 `pyserial`을 설치한 후 [포트 확인 예제](../examples/mqtt-iot/ev3_serial_ports.py)를 실행합니다.
- 포트가 목록에 보인다는 사실만으로 EV3 사용자 프로그램과 임의 문자열 통신이 된다는 뜻은 아닙니다. 손 씻기 스테이션 v8의 성공한 메시지 처리 코드를 분석해 재사용합니다.
- [EV3 Legendary 연결 설계 메모](ev3-legendary-serial.md)
