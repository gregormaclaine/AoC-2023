def find_index(arr, pred):
    return next(map(lambda x: x[0], filter(lambda x: pred(x[1]), enumerate(arr))), -1)


def chash(str):
    h = 0
    for c in str:
        h = (h + ord(c)) * 17 % 256
    return h


def calc_power(bindex, box):
    return sum(bindex * (i + 1) * lens for i, (_, lens) in enumerate(box))


with open('input/day-15.txt', 'r') as f:
    steps = f.read().split(',')

    boxes = [[] for _ in range(256)]

    for s in steps:
        lbl = s[:-1] if '-' in s else s[:-2]
        box = boxes[chash(lbl)]
        index = find_index(box, lambda l: l[0] == lbl)

        if s.endswith('-'):
            if index >= 0:
                box.pop(index)
            continue

        lens = int(s.split('=')[1])
        if index >= 0:
            box[index] = (lbl, lens)
        else:
            box.append((lbl, lens))

    print(sum(calc_power(i + 1, b) for i, b in enumerate(boxes)))
