import re

_map = map


def get_next_poses(map, p):
    pipe = map[p[0]][p[1]]

    if pipe == 'S' or pipe == '.':
        return [
            (p[0] - 1, p[1]),
            (p[0] + 1, p[1]),
            (p[0], p[1] - 1),
            (p[0], p[1] + 1)
        ]

    if pipe == '|':
        return [(p[0] - 1, p[1]), (p[0] + 1, p[1])]

    if pipe == '-':
        return [(p[0], p[1] - 1), (p[0], p[1] + 1)]

    if pipe == 'L':
        return [(p[0] - 1, p[1]), (p[0], p[1] + 1)]

    if pipe == 'J':
        return [(p[0] - 1, p[1]), (p[0], p[1] - 1)]

    if pipe == '7':
        return [(p[0] + 1, p[1]), (p[0], p[1] - 1)]

    if pipe == 'F':
        return [(p[0] + 1, p[1]), (p[0], p[1] + 1)]


def is_valid(p, map):
    return p[0] >= 0 and p[1] >= 0 and p[0] < len(map) and p[1] < len(map[0])


def do_points_link(map, p1, p2):
    p1p = map[p1[0]][p1[1]]
    p2p = map[p2[0]][p2[1]]

    if p1[0] > p2[0]:  # Up
        return (p1p in ['|', 'L', 'J', 'S']) and (p2p in ['|', 'F', '7', 'S'])

    if p1[0] < p2[0]:  # Down
        return (p1p in ['|', 'F', '7', 'S']) and (p2p in ['|', 'L', 'J', 'S'])

    if p1[1] > p2[1]:  # Left
        return (p1p in ['-', 'J', '7', 'S']) and (p2p in ['-', 'L', 'F', 'S'])

    if p1[1] < p2[1]:  # Right
        return (p1p in ['-', 'L', 'F', 'S']) and (p2p in ['-', 'J', '7', 'S'])

    raise Exception('dont go here')


def get_dir(p1, p2):
    if p1[0] > p2[0]:  # Up
        return 'u'

    if p1[0] < p2[0]:  # Down
        return 'd'

    if p1[1] > p2[1]:  # Left
        return 'l'

    if p1[1] < p2[1]:  # Right
        return 'r'

    raise Exception('not here pls')


def get_links(map, p):
    neighbours = get_next_poses(map, p)
    return [n for n in neighbours if is_valid(n, map) and do_points_link(map, p, n)]


def combine_lines(points):
    remaining = [*points[2:], points[0]]

    cur_dir = get_dir(points[0], points[1])
    lines = [{
        'dir': cur_dir,
        'src': points[0],
        'end': points[1]
    }]

    for p in remaining:
        new_dir = get_dir(lines[-1]['end'], p)
        if new_dir == cur_dir:
            lines[-1]['end'] = p
        else:
            lines.append({
                'dir': new_dir,
                'src': lines[-1]['end'],
                'end': p
            })

            cur_dir = new_dir

    for i, line in enumerate(lines):
        before = lines[i - 1]
        after = lines[(i + 1) % len(lines)]
        line['simple'] = before['dir'] != after['dir']

    for line in lines:
        if line['dir'] in ['l', 'u']:
            # Swap lefts and ups to rights and downs
            line['dir'] = 'r' if line['dir'] == 'l' else 'd'
            line['src'], line['end'] = line['end'], line['src']

    # for l in lines:
    #     print(l)

    return lines


def is_between(n, a, b):
    if n >= a and n <= b:
        return True
    return n >= b and n <= a


with open('input/day-10.txt', 'r') as f:
    txt = f.read()
    map = txt.split('\n')
    w = len(map[0]) + 1
    start_pos = (txt.index('S') // w, txt.index('S') % w)

    seen = []
    stack = [start_pos]

    while len(stack):
        n = stack.pop()
        if n in seen:
            continue
        seen.append(n)

        new_points = [p for p in get_links(map, n) if p not in seen]
        stack.extend(new_points)

    print('Simplifying map...')
    for i in range(len(map)):
        for j in range(len(map[0])):
            map[i] = list(map[i])
            if (i, j) not in seen:
                map[i][j] = '.'

    # print(seen)
    print('Combining pipe lines...\n\n')
    pipe_lines = combine_lines(seen)
    # print('\n'.join(_map(str, pipe_lines)), len(pipe_lines))

    inside_points = []
    for i in range(len(map)):
        # print(''.join(map[i]))
        line = ['|' if c == '|' else '.' for c in map[i]]
        widths = [l for l in pipe_lines if l['dir']
                  == 'r' and l['src'][0] == i]

        for w in widths:
            for ii in range(w['src'][1], w['end'][1] + 1):
                line[ii] = 'x'
            if not w['simple']:
                line[w['src'][1]] = '|'

        line = [c for c in line if c != 'x']

        # print(''.join(line))

        running_points = None
        for j, c in enumerate(line):
            if c == '|':
                if running_points is None:
                    running_points = []
                else:
                    inside_points.extend(running_points)
                    running_points = None

            elif running_points is not None:
                running_points.append((i, j))

    print(inside_points)
    print(len(inside_points))
