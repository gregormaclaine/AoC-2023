def get_rank(cards):
    counts = [cards.count(c) for c in cards]

    if 5 in counts:
        return 6

    if 4 in counts:
        return 5

    if 3 in counts:
        return 4 if 2 in counts else 3

    if 2 in counts:
        return 2 if counts.count(2) == 4 else 1

    return 0


def get_order(cards):
    chars = list(reversed('AKQJT98765432'))
    return sum(chars.index(c) * (15 ** (5 - i)) for i, c in enumerate(cards))


with open('input/day-7.txt', 'r') as f:
    lines = [line.split() for line in f.read().split('\n')]
    hands = [(cards, int(bet)) for cards, bet in lines]
    ranked_hands = sorted(hands, key=lambda x: get_rank(
        x[0]) * (15 ** 7) + get_order(x[0]))
    print(sum((i + 1) * bet for i, (cards, bet) in enumerate(ranked_hands)))
