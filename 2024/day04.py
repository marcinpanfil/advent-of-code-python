from typing import List, Dict

from file_utils import file_reader
from utils.IntPoint import IntPoint

POSSIBLE_DIR: List[IntPoint] = [
    IntPoint(1, 1),
    IntPoint(1, 0),
    IntPoint(1, -1),
    IntPoint(0, 1),
    IntPoint(0, -1),
    IntPoint(-1, 1),
    IntPoint(-1, 0),
    IntPoint(-1, -1)
]

POSSIBLE_X_DIR: List[IntPoint] = [
    IntPoint(1, 1),
    IntPoint(1, -1),
    IntPoint(-1, -1),
    IntPoint(-1, 1),
]


def count_xmas_occurrences(data: List[str]) -> int:
    curr_pos: List[IntPoint] = find_all_chars(data, 'X')
    search_for = 'XMAS'
    len_x = len(data[0])
    len_y = len(data)

    result = 0
    for d in POSSIBLE_DIR:
        for pos in curr_pos:
            cur_pos_x = pos.x
            cur_pos_y = pos.y
            stop = False
            for i in range(len(search_for) - 1):
                pos_x = d.x + cur_pos_x
                pos_y = d.y + cur_pos_y
                if len_x > pos_x >= 0 and len_y > pos_y >= 0 and data[pos_y][pos_x] == search_for[i + 1]:
                    cur_pos_x = pos_x
                    cur_pos_y = pos_y
                else:
                    stop = True
                    break
            if not stop:
                result += 1

    return result


def count_mas_occurrences(data: List[str]) -> int:
    curr_pos: List[IntPoint] = find_all_chars(data, 'A')
    search_for = ['M', 'S']
    len_x = len(data[0])
    len_y = len(data)

    result = 0
    for pos in curr_pos:
        x_str: Dict[IntPoint, str] = {}
        for d in POSSIBLE_X_DIR:
            pos_x = d.x + pos.x
            pos_y = d.y + pos.y
            if len_x > pos_x >= 0 and len_y > pos_y >= 0 and data[pos_y][pos_x] in search_for:
                x_str[d] = data[pos_y][pos_x]
            else:
                break
        if is_x_shape(x_str):
            result += 1

    return result


def is_x_shape(points: Dict[IntPoint, str]) -> bool:
    return (len(points) == 4 and
            points[IntPoint(-1, -1)] != points[IntPoint(1, 1)] and
            points[IntPoint(1, -1)] != points[IntPoint(-1, 1)])


def find_all_chars(data: List[str], char_to_find: str) -> List[IntPoint]:
    return [IntPoint(x, y) for y, row in enumerate(data) for x, char in enumerate(row) if char == char_to_find]


TEST_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
SOLUTION_INPUT = file_reader.read_str_from_file('input\\day04.txt')

assert count_xmas_occurrences(TEST_INPUT.split('\n')) == 18
assert count_xmas_occurrences(SOLUTION_INPUT) == 2530
assert count_mas_occurrences(TEST_INPUT.split('\n')) == 9
assert count_mas_occurrences(SOLUTION_INPUT) == 1921
