import copy

from file_utils import file_reader


class Operation:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + " " + str(self.value)

    def __repr__(self):
        return self.name + " " + str(self.value)

    def __eq__(self, other):
        return self.name == other.name and self.value == self.value

    def __hash__(self):
        return hash(self.name) ^ hash(self.value)


def operate(operations):
    accumulator = 0
    cur_pos = 0
    run_ops = []
    while cur_pos < len(operations):
        operation = operations[cur_pos]
        if cur_pos in run_ops:
            return accumulator
        else:
            run_ops.append(cur_pos)

        if operation.name == 'nop':
            cur_pos += 1
        elif operation.name == 'acc':
            accumulator += operation.value
            cur_pos += 1
        elif operation.name == 'jmp':
            cur_pos += operation.value


def operate_after_change(operations):
    accumulator = 0
    cur_pos = 0
    run_ops = []
    while cur_pos < len(operations):
        operation = operations[cur_pos]
        if cur_pos in run_ops:
            return False, -1
        else:
            run_ops.append(cur_pos)
        if operation.name == 'nop':
            cur_pos += 1
        elif operation.name == 'acc':
            accumulator += operation.value
            cur_pos += 1
        elif operation.name == 'jmp':
            cur_pos += operation.value
    return True, accumulator


def find_wrong_operations(operations):
    idx = find_ops_to_change(operations)

    for id in idx:
        curr_ops = copy.deepcopy(operations)
        if curr_ops[id].name == 'jmp':
            curr_ops[id].name = 'nop'
        elif curr_ops[id].name == 'nop':
            curr_ops[id].name = 'jmp'
        result = operate_after_change(curr_ops)
        if result[0]:
            return result[1]
    return -1


def find_ops_to_change(operations):
    idx = []
    cur_id = 0
    for op in operations:
        if op.name == 'jmp' or op.name == 'nop':
            idx.append(cur_id)
        cur_id += 1
    return idx


def parse_input(values):
    operations = []
    for value in values:
        split = value.split(' ')
        name = split[0]
        count = int(split[1].replace('+', ''))
        operations.append(Operation(name, count))
    return operations


def solve_1():
    values = file_reader.read_str_from_file('input/day08_input.txt')
    operations = parse_input(values)
    return operate(operations)


def solve_2():
    values = file_reader.read_str_from_file('input/day08_input.txt')
    operations = parse_input(values)
    return find_wrong_operations(operations)


test_case_1 = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''

# part 1
assert 5 == operate(parse_input(test_case_1.split('\n')))
assert 1337 == solve_1()

# part 2
assert 8 == find_wrong_operations(parse_input(test_case_1.split('\n')))
assert 1358 == solve_2()
