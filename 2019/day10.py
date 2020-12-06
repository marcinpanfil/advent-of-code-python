import math

from file_utils import file_reader
from utils.IntPoint import IntPoint


def detect_asteroids(data):
    points = load_points(data)
    return find_all_in_sight(points)


def load_points(data):
    points = []
    for y, line in enumerate(data):
        for x, obj in enumerate(line):
            if obj == '#':
                points.append(IntPoint(x, y))
    return points


def find_all_in_sight(asteroids):
    max_in_sight = 0
    for asteroid in asteroids:
        to_check = asteroids.copy()
        angles = calculate_angles(to_check, asteroid)
        curr_in_sight = len(to_check)
        for k, v in angles.items():
            if len(v) > 1:
                curr_in_sight = curr_in_sight - (len(v) - 1)
        if curr_in_sight > max_in_sight:
            max_in_sight = curr_in_sight
            best_point = asteroid
    return [max_in_sight, best_point]


def is_on_the_same_line(first: IntPoint, second: IntPoint, test: IntPoint):
    return first.x * (second.y - test.y) + second.x * (test.y - first.y) + test.x * (first.y - second.y) == 0


def calculate_angles(asteroids: [IntPoint], middle: IntPoint):
    angles = {}
    asteroids.remove(middle)
    for point in asteroids:
        dx = middle.x - point.x
        dy = middle.y - point.y
        angle = math.atan2(-dx, dy)
        value = round(math.degrees(angle if angle >= 0 else 2 * math.pi + angle), 4)

        if value in angles:
            angles[value].append(point)
        else:
            angles[value] = [point]
    return angles


def destroy_asteroids(data, middle: IntPoint, elem_pos):
    angles = list(data.keys())
    angles.sort()

    for angle in angles:
        curr = list(data[angle])
        curr.sort(key=lambda p: abs(middle.x - p.x) + abs(middle.y - p.y))
        data[angle] = curr

    idx = 1
    angle_idx = 0
    while idx <= elem_pos:
        angle = angles[angle_idx]
        angle_points = list(data[angle])
        to_remove = angle_points.pop(0)
        if len(angle_points) == 0:
            angles.pop(angle_idx)
            data.pop(angle, None)
        else:
            data[angle] = angle_points
            angle_idx += 1

        if idx == elem_pos:
            return to_remove

        idx += 1
        if angle_idx == len(angles) - 1:
            angle_idx = 0

    raise Exception('no point at pos {}', elem_pos)


def get_removed_element_at_pos(data, pos):
    points = load_points(data)
    middle = find_all_in_sight(points)[1]
    angles = calculate_angles(points, middle)
    return destroy_asteroids(angles, middle, pos)


def solve_1():
    values = file_reader.read_str_from_file('input/day10_input.txt')
    return detect_asteroids(values)


def solve_2():
    values = file_reader.read_str_from_file('input/day10_input.txt')
    result = get_removed_element_at_pos(values, 200)
    return result.x * 100 + result.y


assert is_on_the_same_line(IntPoint(0, 0), IntPoint(5, 5), IntPoint(2, 2))
assert is_on_the_same_line(IntPoint(1, 1), IntPoint(1, 4), IntPoint(1, 5))
assert is_on_the_same_line(IntPoint(0, 0), IntPoint(5, 5), IntPoint(11, 11))
assert not is_on_the_same_line(IntPoint(0, 0), IntPoint(5, 5), IntPoint(11, 12))
assert not is_on_the_same_line(IntPoint(1, 5), IntPoint(2, 5), IntPoint(4, 6))

test_case_1 = '''.#..#
.....
#####
....#
...##'''

test_case_2 = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''

test_case_3 = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''

test_case_4 = '''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'''

# part1
result_1 = detect_asteroids(test_case_1.split('\n'))
assert 8 == result_1[0]
assert IntPoint(3, 4) == result_1[1]
result_2 = detect_asteroids(test_case_2.split('\n'))
assert 33 == result_2[0]
assert IntPoint(5, 8) == result_2[1]
result_3 = detect_asteroids(test_case_3.split('\n'))
assert 210 == result_3[0]
assert IntPoint(11, 13) == result_3[1]
result_4 = detect_asteroids(test_case_4.split('\n'))
assert 41 == result_4[0]
assert IntPoint(6, 3) == result_4[1]
assert 253 == solve_1()[0]

# part2
assert IntPoint(4, 3) == get_removed_element_at_pos(test_case_1.split('\n'), 4)
middle = IntPoint(11, 13)
points = [IntPoint(11, 12), IntPoint(12, 1), IntPoint(12, 2), middle, IntPoint(9, 6), IntPoint(8, 2),
          IntPoint(12, 8), IntPoint(16, 0), IntPoint(16, 9), IntPoint(10, 16)]
assert IntPoint(8, 2) == destroy_asteroids(calculate_angles(points, middle), middle, 9)
assert IntPoint(8, 2) == get_removed_element_at_pos(test_case_3.split('\n'), 200)
assert 815 == solve_2()
