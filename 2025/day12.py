from typing import List

import file_reader


def solve(input_str: str) -> int:
    shapes, regions = __parse_data(input_str)

    to_big = 0
    to_big_3x3 = 0
    for region in regions:
        required_size = 0
        required_3x3_size = 0
        for i in range(len(region.counts)):
            c = region.counts[i]
            required_size += (c * shapes[i].used_s)
            required_3x3_size += (c * 9)
        if required_size > region.size:
            to_big += 1
        if required_3x3_size > region.size:
            to_big_3x3 += 1
    if to_big != to_big_3x3:
        raise Exception("didn't work! :(")
    return len(regions) - to_big


class Shape:

    def __init__(self, grid: List[str]):
        self.grid = grid
        self.used_s = sum(s.count("#") for s in self.grid)

class Region:

    def __init__(self, x, y, counts: List[int]):
        self.x = x
        self.y = y
        self.size = self.x * self.y
        self.counts = counts


def __parse_data(input_str: str) -> tuple[List[Shape], List[Region]]:
    split_data = input_str.split("\n\n")
    shapes: List[Shape] = []
    for idx in range(0, 6):
        shape_str = split_data[idx].split("\n")
        shapes.append(Shape(shape_str[1:]))

    regions: List[Region] = []
    for region_str in split_data[6].split("\n")[1:]:
        data_str = region_str.split(": ")
        x, y = [int(x) for x in data_str[0].split("x")]
        counts = [int(x) for x in data_str[1].split(" ")]
        regions.append(Region(x, y, counts))
    return shapes, regions

test_data = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

SOLUTION_INPUT = file_reader.read_whole_file_as_string('input/day12.txt')
assert solve(SOLUTION_INPUT) == 414