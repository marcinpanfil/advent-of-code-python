from collections import deque
from typing import List
from functools import cache

import file_reader


def find_all_paths(input_str: List[str]) -> int:
    device_outputs = __read_data(input_str)

    result: int = 0
    outputs: list[str] = device_outputs["you"]
    queue = deque(outputs)
    while len(queue) > 0:
        current: str = queue.popleft()
        if current == "out":
            result += 1
        else:
            outputs = device_outputs[current]
            for o in outputs:
                queue.append(o)

    return result


def find_all_paths_with_fft_and_dac(input_str: List[str]) -> int:
    device_outputs = __read_data(input_str)

    @cache
    def dfs(device: str, fft: bool, dac: bool) -> int:
        if device == "out":
            return 1 if fft and dac else 0
        outputs = device_outputs.get(device)
        if outputs is None:
            return 0
        if device == "fft":
            fft = True
        elif device == "dac":
            dac = True
        return sum(dfs(out, fft, dac) for out in outputs)

    return dfs("svr", False, False)


def __read_data(input_str: List[str]) -> dict[str, List[str]]:
    result: dict[str, List[str]] = {}
    for line in input_str:
        line_split = line.split(": ")
        device = line_split[0]
        outputs = line_split[1].split(" ")
        result[device] = outputs
    return result


test_data = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

test_data_part_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day11.txt')

assert find_all_paths(test_data.splitlines()) == 5
assert find_all_paths(SOLUTION_INPUT) == 511
assert find_all_paths_with_fft_and_dac(test_data_part_2.splitlines()) == 2
assert find_all_paths_with_fft_and_dac(SOLUTION_INPUT) == 458618114529380
