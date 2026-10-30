"""메시지 검증 테스트: 브로커·GUI·실물 로봇 없이 실행 가능."""
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "examples" / "mqtt-iot"))
from protocol import make_command, parse_command, topic  # noqa: E402


class ProtocolTests(unittest.TestCase):
    def test_topic(self):
        self.assertEqual(topic("class01", "robot01", "cmd"),
                         "robottagram/class01/robot01/cmd")
        with self.assertRaises(ValueError):
            topic("class/#", "robot01", "cmd")

    def test_command_valid(self):
        obj = make_command("forward")
        self.assertEqual(parse_command(json.dumps(obj))["action"], "forward")

    def test_stop(self):
        obj = make_command("stop")
        self.assertEqual((obj["duration_ms"], obj["speed_pct"]), (0, 0))

    def test_reject_stale(self):
        obj = make_command("forward")
        obj["sent_at"] -= 10
        with self.assertRaises(ValueError):
            parse_command(json.dumps(obj))

    def test_reject_overspeed(self):
        obj = make_command("forward")
        obj["speed_pct"] = 100
        with self.assertRaises(ValueError):
            parse_command(json.dumps(obj))

    def test_reject_bad_action(self):
        obj = make_command("forward")
        obj["action"] = "arbitrary_python"
        with self.assertRaises(ValueError):
            parse_command(json.dumps(obj))

    def test_reject_garbage(self):
        with self.assertRaises(ValueError):
            parse_command(b"not-json")


if __name__ == "__main__":
    unittest.main()
