maxes = {
    'red': 12,
    'green': 13,
    'blue': 14
}


def is_valid_round(r):
    pairs = [p.split(' ') for p in r.split(', ')]
    return all(map(lambda p: int(p[0]) <= maxes[p[1]], pairs))


with open('input/day-2.txt', 'r') as f:
    lines = [s.split(': ')[1] for s in f.read().split('\n')]
    games = [l.split('; ') for l in lines]

    print(sum(i + 1 for i, v in enumerate(all(is_valid_round(r)
          for r in g) for g in games) if v))
