from typing import Callable

from file_utils import file_reader

GATES: dict[str, Callable[[int, int], int]] = {
    "AND": lambda a, b: 1 if (a == 1 and b == 1) else 0,
    "OR": lambda a, b: 1 if (a == 1 or b == 1) else 0,
    "XOR": lambda a, b: 1 if (a != b) else 0,
}


class Connection:

    def __init__(self, n1: str, n2: str, gate: str, result_n: str):
        self.n1 = n1
        self.n2 = n2
        self.gate = gate
        self.result_n = result_n

# idea + solution from google, improved by AI
def find_swapped_wires(input_str: str) -> str:
    values, connections = __read_date(input_str)

    gates: dict[str, tuple[str, str, str]] = {}
    for c in connections:
        gates[c.result_n] = (c.gate, c.n1, c.n2)

    wrong_outputs: set[str] = set()
    max_z: str = max(out for out in gates if out.startswith('z'))

    for output, (op, n1, n2) in gates.items():
        if output.startswith('z') and output != max_z and op != 'XOR':
            wrong_outputs.add(output)

    for output, (op, n1, n2) in gates.items():
        if op == 'XOR':
            has_xy_inputs = (n1[0] in 'xy' and n2[0] in 'xy')
            outputs_to_z = output.startswith('z')

            if has_xy_inputs and not outputs_to_z and n1 not in ['x00', 'y00']:
                used_by_xor = any(opc == 'XOR' and output in [n1c, n2c] for _, (opc, n1c, n2c) in gates.items())
                if not used_by_xor:
                    wrong_outputs.add(output)
            elif not has_xy_inputs and not outputs_to_z:
                wrong_outputs.add(output)

    for output, (op, n1, n2) in gates.items():
        if op == 'AND' and {n1, n2} != {'x00', 'y00'}:
            feeds_or = any(opc == 'OR' and output in [n1c, n2c] for _, (opc, n1c, n2c) in gates.items())
            if not feeds_or:
                wrong_outputs.add(output)

    for output, (op, n1, n2) in gates.items():
        if op == 'OR':
            if n1 in gates and gates[n1][0] != 'AND':
                wrong_outputs.add(n1)
            if n2 in gates and gates[n2][0] != 'AND':
                wrong_outputs.add(n2)

    return ','.join(sorted(wrong_outputs))


def connect_bits(input_str: str) -> int:
    values, connections = __read_date(input_str)

    waiting = []
    while connections:
        for c in connections:
            if values.get(c.n1) is not None and values.get(c.n2) is not None:
                res = GATES[c.gate](values[c.n1], values[c.n2])
                values[c.result_n] = res
            else:
                waiting.append(c)
        connections = waiting
        waiting = []

    keys_with_z = sorted([s for s in values.keys() if s.startswith("z")], reverse=True)
    bits = [values[s] for s in keys_with_z]
    return int("".join(map(str, bits)), 2)


def __read_date(input_str: str) -> tuple[dict[str, int], list[Connection]]:
    start_values_part, operations_part = input_str.split("\n\n")
    values: dict[str, int] = {}
    for line in start_values_part.split("\n"):
        n, v = line.split(": ")
        values[n] = int(v)

    connections: list[Connection] = []
    for operation in operations_part.split("\n"):
        n1, g, n2, _, rn = operation.split(" ")
        connections.append(Connection(n1, n2, g, rn))

    return values, connections


test_date = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

SOLUTION_INPUT = file_reader.read_whole_file_as_string("input/day24.txt")

assert connect_bits(test_date) == 2024
assert connect_bits(SOLUTION_INPUT) == 36902370467952

assert find_swapped_wires(SOLUTION_INPUT) == "cvp,mkk,qbw,wcb,wjb,z10,z14,z34"
