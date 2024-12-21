from collections import defaultdict
from typing import List, Dict


def count_stones_after_x_blinks(data: List[str], blinks: int) -> int:
    # just count how many occurrences appear during the processing because 1 number always
    # returns the same number(s), 0 -> 1, 2000 -> 20 and 0, etc
    counter: Dict[str, int] = {s: 1 for s in data}
    for _ in range(blinks):
        new_stones: Dict[str, int] = defaultdict(int)
        for stone, count in counter.items():
            if stone == '0':
                new_stones['1'] += count
            elif len(stone) % 2 == 0:
                idx: int = len(stone) // 2
                new_stones[str(int(stone[:idx]))] += count
                new_stones[str(int(stone[idx:]))] += count
            else:
                value = str(int(stone) * 2024)
                new_stones[value] += count
        counter = new_stones
    return sum(counter.values())


TEST_INPUT = '125 17'
SOLUTION_INPUT = '92 0 286041 8034 34394 795 8 2051489'
assert count_stones_after_x_blinks(TEST_INPUT.split(' '), 25) == 55312
assert count_stones_after_x_blinks(SOLUTION_INPUT.split(' '), 25) == 239714
assert count_stones_after_x_blinks(SOLUTION_INPUT.split(' '), 75) == 284973560658514
