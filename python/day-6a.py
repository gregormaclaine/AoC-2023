from math import ceil, floor, sqrt, prod


def count_wins(t, d):
    det = sqrt(t**2 - 4*d)
    return floor((t + det) / 2 - 0.00001) - ceil((t - det) / 2 + 0.00001) + 1


with open('input/day-6.txt', 'r') as f:
    lines = f.read().split('\n')
    races = zip(lines[0].split()[1:], lines[1].split()[1:])
    counts = [count_wins(int(t), int(d)) for t, d, in races]
    print(prod(counts))
