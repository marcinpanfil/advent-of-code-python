from typing import List, Dict, Set

from file_utils import file_reader
from utils.IntPoint import IntPoint

DIRS: List[IntPoint] = [
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(1, 0),
    IntPoint(-1, 0),
]


def calculate_total_price(plants: List[str]) -> (int, int):
    regions_by_plot: Dict[str, List[(int, int)]] = __calculate_all_regions(plants)
    total_1 = 0
    total_2 = 0
    for plot, regions in regions_by_plot.items():
        for idx, (size, perimeter, plants) in enumerate(regions):
            total_1 += size * perimeter
            total_2 += size * __calculate_sides(plants)
    return total_1, total_2


def __calculate_all_regions(plants: List[str]) -> (int, int, Set[IntPoint]):
    visited = [[False] * len(plants[0]) for _ in range(len(plants))]
    results: Dict[str, List[(int, int, Set[IntPoint])]] = {}

    def dfs(pos_x: int, pos_y: int, curr_plant: str) -> (int, int, Set[IntPoint]):
        if pos_y < 0 or pos_y >= len(plants) or pos_x < 0 or pos_x >= len(plants[0]):
            return 0, 1, set()
        if plants[pos_y][pos_x] != curr_plant:
            return 0, 1, set()
        if visited[pos_y][pos_x]:
            return 0, 0, set()

        visited[pos_y][pos_x] = True
        s: int = 1
        p: int = 0
        ps: Set[IntPoint] = {IntPoint(pos_x, pos_y)}

        for d in DIRS:
            adj_size, adj_perimeter, adj_plants = dfs(pos_x + d.x, pos_y + d.y, curr_plant)
            s += adj_size
            p += adj_perimeter
            ps |= adj_plants

        return s, p, ps

    for y in range(len(plants)):
        for x in range(len(plants[0])):
            if not visited[y][x]:
                plant: str = plants[y][x]
                size, perimeter, plants_in_region = dfs(x, y, plant)
                if plant not in results:
                    results[plant] = []
                results[plant].append((size, perimeter, plants_in_region))

    return results


def __calculate_sides(plants: Set[IntPoint]) -> int:
    ups = downs = lefts = rights = 0

    for point in plants:
        left_x, right_x = point.x - 1, point.x + 1
        above_y, below_y = point.y - 1, point.y + 1

        is_left_in_region = IntPoint(left_x, point.y) in plants
        is_right_in_region = IntPoint(right_x, point.y) in plants
        is_above_in_region = IntPoint(point.x, above_y) in plants
        is_below_in_region = IntPoint(point.x, below_y) in plants

        if not is_above_in_region and (not is_right_in_region or IntPoint(right_x, above_y) in plants):
            ups += 1

        if not is_below_in_region and (not is_right_in_region or IntPoint(right_x, below_y) in plants):
            downs += 1

        if not is_left_in_region and (not is_below_in_region or IntPoint(left_x, below_y) in plants):
            lefts += 1

        if not is_right_in_region and (not is_below_in_region or IntPoint(right_x, below_y) in plants):
            rights += 1

    return ups + downs + lefts + rights


TEST_INPUT_1 = """AAAA
BBCD
BBCC
EEEC"""

TEST_INPUT_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

TEST_INPUT_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

TEST_INPUT_4 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

TEST_INPUT_5 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day12.txt')

assert calculate_total_price(TEST_INPUT_1.splitlines()) == (140, 80)
assert calculate_total_price(TEST_INPUT_2.splitlines()) == (772, 436)
assert calculate_total_price(TEST_INPUT_3.splitlines()) == (1930, 1206)
assert calculate_total_price(TEST_INPUT_4.splitlines()) == (1184, 368)
assert calculate_total_price(TEST_INPUT_5.splitlines()) == (692, 236)
assert calculate_total_price(SOLUTION_INPUT) == (1518548, 909564)
