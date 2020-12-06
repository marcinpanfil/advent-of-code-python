from file_utils import file_reader


def int_code(values):
    i = 0
    while i < len(values):
        opcode = values[i]
        if opcode == 1:
            values[values[i + 3]] = values[values[i + 2]] + values[values[i + 1]]
            i += 4
        elif opcode == 2:
            values[values[i + 3]] = values[values[i + 2]] * values[values[i + 1]]
            i += 4
        elif opcode == 99:
            return values
        else:
            raise Exception('not known opcode on pos: ' + str(i))


def solve_1():
    values = file_reader.read_ints_from_file_string('input/day02_input.txt')
    values[1] = 12
    values[2] = 2
    values = int_code(values)
    return values[0]


def solve_2(output):
    values = file_reader.read_ints_from_file_string('input/day02_input.txt')
    for noun in range(99):
        for verb in range(99):
            tmp_values = values.copy()
            tmp_values[1] = noun
            tmp_values[2] = verb
            if output == int_code(tmp_values)[0]:
                return 100 * noun + verb


assert [2, 0, 0, 0, 99] == int_code([1, 0, 0, 0, 99])
assert [2, 3, 0, 6, 99] == int_code([2, 3, 0, 3, 99])
assert [2, 4, 4, 5, 99, 9801] == int_code([2, 4, 4, 5, 99, 0])
assert [30, 1, 1, 4, 2, 5, 6, 0, 99] == int_code([1, 1, 1, 4, 99, 5, 6, 0, 99])
assert 2842648 == solve_1()
assert 9074 == solve_2(19690720)
