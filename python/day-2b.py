import re


def calc_power(rounds):
    max_red = max(map(int, (num for num, c in rounds if c == 'red')))
    max_green = max(map(int, (num for num, c in rounds if c == 'green')))
    max_blue = max(map(int, (num for num, c in rounds if c == 'blue')))
    return max_red * max_green * max_blue


with open('input/day-2.txt', 'r') as f:
    pat = r'(\d+) (red|green|blue)'
    lines = [re.findall(pat, s) for s in f.read().split('\n')]
    print(sum(map(calc_power, lines)))
