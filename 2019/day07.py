import copy
import itertools

from file_utils import file_reader


def find_max(values):
    max_output = 0
    for phases in itertools.permutations(range(5)):
        prev_out = 0
        for i in phases:
            apl = Aplifier(copy.deepcopy(values), i)
            prev_out = apl.int_code(prev_out)
        max_output = max(max_output, prev_out)

    return max_output


def find_max_with_feedback(values):
    max_output = 0
    for phases in itertools.permutations(range(5, 10)):
        prev_out = 0
        amps = [Aplifier(copy.deepcopy(values), phase) for phase in phases]
        while all([not amp.finished for amp in amps]):
            for i in range(5):
                result = amps[i].int_code(prev_out)
                if result is not None:
                    prev_out = result
        max_output = max(max_output, prev_out)

    return max_output


class Aplifier:

    def __init__(self, values, in_value):
        self.finished = False
        self.values = values
        self.in_value = in_value
        self.first_in = True
        self.curr_idx = 0

    def int_code(self, phase):
        while self.curr_idx < len(self.values):
            instruction = self.values[self.curr_idx]

            opcode = int(instruction % 100)
            mode_1 = int(instruction / 100) % 10
            mode_2 = int(instruction / 1000) % 10
            mode_3 = int(instruction / 10000) % 10

            if opcode == 1:
                self.values[self.values[self.curr_idx + 3]] = self.get_param(mode_1, self.curr_idx + 1) + \
                                                              self.get_param(mode_2, self.curr_idx + 2)
                self.curr_idx += 4
            elif opcode == 2:
                self.values[self.values[self.curr_idx + 3]] = self.get_param(mode_1, self.curr_idx + 1) * \
                                                              self.get_param(mode_2, self.curr_idx + 2)
                self.curr_idx += 4
            elif opcode == 3:
                if self.first_in:
                    self.values[self.values[self.curr_idx + 1]] = self.in_value
                    self.first_in = False
                else:
                    self.values[self.values[self.curr_idx + 1]] = phase
                self.curr_idx += 2
            elif opcode == 4:
                self.curr_idx += 2
                return self.get_param(mode_1, self.curr_idx - 1)
            elif opcode == 5:
                if self.get_param(mode_1, self.curr_idx + 1) != 0:
                    self.curr_idx = self.get_param(mode_2, self.curr_idx + 2)
                else:
                    self.curr_idx += 3
            elif opcode == 6:
                if self.get_param(mode_1, self.curr_idx + 1) == 0:
                    self.curr_idx = self.get_param(mode_2, self.curr_idx + 2)
                else:
                    self.curr_idx += 3
            elif opcode == 7:
                if self.get_param(mode_1, self.curr_idx + 1) < self.get_param(mode_2, self.curr_idx + 2):
                    self.values[self.values[self.curr_idx + 3]] = 1
                else:
                    self.values[self.values[self.curr_idx + 3]] = 0
                self.curr_idx += 4
            elif opcode == 8:
                if self.get_param(mode_1, self.curr_idx + 1) == self.get_param(mode_2, self.curr_idx + 2):
                    self.values[self.values[self.curr_idx + 3]] = 1
                else:
                    self.values[self.values[self.curr_idx + 3]] = 0
                self.curr_idx += 4
            elif opcode == 99:
                self.finished = True
                return None
            else:
                raise Exception('not known opcode on pos: ' + str(self.curr_idx))
        return -1

    def get_param(self, mode, pos):
        if mode == 0:
            return self.values[self.values[pos]]
        elif mode == 1:
            return self.values[pos]


def solve_1():
    values = file_reader.read_ints_from_file_string('input/day07_input.txt')
    return find_max(values)


def solve_2():
    values = file_reader.read_ints_from_file_string('input/day07_input.txt')
    return find_max_with_feedback(values)


assert 43210 == find_max([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])
assert 65210 == find_max(
    [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31,
     4, 31, 99, 0, 0, 0])
assert 54321 == find_max(
    [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0])
assert 30940 == solve_1()

assert 139629729 == find_max_with_feedback(
    [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0,
     5])
assert 18216 == find_max_with_feedback(
    [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53,
     54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10])
assert 76211147 == solve_2()
