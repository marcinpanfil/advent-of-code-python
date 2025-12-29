import heapq
import math
from typing import List

from scipy.spatial import KDTree

from file_utils import file_reader


def find_all_circuits(input_str: List[str], n: int = 10) -> int:
    points = __parse_data(input_str)
    distances = __get_n_shortest_distances(points, n, len(points))
    circuits = [[distances[0][1], distances[0][2]]]

    for d in distances[1:]:
        __create_circuits_connections(circuits, d)

    best = sorted(circuits, key=lambda x: len(x), reverse=True)
    return math.prod([len(x) for x in best[:3]])


def find_multiplied_coordinates(input_str: List[str]) -> int:
    points = __parse_data(input_str)
    distances = __get_n_shortest_distances(points, len(points) * (len(points) // 2 - 1), len(points))
    circuits = [[distances[0][1], distances[0][2]]]

    for d in distances[1:]:
        __create_circuits_connections(circuits, d)

        if len(circuits) == 1 and len(circuits[0]) == len(points):
            return d[1][0] * d[2][0]

    return 0

def __create_circuits_connections(circuits: list[list[list[int]]], d):
    b1 = d[1]
    b2 = d[2]

    c1 = next((idx for idx, cr in enumerate(circuits) for d in cr if d == b1), None)
    c2 = next((idx for idx, cr in enumerate(circuits) for d in cr if d == b2), None)

    if c1 is None and c2 is None:
        circuits.append([b1, b2])
    elif c1 is not None and c2 is None:
        circuits[c1].append(b2)
    elif c2 is not None and c1 is None:
        circuits[c2].append(b1)
    elif c1 is not None and c2 is not None and c1 != c2:
        circuits[c1] = circuits[c1] + circuits[c2]
        del circuits[c2]

def __get_n_shortest_distances(points, n, k):
    tree = KDTree(points)
    heap = []

    for i, p in enumerate(points):
        dists, ids = tree.query(p, k=k + 1)
        for d, j in zip(dists[1:], ids[1:]):
            if i < j:
                heapq.heappush(heap, (d, i, j))

    result = []
    while heap and len(result) < n:
        d, i, j = heapq.heappop(heap)
        result.append((d, points[i], points[j]))

    return result


def __parse_data(input_str: list[str]) -> list[list[int]]:
    points = []
    for line in input_str:
        p = [int(n) for n in line.split(",")]
        points.append(p)
    return points


test_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day08.txt')

assert find_all_circuits(test_data.splitlines()) == 40
assert find_all_circuits(SOLUTION_INPUT, len(SOLUTION_INPUT)) == 244188
assert find_multiplied_coordinates(test_data.splitlines()) == 25272
assert find_multiplied_coordinates(SOLUTION_INPUT) == 8361881885
