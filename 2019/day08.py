import sys

from file_utils import file_reader


def calculate_result(input_stream, width, height):
    layers = create_layers(input_stream, width, height)

    min_0 = sys.maxsize
    number_1 = 0
    number_2 = 0
    for layer in layers:
        count_0 = layer.count('0')
        if count_0 <= min_0:
            min_0 = count_0
            number_1 = layer.count('1')
            number_2 = layer.count('2')
    return number_2 * number_1


def create_layers(input_stream, width, height):
    size = width * height
    return [input_stream[i:i + size] for i in range(0, len(input_stream), size)]


# 0 black 1 white 2 transparent
def print_layer(layers, width, height):
    result = ['2'] * (width * height)
    for i in range(height):
        for j in range(width):
            for l in layers:
                pixel = l[i * width + j]
                if pixel == '0' or pixel == '1':
                    result[i * width + j] = pixel
                    break
    return ''.join(result)


def solve_1():
    values = file_reader.read_one_line_str_from_file('input/day08_input.txt')
    return calculate_result(values, 25, 6)


def solve_2():
    values = file_reader.read_one_line_str_from_file('input/day08_input.txt')
    width = 25
    height = 6
    layer = print_layer(create_layers(values, width, height), width, height)
    for i in range(0, len(layer), width):
        print(layer[i:i + width])


# part1
assert 1 == calculate_result('123456789012', 3, 2)
assert 1677 == solve_1()

# part2 result: UBUFP
assert '0110' == str(print_layer(create_layers('0222112222120000', 2, 2), 2, 2))
solve_2()
