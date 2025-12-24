import time


def find_invalid_ids(input: str) -> int:
    ranges = input.split(',')
    result: int = 0
    for range_str in ranges:
        start, end = map(int, range_str.split('-'))

        for i in range(start, end + 1):
            s = str(i)
            mid_idx = len(s) // 2
            if s[:mid_idx] == s[mid_idx:]:
                result += i
    return result


def find_invalid_ids_at_least_twice(input: str) -> int:
    ranges = input.split(',')
    result: int = 0
    start = time.time()
    for range_str in ranges:
        start, end = map(int, range_str.split('-'))

        for i in range(start, end + 1):
            s = str(i)
            for j in range(2, len(s) + 1):
                if len(s) % j == 0:
                    idx = len(s) // j
                    s_to_cmp = s[:idx] * j
                    if s_to_cmp == s:
                        result += i
                        break
    end = time.time()
    print((start - end))
    return result


test_case = (
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,"
    "565653-565659,824824821-824824827,2121212118-2121212124")

SOLUTION_INPUT = (
    "52500467-52574194,655624494-655688785,551225-576932,8418349387-8418411293,678-1464,33-79,74691-118637,"
    "8787869169-8787890635,9898977468-9899009083,548472423-548598890,337245835-337375280,482823-543075,"
    "926266-991539,1642682920-1642753675,3834997-3940764,1519-2653,39697698-39890329,3-21,3251796-3429874,"
    "3467-9298,26220798-26290827,80-124,200638-280634,666386-710754,21329-64315,250-528,9202893-9264498,"
    "819775-903385,292490-356024,22-32,2663033-2791382,133-239,56514707-56704320,432810-458773,"
    "4949427889-4949576808")

# assert find_invalid_ids(test_case) == 1227775554
# assert find_invalid_ids(SOLUTION_INPUT) == 41294979841
assert find_invalid_ids_at_least_twice(test_case) == 4174379265
assert find_invalid_ids_at_least_twice(SOLUTION_INPUT) == 66500947346