def flatten(matrix):
    return [item for row in matrix for item in row]


def is_empty(line):
    return all(c == '.' for c in line)


def is_between(n, a, b):
    return (n >= a and n <= b) or (n >= b and n <= a)


def combinations(arr):
    return flatten([[(x, y) for y in arr[i + 1:]] for i, x in enumerate(arr)])


def calc_dist(p1, p2, empty_rows, empty_cols):
    h_growth = len([i for i in empty_rows if is_between(i, p1[0], p2[0])])
    w_growth = len([i for i in empty_cols if is_between(i, p1[1], p2[1])])
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + h_growth + w_growth


with open('input/day-11.txt', 'r') as f:
    map = f.read().split('\n')
    size = (len(map), len(map[0]))
    cols = [[row[i] for row in map] for i in range(size[1])]

    empty_rows = [i for i, row in enumerate(map) if is_empty(row)]
    empty_cols = [i for i, col in enumerate(cols) if is_empty(col)]

    galaxies = [[(i, j) for j, c in enumerate(row) if c == '#']
                for i, row in enumerate(map)]
    galaxies = flatten(galaxies)

    pairs = combinations(galaxies)
    print(sum(calc_dist(p1, p2, empty_rows, empty_cols)
          for p1, p2 in pairs))
