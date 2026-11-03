ROOMS = {
    1: [
        '......',
        '..##..',
        '......',
        '.#....',
        'D.....',
    ],
    2: [
        '.......',
        '.##..#.',
        '.......',
        '...#...',
        '.#.....',
        'D......',
    ],
    3: [
        '........',
        '.##..#..',
        '....#...',
        '..#.....',
        '.....##.',
        '..#.....',
        'D.......',
    ],
}


def load_room(level=1):
    if level not in ROOMS:
        raise ValueError('level은 1, 2, 3 중 하나입니다.')
    return [list(row) for row in ROOMS[level]]


def start_position(room):
    for y, row in enumerate(room):
        for x, value in enumerate(row):
            if value == 'D':
                return (x, y)
    raise ValueError('충전기 D가 없습니다.')


def can_move(room, pos):
    x, y = pos
    return 0 <= y < len(room) and 0 <= x < len(room[y]) and room[y][x] != '#'


def neighbors(room, pos):
    x, y = pos
    candidates = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
    return [p for p in candidates if can_move(room, p)]


def floor_cells(room):
    return {(x, y) for y, row in enumerate(room) for x, cell in enumerate(row) if cell != '#'}


def cleaning_percent(room, cleaned):
    floor = floor_cells(room)
    return round(100 * len(floor.intersection(cleaned)) / len(floor), 1)


def show_room(room, cleaned=None, robot=None):
    cleaned = cleaned or set()
    for y, row in enumerate(room):
        displayed = []
        for x, cell in enumerate(row):
            pos = (x, y)
            if pos == robot:
                displayed.append('R')
            elif cell == '#':
                displayed.append('#')
            elif pos in cleaned:
                displayed.append('*')
            else:
                displayed.append(cell)
        print(' '.join(displayed))
    print()
