from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cleaner_core import load_room, floor_cells
from sample_runs import RUNS

room = load_room(level=1)
total = len(floor_cells(room))

# 여기에 코드를 작성하세요.
