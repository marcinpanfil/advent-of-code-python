from functools import lru_cache

from file_utils import file_reader


def count_possible_designs(lines: list[str]) -> int:
    patterns, words = lines[0].split(", "), lines[2:]

    result = 0
    for w in words:
        result += 1 if __can_build(w, patterns) else 0
    return result


def count_all_possible_ways(lines: list[str]) -> int:
    patterns, words = lines[0].split(", "), lines[2:]

    result = 0
    for w in words:
        result += __count_ways(w, patterns)
    return result


def __can_build(word: str, patterns: list[str]) -> bool:
    patterns = tuple(p for p in patterns if p)

    @lru_cache
    def dfs(remaining):
        if not remaining:
            return True

        for p in patterns:
            if remaining.startswith(p):
                if dfs(remaining[len(p):]):
                    return True
        return False

    return dfs(word)


def __count_ways(word: str, patterns: list[str]) -> int:
    patterns = tuple(p for p in patterns if p)

    @lru_cache
    def dfs(remaining):
        if not remaining:
            return 1

        total = 0
        for p in patterns:
            if remaining.startswith(p):
                total += dfs(remaining[len(p):])
        return total

    return dfs(word)


test_data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

SOLUTION_INPUT = file_reader.read_str_from_file('input/day19.txt')

assert count_possible_designs(test_data.splitlines()) == 6
assert count_possible_designs(SOLUTION_INPUT) == 327

assert count_all_possible_ways(test_data.splitlines()) == 16
assert count_all_possible_ways(SOLUTION_INPUT) == 772696486795255
