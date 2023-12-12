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


# Should only take in spring run with no '.'s (Only 1 wide slot)
def brute_force_v2(springs: str, groups):
    while True:
        print(springs, '\n', '  -', groups)
        if sum(groups) - springs.count('#') < 0:
            print(sum(groups), springs.count('#'))
            return 0

        vis_groups = [len(g) for g in springs.split('?') if len(g)]
        if len(vis_groups) >= 2:
            space_before_first_visible = springs.index('#')
            if space_before_first_visible < groups[1] + 1:
                springs = springs[space_before_first_visible +
                                  vis_groups[0] + 1:]
                groups = groups[1:]
                continue

            space_after_last_visible = ''.join(reversed(springs)).index('#')
            if space_after_last_visible < groups[-2] + 1:
                springs = springs[: -
                                  (space_after_last_visible + vis_groups[-1] + 1)]
                groups = groups[:-1]
                continue

            # if max(groups) in vis_groups:
            #     m = max(groups)
            #     max_indexes = [i for i, g in enumerate(groups) if g == m]

            #     total = 0

            #     for max_index in max_indexes:
            #         space_req = sum(groups[:max_index]) + max_index
            #         if space_req >= springs.index('#' * m):
            #             pass

        break

    # free_spaces = len(springs) - sum(groups) - len(groups) + 1
    # num_gaps = len(groups) + 1
    # print('fs', free_spaces, num_gaps)

    visible_groups = [len(g) for g in springs.split('?') if len(g)]
    print(visible_groups)

    if len(visible_groups) == 0:
        return brute_force(springs, groups)

    return brute_force(springs, groups)


def brute_force_by_group(springs: str, groups):
    if sum(groups) - springs.count('#') < 0:
        return 0

    wide_slots = [g for g in springs.split('.') if len(g)]
    if len(wide_slots) == 1:
        return brute_force_v2(springs, groups)

    total = 0

    first_slot_count = 0
    for first_slot_count in range(len(groups) + 1):
        if sum(groups[:first_slot_count]) + len(groups[:first_slot_count]) - 1 > len(wide_slots[0]):
            break

        total += brute_force_v2(wide_slots[0], groups[:first_slot_count]) * \
            calc_possiblities_loop(
                '.'.join(wide_slots[1:]), groups[first_slot_count:])

    return total


def calc_possiblities_loop(springs: str, groups, first=False):
    while True:
        print(springs, '\n', '  -', groups)
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
    print(sum(calc_possiblities_loop(*parse_line(l), True) for l in lines[:1]))
