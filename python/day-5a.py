def parse_map(rows):
    return [tuple(int(n) for n in row.split()) for row in rows]


def apply_maps(seed: int, maps):
    for m in maps:
        for dest, source, span in m:
            if seed < source or seed >= source + span:
                continue

            seed = seed - source + dest
            break
    return seed


with open('input/day-5.txt', 'r') as f:
    chunks = f.read().split('\n\n')
    seeds = [int(s) for s in chunks[0][7:].split()]
    maps = [parse_map(chunk.split('\n')[1:]) for chunk in chunks[1:]]

    print(min(apply_maps(seed, maps) for seed in seeds))
