from file_utils import file_reader


def int_code(values, in_value):
    i = 0
    while i < len(values):
        instruction = values[i]

        opcode = int(instruction % 100)
        mode_1 = int(instruction / 100) % 10
        mode_2 = int(instruction / 1000) % 10
        mode_3 = int(instruction / 10000) % 10

        if opcode == 1:
            values[values[i + 3]] = get_param(values, mode_1, i + 1) + get_param(values, mode_2, i + 2)
            i += 4
        elif opcode == 2:
            values[values[i + 3]] = get_param(values, mode_1, i + 1) * get_param(values, mode_2, i + 2)
            i += 4
        elif opcode == 3:
            if mode_1 == 0:
                values[values[i + 1]] = in_value
            else:
                values[i + 1] = in_value
            i += 2
        elif opcode == 4:
            in_value = get_param(values, mode_1, i + 1)
            i += 2
        elif opcode == 5:
            if get_param(values, mode_1, i + 1) != 0:
                i = get_param(values, mode_2, i + 2)
            else:
                i += 3
        elif opcode == 6:
            if get_param(values, mode_1, i + 1) == 0:
                i = get_param(values, mode_2, i + 2)
            else:
                i += 3
        elif opcode == 7:
            if get_param(values, mode_1, i + 1) < get_param(values, mode_2, i + 2):
                values[values[i + 3]] = 1
            else:
                values[values[i + 3]] = 0
            i += 4
        elif opcode == 8:
            if get_param(values, mode_1, i + 1) == get_param(values, mode_2, i + 2):
                values[values[i + 3]] = 1
            else:
                values[values[i + 3]] = 0
            i += 4
        elif opcode == 99:
            return in_value
        else:
            raise Exception('not known opcode on pos: ' + str(i))
    return -1


def get_param(values, mode, pos):
    if mode == 0:
        return values[values[pos]]
    elif mode == 1:
        return values[pos]


def solve_1():
    values = file_reader.read_ints_from_file_string('input/day05_input.txt')
    return int_code(values, 1)


def solve_2():
    values = file_reader.read_ints_from_file_string('input/day05_input.txt')
    return int_code(values, 5)


# part 1
assert 1 == int_code([1002, 4, 3, 4, 33], 1)
assert 8332629 == solve_1()

# part_2
test_values = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
assert 999 == int_code(test_values, 7)
assert 1000 == int_code(test_values, 8)
assert 1001 == int_code(test_values, 1234)
assert 8805067 == solve_2()
