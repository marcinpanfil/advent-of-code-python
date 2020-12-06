import math
import sys

from file_utils import file_reader


def calculate_seat(boarding_pass):
    row = boarding_pass[:7]
    col = boarding_pass[-3:]
    min_row = 0
    max_row = 127
    for i in range(7):
        if row[i] == 'F':
            max_row = min_row + int(math.floor((max_row - min_row) / 2))
        elif row[i] == 'B':
            min_row = min_row + int(math.ceil((max_row - min_row) / 2))
    if min_row != max_row:
        raise Exception('wrong row seat')

    min_col = 0
    max_col = 7
    for i in range(3):
        if col[i] == 'R':
            min_col = min_col + int(math.ceil((max_col - min_col) / 2))
        elif col[i] == 'L':
            max_col = min_col + int(math.floor((max_col - min_col) / 2))

    if max_col != min_col:
        raise Exception('wrong col seat')

    return min_row * 8 + min_col


def solve_1():
    values = file_reader.read_str_from_file('input/day05_input.txt')
    max_value = 0
    for boarding_pass in values:
        seat = calculate_seat(boarding_pass)
        max_value = max(max_value, seat)
    return max_value


def solve_2():
    values = file_reader.read_str_from_file('input/day05_input.txt')
    all_seats = []
    for boarding_pass in values:
        seat = calculate_seat(boarding_pass)
        all_seats.append(seat)
    all_seats.sort()

    min_seat = min(all_seats)
    max_seat = max(all_seats)
    counter = 0
    for i in range(min_seat, max_seat):
        if i != all_seats[counter]:
            return all_seats[counter] - 1
        counter += 1


# part 1
assert 357 == calculate_seat('FBFBBFFRLR')
assert 567 == calculate_seat('BFFFBBFRRR')
assert 119 == calculate_seat('FFFBBBFRRR')
assert 820 == calculate_seat('BBFFBBFRLL')
assert 978 == solve_1()

# part 2
assert 727 == solve_2()
