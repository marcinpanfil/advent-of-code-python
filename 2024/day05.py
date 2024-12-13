import math
from typing import List, Tuple, Dict

from file_utils import file_reader


def sum_middle_pages_for_correct(data: List[str]) -> int:
    pages_before, updates = prepare_data(data)
    return sum([int(update[math.floor(len(update) / 2)]) for update in updates if is_correct(pages_before, update)])


def is_correct(pages_before, update):
    for i in range(len(update) - 1):
        curr_page: str = update[i + 1]
        prev_page: str = update[i]

        if curr_page not in pages_before or prev_page not in pages_before[curr_page]:
            return False
    return True


def sum_middle_pages_for_incorrect(data: List[str]) -> int:
    pages_before, updates = prepare_data(data)
    incorrect_updates = [update for update in updates if not is_correct(pages_before, update)]

    result = 0
    for update in incorrect_updates:
        correct_update = []
        for page in update:
            for correct_page in correct_update:
                idx = correct_update.index(correct_page)
                before = pages_before[correct_page] if correct_page in pages_before else []
                if page in before:
                    correct_update = correct_update[:idx] + [page] + correct_update[idx:]
                    break
            if page not in correct_update:
                correct_update.append(page)

        result += int(correct_update[math.floor(len(correct_update) / 2)])
    return result


def prepare_data(data: List[str]) -> Tuple[Dict[str, List[str]], List[List[str]]]:
    pages_before: Dict[str, List[str]] = {}
    updates: List[List[str]] = []

    updates_part_line_nr = 0
    for i, line in enumerate(data):
        if line.strip() == "":
            updates_part_line_nr = i
            break
        pages = line.split("|")
        pages_before.setdefault(pages[1], []).append(pages[0])

    for _, update_line in enumerate(data[updates_part_line_nr + 1:]):
        updates.append(update_line.strip().split(","))

    return pages_before, updates


SOLUTION_INPUT = file_reader.read_str_from_file('input\\day05.txt')
TEST_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

assert 143 == sum_middle_pages_for_correct(TEST_INPUT.splitlines())
assert 6612 == sum_middle_pages_for_correct(SOLUTION_INPUT)
assert 123 == sum_middle_pages_for_incorrect(TEST_INPUT.splitlines())
assert 4944 == sum_middle_pages_for_incorrect(SOLUTION_INPUT)
