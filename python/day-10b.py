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


def get_links(map, p):
    neighbours = get_next_poses(map, p)
    return [n for n in neighbours if is_valid(n, map) and do_points_link(map, p, n)]


def combine_lines(points):
    remaining = [*points[2:], points[0]]

    cur_dir = get_dir(points[0], points[1])
    lines = [[cur_dir, points[0], points[1]]]
    for p in remaining:
        new_dir = get_dir(lines[-1][2], p)
        if new_dir == cur_dir:
            lines[-1][2] = p
        else:
            lines.append([new_dir, lines[-1][2], p])
            cur_dir = new_dir

    return lines


def get_edge_points(map):
    w = len(map[0])
    return [(0, i) for i in range(w)] + \
        [(w - 1, i) for i in range(w)] + \
        [(i, 0) for i in range(1, w - 1)] + \
        [(i, w - 1) for i in range(1, w - 1)]


def is_between(n, a, b):
    if n >= a and n <= b:
        return True
    return n >= b and n <= a


def point_crosses_vert_line(lines, p):
    vert_lines = [l for l in lines if l[0] in ['u', 'd']]
    return any(p[1] == src[1] and is_between(p[0], src[0], end[0]) for _, src, end in vert_lines)


def point_crosses_hor_line(lines, p):
    hor_lines = [l for l in lines if l[0] in ['l', 'r']]
    return any(p[1] == src[1] and is_between(p[0], src[0], end[0]) for _, src, end in hor_lines)


def collapse_line(line):
    return re.sub(r'(L|F|S)-*(7|J|S)', r'|', line)


def organise_lines(lines):
    return [[l[0], l[1], l[2]] if l[0] in ['d', 'r'] else [l[0], l[2], l[1]] for l in lines]


def get_horiz_line_from_p(p, lines):
    for l in lines:
        if l[1] == p and l[0] in ['r', 'l']:
            return l
    return None


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

    # print(seen)
    print('Combining pipe lines...\n\n')
    pipe_lines = organise_lines(combine_lines(seen))
    # print('\n'.join(_map(str, pipe_lines)), len(pipe_lines))

    # inside_points_h = []
    # for i in range(len(map)):
    #     is_inside = (i, 0) in seen
    #     count = 0
    #     for j in range(1, len(map[0])):
    #         if point_crosses_vert_line(pipe_lines, (i, j)):
    #             is_inside = not is_inside

    #         p = map[i][j]
    #         print((i, j), p, point_crosses_vert_line(
    #             pipe_lines, (i, j)), 'inside=' + str(is_inside))

    #         if is_inside and ((i, j) not in seen):
    #             print('counting', (i, j))
    #             inside_points_h.append((i, j))

    #     print('')

    # inside_points_v = []
    # for j in range(len(map[0])):
    #     is_inside = (0, j) in seen
    #     count = 0
    #     for i in range(1, len(map)):
    #         if point_crosses_hor_line(pipe_lines, (i, j)):
    #             is_inside = not is_inside

    #         if is_inside and ((i, j) not in seen):
    #             inside_points_v.append((i, j))

    #         p = map[i][j]
    #         # print((i, j), p, point_crosses_vert_line(
    #         # pipe_lines, (i, j)), 'inside=' + str(is_inside))

    # print(inside_points_h)
    # print(inside_points_v)
    # print(len(set(inside_points_h).intersection(set(inside_points_v))))

    inside_points = []
    for i in [1]:
        is_inside = (i, 0) in seen

        j = 1
        while j < len(map[0]):
            print(map[i][j])
            if point_crosses_vert_line(pipe_lines, (i, j)):
                is_inside = not is_inside

                hline = get_horiz_line_from_p((i, j), pipe_lines)
                if hline is not None:
                    j = hline[2][1]

            if is_inside and ((i, j) not in seen):
                inside_points.append((i, j))

            j += 1

    print(inside_points)
