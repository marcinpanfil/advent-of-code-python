from file_utils import file_reader


def find_not_valid(values, preamble_count):
    preamble = values[:preamble_count]
    values = values[preamble_count:]
    for value in values:
        found = False
        for n in preamble:
            m = value - n
            if m in preamble:
                found = True
                break
        if not found:
            return value
        preamble.pop(0)
        preamble.append(value)

    return None


def find_contiguous_numbers(values, sum_value):
    curr_pos = 0
    while curr_pos < len(values):
        for i in range(curr_pos + 1, len(values)):
            tmp_values = values[curr_pos: i + 1]
            tmp_sum = sum(tmp_values)
            if sum_value == tmp_sum:
                return min(tmp_values) + max(tmp_values)
            elif sum_value < tmp_sum:
                break
        curr_pos += 1
    return []


def solve_1():
    values = file_reader.read_ints_from_file('input/day09_input.txt')
    return find_not_valid(values, 25)


def solve_2():
    values = file_reader.read_ints_from_file('input/day09_input.txt')
    result = find_not_valid(values, 25)
    return find_contiguous_numbers(values, result)


test_case_1 = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]

# part 1
assert 127 == find_not_valid(test_case_1, 5)
assert 10884537 == solve_1()

# part2
assert 62 == find_contiguous_numbers(test_case_1, 127)
assert 1261309 == solve_2()
