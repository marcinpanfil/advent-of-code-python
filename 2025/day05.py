from file_utils import file_reader


def count_fresh_available_ingredients(data: str) -> int:
    ranges_str, ingredients_str = data.split('\n\n')
    ranges = [[int(x) for x in r.split("-")] for r in ranges_str.split('\n')]
    ingredients = [int(x) for x in ingredients_str.split('\n') if x.strip()]

    result = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                result += 1
                break

    return result


def count_all_fresh_ingredients(data: str) -> int:
    ranges_str, _ = data.split('\n\n')
    ranges = sorted([[int(x) for x in r.split("-")] for r in ranges_str.split('\n')], key=lambda x: x[0])

    merged_ranges = []
    cur_start = ranges[0][0]
    cur_end = ranges[0][1]
    for i in range(1, len(ranges)):
        r = ranges[i]
        if r[0] <= cur_end:
            cur_end = max(cur_end, r[1])
        else:
            merged_ranges.append([cur_start, cur_end])
            cur_start = r[0]
            cur_end = r[1]
    merged_ranges.append([cur_start, cur_end])

    return sum(end - start + 1 for start, end in merged_ranges)


test_data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

SOLUTION_INPUT = file_reader.read_whole_file_as_string('input/day05.txt')

assert count_fresh_available_ingredients(test_data) == 3
assert count_fresh_available_ingredients(SOLUTION_INPUT) == 694
assert count_all_fresh_ingredients(test_data) == 14
assert count_all_fresh_ingredients(SOLUTION_INPUT) == 352716206375547
