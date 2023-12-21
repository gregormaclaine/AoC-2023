from math import ceil


def is_palindromic(lines):
    hw = len(lines) / 2
    return all(x == y for x, y in zip(lines[:ceil(hw)], lines[::-1]))


def calc_value(lines):
    for i in range(len(lines) - 1):
        if lines[i] == lines[-1]:
            if is_palindromic(lines[i + 1:-1]):
                return (len(lines) - i) // 2 + i

    for i in range(len(lines) - 1, 0, -1):
        if lines[i] == lines[0]:
            if is_palindromic(lines[1:i]):
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
