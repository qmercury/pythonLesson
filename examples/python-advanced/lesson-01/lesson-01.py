from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cleaner_core import load_room, start_position, floor_cells, cleaning_percent, show_room

room = load_room(level=1)
position = start_position(room)
cleaned = {position}

# 여기에 코드를 작성하세요.

show_room(room, cleaned, position)
print('청소율:', cleaning_percent(room, cleaned), '%')
