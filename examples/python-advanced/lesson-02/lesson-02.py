from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cleaner_core import load_room, start_position, neighbors, floor_cells, show_room

room = load_room(level=1)
dock = start_position(room)
visited = {dock}
stack = [dock]
route = [dock]

# 여기에 코드를 작성하세요.

show_room(room, visited, dock)
print('방문한 칸:', len(visited), '/', len(floor_cells(room)))
print('주행 기록:', route)
