from file_utils import file_reader

phase_pattern = [0, 1, 0, -1]


def calculate_phase(signal, patterns, start_point=1):
    new_signal = ''
    for i in range(start_point, len(signal) + 1):
        curr_pattern = patterns[i]
        curr_result = 0
        for j in range(i - 1, len(signal)):
            pos = (j + 1) % len(curr_pattern)
            curr_result += curr_pattern[pos] * int(signal[j])
        digit = abs(curr_result) % 10
        new_signal += str(digit)
    return new_signal


def apply_pattern(idx: int):
    new_pattern = []
    for phase in phase_pattern:
        for i in range(0, idx):
            new_pattern.append(phase)
    return new_pattern


def calculate_after_n_phases(signal, phase_count, start_point=1):
    patterns = {}
    for i in range(1, len(signal) + 1):
        patterns[i] = apply_pattern(i)

    for i in range(phase_count):
        signal = calculate_phase(signal, patterns, start_point)
    return signal


def decode_real_signal(signal, phase_count):
    real_signal = signal * 10000
    offset = int(signal[:7])
    real_signal = list(real_signal[offset:])
    for _ in range(phase_count):
        suffix_sum = 0
        for i in range(len(real_signal) - 1, -1, -1):
            suffix_sum = (suffix_sum + int(real_signal[i])) % 10
            real_signal[i] = str(suffix_sum)
    return ''.join(map(str, real_signal[:8]))


def solve_1():
    decoded = file_reader.read_one_line_str_from_file('input/day16_input.txt')
    return calculate_after_n_phases(decoded, 100)[:8]


def solve_2():
    decoded = file_reader.read_one_line_str_from_file('input/day16_input.txt')
    return decode_real_signal(decoded, 100)


# part 1
assert '24176176' == calculate_after_n_phases('80871224585914546619083218645595', 100)[:8]
assert '73745418' == calculate_after_n_phases('19617804207202209144916044189917', 100)[:8]
assert '52432133' == calculate_after_n_phases('69317163492948606335995924319873', 100)[:8]
assert '12541048' == solve_1()

# part 2
assert '62858988' == solve_2()
