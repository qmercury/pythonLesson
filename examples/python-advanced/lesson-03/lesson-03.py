from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from collections import deque
from cleaner_core import load_room, start_position, neighbors

room = load_room(level=2)
start = (6, 0)
goal = start_position(room)
queue = deque([start])
previous = {start: None}
path = []

# 여기에 코드를 작성하세요.

print('출발:', start)
print('목표:', goal)
print('최단 경로:', path)
print('이동 횟수:', max(0, len(path) - 1))
