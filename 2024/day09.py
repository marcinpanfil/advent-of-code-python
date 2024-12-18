from typing import List, Union

from file_utils import file_reader


class MemoryBlock:

    def __init__(self, id: int, size: int, value: Union[int, None]):
        self.id = id
        self.size = size
        self.value = value
        self.is_moved = False

    def __str__(self):
        return f"DiskFile[{self.id}, {self.size}, {self.value}]"

    def __repr__(self):
        return f"DiskFile[{self.id}, {self.size}, {self.value}]"


def compact_files(disk_map: str) -> int:
    blocks, _ = __parse_input(disk_map)
    last_element_idx = len(blocks) - 1
    for i, block in enumerate(blocks):
        if block.value is None:
            for j in range(last_element_idx, i, -1):
                last_block = blocks[j]
                if last_block.value is not None:
                    block.value = last_block.value
                    block.id = last_block.id
                    last_block.value = None
                    last_element_idx = j
                    break
            if last_element_idx <= i:
                break

    return sum(block.id * i for i, block in enumerate(blocks) if block.value is not None)


def compact_blocks(disk_map: str) -> int:
    _, blocks = __parse_input(disk_map)
    for i in range(len(blocks) - 1, 0, -1):
        curr_block: MemoryBlock = blocks[i]
        if curr_block.value is None or curr_block.is_moved:
            continue
        for j in range(0, i):
            block = blocks[j]
            if block.value is not None or curr_block.size > block.size:
                continue

            # merge empty blocks that are created after moving files
            empty_block, end_idx, start_idx = __create_empty_block(blocks, curr_block.size, i, j)
            blocks = blocks[:j] + [curr_block] + blocks[j + 1:start_idx] + [empty_block] + blocks[end_idx:]

            # if the block is smaller than the gap -> insert a new empty space
            diff: int = block.size - curr_block.size
            if diff > 0:
                blocks = blocks[:j + 1] + [MemoryBlock(-1, diff, None)] + blocks[j + 1:]
            curr_block.is_moved = True
            break

    cur_pos = 0
    result = 0
    for block in blocks:
        if block.value is not None:
            for i in range(block.size):
                result += block.id * cur_pos
                cur_pos += 1
        else:
            cur_pos += block.size
    return result


def __create_empty_block(blocks: List[MemoryBlock], size: int, cur_pos: int, new_pos: int) -> (MemoryBlock, int, int):
    new_empty_block_size = size
    start_merge_idx = cur_pos
    end_merge_idx = cur_pos + 1
    if cur_pos >= 1 and blocks[cur_pos - 1].value is None and cur_pos - 1 != new_pos:
        new_empty_block_size += blocks[cur_pos - 1].size
        start_merge_idx = cur_pos - 1
    if cur_pos < len(blocks) - 1 and blocks[cur_pos + 1].value is None:
        new_empty_block_size += blocks[cur_pos + 1].size
        end_merge_idx = cur_pos + 2

    return MemoryBlock(-1, new_empty_block_size, None), end_merge_idx, start_merge_idx


class DiskBlock:

    def __init__(self, id: int, value: Union[int, None]):
        self.id = id
        self.value = value

    def __repr__(self):
        return f"Disk({self.id}, {self.value})"

    def __str__(self):
        return f"Disk {self.id}: {self.value}"


def __parse_input(disk_map: str) -> (List[DiskBlock], List[MemoryBlock]):
    disks: List[DiskBlock] = []
    disks_files: List[MemoryBlock] = []
    cur_id = 0
    for pos, c in enumerate(disk_map):
        value = int(c)
        for _ in range(value):
            if pos % 2 == 1:
                disks.append(DiskBlock(cur_id, None))
            else:
                disks.append(DiskBlock(cur_id, cur_id))
        if pos % 2 == 0:
            disks_files.append(MemoryBlock(cur_id, value, value))
            cur_id += 1
        else:
            disks_files.append(MemoryBlock(-1, value, None))
    return disks, disks_files


SOLUTION_INPUT = file_reader.read_whole_file_as_string('input\\day09.txt')
assert compact_files('2333133121414131402') == 1928
assert compact_files(SOLUTION_INPUT) == 6430446922192
assert compact_blocks('2333133121414131402') == 2858
assert compact_blocks('1313165') == 169
assert compact_blocks(SOLUTION_INPUT) == 6460170593016
