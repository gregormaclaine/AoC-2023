def parse_map(rows):
    return [tuple(int(n) for n in row.split()) for row in rows]


def apply_map(sr: [int, int], m: [(int, int, int)]):
    for dest, source, span in m:
        if sr[1] < source or sr[0] >= source + span:
            continue

        map_end = source + span - 1

        if sr[0] >= source and sr[1] <= map_end:
            return ([sr[0] - source + dest, sr[1] - source + dest],)

        if sr[0] < source:
            return (*apply_map([sr[0], source - 1], m), *apply_map([source, sr[1]], m))

        if sr[1] > map_end:
            return (*apply_map([sr[0], map_end], m), *apply_map([map_end + 1, sr[1]], m))

        raise Exception('This shouldn\'t happen')

    return (sr,)


with open('input/day-5.txt', 'r') as f:
    chunks = f.read().split('\n\n')
    seeds = [int(s) for s in chunks[0][7:].split()]
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1] - 1)
                   for i in range(0, len(seeds), 2)]
    maps = [parse_map(chunk.split('\n')[1:]) for chunk in chunks[1:]]

    for m in maps:
        for _ in range(len(seed_ranges)):
            srange = seed_ranges.pop(0)
            seed_ranges.extend(apply_map(srange, m))

    print(min(srange[0] for srange in seed_ranges))
