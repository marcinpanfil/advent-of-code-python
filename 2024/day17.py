from typing import List, Callable


class Program:
    register_A: int = 0
    register_B: int = 0
    register_C: int = 0
    instructions: List[int] = []
    outputs: List[int] = []
    ins_to_func: dict[int, Callable[[int], int]] = {}

    def __init__(self, register_a, register_b, register_c, instructions: List[int]):
        self.register_A = register_a
        self.register_B = register_b
        self.register_C = register_c
        self.instructions = instructions
        self.outputs = []
        self.ins_to_func: dict[int, Callable[[int], int]] = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    def execute(self):
        idx = 0
        while idx < len(self.instructions):
            opcode = self.instructions[idx]
            jump = self.ins_to_func[opcode](self.instructions[idx + 1])
            if jump == -1:
                idx += 2
            else:
                idx = jump

    def operand_value(self, operand: int) -> int:
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.register_A
        elif operand == 5:
            return self.register_B
        elif operand == 6:
            return self.register_C
        else:
            raise ValueError(f"Shouldn't be here: {operand}")

    def adv(self, operand: int) -> int:
        self.register_A >>= self.operand_value(operand)
        return -1

    def bxl(self, operand: int) -> int:
        self.register_B ^= operand
        return -1

    def bst(self, operand: int) -> int:
        self.register_B = self.operand_value(operand) % 8
        return -1

    def jnz(self, operand: int) -> int:
        if self.register_A == 0:
            return -1
        else:
            return operand

    def bxc(self, _: int) -> int:
        self.register_B ^= self.register_C
        return -1

    def out(self, operand: int) -> int:
        self.outputs.append(self.operand_value(operand) % 8)
        return -1

    def bdv(self, operand: int) -> int:
        self.register_B = int(self.register_A / pow(2, self.operand_value(operand)))
        return -1

    def cdv(self, operand: int) -> int:
        self.register_C = int(self.register_A / pow(2, self.operand_value(operand)))
        return -1


def find_output(a: int, b: int, c: int, instructions: List[int]) -> tuple[List[int], int, int, int]:
    p: Program = Program(a, b, c, instructions)
    p.execute()
    return p.outputs, p.register_A, p.register_B, p.register_C


def find_min_value_of_copy(instructions: List[int], pos: int = 0, current_a: int = 0) -> int:
    if pos == len(instructions):
        return current_a

    for digit in range(8):
        test_a = (current_a << 3) | digit
        test_p = Program(test_a, 0, 0, instructions)
        test_p.execute()

        if test_p.outputs == instructions[-(pos + 1):]:
            result = find_min_value_of_copy(instructions, pos + 1, test_a)
            if result != -1:
                return result
    return -1


assert find_output(0, 0, 9, [2, 6])[2] == 1
assert find_output(10, 0, 0, [5, 0, 5, 1, 5, 4])[0] == [0, 1, 2]
assert find_output(2024, 0, 0, [0, 1, 5, 4, 3, 0])[0] == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
assert find_output(0, 29, 0, [1, 7])[2] == 26
assert find_output(0, 2024, 43690, [4, 0])[2] == 44354
assert find_output(729, 0, 0, [0, 1, 5, 4, 3, 0])[0] == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]
assert (find_output(52884621, 0, 0, [2, 4, 1, 3, 7, 5, 4, 7, 0, 3, 1, 5, 5, 5, 3, 0])[0]
        == [1, 3, 5, 1, 7, 2, 5, 1, 6])

assert find_min_value_of_copy([0, 3, 5, 4, 3, 0]) == 117440
assert find_min_value_of_copy([2, 4, 1, 3, 7, 5, 4, 7, 0, 3, 1, 5, 5, 5, 3, 0]) == 236555997372013
