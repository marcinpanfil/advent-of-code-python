import math as m
from file_utils import file_reader


def calculate_module_fuel(value):
    result = m.floor(value / 3) - 2
    return result


def calculate_fuel_for_fuel(value):
    result = 0
    while value > 0:
        value = calculate_module_fuel(value)
        if value > 0:
            result += value
    return result


def sum_fuel_from_all_modules(values):
    result = 0
    for value in values:
        result += calculate_module_fuel(value)
    return result


def sum_fuel_from_all_modules_plus_fuel(values):
    result = 0
    for value in values:
        fuel = calculate_module_fuel(value)
        result += fuel
        result += calculate_fuel_for_fuel(fuel)
    return result


def solve_part1():
    values = file_reader.read_ints_from_file('input/day01_input.txt')
    result = sum_fuel_from_all_modules(values)
    print('solution part 1: ', result)
    return result


def solve_part2():
    values = file_reader.read_ints_from_file('input/day01_input.txt')
    result = sum_fuel_from_all_modules_plus_fuel(values)
    print('solution part 2: ', result)
    return result


# part 1
assert 2 == calculate_module_fuel(12)
assert 2 == calculate_module_fuel(14)
assert 654 == calculate_module_fuel(1969)
assert 33583 == calculate_module_fuel(100756)
assert 3188480 == solve_part1()

# part 2
assert 0 == calculate_fuel_for_fuel(2)
assert 312 == calculate_fuel_for_fuel(654)
assert 16763 == calculate_fuel_for_fuel(33583)
assert 4779847 == solve_part2()
