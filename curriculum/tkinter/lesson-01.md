# Tkinter 1차시 상세 지도안 — 나의 첫 번째 윈도우 프로그램

- 대상: SPIKE Prime Python 기초를 배운 초등 4~6학년
- 시간: 90분
- 환경: Thonny + 데스크톱 Python + tkinter
- 결과물: 학생 자신의 소개 앱 (제목, 이름/별명, 취미, 색상)

## 학습 목표

1. 텍스트 출력 콘솔과 GUI 창의 차이를 말할 수 있다.
2. Tk(), title(), geometry(), mainloop()가 하는 일을 설명할 수 있다.
3. Label을 만들고 pack()으로 화면에 표시한다.
4. 자기소개 문구, 글꼴, 색상, 여백을 직접 바꿀 수 있다.

## 준비물

- Thonny 실행 가능한 PC, 스크린/프로젝터
- 시작 코드, 기본·응용·도전 미션
- 결과물 저장 경로 (예: pythonLesson/tkinter/lesson01/)
- 테스트: 일반 Python 인터프리터에서 import tkinter 실행 확인

## 수업 시간표

| 시간 | 활동 | 교사 안내 |
|---|---|---|
| 0~10분 | 콘솔 vs GUI 비교 | print() 출력과 별도 창을 시연 |
| 10~20분 | 빈 창 만들기 | Tk, title, geometry, mainloop |
| 20~35분 | 글자와 배경색 | Label, pack, font, bg, fg |
| 35~55분 | 자기소개 앱 제작 | 여러 Label과 여백 |
| 55~75분 | 미션 수행 | 기본·응용·도전으로 차등 |
| 75~85분 | 발표·짝 테스트 | 코드가 화면을 어떻게 바꾸는지 설명 |
| 85~90분 | 포트폴리오 | 실행 화면과 4문장 기록 |

## 도입: 이전 수업과 연결

~~~python
name = "Robot"
print("안녕하세요!", name)
~~~

질문: 콘솔에서 글자가 나오는 것과 계산기처럼 창이 나타나는 것은 무엇이 다를까? 버튼이나 입력창이 있으면 무엇을 더 할 수 있을까?

## 실습 1: 첫 번째 창

~~~python
import tkinter as tk

root = tk.Tk()
root.title("My First App")
root.geometry("500x350")
root.mainloop()
~~~

- Tk(): 기본 창 생성
- title(): 창의 제목
- geometry(): 창의 크기, 가로x세로(영문 x)
- mainloop(): 창의 이벤트를 처리하는 반복 루프
- 실험: 500x350을 700x500으로 바꾸고 차이 관찰.

## 실습 2: 글자와 배경

~~~python
import tkinter as tk

root = tk.Tk()
root.title("My First App")
root.geometry("500x350")
root.configure(bg="lightblue")

title = tk.Label(
    root,
    text="안녕하세요!",
    font=("Arial", 24, "bold"),
    bg="lightblue",
    fg="blue",
)
title.pack(pady=30)

root.mainloop()
~~~

설명할 속성: text(내용), font(글꼴/크기/굵기), bg(배경), fg(글자색), pady(세로 여백).

실험: title.pack()을 주석 처리하면 왜 글자가 보이지 않을까?

## 실습 3: 자기소개 앱 완성 예제

~~~python
import tkinter as tk

root = tk.Tk()
root.title("나의 첫 번째 앱")
root.geometry("520x360")
root.configure(bg="#EAF4FF")

title = tk.Label(
    root, text="안녕하세요!",
    font=("Arial", 26, "bold"),
    fg="#1455A0", bg="#EAF4FF",
)
title.pack(pady=(30, 15))

name = tk.Label(
    root, text="저는 로보타그램 학생입니다.",
    font=("Arial", 18),
    fg="#1E293B", bg="#EAF4FF",
)
name.pack(pady=10)

intro = tk.Label(
    root, text="저는 로봇과 프로그래밍을 좋아합니다.",
    font=("Arial", 13),
    fg="#475569", bg="#EAF4FF",
)
intro.pack(pady=10)

footer = tk.Label(
    root, text="Python + Tkinter",
    font=("Arial", 12, "bold"),
    bg="#D0E6FF", fg="#1455A0",
    padx=35, pady=15,
)
footer.pack(pady=20)

root.mainloop()
~~~

학생 수정 포인트: 프로그램 제목, 소개 이름(가명 가능), 취미, 배경색, 폰트 크기, 여백.

## 실습 미션 카드

| 수준 | 미션 | 성공 기준 |
|---|---|---|
| 기본 | 제목·배경·글자색 변경 | 실행 화면에 반영 |
| 기본 | 자신의 소개 문구로 변경 | 문자열 수정 위치를 설명 |
| 응용 | Label 하나 추가 | 자신이 만든 위젯이 표시됨 |
| 응용 | 여백과 글자 크기 조절 | 겹침 없이 읽힘 |
| 도전 | 소개 항목 5개 디자인 | 내용과 레이아웃을 구분 |
| 도전 | 창 크기 변경에도 보기 좋게 수정 | 직접 창 크기를 바꿔 테스트 |

## 교사 확인 질문

- Tk()는 어떤 역할인가? → 프로그램 창 생성
- Label은 어떤 역할인가? → 글자/이미지 등 화면 요소 표시
- pack()이 없으면? → 해당 위젯이 배치되지 않음
- mainloop()는? → 화면과 이벤트를 처리하며 앱이 실행되게 함

## 대표 오류와 지도

| 증상 | 확인할 점 |
|---|---|
| 창이 안 보임 | Thonny 뒤에 창이 숨었는지, 인터프리터가 데스크톱 Python인지 |
| 글자가 안 보임 | Label 생성 이후 pack() 호출 여부 |
| NameError | 변수 이름 오타·선언 순서 |
| TclError | 잘못된 색상/속성, 괄호·따옴표 |
| 화면 밖으로 글자가 나감 | 창 크기, 글자 크기, padx/pady |

## 포트폴리오(학생 작성 4문장)

1. 오늘 만든 프로그램: __________
2. 배운 명령어 중 하나와 역할: __________
3. 내가 직접 바꾼 코드: __________
4. 다음 시간에 추가하고 싶은 기능: __________

프로그램 실행 화면을 캡처해서 첨부한다. 개인 정보는 공개하지 않는다.

## 다음 차시 예고

'오늘은 화면에 글자를 표시했다. 버튼을 누를 때마다 숫자가 바뀌게 하려면?'
→ 2차시 Button, command, 클릭 카운터로 연결.

[ Tkinter 12차시 커리큘럼 ](README.md)
