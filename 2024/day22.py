from collections import deque, defaultdict
from typing import List

from file_utils import file_reader


def generate_new_secrets(secrets: List[int]) -> int:
    res = 0
    for s in secrets:
        for i in range(2000):
            s1 = ((s << 6) ^ s) & 0xFFFFFF
            s2 = ((s1 >> 5) ^ s1) & 0xFFFFFF
            s = ((s2 << 11) ^ s2) & 0xFFFFFF
        res += s

    return res


def generate_new_secrets_one_digit(secrets: List[int]) -> int:
    d: dict[tuple[int], int] = defaultdict(int)
    for s in secrets:
        last_digit = s % 10
        q = deque(maxlen=4)
        v = set()
        for i in range(2000):
            s1 = ((s << 6) ^ s) & 0xFFFFFF
            s2 = ((s1 >> 5) ^ s1) & 0xFFFFFF
            s = ((s2 << 11) ^ s2) & 0xFFFFFF
            cur_digit = s % 10
            q.append(cur_digit - last_digit)
            lq = tuple(q)
            if lq not in v:
                if len(lq) == 4:
                    if lq in d:
                        d[lq] += cur_digit
                    else:
                        d[lq] = cur_digit

            v.add(lq)
            last_digit = cur_digit

    return max(d.values())


SOLUTION_INPUT = file_reader.read_ints_from_file("input/day22.txt")

assert generate_new_secrets([1, 10, 100, 2024]) == 37327623
assert generate_new_secrets(SOLUTION_INPUT) == 20215960478

assert generate_new_secrets_one_digit([1, 2, 3, 2024]) == 23
assert generate_new_secrets_one_digit(SOLUTION_INPUT) == 2221