import math
import re
from typing import List

from file_utils import file_reader


def do_weird_math(worksheet: List[str]) -> int:
    data = [[int(x) for x in re.split(r'\s+', line.strip())] for line in worksheet[:-1]]
    operations = [x for x in worksheet[len(worksheet) - 1].split()]

    result = 0
    for x in range(len(data[0])):
        op_result = data[0][x]
        for y in range(1, len(data)):
            if operations[x] == '+':
                op_result += data[y][x]
            elif operations[x] == '*':
                op_result *= data[y][x]
            else:
                raise Exception("unknown operation: " + operations[x])
        result += op_result

    return result


def do_weird_math_reverse(worksheet: List[str]) -> int:
    line_len = len(worksheet[0]) - 1

    result = 0
    numbers = []
    for x in range(line_len, -1, -1):
        number: str = ''
        for y in range(0, len(worksheet) - 1):
            if worksheet[y][x] != ' ':
                number += worksheet[y][x]
        if x == 0:
            numbers.append(int(number))
        if number == '' or x == 0:
            idx = 0 if x == 0 else x + 1
            operation = worksheet[-1][idx]
            if operation == '+':
                result += sum(numbers)
            elif operation == '*':
                result += math.prod(numbers)
            else:
                raise ValueError("unknown operation: " + operation)
            numbers = []
        else:
            numbers.append(int(number))
    return result


test_data = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   + """

SOLUTION_INPUT = file_reader.read_str_from_file('input/day06.txt')

assert do_weird_math(test_data.split('\n')) == 4277556
assert do_weird_math_reverse(test_data.split('\n')) == 3263827
assert do_weird_math(SOLUTION_INPUT) == 3968933219902
assert do_weird_math_reverse(SOLUTION_INPUT) == 6019576291014
