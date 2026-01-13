import heapq
import itertools
from collections import deque
from typing import List

from file_utils import file_reader
from utils.IntPoint import IntPoint

DIRS: List[IntPoint] = [
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(-1, 0),
    IntPoint(1, 0),
]


def find_shortest_path(input_str: List[str], size=71, limit=1024) -> int:
    corrupted_points = __parse_data(input_str)
    start: IntPoint = IntPoint(0, 0)
    end: IntPoint = IntPoint(size - 1, size - 1)

    counter = itertools.count()
    pq: list[tuple[int, int, int, IntPoint]] = []
    heapq.heappush(pq, (0, next(counter), 0, start))
    visited: dict[tuple[IntPoint, int], int] = {(start, 0): 0}

    while pq:
        dist, _, dir_idx, cur = heapq.heappop(pq)
        if cur == end:
            return dist

        state = (cur, dir_idx)
        if visited.get(state, float("inf")) < dist:
            continue

        for next_dir_idx, d in enumerate(DIRS):
            nxt = cur + d
            if not (0 <= nxt.y < size and 0 <= nxt.x < size and nxt not in corrupted_points[:limit]):
                continue

            new_dist = dist + 1
            next_state = (nxt, next_dir_idx)

            if new_dist < visited.get(next_state, float("inf")):
                visited[next_state] = new_dist
                heapq.heappush(pq, (new_dist, next(counter), next_dir_idx, IntPoint(nxt.x, nxt.y)))
    raise ValueError("No path found")


def find_the_cuf_off_byte(input_str: List[str], size=71, start_idx=1024) -> IntPoint:
    corrupted_points = __parse_data(input_str)
    start: IntPoint = IntPoint(0, 0)
    end: IntPoint = IntPoint(size - 1, size - 1)

    end_idx = len(corrupted_points)
    while True:
        idx = start_idx + (end_idx - start_idx) // 2
        if idx == start_idx:
            return corrupted_points[idx + 1]
        elif not __has_path(corrupted_points[:idx + 1], start, end, size):
            end_idx = idx
        else:
            start_idx = idx


def __has_path(corrupted_points: List[IntPoint], start: IntPoint, end: IntPoint, size: int) -> bool:
    queue = deque([start])
    visited: set[IntPoint] = set()

    while queue:
        curr: IntPoint = queue.popleft()
        if curr == end:
            return True

        if curr in visited:
            continue
        visited.add(curr)

        for d in DIRS:
            nxt = curr + d
            if 0 <= nxt.y < size and 0 <= nxt.x < size and nxt not in corrupted_points and nxt not in visited:
                queue.append(nxt)

    return False


def __parse_data(input_str: List[str]) -> List[IntPoint]:
    points: List[IntPoint] = []
    for line in input_str:
        ps = [int(x) for x in line.split(",")]
        points.append(IntPoint(ps[0], ps[1]))
    return points


test_data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

SOLUTION_INPUT = file_reader.read_str_from_file("input/day18.txt")

assert find_shortest_path(test_data.splitlines(), size=7, limit=12) == 22
assert find_shortest_path(SOLUTION_INPUT) == 370

assert find_the_cuf_off_byte(test_data.splitlines(), size=7, start_idx=0) == IntPoint(6, 1)
assert find_the_cuf_off_byte(SOLUTION_INPUT) == IntPoint(65, 6)
