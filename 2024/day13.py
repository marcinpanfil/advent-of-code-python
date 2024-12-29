import re
from typing import List, Tuple

from file_utils import file_reader
from utils.IntPoint import IntPoint


def calculate_total_cost(lines: str, addition: int = 0) -> int:
    data: List[Tuple[IntPoint, IntPoint, IntPoint]] = __parse_input(lines)
    total_cost: int = 0

    for (button_1, button_2, prize) in data:
        a, b = solve_two_equations(button_1.x, button_2.x, prize.x + addition, button_1.y, button_2.y,
                                   prize.y + addition)
        if a and b:
            total_cost += a * 3 + b

    return total_cost


def solve_two_equations(a1, b1, c1, a2, b2, c2) -> (int, int):
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None, None

    a = (c1 * b2 - c2 * b1) / determinant
    b = (a1 * c2 - a2 * c1) / determinant

    if a.is_integer() and b.is_integer():
        return int(a), int(b)
    return None, None


def __parse_input(lines: str) -> List[Tuple[IntPoint, IntPoint, IntPoint]]:
    claw_machines = lines.split("\n\n")
    result: List[Tuple[IntPoint, IntPoint, IntPoint]] = []
    for claw_machine in claw_machines:
        behaviour = ()
        for line in claw_machine.splitlines():
            numbers = re.findall(r"\d+", line)
            behaviour = behaviour + tuple([IntPoint(int(numbers[0]), int(numbers[1]))])
        result.append(behaviour)
    return result


TEST_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

SOLUTION_INPUT = file_reader.read_whole_file_as_string('input\\day13.txt')

assert calculate_total_cost(TEST_INPUT) == 480
assert calculate_total_cost(SOLUTION_INPUT) == 28753
assert calculate_total_cost(SOLUTION_INPUT, 10000000000000) == 102718967795500
