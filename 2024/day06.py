from typing import List, Set

from file_utils import file_reader
from utils.IntPoint import IntPoint


def count_distinct_visited_pos(data: List[str]) -> int:
    cur: IntPoint = __find_starting_point(data)
    visited: Set[IntPoint] = set()
    cur_dir: IntPoint = IntPoint(0, -1)
    while 0 <= cur_dir.x + cur.x < len(data[0]) and 0 <= cur_dir.y + cur.y < len(data):
        visited.add(cur)
        next_step: IntPoint = IntPoint(cur_dir.x + cur.x, cur_dir.y + cur.y)
        if data[next_step.y][next_step.x] == '#':
            cur_dir = __next_dir(cur_dir)
            next_step = IntPoint(cur_dir.x + cur.x, cur_dir.y + cur.y)
        cur = next_step
    return len(visited) + 1


def count_possible_obstructions(data: List[str]) -> int:
    cur_dir: IntPoint = IntPoint(0, -1)
    cur: IntPoint = __find_starting_point(data)
    visited: Set[IntPoint] = set()

    result = 0
    while 0 <= cur_dir.x + cur.x < len(data[0]) and 0 <= cur_dir.y + cur.y < len(data):
        visited.add(cur)

        potential_obstacle: IntPoint = IntPoint(cur_dir.x + cur.x, cur_dir.y + cur.y)
        if 0 <= potential_obstacle.x < len(data[0]) and 0 <= potential_obstacle.y < len(data):
            # check if next step is an obstacle and if not visited - if an obstacle is put on the path = path blocked
            if data[potential_obstacle.y][potential_obstacle.x] != '#' and potential_obstacle not in visited:
                # change the map of obstacles
                prev_value = data[potential_obstacle.y][potential_obstacle.x]
                __replace_position_on_map(data, potential_obstacle, '#')

                obstacle_point, obstacle_dir = __find_next_obstacle(cur_dir, cur, data)
                if obstacle_point:
                    # log if obstacle was visited from the given direction
                    obstacles_visited: Set[(IntPoint, IntPoint)] = {(obstacle_point, obstacle_dir)}
                    while obstacle_point and cur != obstacle_point:
                        obstacle_point, obstacle_dir = __find_next_obstacle(obstacle_dir, obstacle_point, data)
                        # guard has left the area
                        if not obstacle_point:
                            break
                        # guard stuck in the loop (the same position was already visited)
                        # or reached the starting obstacle
                        if ((obstacle_point, obstacle_dir) in obstacles_visited
                                or not __has_obstacles_between(potential_obstacle, obstacle_point, data)):
                            result += 1
                            break
                        obstacles_visited.add((obstacle_point, obstacle_dir))
                __replace_position_on_map(data, potential_obstacle, prev_value)

            if data[potential_obstacle.y][potential_obstacle.x] == '#':
                cur_dir = __next_dir(cur_dir)
                potential_obstacle = IntPoint(cur_dir.x + cur.x, cur_dir.y + cur.y)
            cur = potential_obstacle
    return result


def __replace_position_on_map(data, point: IntPoint, c: str):
    data[point.y] = data[point.y][:point.x] + c + data[point.y][point.x + 1:]


#
def __has_obstacles_between(start: IntPoint, end: IntPoint, data: List[str]) -> bool:
    # can't compare obstacles on different axis
    if start.x != end.x and start.y != end.y:
        return True
    if start.x == end.x and abs(start.y - end.y) > 2:
        for y in range(min(start.y, end.y) + 1, max(start.y, end.y) + 1):
            if data[y][start.x] == '#':
                return True
    if start.y == end.y and abs(start.x - end.x) > 1:
            for x in range(min(start.x, end.x) + 1, max(start.x, end.x) + 1):
                if data[start.y][x] == '#':
                    return True
    return False


def __find_next_obstacle(cur_dir: IntPoint, cur: IntPoint, data: List[str]) -> (IntPoint, IntPoint):
    next_dir = __next_dir(cur_dir)

    if cur_dir.y == 0:
        end = -1 if next_dir.y == -1 else len(data)
        step = -1 if end == -1 else 1
        for y in range(cur.y, end, step):
            if data[y][cur.x] == '#':
                return IntPoint(cur.x, y - next_dir.y), next_dir
    elif cur_dir.x == 0:
        end = -1 if next_dir.x == -1 else len(data[0])
        step = -1 if end == -1 else 1
        for x in range(cur.x, end, step):
            if data[cur.y][x] == '#':
                return IntPoint(x - next_dir.x, cur.y), next_dir

    return None, None


def __next_dir(cur_dir: IntPoint):
    return IntPoint(-cur_dir.y, cur_dir.x)


def __find_starting_point(data: List[str]) -> IntPoint:
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '^':
                return IntPoint(x, y)
    raise ValueError("No starting-point found")


TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

TEST_INPUT_1 = """...#...
.......
.......
..#^...
......#
.#.....
.....#."""

TEST_INPUT_2 = """.##..
....#
.....
.^.#.
....."""

TEST_INPUT_3 = """.#.....
#......
..#...#
...^...
#......
..#..#."""

TEST_INPUT_4 = """###
#.#
#.#
#^#"""

TEST_INPUT_5 = """....#.....
......#...
.#........
.........#
....^....#
#.........
.....#....
..#.......
........#."""

TEST_INPUT_6 = """.#..
#..#
....
^...
#...
.#.."""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day06.txt')

assert count_distinct_visited_pos(TEST_INPUT.splitlines()) == 41
assert count_distinct_visited_pos(SOLUTION_INPUT) == 5162
assert count_possible_obstructions(TEST_INPUT.splitlines()) == 6
assert count_possible_obstructions(TEST_INPUT_1.splitlines()) == 1
assert count_possible_obstructions(TEST_INPUT_2.splitlines()) == 1
assert count_possible_obstructions(TEST_INPUT_3.splitlines()) == 1
assert count_possible_obstructions(TEST_INPUT_4.splitlines()) == 0
assert count_possible_obstructions(TEST_INPUT_5.splitlines()) == 6
assert count_possible_obstructions(TEST_INPUT_6.splitlines()) == 1
assert count_possible_obstructions(SOLUTION_INPUT) == 1909
