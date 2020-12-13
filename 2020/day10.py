from file_utils import file_reader


def find_jolts(values):
    cur_step = 0
    one_jolts_count = 0
    three_jolts_count = 0

    while True:
        if cur_step + 1 in values:
            cur_step += 1
            one_jolts_count += 1
        elif cur_step + 2 in values:
            cur_step += 2
        elif cur_step + 3 in values:
            cur_step += 3
            three_jolts_count += 1
        else:
            return one_jolts_count * (three_jolts_count + 1)


def find_arrangements(values):
    values.append(0)
    values.sort()
    counter = {0: 1}
    for value in values:
        if value + 1 in counter:
            counter[value + 1] += counter[value]
        else:
            counter[value + 1] = counter[value]

        if value + 2 in counter:
            counter[value + 2] += counter[value]
        else:
            counter[value + 2] = counter[value]

        if value + 3 in counter:
            counter[value + 3] += counter[value]
        else:
            counter[value + 3] = counter[value]

    return counter[max(values)]


def solve_1():
    values = file_reader.read_ints_from_file('input/day10_input.txt')
    return find_jolts(values)


def solve_2():
    values = file_reader.read_ints_from_file('input/day10_input.txt')
    values.sort()
    return find_arrangements(values)


test_case_1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
test_case_2 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2,
               34, 10, 3]


# part 1
assert 35 == find_jolts(test_case_1)
assert 220 == find_jolts(test_case_2)
assert 2201 == solve_1()
# part 2
assert 8 == find_arrangements(test_case_1)
assert 19208 == find_arrangements(test_case_2)
assert 169255295254528 == solve_2()
