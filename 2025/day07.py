from typing import List

from file_utils import file_reader


def count_splits(manifold: List[str]) -> int:
    idx: int = manifold[0].index('S')

    result = 0
    cur_beams = set()
    cur_beams.add(idx)
    for line in manifold[1:]:
        next_beams = set()
        for cur_beam in cur_beams:
            if line[cur_beam] == '^':
                if cur_beam - 1 >= 0:
                    next_beams.add(cur_beam - 1)
                if cur_beam + 1 < len(manifold):
                    next_beams.add(cur_beam + 1)
                result += 1
            else:
                next_beams.add(cur_beam)
        if next_beams:
            cur_beams = next_beams
    return result


def count_timelines(manifold: List[str]) -> int:
    idx: int = manifold[0].index('S')

    cur_beams = {idx: 1}
    for line in manifold[1:]:
        next_beams = {}
        for cur_beam, count in cur_beams.items():
            if line[cur_beam] == '^':
                if cur_beam - 1 >= 0:
                    next_beams[cur_beam - 1] = next_beams.get(cur_beam - 1, 0) + count
                if cur_beam + 1 < len(manifold):
                    next_beams[cur_beam + 1] = next_beams.get(cur_beam + 1, 0) + count
            else:
                next_beams[cur_beam] = next_beams.get(cur_beam, 0) + count
        if next_beams:
            cur_beams = next_beams

    return sum(cur_beams.values())


test_data = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day07.txt')

assert count_splits(test_data.splitlines()) == 21
assert count_splits(SOLUTION_INPUT) == 1516
assert count_timelines(test_data.splitlines()) == 40
assert count_timelines(SOLUTION_INPUT) == 1393669447690