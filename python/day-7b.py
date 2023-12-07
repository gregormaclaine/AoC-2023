def get_rank(cards):
    counts = [cards.count(c) for c in cards if c != 'J']
    num_js = cards.count('J')

    if num_js == 5 or num_js == 4:
        return 6

    if num_js == 3:
        if 2 in counts:
            return 6
        return 5

    if num_js == 2:
        if 3 in counts:
            return 6

        if 2 in counts:
            return 5

        return 3

    if num_js == 1:
        if 4 in counts:
            return 6

        if 3 in counts:
            return 5

        if 2 in counts:
            if counts.count(2) == 4:
                return 4
            return 3

        return 1

    if 5 in counts:
        return 6

    if 4 in counts:
        return 5

    if 3 in counts:
        if 2 in counts:
            return 4
        return 3

    if 2 in counts:
        if counts.count(2) == 4:
            return 2
        return 1

    return 0


def get_order(cards):
    chars = list(reversed('AKQT98765432J'))
    return sum(chars.index(c) * (15 ** (5 - i)) for i, c in enumerate(cards))


with open('input/day-7.txt', 'r') as f:
    lines = [line.split() for line in f.read().split('\n')]
    hands = [(cards, int(bet)) for cards, bet in lines]
    ranked_hands = sorted(hands, key=lambda x: get_rank(
        x[0]) * (15 ** 7) + get_order(x[0]))
    print(sum((i + 1) * bet for i, (cards, bet) in enumerate(ranked_hands)))
