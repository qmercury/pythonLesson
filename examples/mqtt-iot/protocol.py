"""MQTT 로봇 제어용 안전한 메시지 형식 (표준 라이브러리만 사용)."""
# 브로커는 메시지를 전달하지만 내용이 안전한지 판단해 주지 않습니다.
# 수신자 B가 반드시 '허용된 명령인지' 검사해야 합니다.
import json
import re
import time
import uuid

# [화이트리스트] 학생이 미리 정한 다섯 동작만 사용할 수 있습니다.
ALLOWED = {"forward", "backward", "left", "right", "stop"}
# 토픽의 room/robot에는 길이 1~32의 안전한 영문·숫자 이름만 허용.
# 와일드카드 기호(+/#)가 섞인 임의 토픽을 만들지 않도록 제한합니다.
NAME = re.compile(r"^[a-zA-Z0-9_-]{1,32}$")
# [제한값] 오래된 명령 또는 과도한 로봇 움직임 요청을 거부합니다.
# 이것만으로 물리 모터가 자동 정지하는 것은 아닙니다.
MAX_AGE_SECONDS = 2.0
MAX_DURATION_MS = 300
MAX_SPEED_PERCENT = 30


# [토픽 생성] "어느 반/어느 로봇/명령 또는 상태"를 문자열로 만듭니다.
def topic(room, robot, kind):
    """수업실/로봇을 분리하여 MQTT 토픽을 만듭니다."""
    # 확인되지 않은 로봇 ID나 특수 문자가 들어오면 오류를 냅니다.
    if not NAME.fullmatch(room) or not NAME.fullmatch(robot):
        raise ValueError("room과 robot은 영문/숫자/_/- 1~32자여야 합니다.")
    if kind not in {"cmd", "status", "chat"}:
        raise ValueError("알 수 없는 토픽 종류입니다.")
    # 예: robottagram/class01/robot01/cmd
    return f"robottagram/{room}/{robot}/{kind}"


# [명령 생성] 송신자 A가 버튼을 누르면 호출합니다.
def make_command(action, duration_ms=200, speed_pct=20):
    # 위험하거나 알려지지 않은 명령은 생성하지 않습니다.
    if action not in ALLOWED:
        raise ValueError("허용되지 않은 동작")
    # STOP에는 동작 시간·속도가 의미 없으므로 모두 0으로 통일합니다.
    if action == "stop":
        duration_ms, speed_pct = 0, 0
    elif not (100 <= duration_ms <= MAX_DURATION_MS and
              1 <= speed_pct <= MAX_SPEED_PERCENT):
        raise ValueError("교육용 속도 또는 동작 시간 제한 초과")
    # v: 메시지 규칙 버전 / id: 매번 달라지는 번호(중복 명령 방지)
    # sent_at: 만든 시각(초) / action: 명령 이름
    # duration_ms: 요청 동작 시간(밀리초) / speed_pct: 요청 속도(%)
    return {
        "v": 1, "id": uuid.uuid4().hex,
        "sent_at": time.time(), "action": action,
        "duration_ms": duration_ms, "speed_pct": speed_pct,
    }


# [명령 해석] 수신자 B가 전달받은 데이터를 반드시 확인합니다.
# invalid 메시지를 그냥 실행하면 실제 로봇에서는 위험할 수 있습니다.
def parse_command(payload, now=None):
    """유효하고 최근에 전송된 명령만 통과시킵니다."""
    # 너무 긴 메시지는 메모리·처리 문제를 줄이기 위해 미리 차단.
    if len(payload) > 1024:
        raise ValueError("메시지가 너무 깁니다.")
    try:
        # JSON 문자열(또는 bytes)을 Python dict로 변환합니다.
        obj = json.loads(payload)
    except (TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("JSON 형식 오류") from exc
    # 자료형과 버전이 맞지 않으면 학생이 만든 규칙과 다르다는 뜻입니다.
    if not isinstance(obj, dict) or obj.get("v") != 1:
        raise ValueError("프로토콜 버전 오류")
    # id는 32개의 16진수 문자열인지 확인합니다.
    mid = obj.get("id")
    if not isinstance(mid, str) or not re.fullmatch(r"[0-9a-f]{32}", mid):
        raise ValueError("메시지 ID 오류")
    sent_at = obj.get("sent_at")
    if isinstance(sent_at, bool) or not isinstance(sent_at, (int, float)):
        raise ValueError("시간 형식 오류")
    # 메시지가 만든 지 너무 오래됐으면 늦게 도착한 전진 명령 등을 거부.
    # PC 간 시간이 크게 다르면 정상 메시지도 거부될 수 있습니다.
    age = (time.time() if now is None else now) - sent_at
    if not (-1 <= age <= MAX_AGE_SECONDS):
        raise ValueError("오래된 명령 또는 시간 불일치")
    # 허용된 다섯 동작만 처리합니다. 어떤 Python 코드도 실행하지 않습니다.
    action = obj.get("action")
    if action not in ALLOWED:
        raise ValueError("알 수 없는 동작")
    # 문자열 '200'과 정수 200은 다릅니다. 타입도 검사합니다.
    duration, speed = obj.get("duration_ms"), obj.get("speed_pct")
    if isinstance(duration, bool) or not isinstance(duration, int) or (
            isinstance(speed, bool) or not isinstance(speed, int)):
        raise ValueError("속도/동작 시간 형식 오류")
    if action == "stop":
        if duration != 0 or speed != 0:
            raise ValueError("정지 명령 형식 오류")
    elif not (100 <= duration <= MAX_DURATION_MS and 1 <= speed <= MAX_SPEED_PERCENT):
        raise ValueError("안전 범위 밖의 명령")
    # 검사 통과! 이제 로봇 제어가 아니라 '검증된 명령 데이터'만 반환합니다.
    return obj


# [상태 회신] 처리 결과를 송신자에게 보내기 쉬운 JSON 문자열로 만듭니다.
def status_payload(state, detail):
    return json.dumps({
        "v": 1, "state": state, "detail": detail,
        "sent_at": time.time(),
    }, ensure_ascii=False)
