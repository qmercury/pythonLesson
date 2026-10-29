"""예제 36개 존재 여부 및 파이썬 문법 검사 (GUI 실행 없이 확인)."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOTAL = 0

for course in ("turtle", "tkinter", "flet"):
    folder = ROOT / "examples" / course
    files = sorted(folder.glob("lesson-??.py"))
    expected = [f"lesson-{n:02d}.py" for n in range(1, 13)]
    actual = [file.name for file in files]
    assert actual == expected, f"{course}: expected {expected}, got {actual}"
    for file in files:
        ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
    TOTAL += len(files)
    print(f"{course}: {len(files)} files, Python syntax OK")

assert TOTAL == 36
print("PASS: 36 lesson examples")
