from typing import List

from IntPoint import IntPoint


def char_at(grid: List[str], x: int, y: int) -> str | None:
    if y < 0 or y >= len(grid):
        return None
    row = grid[y]
    if x < 0 or x >= len(row):
        return None

    return row[x]


def replace_char(grid: List[str], x: int, y: int, new_char: str) -> List[str]:
    if len(new_char) != 1:
        return grid
    if y < 0 or y >= len(grid):
        return grid
    row = grid[y]
    if x < 0 or x >= len(row):
        return grid

    updated_row = row[:x] + new_char + row[x + 1:]
    grid[y] = updated_row

    return grid


def replace_chars(grid: List[str], start_x: int, start_y: int, new_chars: str) -> List[str]:
    if start_y < 0 or start_y >= len(grid) or len(new_chars) > len(grid[0]):
        return grid
    row = grid[start_y]
    if start_x < 0 or start_x >= len(row):
        return grid

    updated_row = row[:start_x] + new_chars + row[start_x + len(new_chars):]
    grid[start_y] = updated_row

    return grid


def find_first_char(grid: List[str], to_find: str) -> IntPoint | None:
    if to_find is not None:
        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                if char == to_find:
                    return IntPoint(x, y)
    return None
