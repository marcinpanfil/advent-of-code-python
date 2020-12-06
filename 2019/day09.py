from file_utils import file_reader


def int_code(values, in_value=[]):
    for _ in range(10000):
        values.append(0)
    i = 0
    rel_base = 0
    while i < len(values):
        instruction = values[i]

        opcode = int(instruction % 100)
        mode_1 = int(instruction / 100) % 10
        mode_2 = int(instruction / 1000) % 10
        mode_3 = int(instruction / 10000) % 10

        if opcode == 1:
            new_value = get_param(values, mode_1, i + 1, rel_base) + get_param(values, mode_2, i + 2, rel_base)
            set_param(values, mode_3, i + 3, rel_base, new_value)
            i += 4
        elif opcode == 2:
            new_value = get_param(values, mode_1, i + 1, rel_base) * get_param(values, mode_2, i + 2, rel_base)
            set_param(values, mode_3, i + 3, rel_base, new_value)
            i += 4
        elif opcode == 3:
            if len(in_value) > 0:
                set_param(values, mode_1, i + 1, rel_base, in_value[0])
                in_value.pop(0)
            i += 2
        elif opcode == 4:
            in_value.append(get_param(values, mode_1, i + 1, rel_base))
            i += 2
        elif opcode == 5:
            if get_param(values, mode_1, i + 1, rel_base) != 0:
                i = get_param(values, mode_2, i + 2, rel_base)
            else:
                i += 3
        elif opcode == 6:
            if get_param(values, mode_1, i + 1, rel_base) == 0:
                i = get_param(values, mode_2, i + 2, rel_base)
            else:
                i += 3
        elif opcode == 7:
            if get_param(values, mode_1, i + 1, rel_base) < get_param(values, mode_2, i + 2, rel_base):
                set_param(values, mode_3, i + 3, rel_base, 1)
            else:
                set_param(values, mode_3, i + 3, rel_base, 0)
            i += 4
        elif opcode == 8:
            if get_param(values, mode_1, i + 1, rel_base) == get_param(values, mode_2, i + 2, rel_base):
                set_param(values, mode_3, i + 3, rel_base, 1)
            else:
                set_param(values, mode_3, i + 3, rel_base, 0)
            i += 4
        elif opcode == 9:
            rel_base += get_param(values, mode_1, i + 1, rel_base)
            i += 2
        elif opcode == 99:
            return in_value
        else:
            raise Exception('not known opcode on pos: ' + str(i))
    return -1


def get_param(values, mode, pos, rel_base):
    # position mode
    if mode == 0:
        return values[values[pos]]
    # immediate mode
    elif mode == 1:
        return values[pos]
    # relative mode
    elif mode == 2:
        return values[values[pos] + rel_base]
    else:
        raise Exception('not know mode in getting param')


def set_param(values, mode, pos, rel_base, new_value):
    if mode == 0:
        values[values[pos]] = new_value
    elif mode == 2:
        values[values[pos] + rel_base] = new_value
    else:
        raise Exception('not know mode in setting param')


def solve_1():
    values = file_reader.read_ints_from_file_string('input/day09_input.txt')
    return int_code(values, [1])


def solve_2():
    values = file_reader.read_ints_from_file_string('input/day09_input.txt')
    return int_code(values, [2])


# part1
assert [1125899906842624] == int_code([104, 1125899906842624, 99], [])
assert 16 == len(str(int_code([1102, 34915192, 34915192, 7, 4, 7, 99, 0], [])[0]))
assert [-1] == int_code([109, -1, 4, 1, 99], [])
assert [1] == int_code([109, -1, 104, 1, 99], [])
assert [109] == int_code([109, -1, 204, 1, 99], [])
assert [204] == int_code([109, 1, 9, 2, 204, -6, 99], [])
assert [204] == int_code([109, 1, 109, 9, 204, -6, 99], [])
assert [204] == int_code([109, 1, 209, -1, 204, -106, 99], [])
assert [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99] == int_code(
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99], [])
assert [3507134798] == solve_1()
# part2
assert [84513] == solve_2()
