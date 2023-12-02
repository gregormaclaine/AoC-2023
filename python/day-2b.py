def calc_power(game):
    r, g, b = (0, 0, 0)
    for counts in game:
        for count in counts.split(', '):
            n, c = count.split(' ')
            if c == 'blue':
                b = max(b, int(n))
            elif c == 'red':
                r = max(r, int(n))
            else:
                g = max(g, int(n))
    return r * g * b


with open('input/day-2.txt', 'r') as f:
    lines = [s.split(': ')[1] for s in f.read().split('\n')]
    games = [l.split('; ') for l in lines]
    print(sum(calc_power(g) for g in games))
