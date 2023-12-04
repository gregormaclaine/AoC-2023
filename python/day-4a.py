def to_bit_seq(vals):
    s = 0
    for n in vals:
        s |= 1 << int(n)
    return s


with open('input/day-4.txt', 'r') as f:
    cards = [line.split(':')[1] for line in f.read().split('\n')]

    points = 0

    for card in cards:
        targets, given = card.split(' | ')
        t = to_bit_seq(targets.split())
        g = to_bit_seq(given.split())

        matches = (t & g).bit_count()
        if matches:
            points += 2 ** (matches - 1)

    print(points)
