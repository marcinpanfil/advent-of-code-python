from typing import List

from file_utils import file_reader


def calculate_dist(data: List[str]) -> int:
    left_list = []
    right_list = []
    for line in data:
        left, right = map(int, line.split('   '))
        left_list.append(left)
        right_list.append(right)

    if len(left_list) != len(right_list):
        raise AssertionError("Wrong length of lists")

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    return sum(abs(left - right) for left, right in zip(left_list, right_list))


def calculate_similarity_score(data: List[str]) -> int:
    left_list = []
    right_list = {}
    for line in data:
        left, right = map(int, line.split('   '))
        left_list.append(left)
        right_list[right] = right_list.get(right, 0) + 1

    return sum(left * right_list.get(left, 0) for left in left_list)


test_case = """3   4
4   3
2   5
1   3
3   9
3   3"""

SOLUTION_INPUT = file_reader.read_str_from_file('input\\day01.txt')

# part 1
assert calculate_dist(test_case.split('\n')) == 11
assert calculate_dist(SOLUTION_INPUT) == 1882714
# part 2
assert calculate_similarity_score(test_case.split('\n')) == 31
assert calculate_similarity_score(SOLUTION_INPUT) == 19437052
