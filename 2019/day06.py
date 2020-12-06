from collections import defaultdict

from file_utils import file_reader


def build_orbits_graph(values):
    data = defaultdict(list)
    for value in values:
        relation = value.split(')')
        data[relation[0]].append(relation[1])
    return data


def build_reversed_orbits_graph(values):
    data = {}
    for value in values:
        relation = value.split(')')
        data[relation[1]] = relation[0]
    return data


def calculate_total_count(data):
    count = 0
    for planet in list(data.keys()):
        count += calculate_children_count(data, planet)

    return count


def calculate_children_count(data, planet):
    children = data[planet]
    count = len(children)
    for child in children:
        count += calculate_children_count(data, child)
    return count


def calculate_transfers(data):
    you_parent = data['YOU']
    san_parent = data['SAN']
    you_parents = [you_parent]
    san_parents = [san_parent]

    find_parents(data, you_parent, you_parents)
    find_parents(data, san_parent, san_parents)

    return len(list(set(you_parents) ^ set(san_parents)))


def find_parents(data, curr_parent, parents):
    while curr_parent in data:
        curr_parent = data[curr_parent]
        parents.append(curr_parent)


def solve_1():
    orbits = file_reader.read_str_from_file('input/day06_input.txt')
    return calculate_total_count(build_orbits_graph(orbits))


def solve_2():
    orbits = file_reader.read_str_from_file('input/day06_input.txt')
    return calculate_transfers(build_reversed_orbits_graph(orbits))


assert 42 == calculate_total_count(
    build_orbits_graph(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']))
assert 270768 == solve_1()
assert 4 == calculate_transfers(build_reversed_orbits_graph(
    ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']))
assert 451 == solve_2()
