def points_to_check(span, row, size):
    a, b = span
    l, h = size

    points = []

    left = max(0, a - 1)
    right = min(l, b + 2)

    if row != 0:
        points.extend((row - 1, i) for i in range(left, right))

    if a != 0:
        points.append((row, a - 1))

    if b != l - 1:
        points.append((row, b + 1))

    if row != h - 1:
        points.extend((row + 1, i) for i in range(left, right))

    return points


def is_symbol(c: str):
    return not c.isdigit() and c != '.'


with open('input/day-3.txt', 'r') as f:
    lines = f.read().split('\n')

    size = [len(lines[0]), len(lines)]

    total = 0
    for row, line in enumerate(lines):
        num_indexes = [i for i, c in enumerate(line) if c.isdigit()]

        num_regions = []
        if num_indexes:
            cur_start = num_indexes[0]
            for index1, index2 in zip(num_indexes, num_indexes[1:]):
                if index2 - index1 != 1:
                    num_regions.append((cur_start, index1))
                    cur_start = index2
            num_regions.append((cur_start, num_indexes[-1]))

        for span in num_regions:
            neighbours = points_to_check(span, row, size)
            if any(map(is_symbol, (lines[i][j] for i, j in neighbours))):
                total += int(line[span[0]: span[1] + 1])

    print(total)
