def get_next_poses(map, p):
    pipe = map[p[0]][p[1]]

    if pipe == 'S':
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


def is_valid(p, w):
    return p[0] >= 0 and p[1] >= 0 and p[0] < w and p[1] < w


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


def get_links(map, p):
    neighbours = get_next_poses(map, p)
    return [n for n in neighbours if is_valid(n, len(map[0])) and do_points_link(map, p, n)]


with open('input/day-10.txt', 'r') as f:
    txt = f.read()
    map = txt.split('\n')
    w = len(map[0]) + 1
    start_pos = (txt.index('S') // w, txt.index('S') % w)
    print(map)
    print('')

    seen = []
    stack = [start_pos]
    count = 0

    while len(stack):
        n = stack.pop()
        if n in seen:
            continue
        seen.append(n)

        print(n, map[n[0]][n[1]], get_links(map, n))
        new_points = [p for p in get_links(map, n) if p not in seen]
        stack.extend(new_points)
        count += 1
    print(count / 2)
