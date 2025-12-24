from typing import List


def char_at(grid: List[str], x: int, y: int) -> str | None:
    if y < 0 or y >= len(grid):
        return None
    row = grid[y]
    if x < 0 or x >= len(row):
        return None

    return row[x]

def replace_char(grid: List[str], x: int, y: int, new_char: str) -> List[str]:
    if y < 0 or y >= len(grid):
        return grid
    row = grid[y]
    if x < 0 or x >= len(row):
        return grid

    updated_row = row[:x] + new_char + row[x+1:]
    grid[y] = updated_row

    return grid