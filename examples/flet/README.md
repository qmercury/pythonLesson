# Flet — 12차시 예제 모음 (교육과정 초안)

**중요:** Flet은 설치 버전에 따라 API가 바뀔 수 있습니다. 아래 예제는 2026-10-29 기준 공식 문서에 나온 `ft.run`, `ft.Button`, `ft.TextField` 등 최신 형태를 참고했습니다. **실제 학생 PC/휴대폰에서 전체 12개 실행 검증은 아직 수행하지 않았습니다.**

## 실행 준비

1. Thonny가 선택한 일반 PC Python이 **Flet이 지원하는 버전인지** 확인합니다 (공식 안내상 Python 3.10+).
2. Thonny **도구 → 패키지 관리**에서 `flet`을 설치합니다.
3. `lesson-01.py`부터 열어 F5로 실행합니다.
4. 같은 Python 환경의 터미널에서는 `flet run <파일명>`으로 실행할 수 있습니다.
5. 모바일 테스트는 Flet 모바일 앱과 같은 Wi-Fi 연결, 방화벽 점검 및 별도의 `flet run --android` 또는 `--ios` 실행이 필요합니다.
6. 모바일 미리보기는 독립 APK/IPA 설치 파일을 만드는 것과 다릅니다.

## 예제 목록

| 차시 | 파일 | 동작 |
|---:|---|---|
| 01 | [lesson-01.py](lesson-01.py) | 첫 Flet 소개 앱 |
| 02 | [lesson-02.py](lesson-02.py) | 버튼 클릭 카운터 |
| 03 | [lesson-03.py](lesson-03.py) | 입력창과 인사말 |
| 04 | [lesson-04.py](lesson-04.py) | Row/Column 프로필 UI |
| 05 | [lesson-05.py](lesson-05.py) | 입력 검증 계산기 |
| 06 | [lesson-06.py](lesson-06.py) | 객관식 퀴즈 |
| 07 | [lesson-07.py](lesson-07.py) | 메뉴/퀴즈 두 화면 |
| 08 | [lesson-08.py](lesson-08.py) | 할 일 목록 |
| 09 | [lesson-09.py](lesson-09.py) | SharedPreferences 메모 저장 |
| 10 | [lesson-10.py](lesson-10.py) | 반응형 모바일 화면 |
| 11 | [lesson-11.py](lesson-11.py) | 로봇축구 점수판 시작 코드 |
| 12 | [lesson-12.py](lesson-12.py) | 팀 이름 변경과 승리 판정 점수판 |

## 지도시 주의

- [공식 Flet 문서](https://flet.dev/docs/)를 사용하여 수업 시작 전에 해당 버전을 확정하고 예제를 테스트합니다.
- 저장소 API와 모바일 앱의 로컬 저장 정책은 다를 수 있습니다. 학생의 실명·개인정보를 저장하지 않습니다.
- GUI 동작, 모바일 QR 연결, 앱 패키징은 단순 Python 구문 검사로 보증되지 않습니다.
- 10차시를 위해 휴대폰과 PC가 같은 네트워크에서 서로 접근 가능한지 먼저 점검합니다.

[커리큘럼으로 돌아가기](../../curriculum/flet/README.md)
