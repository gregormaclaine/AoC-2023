from math import ceil


def ltb(line):
    return sum(1 << i for i, c in enumerate(line) if c == '#')


def can_be_palindromic(lines):
    if len(lines) % 2 == 1:
        return False

    mistake_used = False
    for line1, line2 in zip(lines[:int(len(lines) / 2)], lines[::-1]):
        num = bin(ltb(line1) ^ ltb(line2)).count('1')
        if num > 1:
            return False
        if num == 1:
            if mistake_used:
                return False
            mistake_used = True

    return mistake_used


def calc_value(lines):
    for i in range(len(lines) - 1):
        if can_be_palindromic(lines[i:]):
            return (len(lines) - i) // 2 + i

    for i in range(len(lines) - 1, 0, -1):
        if can_be_palindromic(lines[:i + 1]):
            return (i + 1) // 2

    return None


def calc_grid(grid):
    row_val = calc_value(grid)
    if row_val is not None:
        return row_val * 100

    col_val = calc_value([''.join(r[i] for r in grid)
                         for i in range(len(grid[0]))])
    if col_val is not None:
        return col_val

    raise Exception('No mirror found')


with open('input/day-13.txt', 'r') as f:
    grids = f.read().split('\n\n')
    print(sum(calc_grid(g.split('\n')) for g in grids))
