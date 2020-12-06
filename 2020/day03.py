from file_utils import file_reader


def calculate_trees(values, down, right):
    x_id = 0
    tree_count = 0
    for i in range(0, len(values), down):
        line = values[i]
        if line[x_id] == '#':
            tree_count += 1
        x_id += right
        if x_id >= len(line) - 1:
            x_id -= len(line)
    return tree_count


def calculate_trees_2(values):
    return calculate_trees(values, 1, 1) * calculate_trees(values, 1, 3) * calculate_trees(values, 1, 5) * \
           calculate_trees(values, 1, 7) * calculate_trees(values, 2, 1)


def solve_1():
    values = file_reader.read_str_from_file('input/day03_input.txt')
    return calculate_trees(values, 1, 3)


def solve_2():
    values = file_reader.read_str_from_file('input/day03_input.txt')
    return calculate_trees_2(values)


test_case = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''

# part 1
assert 7 == calculate_trees(test_case.split('\n'), 1, 3)
assert 2 == calculate_trees(test_case.split('\n'), 2, 1)
assert 278 == solve_1()
# part 2
assert 336 == calculate_trees_2(test_case.split('\n'))
assert 9709761600 == solve_2()
