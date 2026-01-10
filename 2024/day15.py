from collections import deque
from typing import List, Dict

import grid
from file_utils import file_reader
from utils.IntPoint import IntPoint

DIR: Dict[str, IntPoint] = {
    '^': IntPoint(0, -1),
    'v': IntPoint(0, 1),
    '<': IntPoint(-1, 0),
    '>': IntPoint(1, 0),
}


def sum_up_coordinates(data: str) -> int:
    robot_map, commands, pos = __parse_input(data)

    for c in commands:
        next_pos: IntPoint = pos + DIR[c]
        if robot_map[next_pos.y][next_pos.x] == '.':
            robot_map = __move_robot(robot_map, pos, next_pos)
            pos = next_pos
        elif robot_map[next_pos.y][next_pos.x] == 'O':
            end_pos = next_pos + DIR[c]
            while robot_map[end_pos.y][end_pos.x] == 'O':
                end_pos += DIR[c]
            if robot_map[end_pos.y][end_pos.x] == '#':
                continue
            robot_map = __move_robot(robot_map, pos, next_pos)
            grid.replace_char(robot_map, end_pos.x, end_pos.y, 'O')
            pos = next_pos
        else:
            continue

    return __calculate_gps(robot_map, 'O')


def sum_up_coordinates_wide(data: str) -> int:
    robot_map, commands, pos = __parse_input_wide(data)

    for c in commands:
        next_pos: IntPoint = pos + DIR[c]
        if robot_map[next_pos.y][next_pos.x] == '.':
            __move_robot(robot_map, pos, next_pos)
            pos = next_pos
        elif robot_map[next_pos.y][next_pos.x] == '#':
            continue
        elif robot_map[next_pos.y][next_pos.x] == '[' or robot_map[next_pos.y][next_pos.x] == ']':
            if DIR[c].y == 0:
                end_pos = next_pos + DIR[c]
                while robot_map[end_pos.y][end_pos.x] == '[' or robot_map[end_pos.y][end_pos.x] == ']':
                    end_pos += DIR[c]
                if robot_map[end_pos.y][end_pos.x] == '#':
                    continue

                start_x = next_pos.x if DIR[c].x == 1 else end_pos.x + 1
                end_x = end_pos.x if DIR[c].x == 1 else next_pos.x + 1
                chars_to_move = robot_map[next_pos.y][start_x:end_x]
                robot_map = grid.replace_chars(robot_map, start_x + DIR[c].x, next_pos.y, chars_to_move)
                __move_robot(robot_map, pos, next_pos)
                pos = next_pos
            elif DIR[c].x == 0:
                to_move = __get_boxes_to_move(robot_map, next_pos, c)
                is_movable = True
                for box in to_move:
                    if not (len(robot_map) > box.y + DIR[c].y >= 0 and robot_map[box.y + DIR[c].y][box.x] != '#'):
                        is_movable = False
                if is_movable:
                    to_move.sort(key=lambda p: p.y, reverse=True if DIR[c].y > 0 else False)
                    symbols_to_move = [(box, robot_map[box.y][box.x]) for box in to_move]
                    for box, new_sym in symbols_to_move:
                        robot_map = grid.replace_char(robot_map, box.x, box.y + DIR[c].y, new_sym)
                        robot_map = grid.replace_char(robot_map, box.x, box.y, '.')
                    __move_robot(robot_map, pos, next_pos)
                    pos = next_pos

    return __calculate_gps(robot_map, '[')


def __get_boxes_to_move(robot_map: list[str], next_pos: IntPoint, command: str) -> list[IntPoint]:
    dir_x = 1 if robot_map[next_pos.y][next_pos.x] == '[' else -1
    to_move = [next_pos, next_pos + IntPoint(dir_x, 0)]
    valid_boxes = deque(__find_valid_boxes(robot_map, to_move, DIR[command]))
    while len(valid_boxes) > 0:
        box = valid_boxes.popleft()
        if robot_map[box.y][box.x] == '.' or robot_map[box.y][box.x] == '#':
            continue
        current_dir_x = 1 if robot_map[box.y][box.x] == '[' else -1
        box_adj = box + IntPoint(current_dir_x, 0)
        next_boxes = __find_valid_boxes(robot_map, [box, box_adj], DIR[command])
        for next_box in next_boxes:
            if next_box not in valid_boxes:
                valid_boxes.append(next_box)
        if box not in to_move:
            to_move.append(box)
        if box_adj not in to_move:
            to_move.append(box_adj)
    return to_move


