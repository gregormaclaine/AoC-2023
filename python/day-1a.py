with open('input/day-1.txt', 'r') as f:
    lines = f.read().split('\n')
    line_nums = [[int(c) for c in l if c.isdigit()] for l in lines]
    print(sum(l[0] * 10 + l[-1] for l in line_nums))
