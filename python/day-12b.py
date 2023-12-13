from functools import cache


def parse_line(line: str):
    springs, groups = line.split()
    groups = [int(g) for g in groups.split(',')]
    return '?'.join([springs] * 5), tuple(groups * 5)


@cache
def solve(springs: str, groups: tuple, cur_len=0) -> int:
    if len(groups) == 0:
        return 0 if '#' in springs else 1

    if len(springs) == 0:
        return 0

    if springs[0] == '.':
        if cur_len > 0:
            return 0
        return solve(springs[1:], groups)

    if springs[0] == '#':
        if cur_len + 1 == groups[0]:
            if len(springs) == 1:
                return 1 if len(groups) == 1 else 0

            if springs[1] != '#':
                return solve(springs[2:], groups[1:])
            else:
                return 0
        return solve(springs[1:], groups, cur_len + 1)

    return solve('#' + springs[1:], groups, cur_len) + solve('.' + springs[1:], groups, cur_len)


with open('input/day-12.txt', 'r') as f:
    lines = f.read().split('\n')
    print(sum(solve(*parse_line(l)) for l in lines))
