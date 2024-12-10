import re

from file_utils import file_reader


def find_mul(data: str) -> int:
    muls = re.findall(r'mul\((\d+),(\d+)\)', data)
    return sum(int(x) * int(y) for x, y in muls)


def find_mul_when_do(data: str) -> int:
    matches = re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))', data)

    result = 0
    is_on = True
    for x, y, do, dont in matches:
        if do:
            is_on = True
        elif dont:
            is_on = False
        elif is_on:
            result += int(x) * int(y)

    return result


TEST_INPUT_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
TEST_INPUT_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
SOLUTION_INPUT = file_reader.read_whole_file_as_string('input\\day03.txt')

assert find_mul(TEST_INPUT_1) == 161
assert find_mul(SOLUTION_INPUT) == 178538786

assert find_mul_when_do(TEST_INPUT_2) == 48
assert find_mul_when_do(SOLUTION_INPUT) == 102467299
