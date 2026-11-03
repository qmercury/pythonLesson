# Python 심화 — 학생용 예제

이 폴더에는 실제 로봇청소기 구동 코드가 아닌, **Thonny 데스크톱 Python으로 실행하는 자료구조·알고리즘·GUI·MQTT 연습**이 있습니다.

## 파일 사용법

1. 학생 개인 `pythonLesson` 폴더에서 `git pull`합니다.
2. 예: `lesson-01/lesson-01.py`를 Thonny로 엽니다.
3. 같은 폴더에 `main.py`로 복사해 저장하고 `# 여기에 코드를 작성하세요.` 아래를 작성합니다.
4. 수업별로 폴더가 분리되어 있어 다른 차시 `main.py`를 덮어쓰지 않습니다.
5. `cleaner_core.py`와 `sample_runs.py`는 수정하지 않습니다.

**1~7차시** Python 3.10 이상, Tkinter가 포함된 일반 Python을 사용합니다.  
**8차시** 두 컴퓨터, 교실 MQTT 브로커, `paho-mqtt>=2,<3` 패키지 설치가 필요합니다. 기본 템플릿의 브로커 주소는 예시입니다.

### 공통 지도 표시
- `D`: 충전기
- `#`: 장애물
- `.`: 청소 전 바닥
- `*`: 청소 완료 바닥
- `R`: 현재 로봇 위치

### 파일 목록

| 수업 | 파일 | 구현 목표 |
|---:|---|---|
| 01 | `lesson-01/lesson-01.py` | 집합으로 청소 칸 기록 |
| 02 | `lesson-02/lesson-02.py` | DFS + 백트래킹 탐색 |
| 03 | `lesson-03/lesson-03.py` | BFS 최단 경로 |
| 04 | `lesson-04/lesson-04.py` | 이동 기록 분석 |
| 05 | `lesson-05/lesson-05.py` | JSON 파일 저장·복구 |
| 06 | `lesson-06/lesson-06.py` | Tkinter Canvas 지도 |
| 07 | `lesson-07/lesson-07.py` | after() 자동 동작·정지 |
| 08 | `lesson-08/lesson-08.py` | MQTT 원격 명령 |

[전체 이론과 미션](../../curriculum/python-advanced/README.md)

8차시는 PC A에서 `lesson-08-sender.py`를 `sender.py`로 복사해 명령을 보내고, PC B에서 `lesson-08.py`를 `main.py`로 복사해 상태를 처리합니다. 두 파일의 `HOST`, `TOPIC` 설정이 같아야 합니다.
