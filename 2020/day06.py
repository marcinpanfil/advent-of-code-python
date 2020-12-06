from file_utils import file_reader


def calculate_group(answers):
    all_answers = set()
    for answer in answers:
        for question in answer:
            all_answers.add(question)
    return len(all_answers)


def calculate_all_groups(all_answers, calculator):
    total_count = 0
    for answers in all_answers:
        total_count += calculator(answers.split('\n'))
    return total_count


def calculate_everyone(answers):
    all_answers = {}
    for answer in answers:
        for question in answer:
            if question in all_answers:
                all_answers[question] += 1
            else:
                all_answers[question] = 1
    total_count = 0
    for answer in list(all_answers.keys()):
        if all_answers[answer] == len(answers):
            total_count += 1
    return total_count


def solve_1():
    values = file_reader.read_whole_file_as_string('input/day06_input.txt')
    return calculate_all_groups(values.split('\n\n'), calculate_group)


def solve_2():
    values = file_reader.read_whole_file_as_string('input/day06_input.txt')
    return calculate_all_groups(values.split('\n\n'), calculate_everyone)


test_case_1 = '''abc

a
b
c

ab
ac

a
a
a
a

b'''

# part 1
assert 11 == calculate_all_groups(test_case_1.split('\n\n'), calculate_group)
assert 6662 == solve_1()

# part 2
assert 6 == calculate_all_groups(test_case_1.split('\n\n'), calculate_everyone)
assert 3382 == solve_2()
