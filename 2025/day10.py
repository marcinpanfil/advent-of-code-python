import pulp
import re

from typing import List

import file_reader


def configure_machines(data: List[str]) -> int:
    machines = __parse_data(data)

    result = 0
    for machine in machines:
        ld = machine.light_diagram
        expected_res = [0 if l == '.' else 1 for l in ld]
        bs = machine.button_schemantic
        matrix = []
        for i in range(len(expected_res)):
            line = []
            for b in bs:
                if i in b:
                    line.append(1)
                else:
                    line.append(0)
            matrix.append(line)
        result += sum(__solve_mod2_min(matrix, expected_res))
    return result


def configure_machines_counters(data: List[str]) -> int:
    machines = __parse_data(data)

    result = 0
    for machine in machines:
        bs = machine.button_schemantic
        matrix = []
        for i in range(len(machine.joltage_req)):
            line = []
            for b in bs:
                if i in b:
                    line.append(1)
                else:
                    line.append(0)
            matrix.append(line)
        result += sum(__solve_min_sum_integer(matrix, machine.joltage_req))

    return result

def __solve_min_sum_integer(matrix, result) -> List[int]:
    n = len(matrix)
    m = len(matrix[0])

    prob = pulp.LpProblem("min_sum", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(m)]

    prob += pulp.lpSum(x)
    for i in range(n):
        prob += pulp.lpSum(matrix[i][j] * x[j] for j in range(m)) == result[i]

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if status != pulp.LpStatusOptimal:
        raise ValueError(f"problem is not optimal: {status}")

    solution = [int(pulp.value(var)) for var in x]
    return solution

def __solve_mod2_min(matrix, result) -> List[int]:
    n = len(matrix)
    m = len(matrix[0])
    prob = pulp.LpProblem("min_sum", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{j}", cat="Binary") for j in range(m)]
    k = [pulp.LpVariable(f"k{i}", lowBound=0, cat="Integer") for i in range(n)]

    prob += pulp.lpSum(x)
    for i in range(n):
        prob += pulp.lpSum(matrix[i][j] * x[j] for j in range(m)) == 2 * k[i] + result[i]

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if status != pulp.LpStatusOptimal:
        raise ValueError(f"problem is not optimal: {status}")

    return [int(v.value()) for v in x]


class Machine:
    light_diagram: str
    button_schemantic: List[List[int]]
    joltage_req: List[int]

    def __init__(self, light_diagram: str, button_schemantic: List[List[int]], joltage_req: List[int]):
        self.light_diagram = light_diagram
        self.button_schemantic = button_schemantic
        self.joltage_req = joltage_req


def __parse_data(data: List[str]):
    machines: List[Machine] = []
    for line in data:
        match = re.search(r'\[(.*?)]', line)
        if match:
            lg = match.group(1)
        else:
            raise ValueError("light diagram error")
        bs = [list(map(int, group.split(','))) for group in re.findall(r'\((.*?)\)', line)]
        jr = [int(x) for x in re.search(r'\{(.*?)}', line).group(1).split(',')]
        machines.append(Machine(lg, bs, jr))
    return machines


test_data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day10.txt')

assert configure_machines(test_data.splitlines()) == 7
assert configure_machines(SOLUTION_INPUT) == 417
assert configure_machines_counters(test_data.splitlines()) == 33
assert configure_machines_counters(SOLUTION_INPUT) == 16765