def calc_load(col):
    total = 0
    cur_load = len(col)
    for i, c in enumerate(col):
        if c == 'O':
            total += cur_load
            cur_load -= 1
        if c == '#':
            cur_load = len(col) - i - 1
    return total


with open('input/day-14.txt', 'r') as f:
    lines = f.read().split('\n')
    cols = [''.join([r[i] for r in lines]) for i in range(len(lines[0]))]
    print(sum(calc_load(c) for c in cols))
