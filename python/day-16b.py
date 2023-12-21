import sys
sys.setrecursionlimit(10000)


def flatten(arr):
    return [item for row in arr for item in row]


def is_oob(i, j):
    return i < 0 or j < 0 or i >= size[0] or j >= size[1]


def fill_out(i: int, j: int, dir: str):
    if is_oob(i, j):
        return

    c = grid[i][j]

    prev_hit = hit_map[i][j]
    if dir in ['r', 'l']:
        if prev_hit[0] and c not in ['/', '\\']:
            return
        prev_hit[0] = True
    else:
        if prev_hit[1] and c not in ['/', '\\']:
            return
        prev_hit[1] = True

    if dir == 'r':
        if c == '|':
            fill_out(i - 1, j, 'u')
            fill_out(i + 1, j, 'd')
            return
        if c == '\\':
            return fill_out(i + 1, j, 'd')
        if c == '/':
            return fill_out(i - 1, j, 'u')
        return fill_out(i, j + 1, 'r')

    if dir == 'l':
        if c == '|':
            fill_out(i - 1, j, 'u')
            fill_out(i + 1, j, 'd')
            return
        if c == '\\':
            return fill_out(i - 1, j, 'u')
        if c == '/':
            return fill_out(i + 1, j, 'd')
        return fill_out(i, j - 1, 'l')

    if dir == 'u':
        if c == '-':
            fill_out(i, j - 1, 'l')
            fill_out(i, j + 1, 'r')
            return
        if c == '\\':
            return fill_out(i, j - 1, 'l')
        if c == '/':
            return fill_out(i, j + 1, 'r')
        return fill_out(i - 1, j, 'u')

    if dir == 'd':
        if c == '-':
            fill_out(i, j - 1, 'l')
            fill_out(i, j + 1, 'r')
            return
        if c == '\\':
            return fill_out(i, j + 1, 'r')
        if c == '/':
            return fill_out(i, j - 1, 'l')
        return fill_out(i + 1, j, 'd')


def calc_energised(start):
    global hit_map
    hit_map = [[[False, False] for _ in grid[0]] for _ in grid]
    fill_out(*start)
    return len([x for x in flatten(hit_map) if x[0] or x[1]])


with open('input/day-16.txt', 'r') as f:
    lines = f.read().split('\n')
    grid = [list(l) for l in lines]
    size = (len(grid), len(grid[0]))
    hit_map = [[[False, False] for _ in grid[0]] for _ in grid]

    starts = [(0, j, 'd') for j in range(size[1])] + \
        [(size[0] - 1, j, 'u') for j in range(size[1])] + \
        [(i, 0, 'r') for i in range(size[0])] + \
        [(i, size[1] - 1, 'l') for i in range(size[0])]

    print(max(map(calc_energised, starts)))
