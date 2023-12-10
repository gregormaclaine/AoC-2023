def all_constant(line):
    s = line[0]
    return all(s == n for n in line[1:])


def get_dif_line(line):
    return [b - a for a, b in zip(line, line[1:])]


def get_prev_num(line):
    layers = [line]
    while not all_constant(layers[-1]):
        layers.append(get_dif_line(layers[-1]))

    return sum(line[0] * (1 if i % 2 == 0 else -1)
               for i, line in enumerate(layers))


with open('input/day-9.txt', 'r') as f:
    lines = [[int(n) for n in line.split()] for line in f.read().split('\n')]
    print(sum(get_prev_num(line) for line in lines))
