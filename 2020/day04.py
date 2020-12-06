import re

from file_utils import file_reader


def parse_input(input_data, required_fields):
    passports = input_data.split('\n\n')
    valid_pass_count = 0
    for passport in passports:
        req_fields_count = 0
        data_fields = passport.split()
        for data_field in data_fields:
            data = data_field.split(':')
            key = data[0]
            value = data[1]
            if key in list(required_fields.keys()) and required_fields[key](value):
                req_fields_count += 1
        if req_fields_count == len(required_fields.keys()):
            valid_pass_count += 1

    return valid_pass_count


def solve_2():
    values = file_reader.read_one_line_str_from_file('input/day04_input.txt').split('\n\n')
    return parse_input(values, )


hcl_reqex = re.compile('^#[0-9,a-f]{6}$')
pid_regex = re.compile('^[0-9]{9}$')


def byr_validator(value):
    if 1920 <= int(value) <= 2002:
        return True
    return False


def iyr_validator(value):
    if 2010 <= int(value) <= 2020:
        return True
    return False


def eyr_validator(value):
    if 2020 <= int(value) <= 2030:
        return True
    return False


def hgt_validator(value):
    metric = value[-2:]
    if metric == 'cm':
        if 150 <= int(value[:-2]) <= 193:
            return True
        else:
            return False
    elif metric == 'in':
        if 59 <= int(value[:-2]) <= 76:
            return True
        else:
            return False
    return False


def hcl_validator(value):
    return hcl_reqex.match(value)


def ecl_validator(value):
    if value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return True
    return False


def pid_validator(value):
    return pid_regex.match(value)


test_case_1 = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''

test_case_2 = '''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007'''

test_case_3 = '''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''


def always_true(value):
    return True


required_fields_1 = {'byr': always_true, 'iyr': always_true, 'eyr': always_true, 'hgt': always_true,
                     'hcl': always_true, 'ecl': always_true, 'pid': always_true}

required_fields_2 = {'byr': byr_validator, 'iyr': iyr_validator, 'eyr': eyr_validator, 'hgt': hgt_validator,
                     'hcl': hcl_validator, 'ecl': ecl_validator, 'pid': pid_validator}


def solve_1():
    values = file_reader.read_whole_file_as_string('input/day04_input.txt')
    return parse_input(values, required_fields_1)


def solve_2():
    values = file_reader.read_whole_file_as_string('input/day04_input.txt')
    return parse_input(values, required_fields_2)


assert byr_validator('2002')
assert not byr_validator('2003')
assert hgt_validator('60in')
assert hgt_validator('190cm')
assert not hgt_validator('190in')
assert not hgt_validator('190')
assert ecl_validator('brn')
assert not ecl_validator('wat')
assert pid_validator('000000001')
assert not pid_validator('0123456789')
assert not pid_validator('0123456789a')
assert hcl_validator('#abcdef')
assert not hcl_validator('#abcdef1')

# part 1
assert 2 == parse_input(test_case_1, required_fields_1)
assert 204 == solve_1()
# part 2
assert 0 == parse_input(test_case_2, required_fields_2)
assert 4 == parse_input(test_case_3, required_fields_2)
assert 179 == solve_2()
