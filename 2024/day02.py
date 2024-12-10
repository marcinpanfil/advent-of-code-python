from itertools import combinations
from typing import List

from file_utils import file_reader


def count_safe_reports(data: List[str]) -> int:
    result = 0
    for line in data:
        levels = [int(x) for x in line.split(' ') if x.isdigit()]
        if check_if_safe(levels):
            result += 1
    return result


def check_if_safe(levels: List[int]) -> bool:
    is_dec = True
    is_inc = True
    for i in range(len(levels) - 1):
        i1 = levels[i]
        i2 = levels[i + 1]
        if abs(i1 - i2) > 3:
            return False

        if i1 >= i2:
            is_dec = False
        if i1 <= i2:
            is_inc = False

        if not is_dec and not is_inc:
            return False

    if is_inc or is_dec:
        return True

    return False


def count_safe_reports_with_tolerance(data: List[str]) -> int:
    result = 0
    for line in data:
        levels = [int(x) for x in line.split(' ') if x.isdigit()]

        for i in range(len(levels)):
            if check_if_safe(levels[:i] + levels[i + 1:]):
                result += 1
                break

    return result


TEST_CASE = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day02.txt')

assert count_safe_reports(TEST_CASE.split('\n')) == 2
assert count_safe_reports(SOLUTION_INPUT) == 483

assert count_safe_reports_with_tolerance(TEST_CASE.split('\n')) == 4
assert count_safe_reports_with_tolerance(SOLUTION_INPUT) == 528
