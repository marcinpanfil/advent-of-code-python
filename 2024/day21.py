from collections import Counter
from functools import lru_cache
from typing import List

DIRECTIONAL_KEYPAD = [" ^A", "<v>"]

NUMERIC_KEYPAD = ["789", "456", "123", " 0A"]


def calculate_complexities(codes: List[str], nr_dir_keypads: int = 2) -> int:
    res: int = 0
    for c in codes:
        moves = __count_min_moves(c, nr_dir_keypads)
        res += moves
    return res


def __count_min_moves(code: str, nr_dir_keypads: int = 2) -> int:
    segment_counts = Counter()

    prev_c: str = 'A'
    for c in code:
        path = __get_shortest_path(prev_c, c, NUMERIC_KEYPAD)
        segment_counts[('A', path)] += 1
        prev_c = c

    for _ in range(nr_dir_keypads):
        new_counts = Counter()
        for (start, segment), count in segment_counts.items():
            prev = start
            for char in segment:
                path = __get_shortest_path_for_dir_keypad(prev, char)
                new_counts[('A', path)] += count
                prev = char
        segment_counts = new_counts

    total_length = sum(len(segment) * count for (_, segment), count in segment_counts.items())
    return total_length * int(code[:-1])


@lru_cache
def __get_shortest_path_for_dir_keypad(from_key: str, to_key: str) -> str:
    return __get_shortest_path(from_key, to_key, DIRECTIONAL_KEYPAD)


def __get_shortest_path(from_key: str, to_key: str, keypad: List[str]) -> str:
    from_pos = __get_position(from_key, keypad)
    to_pos = __get_position(to_key, keypad)
    gap = __get_position(' ', keypad)

    if from_pos == to_pos:
        return 'A'

    row_diff = to_pos[0] - from_pos[0]
    col_diff = to_pos[1] - from_pos[1]

    vertical = ('^' * -row_diff if row_diff < 0 else 'v' * row_diff)
    horizontal = ('<' * -col_diff if col_diff < 0 else '>' * col_diff)

    if col_diff < 0:
        path = horizontal + vertical + 'A'
        if not __crosses_gap(from_pos, path, gap):
            return path

    path = vertical + horizontal + 'A'
    if not __crosses_gap(from_pos, path, gap):
        return path

    return horizontal + vertical + 'A'


@lru_cache
def __crosses_gap(start_pos: tuple[int, int], path: str, gap: tuple[int, int]) -> bool:
    row, col = start_pos

    for move in path[:-1]:
        if move == '<':
            col -= 1
        elif move == '>':
            col += 1
        elif move == '^':
            row -= 1
        elif move == 'v':
            row += 1

        if (row, col) == gap:
            return True

    return False


def __get_position(key: str, keypad: List[str]) -> tuple[int, int] | None:
    for row, line in enumerate(keypad):
        for col, char in enumerate(line):
            if char == key:
                return row, col
    return None


test_data = ["029A", "980A", "179A", "456A", "379A"]
SOLUTION_INPUT = ["140A", "170A", "169A", "803A", "129A"]

assert calculate_complexities(test_data) == 126384
assert calculate_complexities(SOLUTION_INPUT) == 105458

assert calculate_complexities(SOLUTION_INPUT, nr_dir_keypads=25) == 129551515895690