def __calculate_gps(robot_map: list[str], to_cmp: str) -> int:
    result = 0
    for y, line in enumerate(robot_map):
        for x, char in enumerate(line):
            if char == to_cmp:
                result += 100 * y + x
    return result


def __find_valid_boxes(robot_map: List[str], cur_positions: List[IntPoint], d: IntPoint) -> set[IntPoint]:
    valid_boxes: set[IntPoint] = set()
    for cur_pos in cur_positions:
        next_y = cur_pos.y + d.y
        if len(robot_map) > next_y >= 0:
            if robot_map[next_y][cur_pos.x] == '[':
                valid_boxes.add(IntPoint(cur_pos.x, next_y))
                valid_boxes.add(IntPoint(cur_pos.x + 1, next_y))
            elif robot_map[next_y][cur_pos.x] == ']':
                valid_boxes.add(IntPoint(cur_pos.x, next_y))
                valid_boxes.add(IntPoint(cur_pos.x - 1, next_y))
    return valid_boxes


def __move_robot(robot_map: List[str], pos: IntPoint, next_pos: IntPoint) -> List[str]:
    robot_map = grid.replace_char(robot_map, pos.x, pos.y, '.')
    robot_map = grid.replace_char(robot_map, next_pos.x, next_pos.y, '@')
    return robot_map


def __parse_input(data: str) -> tuple[List[str], str, IntPoint]:
    robot_map_str, commands = data.split('\n\n')
    robot_map = robot_map_str.splitlines()
    start_pos = next(IntPoint(x, y) for y, line in enumerate(robot_map) for x, char in enumerate(line) if char == '@')
    return robot_map_str.split('\n'), commands.replace('\n', '').strip(), start_pos


def __parse_input_wide(data: str) -> tuple[List[str], str, IntPoint]:
    robot_map_str, commands = data.split('\n\n')
    robot_map_str = robot_map_str.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    robot_map = robot_map_str.splitlines()
    for y, line in enumerate(robot_map):
        robot_map[y] = line
    start_pos = next(IntPoint(x, y) for y, line in enumerate(robot_map) for x, char in enumerate(line) if char == '@')
    return robot_map_str.split('\n'), commands.replace('\n', '').strip(), start_pos


TEST_INPUT_1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

TEST_INPUT_2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<"""

TEST_INPUT_3 = """##########
#..O.O@..#
##########

<<<<"""

TEST_INPUT_4 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

TEST_INPUT_5 = """##########
#..@O.O..#
##########

>>>>"""

TEST_INPUT_6 = """##########
#@.......#
#........#
#O.......#
#........#
#O.......#
#........#
##########

vvvv"""

TEST_INPUT_7 = """##########
#........#
#O.......#
#........#
#O.......#
#........#
#@.......#
##########

^^^^"""

TEST_INPUT_8 = """#######
#.....#
#.O.O@#
#..O..#
#..O..#
#.....#
#######

<v<<>vv<^^"""

TEST_INPUT_9 = """######
#....#
#..#.#
#....#
#.O..#
#.OO@#
#.O..#
#....#
######

<vv<<^^^"""

TEST_INPUT_10 = """#########
#.......#
#...O...#
#...OO@.#
#.#OO#..#
#...O...#
#.......#
#########

<^<<v"""

SOLUTION_INPUT = file_reader.read_whole_file_as_string('input/day15.txt')

assert sum_up_coordinates(TEST_INPUT_1) == 2028
assert sum_up_coordinates(TEST_INPUT_2) == 10092
assert sum_up_coordinates(SOLUTION_INPUT) == 1497888
assert sum_up_coordinates_wide(TEST_INPUT_2) == 9021
assert sum_up_coordinates_wide(TEST_INPUT_3) == 210
assert sum_up_coordinates_wide(TEST_INPUT_4) == 618
assert sum_up_coordinates_wide(TEST_INPUT_5) == 224
assert sum_up_coordinates_wide(TEST_INPUT_6) == 1104
assert sum_up_coordinates_wide(TEST_INPUT_7) == 304
assert sum_up_coordinates_wide(TEST_INPUT_8) == 822
assert sum_up_coordinates_wide(TEST_INPUT_9) == 1216
assert sum_up_coordinates_wide(TEST_INPUT_10) == 2145
assert sum_up_coordinates_wide(SOLUTION_INPUT) == 1522420
