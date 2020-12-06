from file_utils import file_reader


def pass_policy_1(password, value, min_value, max_value):
    count = password.count(value)
    if min_value <= count <= max_value:
        return True
    return False


def pass_policy_2(password, value, pos_1, pos_2):
    return (password[pos_1 - 1] == value) != (password[pos_2 - 1] == value)


def count_correct(values, validator):
    count = 0
    for value in values:
        value_split = value.split(': ')
        password = value_split[1]
        count_split = value_split[0].split(' ')
        val = count_split[1]
        nr_split = count_split[0].split('-')
        nr_1 = int(nr_split[0])
        nr_2 = int(nr_split[1])
        if validator(password, val, nr_1, nr_2):
            count += 1
    return count


def solve_1():
    values = file_reader.read_str_from_file('input/day02_input.txt')
    return count_correct(values, pass_policy_1)


def solve_2():
    values = file_reader.read_str_from_file('input/day02_input.txt')
    return count_correct(values, pass_policy_2)


test_case = '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''

# part 1
assert 2 == count_correct(test_case.split('\n'), pass_policy_1)
assert 418 == solve_1()
# part 2
assert 1 == count_correct(test_case.split('\n'), pass_policy_2)
print(solve_2())
