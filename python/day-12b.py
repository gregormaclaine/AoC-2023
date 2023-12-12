from itertools import combinations
from math import comb


def parse_line(line: str):
    springs, groups = line.split()
    groups = [int(g) for g in groups.split(',')]
    return '?'.join([springs] * 5), groups * 5


def is_valid(springs: str, groups):
    found_groups = [len(g) for g in springs.split('.') if len(g) > 0]
    return len(found_groups) == len(groups) and \
        all(a == b for a, b in zip(found_groups, groups))


def brute_force(springs: str, groups):
    needed = sum(groups) - springs.count('#')

    if needed < 0:
        return 0

    slots = [i for i, c in enumerate(springs) if c == '?']
    valid_count = 0
    # print(f'  - checking {comb(len(slots), needed)} combinations')
    for chosen in combinations(slots, needed):
        result = [(c if c != '?' else '.') for c in springs]
        for i in chosen:
            result[i] = '#'
        if is_valid(''.join(result), groups):
            valid_count += 1
    return valid_count


def brute_force_by_group(springs: str, groups):
    if sum(groups) - springs.count('#') < 0:
        return 0

    wide_slots = [g for g in springs.split('.') if len(g)]
    if len(wide_slots) == 1:
        return brute_force(springs, groups)

    total = 0

    first_slot_count = 0
    for first_slot_count in range(len(groups) + 1):
        if sum(groups[:first_slot_count]) + len(groups[:first_slot_count]) - 1 > len(wide_slots[0]):
            break

        total += brute_force(wide_slots[0], groups[:first_slot_count]) * \
            calc_possiblities_loop(
                '.'.join(wide_slots[1:]), groups[first_slot_count:])

    return total


def calc_possiblities_loop(springs: str, groups, first=False):
    while True:
        if len(groups) == 0 or springs.count('?') == 0:
            return 1

        if springs.startswith('.') or springs.endswith('.'):
            springs = springs.lstrip('.').rstrip('.')
            continue

        if springs.startswith('#'):
            g = groups.pop(0)
            springs = springs[g + 1:]
            continue

        if springs.endswith('#'):
            g = groups.pop()
            springs = springs[:-(g + 1)]
            continue

        if '#' in springs[:groups[0]]:
            pos = springs.index('#')
            if pos < groups[0] - 1:
                old = springs
                springs = springs[:pos] + '#' * \
                    (groups[0] - pos) + springs[groups[0]:]
                if old != springs:
                    continue

        if '#' in springs[:-groups[-1]]:
            from_end = ''.join(reversed(springs[:-groups[-1]])).index('#')
            if from_end < groups[-1] - 1:
                old = springs
                springs = springs[:-groups[-1]] + '#' * \
                    (groups[-1] - from_end) + springs[-from_end:]
                if old != springs:
                    continue

        wide_slots = [g for g in springs.split('.') if len(g)]
        if len(wide_slots):
            if len(wide_slots[0]) <= groups[0]:
                springs = '.'.join(wide_slots[1:])
                if len(wide_slots[0]) == groups[0]:
                    groups = groups[1:]
                continue

            if len(wide_slots[-1]) <= groups[-1]:
                springs = '.'.join(wide_slots[:-1])
                if len(wide_slots[-1]) == groups[-1]:
                    groups = groups[:-1]
                continue

        break

    if first:
        print(springs, '\n', '  -', groups)

    return brute_force_by_group(springs, groups)


with open('input/day-12.txt', 'r') as f:
    lines = f.read().split('\n')
    print(sum(calc_possiblities_loop(*parse_line(l), True) for l in lines))
