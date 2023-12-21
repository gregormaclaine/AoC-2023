def chash(str):
    h = 0
    for c in str:
        h = (h + ord(c)) * 17 % 256
    return h


with open('input/day-15.txt', 'r') as f:
    steps = f.read().split(',')
    print(sum(chash(step) for step in steps))
