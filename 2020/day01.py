from file_utils import file_reader


def find_result_with_two(values):
    for value in values:
        search_for = 2020 - value
        if search_for in values:
            return value * search_for


def find_result_with_three(values):
    for value in values:
        for sec_value in values:
            possible_third = 2020 - (sec_value + value)
            if possible_third in values:
                return value * sec_value * possible_third
    return -1


def solve_1():
    values = file_reader.read_ints_from_file('input/day01_input.txt')
    return find_result_with_two(values)


def solve_2():
    values = file_reader.read_ints_from_file('input/day01_input.txt')
    return find_result_with_three(values)


# part1
assert 514579 == find_result_with_two({1721, 979, 366, 299, 675, 1456})
assert 485739 == solve_1()
# part2
assert 241861950 == find_result_with_three({1721, 979, 366, 299, 675, 1456})
assert 161109702 == solve_2()
