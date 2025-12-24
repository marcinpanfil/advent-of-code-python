import math
from typing import List

from file_utils import file_reader


def count_pos_0(data: List[str]) -> int:
    cur_pos = 50
    counter = 0
    for rotation in data:
        dir = 1 if rotation[0] == 'R' else -1
        rot = int(rotation[1:])
        cur_pos = (cur_pos + (dir * rot)) % 100

        if cur_pos == 0:
            counter += 1
    return counter


def count_pos_0_and_dials(data: List[str]) -> int:
    cur_pos = 50
    counter = 0
    for rotation in data:
        dir = 1 if rotation[0] == 'R' else -1
        rot = int(rotation[1:])
        old_pos = cur_pos
        new_pos = cur_pos + dir * rot
        cur_pos = new_pos % 100
        full_rot = abs(new_pos) // 100

        if cur_pos == 0:
            if full_rot > 0:
                if math.copysign(1, new_pos) != math.copysign(1, cur_pos) and old_pos != 0:
                    counter += 1
                counter += full_rot
            else:
                counter += 1
        else:
            if math.copysign(1, new_pos) != math.copysign(1, cur_pos) and old_pos != 0:
                counter += 1
            counter += full_rot
    return counter


test_case = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

test_case_1 = """L200
L50"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day01.txt')

assert count_pos_0(test_case.split('\n')) == 3
assert count_pos_0(test_case_1.split('\n')) == 1
assert count_pos_0(SOLUTION_INPUT) == 995

assert count_pos_0_and_dials(test_case.split('\n')) == 6
assert count_pos_0_and_dials(test_case_1.split('\n')) == 3
assert count_pos_0_and_dials(SOLUTION_INPUT) == 5847
