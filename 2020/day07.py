from file_utils import file_reader


class Bag:

    def __init__(self, name, count):
        self.name = name
        self.count = count


def parse_input(values):
    result = {}
    for value in values:
        if 'bags contain no other bags.' not in value:
            info_split = value.split(' bags contain ')
            type_bag = info_split[0]
            carried_bags_split = info_split[1].split(', ')
            bags = []
            for bag_split in carried_bags_split:
                bag_count = int(bag_split[0])
                bag_name = bag_split[2:].replace('.', '')
                if bag_count == 1:
                    bag_name = bag_name.replace(' bag', '')
                else:
                    bag_name = bag_name.replace(' bags', '')
                bags.append(
                    Bag(bag_name, bag_count))
            result[type_bag] = bags
    return result


def list_containing_bags(parsed_data, name):
    valid_bags = set()
    for bag_name in list(parsed_data.keys()):
        bags = parsed_data[bag_name]
        for bag in bags:
            if name == bag.name:
                valid_bags.add(bag_name)
                next_bags = list_containing_bags(parsed_data, bag_name)
                valid_bags.update(next_bags)
    return valid_bags


def count_containing_bags(values):
    parsed_data = parse_input(values)
    bags = list_containing_bags(parsed_data, 'shiny gold')
    return len(bags)


def count_for_bag(parsed_data, name, counter):
    curr_count = 0
    bags = parsed_data[name]
    for bag in bags:
        local_counter = counter * bag.count
        curr_count += local_counter
        if bag.name in list(parsed_data.keys()):
            count = count_for_bag(parsed_data, bag.name, local_counter)
            curr_count += count
    return curr_count


def containing_total_count(values):
    parsed_data = parse_input(values)
    return count_for_bag(parsed_data, 'shiny gold', 1)


def solve_1():
    values = file_reader.read_str_from_file('input/day07_input.txt')
    return count_containing_bags(values)


def solve_2():
    values = file_reader.read_str_from_file('input/day07_input.txt')
    return containing_total_count(values)


test_case_1 = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''

test_case_2 = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.'''

# part1
assert 4 == count_containing_bags(test_case_1.split('\n'))
assert 378 == solve_1()

# part 2
assert 32 == containing_total_count(test_case_1.split('\n'))
assert 126 == containing_total_count(test_case_2.split('\n'))
assert 27526 == solve_2()
