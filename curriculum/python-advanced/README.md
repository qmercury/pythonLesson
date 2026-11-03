# 로보타그램 Python 심화 — 데이터로 움직이는 로봇 (8차시)

대상: SPIKE Prime Python 기초 및 Turtle 미로 탐색을 마친 초등 4~6학년 학생  
수업: 90분 × 8차시  
환경: Thonny + Python 3.10 이상 (1~7차시 표준 라이브러리만 사용)

| 차시 | 주제 | 핵심 개념 | 결과물 |
|---|---|---|---|
| [01](lessons/lesson-01.md) | 청소 지도 만들기 | 2차원 리스트, 튜플, 집합 | 청소율 계산 |
| [02](lessons/lesson-02.md) | 전체 공간 탐색 | DFS, 스택, 백트래킹 | 모든 칸 방문 후 충전기 복귀 |
| [03](lessons/lesson-03.md) | 충전기 최단 경로 | 큐, BFS, 딕셔너리 | 최단 경로 좌표 목록 |
| [04](lessons/lesson-04.md) | 청소 기록 분석 | 딕셔너리, 중복, 평균 | 알고리즘 성능표 |
| [05](lessons/lesson-05.md) | 기록 저장·복구 | JSON, 파일 입출력 | cleaning_record.json |
| [06](lessons/lesson-06.md) | 청소 지도 UI | Tkinter, Canvas, 이벤트 | 클릭형 청소 대시보드 |
| [07](lessons/lesson-07.md) | 자동 실행과 상태 | after(), 이벤트 루프 | 시작·일시정지·초기화 |
| [08](lessons/lesson-08.md) | 원격 상태 제어 | MQTT, publish/subscribe | PC↔PC 가상 청소 명령 |

### 수업 운영

- 도입·문제 제시 10분 / 이론 20분 / 교사 시연 15분 / 학생 구현 30분 / 심화·검증 15분
- 학생 파일은 `lesson-XX.py`를 같은 차시 폴더에 `main.py`로 복사해서 사용합니다.
- 주석은 코드 작성 위치를 알려주는 한 줄만 남겨 두었습니다. 이론은 차시별 문서에 있습니다.
- `main.py`는 Git 추적에서 제외하여 다음 `git pull`에 의해 덮어써지지 않도록 합니다.
- 이번 과정은 Thonny의 데스크톱 Python 시뮬레이터입니다. SPIKE Prime 허브에서 그대로 실행되는 코드가 아닙니다.
- 제8차시는 교실 MQTT 브로커와 paho-mqtt 2.x 설치가 필요하며 실제 모터 제어가 아닌 시뮬레이터 상태 제어입니다.

[학생 예제 폴더](../../examples/python-advanced/README.md)

**주의:** 8차시 발행기와 수신기는 각각 자기 학생용 파일로 복사해 설정하세요. MQTT 비밀번호는 GitHub에 올리지 마세요.
