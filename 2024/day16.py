import heapq
import itertools
from collections import defaultdict
from typing import List

import file_reader
import grid
from IntPoint import IntPoint

DIRS: List[IntPoint] = [
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(1, 0),
    IntPoint(-1, 0),
]


def find_min_path(maze: List[str]) -> int:
    start = grid.find_first_char(maze, "S")
    end = grid.find_first_char(maze, "E")

    counter = itertools.count()

    pq: list[tuple[int, int, int, IntPoint]] = []
    heapq.heappush(pq, (0, next(counter), 2, start))
    visited: dict[tuple[IntPoint, int], int] = {(start, 2): 0}
    while pq:
        dist, _, dir_idx, cur = heapq.heappop(pq)
        if cur == end:
            return dist

        state = (cur, dir_idx)
        if visited.get(state, float("inf")) < dist:
            continue

        for next_dir_idx, d in enumerate(DIRS):
            n = cur + d
            if __is_valid_move(maze, n):
                continue

            cost = 1 if next_dir_idx == dir_idx else 1001
            new_dist = dist + cost
            next_state = (n, next_dir_idx)

            if new_dist < visited.get(next_state, float("inf")):
                visited[next_state] = new_dist
                heapq.heappush(pq, (new_dist, next(counter), next_dir_idx, IntPoint(n.x, n.y)))

    raise ValueError("No path found")


def find_best_tiles(maze: List[str]) -> int:
    start = grid.find_first_char(maze, "S")
    end = grid.find_first_char(maze, "E")

    counter = itertools.count()

    pq: list[tuple[int, int, int, IntPoint]] = []
    heapq.heappush(pq, (0, next(counter), 2, start))
    visited: dict[tuple[IntPoint, int], int] = {(start, 2): 0}
    predecessors: dict[tuple[IntPoint, int], list[tuple[IntPoint, int]]] = defaultdict(list)

    min_dist = float('inf')
    end_states: list[tuple[IntPoint, int]] = []
    while pq:
        dist, _, dir_idx, cur = heapq.heappop(pq)
        if dist > min_dist:
            break

        if cur == end:
            if dist < min_dist:
                min_dist = dist
                end_states = [(cur, dir_idx)]
            elif dist == min_dist:
                end_states.append((cur, dir_idx))
            continue

        state = (cur, dir_idx)
        if visited.get(state, float("inf")) < dist:
            continue

        for next_dir_idx, d in enumerate(DIRS):
            n = cur + d
            if __is_valid_move(maze, n):
                continue

            cost = 1 if next_dir_idx == dir_idx else 1001
            new_dist = dist + cost
            next_state = (n, next_dir_idx)

            if new_dist < visited.get(next_state, float("inf")):
                visited[next_state] = new_dist
                predecessors[next_state] = [state]
                heapq.heappush(pq, (new_dist, next(counter), next_dir_idx, IntPoint(n.x, n.y)))
            elif new_dist == visited.get(next_state, float("inf")):
                predecessors[next_state].append(state)

    return __count_tiles_on_best_path(end_states, predecessors)


def __count_tiles_on_best_path(end_states: list[tuple[IntPoint, int]],
                               predecessors: dict[tuple[IntPoint, int],
                               list[tuple[IntPoint, int]]]) -> int:
    tiles_on_best_paths: set[IntPoint] = set()
    stack = end_states[:]
    visited_backtrack: set[tuple[IntPoint, int]] = set()

    while stack:
        state = stack.pop()
        if state in visited_backtrack:
            continue
        visited_backtrack.add(state)
        tiles_on_best_paths.add(state[0])
        stack.extend(predecessors[state])

    return len(tiles_on_best_paths)


def __is_valid_move(maze: list[str], n: IntPoint) -> bool:
    return not (0 <= n.y < len(maze) and 0 <= n.x < len(maze[0]) and maze[n.y][n.x] in ('.', 'E'))


test_data_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test_data_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day16.txt')

assert find_min_path(test_data_1.splitlines()) == 7036
assert find_min_path(test_data_2.splitlines()) == 11048
assert find_min_path(SOLUTION_INPUT) == 160624
assert find_best_tiles(test_data_1.splitlines()) == 45
assert find_best_tiles(test_data_2.splitlines()) == 64
assert find_best_tiles(SOLUTION_INPUT) == 692
