import os
import sys


def read_whole_file_as_string(path):
    with open(os.path.join(sys.path[0], path), "r") as f:
        return f.read()


def read_one_line_str_from_file(path):
    with open(os.path.join(sys.path[0], path), "r") as f:
        for line in f:
            return line.strip('\n')


def read_str_from_file(path):
    values = []
    with open(os.path.join(sys.path[0], path), "r") as f:
        for line in f:
            values.append(line.strip('\n'))
    return values


def read_ints_from_file(path):
    values = []
    with open(os.path.join(sys.path[0], path), "r") as f:
        for line in f:
            values.append(int(line.strip('\n')))
    return values


def read_ints_from_file_string(path):
    with open(os.path.join(sys.path[0], path), "r") as f:
        return [int(n) for n in f.readline().split(',')]
