import itertools
from datetime import datetime
from typing import List, Dict, Set

from file_utils import file_reader


def find_correct_operators(lines: List[str], part_2: bool) -> int:
    operators = {'*': lambda x, y: x * y, '+': lambda x, y: x + y}
    if part_2:
        operators['|'] = lambda x, y: (x * (10 ** len(str(y))) + y)

    data: Dict[int, List[int]] = __parse_input(lines)
    counter: int = 0
    for res, equation in data.items():
        possible_operators = itertools.product(operators.keys(), repeat=len(equation) - 1)
        for permutation in possible_operators:
            current_sum = equation[0]
            for i in range(1, len(equation)):
                current_sum = operators[permutation[i - 1]](current_sum, equation[i])
                if current_sum > res:
                    break
            if current_sum == res:
                counter += current_sum
                break

    end = datetime.now()
    return counter


def __parse_input(lines: List[str]) -> Dict[int, List[int]]:
    result: Dict[int, List[int]] = {}
    for line in lines:
        split_strs = line.split(" ")
        key = int(split_strs[0][:-1])
        values = [int(x) for x in split_strs[1:]]
        if key in result:
            raise RuntimeError(f"Duplicate key {key} in line {line}")
        result[key] = values
    return result


TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day07.txt')

assert find_correct_operators(TEST_INPUT.splitlines(), False) == 3749
assert find_correct_operators(TEST_INPUT.splitlines(), True) == 11387
assert find_correct_operators(SOLUTION_INPUT, False) == 1153997401072
assert find_correct_operators(SOLUTION_INPUT, True) == 97902809384118
