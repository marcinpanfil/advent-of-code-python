from file_utils import file_reader


class Instruction:

    def __init__(self, action, steps):
        self.action = action
        self.steps = steps


def move_ship(instructions: [Instruction]):
    x = 0
    y = 0
    directions = 'ESWN'
    curr_dir = 'E'
    for instruction in instructions:
        if instruction.action == 'N':
            y += instruction.steps
        elif instruction.action == 'S':
            y -= instruction.steps
        elif instruction.action == 'E':
            x += instruction.steps
        elif instruction.action == 'W':
            x -= instruction.steps
        elif instruction.action == 'R':
            if instruction.steps == 90:
                curr_dir = directions[(directions.find(curr_dir) + 1) % 4]
            elif instruction.steps == 180:
                curr_dir = directions[(directions.find(curr_dir) + 2) % 4]
            elif instruction.steps == 270:
                curr_dir = directions[(directions.find(curr_dir) + 3) % 4]
        elif instruction.action == 'L':
            if instruction.steps == 90:
                curr_dir = directions[(directions.find(curr_dir) - 1) % 4]
            elif instruction.steps == 180:
                curr_dir = directions[(directions.find(curr_dir) - 2) % 4]
            elif instruction.steps == 270:
                curr_dir = directions[(directions.find(curr_dir) - 3) % 4]
        elif instruction.action == 'F':
            if curr_dir == 'E':
                x += instruction.steps
            elif curr_dir == 'W':
                x -= instruction.steps
            elif curr_dir == 'N':
                y += instruction.steps
            elif curr_dir == 'S':
                y -= instruction.steps
        else:
            raise Exception('unknown action')
    return abs(x) + abs(y)


def move_ship_and_waypoint(instructions: [Instruction]):
    ship_x = 0
    ship_y = 0
    wp_x = 10
    wp_y = 1
    for instruction in instructions:
        if instruction.action == 'N':
            wp_y += instruction.steps
        elif instruction.action == 'S':
            wp_y -= instruction.steps
        elif instruction.action == 'E':
            wp_x += instruction.steps
        elif instruction.action == 'W':
            wp_x -= instruction.steps
        elif instruction.action == 'R':
            if instruction.steps == 90:
                tmp_x = wp_x
                wp_x = wp_y
                wp_y = -tmp_x
            elif instruction.steps == 180:
                wp_x = -wp_x
                wp_y = -wp_y
            elif instruction.steps == 270:
                tmp_x = wp_x
                wp_x = -wp_y
                wp_y = tmp_x
        elif instruction.action == 'L':
            if instruction.steps == 90:
                tmp_x = wp_x
                wp_x = -wp_y
                wp_y = tmp_x
            elif instruction.steps == 180:
                wp_x = -wp_x
                wp_y = -wp_y
            elif instruction.steps == 270:
                tmp_x = wp_x
                wp_x = wp_y
                wp_y = -tmp_x
        elif instruction.action == 'F':
            ship_x += (instruction.steps * wp_x)
            ship_y -= (instruction.steps * wp_y)
        else:
            raise Exception('unknown action')
    return abs(ship_x) + abs(ship_y)


def parse_input(values):
    instructions = []
    for v in values:
        action = v[0]
        steps = int(v[1:])
        instructions.append(Instruction(action, steps))
    return instructions


def solve_1():
    values = file_reader.read_str_from_file('input/day12_input.txt')
    instructions = parse_input(values)
    return move_ship(instructions)


def solve_2():
    values = file_reader.read_str_from_file('input/day12_input.txt')
    instructions = parse_input(values)
    return move_ship_and_waypoint(instructions)


test_data = '''F10
N3
F7
R90
F11'''

assert 25 == move_ship(parse_input(test_data.split('\n')))
assert 1533 == solve_1()
assert 286 == move_ship_and_waypoint(parse_input(test_data.split('\n')))
assert 25235 == solve_2()
