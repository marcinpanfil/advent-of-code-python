from file_utils import file_reader


def find_overlapping_locks_and_keys(input_date: str) -> int:
    locks, keys = __parse_data_into_locks_and_keys(input_date)
    fit: int = 0
    for l in locks:
        for k in keys:
            if all(l + k <= 5 for l, k in zip(l, k)):
                fit += 1
    return fit


def __parse_data_into_locks_and_keys(input_data: str) -> tuple[list[list[int]], list[list[int]]]:
    parts = input_data.split("\n\n")
    locks: list[list[int]] = []
    keys: list[list[int]] = []

    for part in parts:
        pins = part.split("\n")
        if pins[0] == "#####":
            locks.append(["".join(col).rfind("#") for col in zip(*pins)])
        elif pins[0] == ".....":
            keys.append([len(col) - "".join(col).index("#") - 1 for col in zip(*pins)])
    return locks, keys


test_data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

SOLUTION_INPUT = file_reader.read_whole_file_as_string("input/day25.txt")

assert find_overlapping_locks_and_keys(test_data) == 3
assert find_overlapping_locks_and_keys(SOLUTION_INPUT) == 2978
