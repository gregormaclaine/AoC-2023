from math import ceil, floor, sqrt, prod


def count_wins(t, d):
    det = sqrt(t**2 - 4*d)
    return floor((t + det) / 2 - 0.00001) - ceil((t - det) / 2 + 0.00001) + 1


with open('input/day-6.txt', 'r') as f:
    lines = f.read().split('\n')
    t, d = (int(''.join(line.split()[1:])) for line in lines)
    print(count_wins(t, d))
