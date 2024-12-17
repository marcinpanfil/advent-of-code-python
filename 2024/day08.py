from math import copysign
from typing import List, Dict, Set

from file_utils import file_reader
from utils.IntPoint import IntPoint


def find_unique_antinodes_including_inline(antenna_input: List[str]) -> int:
    data: Dict[str, List[IntPoint]] = __parse_input(antenna_input)
    antinodes: Dict[IntPoint, int] = dict()
    for y, line in enumerate(antenna_input):
        for x, c in enumerate(line):
            if c != '.':
                antinodes[IntPoint(x, y)] = 1
    counter: int = len(antinodes)

    for freq, positions in data.items():
        for i, position_1 in enumerate(positions):
            for j in range(i + 1, len(positions)):
                position_2: IntPoint = positions[j]

                dif_x: int = position_2.x - position_1.x
                dif_y: int = position_2.y - position_1.y
                slope = dif_y / dif_x if dif_x != 0 else 0
                vector_x = (copysign(1, slope)) * dif_x if dif_x > 0 else -(copysign(1, slope)) * dif_x

                antinode_1_y = position_1.y - dif_y if dif_y > 0 else position_1.y + dif_y
                antinode_2_y = position_2.y + dif_y if dif_y > 0 else position_2.y - dif_y
                antinode_1 = IntPoint(position_1.x - vector_x, antinode_1_y)
                antinode_2 = IntPoint(position_2.x + vector_x, antinode_2_y)

                while _is_in_range(antinode_1, antenna_input):
                    if antinode_1 not in antinodes:
                        antinodes[antinode_1] = antinodes.get(antinode_1, 0) + 1
                        counter += 1
                    antinode_1_y = antinode_1.y - dif_y if dif_y > 0 else antinode_1.y + dif_y
                    antinode_1 = IntPoint(antinode_1.x - vector_x, antinode_1_y)
                while _is_in_range(antinode_2, antenna_input):
                    if antinode_2 not in antinodes:
                        antinodes[antinode_2] = antinodes.get(antinode_2, 0) + 1
                        counter += 1
                    antinode_2_y = antinode_2.y + dif_y if dif_y > 0 else antinode_2.y - dif_y
                    antinode_2 = IntPoint(antinode_2.x + vector_x, antinode_2_y)

    return counter


def find_unique_antinodes(antenna_input: List[str]) -> int:
    data: Dict[str, List[IntPoint]] = __parse_input(antenna_input)
    antinodes: Set[IntPoint] = set()
    counter: int = 0
    for freq, positions in data.items():
        for i, position_1 in enumerate(positions):
            for j in range(i + 1, len(positions)):
                position_2: IntPoint = positions[j]

                dif_x: int = position_2.x - position_1.x
                dif_y: int = position_2.y - position_1.y
                slope = dif_y / dif_x if dif_x != 0 else 0
                vector_x = (copysign(1, slope)) * dif_x if dif_x > 0 else -(copysign(1, slope)) * dif_x

                antinode_1_y = position_1.y - dif_y if dif_y > 0 else position_1.y + dif_y
                antinode_2_y = position_2.y + dif_y if dif_y > 0 else position_2.y - dif_y
                antinode_1 = IntPoint(position_1.x - vector_x, antinode_1_y)
                antinode_2 = IntPoint(position_2.x + vector_x, antinode_2_y)

                for antinode in (antinode_1, antinode_2):
                    if _is_in_range(antinode, antenna_input) and antinode not in antinodes:
                        antinodes.add(antinode)
                        counter += 1
    return counter


def _is_in_range(antinode: IntPoint, antenna_input: List[str]) -> bool:
    return 0 <= antinode.x < len(antenna_input[0]) and 0 <= antinode.y < len(antenna_input)


def __parse_input(antenna_input: List[str]) -> Dict[str, List[IntPoint]]:
    data: Dict[str, List[IntPoint]] = {}
    for y, line in enumerate(antenna_input):
        for x, c in enumerate(line):
            if c == '.':
                continue
            if c in data:
                data[c].append(IntPoint(x, y))
            else:
                data[c] = [IntPoint(x, y)]
    return data


TEST_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day08.txt')

assert find_unique_antinodes(TEST_INPUT.splitlines()) == 14
assert find_unique_antinodes(SOLUTION_INPUT) == 394
assert find_unique_antinodes_including_inline(TEST_INPUT.splitlines()) == 34
assert find_unique_antinodes_including_inline(SOLUTION_INPUT) == 1277
