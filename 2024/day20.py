from typing import List

from file_utils import file_reader
from utils import grid
from utils.IntPoint import IntPoint

DIRS: List[IntPoint] = [
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(-1, 0),
    IntPoint(1, 0),
]


def find_shortest_path_with_cheats(race_map: List[str], to_save: int = 100) -> int:
    start_p: IntPoint = grid.find_first_char(race_map, 'S')
    end_p: IntPoint = grid.find_first_char(race_map, 'E')

    distances = __calculate_dist_from_the_end(start_p, end_p, race_map)

    counter = 0
    for p, dist in distances.items():
        for d in DIRS:
            n: IntPoint = p + d
            if grid.char_at(race_map, n.x, n.y) == '#':
                nn: IntPoint = n + d
                nn_dist = distances.get(nn)
                if nn_dist is not None and nn_dist - dist - 2 >= to_save:
                    counter += 1

    return counter


def find_shortest_path_with_20_cheats(race_map: List[str], to_save: int = 100) -> int:
    start_p: IntPoint = grid.find_first_char(race_map, 'S')
    end_p: IntPoint = grid.find_first_char(race_map, 'E')

    distances = __calculate_dist_from_the_end(start_p, end_p, race_map)

    offsets = []
    for y in range(-20, 21):
        for x in range(-20, 21):
            m = abs(x) + abs(y)
            if 1 < m <= 20:
                offsets.append((IntPoint(x, y), m))

    counter = 0
    for p, dist in sorted(distances.items(), key=lambda d: d[1], reverse=True):
        if dist <= to_save:
            break
        for o, o_dist in offsets:
            n: IntPoint = p + o
            n_dist = distances.get(n)
            if n_dist is not None and dist - n_dist - o_dist >= to_save:
                counter += 1
    return counter


def __calculate_dist_from_the_end(cur: IntPoint, end: IntPoint, race_map: list[str]) -> dict[IntPoint, int]:
    distances: dict[IntPoint, int] = {cur: 0}
    cur_dist = 0
    prev = None
    while cur != end and cur is not None:
        n = __find_valid_neighbour(race_map, cur, prev)
        if n is not None:
            cur_dist += 1
            distances[n] = cur_dist
            prev = cur
            cur = n
    if cur == end and end not in distances:
        distances[end] = cur_dist
    return distances


def __find_valid_neighbour(race_map: List[str], cur: IntPoint, prev: IntPoint) -> IntPoint | None:
    for d in DIRS:
        n = cur + d
        if n == prev:
            continue
        b = grid.char_at(race_map, n.x, n.y)
        if b == '.' or b == 'E':
            return n
    return None


test_data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

SOLUTION_INPUT = file_reader.read_str_from_file("input/day20.txt")

assert find_shortest_path_with_cheats(test_data.splitlines(), to_save=63) == 1
assert find_shortest_path_with_cheats(test_data.splitlines(), to_save=11) == 8
assert find_shortest_path_with_cheats(SOLUTION_INPUT) == 1389

assert find_shortest_path_with_20_cheats(test_data.splitlines(), to_save=75) == 3
assert find_shortest_path_with_20_cheats(test_data.splitlines(), to_save=73) == 7
assert find_shortest_path_with_20_cheats(SOLUTION_INPUT) == 1005068
