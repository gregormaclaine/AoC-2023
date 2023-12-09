def parse_route(route_s):
    parts = route_s.split()
    return parts[0], parts[2][1:4], parts[3][:3]


with open('input/day-8.txt', 'r') as f:
    steps, line_txt = f.read().split('\n\n')
    routes = (parse_route(line) for line in line_txt.split('\n'))
    routes = {src: (lft, rgt) for src, lft, rgt in routes}

    step_count = 0
    pos = 'AAA'
    while pos != 'ZZZ':
        dir = steps[step_count % len(steps)]
        pos = routes[pos][1 if dir == 'R' else 0]
        step_count += 1

    print(step_count)
