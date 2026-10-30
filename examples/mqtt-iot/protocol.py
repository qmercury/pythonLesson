"""MQTT 로봇 제어용 안전한 메시지 형식 (표준 라이브러리만 사용)."""
import json
import re
import time
import uuid

ALLOWED = {"forward", "backward", "left", "right", "stop"}
NAME = re.compile(r"^[a-zA-Z0-9_-]{1,32}$")
MAX_AGE_SECONDS = 2.0
MAX_DURATION_MS = 300
MAX_SPEED_PERCENT = 30


def topic(room, robot, kind):
    """수업실/로봇을 분리하여 MQTT 토픽을 만듭니다."""
    if not NAME.fullmatch(room) or not NAME.fullmatch(robot):
        raise ValueError("room과 robot은 영문/숫자/_/- 1~32자여야 합니다.")
    if kind not in {"cmd", "status", "chat"}:
        raise ValueError("알 수 없는 토픽 종류입니다.")
    return f"robottagram/{room}/{robot}/{kind}"


def make_command(action, duration_ms=200, speed_pct=20):
    if action not in ALLOWED:
        raise ValueError("허용되지 않은 동작")
    if action == "stop":
        duration_ms, speed_pct = 0, 0
    elif not (100 <= duration_ms <= MAX_DURATION_MS and
              1 <= speed_pct <= MAX_SPEED_PERCENT):
        raise ValueError("교육용 속도 또는 동작 시간 제한 초과")
    return {
        "v": 1, "id": uuid.uuid4().hex,
        "sent_at": time.time(), "action": action,
        "duration_ms": duration_ms, "speed_pct": speed_pct,
    }


def parse_command(payload, now=None):
    """유효하고 최근에 전송된 명령만 통과시킵니다."""
    if len(payload) > 1024:
        raise ValueError("메시지가 너무 깁니다.")
    try:
        obj = json.loads(payload)
    except (TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("JSON 형식 오류") from exc
    if not isinstance(obj, dict) or obj.get("v") != 1:
        raise ValueError("프로토콜 버전 오류")
    mid = obj.get("id")
    if not isinstance(mid, str) or not re.fullmatch(r"[0-9a-f]{32}", mid):
        raise ValueError("메시지 ID 오류")
    sent_at = obj.get("sent_at")
    if isinstance(sent_at, bool) or not isinstance(sent_at, (int, float)):
        raise ValueError("시간 형식 오류")
    age = (time.time() if now is None else now) - sent_at
    if not (-1 <= age <= MAX_AGE_SECONDS):
        raise ValueError("오래된 명령 또는 시간 불일치")
    action = obj.get("action")
    if action not in ALLOWED:
        raise ValueError("알 수 없는 동작")
    duration, speed = obj.get("duration_ms"), obj.get("speed_pct")
    if isinstance(duration, bool) or not isinstance(duration, int) or (
            isinstance(speed, bool) or not isinstance(speed, int)):
        raise ValueError("속도/동작 시간 형식 오류")
    if action == "stop":
        if duration != 0 or speed != 0:
            raise ValueError("정지 명령 형식 오류")
    elif not (100 <= duration <= MAX_DURATION_MS and 1 <= speed <= MAX_SPEED_PERCENT):
        raise ValueError("안전 범위 밖의 명령")
    return obj


def status_payload(state, detail):
    return json.dumps({
        "v": 1, "state": state, "detail": detail,
        "sent_at": time.time(),
    }, ensure_ascii=False)
