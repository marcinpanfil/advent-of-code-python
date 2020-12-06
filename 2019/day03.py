import sys

from file_utils import file_reader
from utils.IntPoint import IntPoint


def draw_wire(values):
    wire = []
    curr_pos = IntPoint(0, 0)
    for v in values:
        direction = v[0]
        steps = int(v[1:])
        x_change = 0
        y_change = 0
        if direction == 'R':
            x_change = 1
            y_change = 0
        if direction == 'L':
            x_change = -1
            y_change = 0
        if direction == 'U':
            x_change = 0
            y_change = 1
        if direction == 'D':
            x_change = 0
            y_change = -1

        for i in range(0, int(steps)):
            curr_pos = IntPoint(curr_pos.x + x_change, curr_pos.y + y_change)
            wire.append(curr_pos)

    return wire


def find_cross_distance(wire_a, wire_b):
    min_dist = sys.maxsize
    for a in wire_a:
        if a in wire_b:
            distance = abs(a.x) + abs(a.y)
            if min_dist > distance:
                min_dist = distance
    return min_dist


def find_min_steps(wire_a, wire_b):
    wire_a_set = set(wire_a.copy())
    wire_b_set = set(wire_b.copy())
    min_steps = sys.maxsize
    for a in wire_a_set:
        if a in wire_b_set:
            steps = list(wire_a).index(a) + list(wire_b).index(a)
            if min_steps > steps:
                min_steps = steps
    return min_steps + 2


def solve_1():
    wire_str = file_reader.read_str_from_file('input/day03_input.txt')
    return find_cross_distance(set(draw_wire(wire_str[0].split(','))), set(draw_wire(wire_str[1].split(','))))


def solve_2():
    wire_str = file_reader.read_str_from_file('input/day03_input.txt')
    return find_min_steps(draw_wire(wire_str[0].split(',')), draw_wire(wire_str[1].split(',')))


#part1
assert 21 == len(draw_wire(['R8', 'U5', 'L5', 'D3']))
assert 6 == find_cross_distance(draw_wire(['R8', 'U5', 'L5', 'D3']), draw_wire(['U7', 'R6', 'D4', 'L4']))
assert 159 == find_cross_distance(draw_wire('R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')),
                                  draw_wire('U62,R66,U55,R34,D71,R55,D58,R83'.split(',')))
assert 135 == find_cross_distance(draw_wire('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')),
                                  draw_wire('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')))
assert 1211 == solve_1()

#part2
assert 30 == find_min_steps(draw_wire(['R8', 'U5', 'L5', 'D3']), draw_wire(['U7', 'R6', 'D4', 'L4']))
assert 610 == find_min_steps(draw_wire('R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')),
                             draw_wire('U62,R66,U55,R34,D71,R55,D58,R83'.split(',')))
assert 410 == find_min_steps(draw_wire('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')),
                             draw_wire('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')))
assert 101386 == solve_2()
