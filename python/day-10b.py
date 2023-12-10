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


def get_links(map, p):
    neighbours = get_next_poses(map, p)
    return [n for n in neighbours if is_valid(n, map) and do_points_link(map, p, n)]


def combine_lines(points):
    remaining = [*points[2:], points[0]]

    cur_dir = get_dir(points[0], points[1])
    lines = [[points[0], points[1]]]
    for p in remaining:
        new_dir = get_dir(lines[-1][1], p)
        if new_dir == cur_dir:
            lines[-1][1] = p
        else:
            lines.append([lines[-1][1], p])
            cur_dir = new_dir

    return lines


def get_edge_points(map):
    w = len(map[0])
    return [(0, i) for i in range(w)] + \
        [(w - 1, i) for i in range(w)] + \
        [(i, 0) for i in range(1, w - 1)] + \
        [(i, w - 1) for i in range(1, w - 1)]


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

    # print('Combining pipe lines...')
    # pipe_lines = combine_lines(seen)
    # # print(pipe_lines, len(pipe_lines))

    o_stack = []
    for o in get_edge_points(map):
        if o not in seen:
            outside_point = o
            break
    else:
        print('No outside points')  # todo fix edgecase here
        print(len(map[0]) ** 2 - len(seen))
        exit(0)

    print('Found outside point:', o)

    o_seen = []
    o_stack = [outside_point]
    while len(o_stack):
        n = o_stack.pop()
        if n in o_seen:
            continue
        o_seen.append(n)
        neighbours = [p for p in get_next_poses(
            map, n) if is_valid(p, map)]
        new_points = [p for p in neighbours if p not in seen]
        # print('np', new_points)
        o_stack.extend(new_points)

    print(len(map[0]) * len(map) - len(o_seen) - len(seen))
