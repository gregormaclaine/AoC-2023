def calc_load(col):
    return sum(len(col) - i for i, c in enumerate(col) if c == 'O')


def calc_full_load(grid):
    cols = [[r[i] for r in grid] for i in range(len(grid[0]))]
    return sum(calc_load(c) for c in cols)


def perform_cycle(grid):
    size = (len(grid), len(grid[0]))

    # ROLL NORTH
    for j in range(size[1]):
        start = 0
        count = 0
        for i in range(size[0]):
            c = grid[i][j]
            if c == 'O':
                count += 1
            if c == '#':
                for _i in range(start, start + count):
                    grid[_i][j] = 'O'
                for _i in range(start + count, i):
                    grid[_i][j] = '.'
                start = i + 1
                count = 0
        if count > 0:
            for _i in range(start, start + count):
                grid[_i][j] = 'O'
            for _i in range(start + count, size[0]):
                grid[_i][j] = '.'

    # ROLL WEST
    for i in range(size[0]):
        start = 0
        count = 0
        for j in range(size[1]):
            c = grid[i][j]
            if c == 'O':
                count += 1
            if c == '#':
                for _j in range(start, start + count):
                    grid[i][_j] = 'O'
                for _j in range(start + count, j):
                    grid[i][_j] = '.'
                start = j + 1
                count = 0
        if count > 0:
            for _j in range(start, start + count):
                grid[i][_j] = 'O'
            for _j in range(start + count, size[1]):
                grid[i][_j] = '.'

    # ROLL SOUTH
    for j in range(size[1]):
        start = 0
        count = 0
        for i in range(size[0]):
            c = grid[i][j]
            if c == 'O':
                count += 1
            if c == '#':
                for _i in range(start, i - count):
                    grid[_i][j] = '.'
                for _i in range(i - count, i):
                    grid[_i][j] = 'O'
                start = i + 1
                count = 0
        if count > 0:
            for _i in range(start, size[0] - count):
                grid[_i][j] = '.'
            for _i in range(size[0] - count, size[0]):
                grid[_i][j] = 'O'

    # ROLL EAST
    for i in range(size[0]):
        start = 0
        count = 0
        for j in range(size[1]):
            c = grid[i][j]
            if c == 'O':
                count += 1
            if c == '#':
                for _j in range(start, j - count):
                    grid[i][_j] = '.'
                for _j in range(j - count, j):
                    grid[i][_j] = 'O'
                start = j + 1
                count = 0
        if count > 0:
            for _j in range(start, size[1] - count):
                grid[i][_j] = '.'
            for _j in range(size[1] - count, size[1]):
                grid[i][_j] = 'O'

    return grid


def efficient_perform_cycles(grid: list, count: int):
    history = []
    loads = []

    for running_count in range(count):
        h = hash(str(grid))
        if h in history:
            break

        history.append(h)
        loads.append(calc_full_load(grid))
        grid = perform_cycle(grid)
        running_count += 1

    start_index = history.index(h)
    cycle_length = len(history) - start_index
    print('Found cycle with length', cycle_length)
    offset = (count - running_count) % cycle_length
    return loads[start_index + offset]


with open('input/day-14.txt', 'r') as f:
    lines = f.read().split('\n')
    grid = [list(l) for l in lines]
    print(efficient_perform_cycles(grid, int(1e9)))
