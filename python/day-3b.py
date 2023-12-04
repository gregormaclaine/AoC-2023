def points_to_check(row, col, size):
    l, h = size

    points = []

    left = max(0, col - 1)
    right = min(l, col + 2)

    if row != 0:
        points.extend((row - 1, i) for i in range(left, right))

    if col != 0:
        points.append((row, col - 1))

    if col != l - 1:
        points.append((row, col + 1))

    if row != h - 1:
        points.extend((row + 1, i) for i in range(left, right))

    return points


def filter_dups_in_spans(spans):
    unique = [spans[0]]
    for s in spans[1:]:
        if s not in unique:
            unique.append(s)
    return unique


with open('input/day-3.txt', 'r') as f:
    lines = f.read().split('\n')

    size = [len(lines[0]), len(lines)]

    total = 0
    for row, line in enumerate(lines):
        star_indexes = [i for i, c in enumerate(line) if c == '*']

        for index in star_indexes:
            num_spans = []
            for p_row, p_col in points_to_check(row, index, size):
                if not lines[p_row][p_col].isdigit():
                    continue

                span = [p_col]

                # Check left
                while True:
                    left_col = span[0] - 1
                    if left_col < 0:
                        break
                    c = lines[p_row][left_col]
                    if not c.isdigit():
                        break
                    span.insert(0, left_col)

                # Check right
                while True:
                    right_col = span[-1] + 1
                    if right_col > size[0] - 1:
                        break
                    c = lines[p_row][right_col]
                    if not c.isdigit():
                        break
                    span.append(right_col)

                num_spans.append((p_row, span[0], span[-1]))

            ratios = filter_dups_in_spans(num_spans)
            if len(ratios) == 2:
                num1 = lines[ratios[0][0]][ratios[0][1]: ratios[0][2] + 1]
                num2 = lines[ratios[1][0]][ratios[1][1]: ratios[1][2] + 1]
                total += int(num1) * int(num2)

    print(total)
