start = 359282
end = 820401


def contains_two_digits_raising(value):
    is_rising = False
    has_two_in_row = False
    mod = value % 10
    while value > 0:
        value = int(value / 10)
        curr_mod = value % 10
        if curr_mod == mod:
            has_two_in_row = True
        if curr_mod <= mod:
            is_rising = True
        else:
            return False
        mod = curr_mod

    return is_rising and has_two_in_row


def contains_exactly_two_digits_raising(value):
    is_rising = False
    count_the_same = 0
    has_two_in_row = False
    mod = value % 10
    while value > 0:
        value = int(value / 10)
        curr_mod = value % 10
        if curr_mod == mod:
            if not has_two_in_row:
                count_the_same += 1
        else:
            if count_the_same == 1:
                has_two_in_row = True
            count_the_same = 0
        if curr_mod <= mod:
            is_rising = True
        else:
            return False
        mod = curr_mod

    return is_rising and has_two_in_row


def solve_1():
    count = 0
    for i in range(start, end):
        if contains_two_digits_raising(i):
            count += 1
    return count


def solve_2():
    count = 0
    for i in range(start, end):
        if contains_exactly_two_digits_raising(i):
            count += 1
    return count


# part1
assert contains_two_digits_raising(122345)
assert contains_two_digits_raising(111123)
assert contains_two_digits_raising(111111)
assert not contains_two_digits_raising(223450)
assert not contains_two_digits_raising(123789)
assert 511 == solve_1()

# part2
assert contains_exactly_two_digits_raising(112233)
assert not contains_exactly_two_digits_raising(123444)
assert contains_exactly_two_digits_raising(111122)
assert 316 == solve_2()
