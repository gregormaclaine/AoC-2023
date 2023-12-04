def to_bit_seq(vals):
    s = 0
    for n in vals:
        s |= 1 << int(n)
    return s


def count_matches(card_str):
    targets, given = card_str.split(' | ')
    t = to_bit_seq(targets.split())
    g = to_bit_seq(given.split())
    return (t & g).bit_count()


with open('input/day-4.txt', 'r') as f:
    cards = [line.split(':')[1] for line in f.read().split('\n')]

    card_nums = [1 for _ in cards]

    for i in range(len(cards)):
        num = card_nums[i]
        matches = count_matches(cards[i])
        for card_i in range(i + 1, i + 1 + matches):
            card_nums[card_i] += num

    print(sum(card_nums))
