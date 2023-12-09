from math import lcm


def parse_route(route_s):
    parts = route_s.split()
    return parts[0], parts[2][1:4], parts[3][:3]


with open('input/day-8.txt', 'r') as f:
    steps, line_txt = f.read().split('\n\n')
    parsed_routes = [parse_route(line) for line in line_txt.split('\n')]
    routes = {src: (lft, rgt) for src, lft, rgt in parsed_routes}

    step_count = 0
    poses = [src for src, _, _ in parsed_routes if src.endswith('A')]
    visited = [[] for _ in poses]
    while not all(pos.endswith('Z') for pos in poses):
        for i, p in enumerate(poses):
            if p.endswith('Z'):
                visited[i].append(step_count)
                if all(len(v) for v in visited):
                    print(lcm(*[v[0] for v in visited]))
                    exit(0)

        dir = steps[step_count % len(steps)]
        poses = [routes[pos][1 if dir == 'R' else 0] for pos in poses]
        step_count += 1
