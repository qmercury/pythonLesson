import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cleaner_core import load_room, start_position, show_room

room = load_room(level=1)
dock = start_position(room)
route = [dock, (1, 4), (2, 4), (3, 4)]
filename = Path(__file__).with_name('cleaning_record.json')

# 여기에 코드를 작성하세요.
