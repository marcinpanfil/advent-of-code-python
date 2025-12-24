from typing import List

from file_utils import file_reader
from utils import grid
from utils.IntPoint import IntPoint

DIRS: List[IntPoint] = [
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(1, 1),
    IntPoint(1, -1),
    IntPoint(1, 0),
    IntPoint(-1, -1),
    IntPoint(-1, 1),
    IntPoint(-1, 0),
]


def count_accessible_roll_papers(input: List[str]) -> int:
    result = 0
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            cur = grid.char_at(input, x, y)
            if cur == '.':
                continue
            adjacent = 0
            for d in DIRS:
                if grid.char_at(input, x + d.x, y + d.y) == '@':
                    adjacent += 1
            if adjacent < 4:
                result += 1
    return result

def count_removed_roll_papers(input: List[str]) -> int:
    result = 0

    valid = {
        (x, y)
        for y, line in enumerate(input)
        for x, c in enumerate(line)
        if c != '.'
    }

    while valid:
        removed = set()
        for x, y in valid:
            cur = grid.char_at(input, x, y)
            if cur == '.':
                continue

            adjacent = 0
            for d in DIRS:
                if grid.char_at(input, x + d.x, y + d.y) == '@':
                    adjacent += 1
            if adjacent < 4:
                grid.replace_char(input, x, y, '.')
                removed.add((x, y))
        result += len(removed)

        valid = {
            (x + d.x, y + d.y)
            for x, y in removed
            for d in DIRS
            if grid.char_at(input, x + d.x, y + d.y) == '@'
        }

    return result

test_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day04.txt')

assert count_accessible_roll_papers(test_data.splitlines()) == 13
assert count_accessible_roll_papers(SOLUTION_INPUT) == 1435
assert count_removed_roll_papers(test_data.splitlines()) == 43
assert count_removed_roll_papers(SOLUTION_INPUT) == 8623
