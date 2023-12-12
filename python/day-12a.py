from itertools import combinations


def parse_line(line: str):
    springs, groups = line.split()
    groups = [int(g) for g in groups.split(',')]
    return springs, groups


def is_valid(springs: str, groups):
    # print('valid', springs, groups)
    found_groups = [len(g) for g in springs.split('.') if len(g) > 0]
    return len(found_groups) == len(groups) and \
        all(a == b for a, b in zip(found_groups, groups))


def brute_force(springs: str, groups):
    needed = sum(groups) - springs.count('#')
    slots = [i for i, c in enumerate(springs) if c == '?']
    valid_count = 0
    for chosen in combinations(slots, needed):
        result = [(c if c != '?' else '.') for c in springs]
        for i in chosen:
            result[i] = '#'
        if is_valid(''.join(result), groups):
            valid_count += 1
    return valid_count


def calc_possiblities(springs: str, groups):
    # return brute_force(springs, groups)
    if len(groups) == 0:
        return 1

    if springs.startswith('.') or springs.endswith('.'):
        return calc_possiblities(springs.lstrip('.').rstrip('.'), groups)

    if springs.startswith('#'):
        g = groups.pop(0)
        return calc_possiblities(springs[g + 1:], groups)

    if springs.endswith('#'):
        g = groups.pop()
        return calc_possiblities(springs[:-(g + 1)], groups)

    # print(springs, groups, brute_force(springs, groups))
    return brute_force(springs, groups)


with open('input/day-12.txt', 'r') as f:
    lines = f.read().split('\n')
    print(sum(calc_possiblities(*parse_line(l)) for l in lines))
