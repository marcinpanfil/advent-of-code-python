from collections import deque
from typing import List, Set

from file_utils import file_reader
from utils.IntPoint import IntPoint

DIRS: List[IntPoint] = [
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(1, 0),
    IntPoint(-1, 0),
]


def find_all_paths(topo_map: List[str]) -> int:
    starts, _ = __find_start_end_points(topo_map)

    counter = 0
    for start in starts:
        counter += __find_path(topo_map, start)
    return counter

def count_all_possible_paths(topo_map: List[str]) -> int:
    starts, ends = __find_start_end_points(topo_map)

    counter = 0
    for start in starts:
        for end in ends:
            counter += __find_all_paths_between_two_points(topo_map, start, end)

    return counter

def __find_all_paths_between_two_points(topo_map: List[str], start: IntPoint, end: IntPoint) -> int:
    queue: deque[(IntPoint, List[IntPoint])] = deque([(start, [start])])
    all_paths: List[List[IntPoint]] = []

    while len(queue) > 0:
        current, path = queue.popleft()

        if current == end:
            all_paths.append(path)
            continue

        next_steps = __get_possible_steps(topo_map, current)
        for next_step in next_steps:
            if next_step in path:
                continue

            queue.append((next_step, path + [next_step]))

    return len(all_paths)

def __find_path(topo_map: List[str], start: IntPoint) -> int:
    visited: Set[IntPoint] = set()
    queue: deque[IntPoint] = deque([start])
    total = 0
    while len(queue) > 0:
        current = queue.popleft()
        next_steps = __get_possible_steps(topo_map, current)

        for next_step in next_steps:
            if next_step in visited:
                continue
            if topo_map[next_step.y][next_step.x] == '9':
                total += 1
            visited.add(next_step)
            queue.append(next_step)
    return total


def __get_possible_steps(topo_map: List[str], point: IntPoint) -> List[IntPoint]:
    result: List[IntPoint] = []

    for d in DIRS:
        next_x = point.x + d.x
        next_y = point.y + d.y
        if 0 <= next_x < len(topo_map) and 0 <= next_y < len(topo_map):
            diff = int(topo_map[next_y][next_x]) - int(topo_map[point.y][point.x])
            if diff == 1:
                result.append(IntPoint(next_x, next_y))

    return result


def __find_start_end_points(topo_map: List[str]) -> (List[IntPoint], List[IntPoint]):
    starts: List[IntPoint] = []
    ends: List[IntPoint] = []

    for y, line in enumerate(topo_map):
        for x, c in enumerate(line):
            if c == '0':
                starts.append(IntPoint(x, y))
            if c == '9':
                ends.append(IntPoint(x, y))

    return starts, ends


TEST_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day10.txt')

assert find_all_paths(TEST_INPUT.splitlines()) == 36
assert find_all_paths(SOLUTION_INPUT) == 459
assert count_all_possible_paths(TEST_INPUT.splitlines()) == 81
assert count_all_possible_paths(SOLUTION_INPUT) == 1034
