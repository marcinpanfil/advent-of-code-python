import math

from file_utils import file_reader


class Chemical:

    def __init__(self, name, count, ingredients):
        self.name = name
        self.count = count
        self.ingredients = ingredients

    def __str__(self):
        return self.name


class Ingredient:

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __str__(self):
        return self.name


def parse_reaction_list(reactions):
    chemicals_data = {}
    for reaction in reactions:
        split = reaction.split(' => ')
        chem = split[1].split(' ')
        chem_count = int(chem[0])
        name = chem[1]
        ingredients_split = split[0].split(', ')
        ingredients = []
        for ingredient in ingredients_split:
            ing_split = ingredient.split(' ')
            ing_count = int(ing_split[0])
            ing_name = ing_split[1]
            ingredients.append(Ingredient(ing_name, ing_count))
        chemicals_data[name] = Chemical(name, chem_count, ingredients)
    return chemicals_data


def calculate_needed_ore(chemicals, created, name, counter):
    chem = chemicals[name]
    total_count = 0
    exist_chem = created.get(name, 0)
    factor = int(math.ceil(max(counter - exist_chem, 0) / chem.count))
    extra = (chem.count * factor) - (counter - exist_chem)
    if chem.name != 'ORE':
        created[name] = extra
    for ing in chem.ingredients:
        if ing.name == 'ORE':
            total_count += factor * ing.count
        else:
            total_count += calculate_needed_ore(chemicals, created, ing.name, factor * ing.count)

    return total_count


def calculate_ore(values, counter):
    chems = parse_reaction_list(values)
    return calculate_needed_ore(chems, {}, 'FUEL', counter)


def calculate_fuel(values, max_cap):
    result = 0
    chems = parse_reaction_list(values)
    prev_res = calculate_needed_ore(chems, {}, 'FUEL', 1)
    # range need to be adopted based on the ore needed for 1 fuel
    for counter in range(2, 5002):
        ore = calculate_needed_ore(chems, {}, 'FUEL', counter)
        diff = int(ore - prev_res)
        prev_res = ore
        result += diff
    start = math.floor(max_cap / math.floor(result / 5000))
    result = 0
    while result <= max_cap:
        result = calculate_needed_ore(chems, {}, 'FUEL', start)
        if result <= max_cap:
            start += 1
    return start - 1


max_cap = 1000000000000


def solve_1():
    values = file_reader.read_str_from_file('input/day14_input.txt')
    return calculate_ore(values, 1)


def solve_2():
    values = file_reader.read_str_from_file('input/day14_input.txt')
    return calculate_fuel(values, max_cap)


test_case_1 = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

test_case_2 = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

test_case_3 = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''

test_case_4 = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''

test_case_5 = '''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX'''

# part 1
assert 31 == calculate_ore(test_case_1.split('\n'), 1)
assert 165 == calculate_ore(test_case_2.split('\n'), 1)
assert 13312 == calculate_ore(test_case_3.split('\n'), 1)
assert 180697 == calculate_ore(test_case_4.split('\n'), 1)
assert 2210736 == calculate_ore(test_case_5.split('\n'), 1)
assert 873899 == solve_1()

# part 2
# assert 82892753 == calculate_fuel(test_case_3.split('\n'), max_cap)
# assert 5586022 == calculate_fuel(test_case_4.split('\n'), max_cap)
assert 460664 == calculate_fuel(test_case_5.split('\n'), max_cap)
assert 1893569 == solve_2()
