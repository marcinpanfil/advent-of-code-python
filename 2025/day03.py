from typing import List, Tuple

from file_utils import file_reader

RATING = ['9', '8', '7', '6', '5', '4', '3', '2', '1']


def find_max_joltage(data: List[str], nr_turned_on=2) -> int:
    res = 0
    for bank in data:
        bank_res = ''
        cur_idx = 0
        for i in range(nr_turned_on):
            end_idx = len(bank) - nr_turned_on + i + 1
            sub_bank = bank[cur_idx:end_idx]
            r, idx = find_next_rating(sub_bank)
            bank_res += r
            cur_idx += idx + 1
            if len(bank[cur_idx:]) == nr_turned_on - len(bank_res):
                bank_res += bank[cur_idx:]
                break
        tmp_rest = int(bank_res)
        res += tmp_rest
    return res


def find_next_rating(sub_bank: str) -> Tuple[str, int]:
    for r in RATING:
        idx = sub_bank.index(r) if r in sub_bank else -1
        if idx >= 0:
            return r, idx
    raise ValueError("no rating found")


test_data = """987654321111111
811111111111119
234234234234278
818181911112111"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day03.txt')

assert find_max_joltage(test_data.split('\n')) == 357
assert find_max_joltage(SOLUTION_INPUT) == 17316
assert find_max_joltage(test_data.split('\n'), 12) == 3121910778619
assert find_max_joltage(SOLUTION_INPUT, 12) == 171741365473332
