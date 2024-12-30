import math
import re
from collections import defaultdict
from typing import Tuple, List, Dict

from file_utils import file_reader
from utils.IntPoint import IntPoint


def calculate_safety_factor(data: List[str], wide: int, tall: int) -> int:
    robots: List[Tuple[IntPoint, IntPoint]] = __parse_input(data)
    __move_robots_by_n_seconds(robots, wide, tall)
    return __calculate_factor(robots, wide, tall)


def find_christmas_tree(data: List[str]) -> int:
    robots: List[Tuple[IntPoint, IntPoint]] = __parse_input(data)
    __move_robots_by_n_seconds(robots, 101, 103)
    min_value = math.inf
    min_sec: int = 0
    for i in range(100, 101 * 103):
        __move_robots_by_n_seconds(robots, 101, 103, 1)
        factor = __calculate_factor(robots, 101, 103)
        if factor == 0:
            return i
        if min_value >= factor:
            min_value = factor
            min_sec = i
    return min_sec + 1


def __calculate_factor(robots, wide, tall):
    quadrant: Dict[int, int] = defaultdict(int)
    for (position, _) in robots:
        if position.x < (wide // 2) and position.y < (tall // 2):
            quadrant[0] += 1
        elif position.x >= (wide // 2) + 1 and position.y < (tall // 2):
            quadrant[1] += 1
        elif position.x < (wide // 2) and position.y >= (tall // 2) + 1:
            quadrant[2] += 1
        elif position.x >= (wide // 2) + 1 and position.y >= (tall // 2) + 1:
            quadrant[3] += 1
    return quadrant[0] * quadrant[1] * quadrant[2] * quadrant[3]


def __move_robots_by_n_seconds(robots: List[Tuple[IntPoint, IntPoint]], wide: int, tall: int, n: int = 100):
    for i, (position, velocity) in enumerate(robots):
        new_pos: IntPoint = IntPoint((position.x + n * velocity.x) % wide, (position.y + n * velocity.y) % tall)
        robots[i] = (new_pos, velocity)


def __parse_input(data: List[str]) -> List[Tuple[IntPoint, IntPoint]]:
    result: List[Tuple[IntPoint, IntPoint]] = []
    for line in data:
        numbers = re.findall(r'-?\b\d+\b', line)
        result.append((IntPoint(int(numbers[0]), int(numbers[1])),
                       IntPoint(int(numbers[2]), int(numbers[3]))))
    return result


TEST_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day14.txt')

assert calculate_safety_factor(TEST_INPUT.splitlines(), wide=11, tall=7) == 12
assert calculate_safety_factor(SOLUTION_INPUT, 101, 103) == 215987200
assert find_christmas_tree(SOLUTION_INPUT) == 8050
