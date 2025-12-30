from typing import List

from file_utils import file_reader
from utils.IntPoint import IntPoint


def find_the_biggest_rectangle(data: List[str]) -> int:
    points = __read_points(data)

    max_dist = 0
    max_size = 0
    for i in range(len(points)):
        p1: IntPoint = points[i]
        for j in range(len(points)):
            p2: IntPoint = points[j]
            dist = abs(p1.x - p2.x) + abs(p1.y - p2.y)
            if dist > max_dist:
                max_dist = dist
                max_size = (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)
    return max_size


def find_the_biggest_rectangle_only_green(data: List[str]) -> int:
    points = __read_points(data)
    max_size = 0

    edges = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]

    for i in range(len(points)):
        p1: IntPoint = points[i]
        for j in range(len(points)):
            p2: IntPoint = points[j]
            min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
            min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)

            crosses_edge = False
            for edge_start, edge_end in edges:
                if __rectangle_crosses_edge(min_x, max_x, min_y, max_y, edge_start, edge_end):
                    crosses_edge = True
                    break

            if not crosses_edge:
                size = (max_x - min_x + 1) * (max_y - min_y + 1)
                if size > max_size:
                    max_size = size

    return max_size


def __rectangle_crosses_edge(min_x: int, max_x: int, min_y: int, max_y: int, edge_start: IntPoint, edge_end: IntPoint) -> bool:
    e_min_x, e_max_x = min(edge_start.x, edge_end.x), max(edge_start.x, edge_end.x)
    e_min_y, e_max_y = min(edge_start.y, edge_end.y), max(edge_start.y, edge_end.y)


    if edge_start.y == edge_end.y:
        edge_y = edge_start.y
        if min_y < edge_y < max_y and e_min_x < max_x and e_max_x > min_x:
            return True

    if edge_start.x == edge_end.x:
        edge_x = edge_start.x
        if min_x < edge_x < max_x and e_min_y < max_y and e_max_y > min_y:
            return True

    return False

def __read_points(data: list[str]) -> list[IntPoint]:
    points = []
    for row in data:
        x, y = row.split(",")
        points.append(IntPoint(int(x), int(y)))
    return points


test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day09.txt')

assert find_the_biggest_rectangle(test_data.splitlines()) == 50
assert find_the_biggest_rectangle(SOLUTION_INPUT) == 4750092396
assert find_the_biggest_rectangle_only_green(test_data.splitlines()) == 24
assert find_the_biggest_rectangle_only_green(SOLUTION_INPUT) == 1468516555
