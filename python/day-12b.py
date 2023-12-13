from itertools import combinations
from math import comb


def parse_line(line: str):
    springs, groups = line.split()
    groups = [int(g) for g in groups.split(',')]
    return '?'.join([springs] * 5), groups * 5


def is_valid(springs: str, groups: list):
    found_groups = [len(g) for g in springs.split('.') if len(g) > 0]
    return len(found_groups) == len(groups) and \
        all(a == b for a, b in zip(found_groups, groups))


def brute_force(springs: str, groups: list):
    needed = sum(groups) - springs.count('#')
    if needed < 0:
        return 0

    slots = [i for i, c in enumerate(springs) if c == '?']
    valid_count = 0
    # print(f'  - checking {comb(len(slots), needed)} combinations')
    for chosen in combinations(slots, needed):
        result = [(c if c != '?' else '.') for c in springs]
        for i in chosen:
            result[i] = '#'
        if is_valid(''.join(result), groups):
            valid_count += 1
    return valid_count


# Should only take in spring run with no '.'s (Only 1 wide slot)
def brute_force_v2(springs: str, groups):
    while True:
        print(springs, '\n', '  -', groups)
        if sum(groups) - springs.count('#') < 0:
            print(sum(groups), springs.count('#'))
            return 0

        vis_groups = [len(g) for g in springs.split('?') if len(g)]
        if len(vis_groups) >= 2:
            space_before_first_visible = springs.index('#')
            if space_before_first_visible < groups[1] + 1:
                springs = springs[space_before_first_visible +
                                  vis_groups[0] + 1:]
                groups = groups[1:]
                continue

            space_after_last_visible = ''.join(reversed(springs)).index('#')
            if space_after_last_visible < groups[-2] + 1:
                springs = springs[: -
                                  (space_after_last_visible + vis_groups[-1] + 1)]
                groups = groups[:-1]
                continue

            # if max(groups) in vis_groups:
            #     m = max(groups)
            #     max_indexes = [i for i, g in enumerate(groups) if g == m]

            #     total = 0

            #     for max_index in max_indexes:
            #         space_req = sum(groups[:max_index]) + max_index
            #         if space_req >= springs.index('#' * m):
            #             pass

        break

    # free_spaces = len(springs) - sum(groups) - len(groups) + 1
    # num_gaps = len(groups) + 1
    # print('fs', free_spaces, num_gaps)

    visible_groups = [len(g) for g in springs.split('?') if len(g)]
    print(visible_groups)

    if len(visible_groups) == 0:
        return brute_force(springs, groups)

    return brute_force(springs, groups)


class Optimise:
    def __init__(self, springs: str, groups: list):
        self.springs = springs
        self.groups = groups
        self.improved = False

    def output(self):
        return self.springs, self.groups

    def trim_sides(self):
        if self.springs.startswith('.') or self.springs.endswith('.'):
            self.springs = self.springs.lstrip('.').rstrip('.')
            self.improved = True

    def remove_edge_groups(self):
        if self.springs.startswith('#'):
            g = self.groups.pop(0)
            self.springs = self.springs[g + 1:]
            self.improved = True

        if self.springs.endswith('#'):
            g = self.groups.pop()
            self.springs = self.springs[:-(g + 1)]
            self.improved = True

    def extend_side_groups(self):
        if len(self.springs) == 0 or len(self.groups) == 0:
            return

        if '#' in self.springs[:self.groups[0]]:
            pos = self.springs.index('#')
            if pos < self.groups[0] - 1:
                old = self.springs
                self.springs = self.springs[:pos] + '#' * \
                    (self.groups[0] - pos) + self.springs[self.groups[0]:]
                if old != self.springs:
                    self.improved = True

        if '#' in self.springs[:-self.groups[-1]]:
            from_end = ''.join(
                reversed(self.springs[:-self.groups[-1]])).index('#')
            if from_end < self.groups[-1] - 1:
                old = self.springs
                self.springs = self.springs[:-self.groups[-1]] + '#' * \
                    (self.groups[-1] - from_end) + self.springs[-from_end:]
                if old != self.springs:
                    self.improved = True

    def trim_redundant_edge_groups(self):
        wide_slots = [g for g in self.springs.split('.') if len(g)]
        if len(wide_slots) < 2:
            return

        if len(wide_slots[0]) < self.groups[0]:
            self.springs = '.'.join(wide_slots[1:])
            self.improved = True

        if len(wide_slots[-1]) < self.groups[-1]:
            self.springs = '.'.join(wide_slots[:-1])
            self.improved = True

    def remove_visible_side_groups(self):
        vis_groups = [len(g) for g in self.springs.split('?') if len(g)]
        if len(vis_groups) < 2:
            return

        sbfv = self.springs.index('#')  # Space Before First Visible (SBFV)
        if sbfv < self.groups[1] + 1:
            self.springs = self.springs[sbfv + vis_groups[0] + 1:]
            self.groups = self.groups[1:]
            self.improved = True
            return

        salv = ''.join(reversed(self.springs)).index(
            '#')  # Space After Last Visible (SALV)
        if salv < self.groups[-2] + 1:
            self.springs = self.springs[:-(salv + vis_groups[-1] + 1)]
            self.groups = self.groups[:-1]
            self.improved = True
            return


class SolveLine:
    memo = {}

    @staticmethod
    def has_result(springs, groups):
        key = springs + ' ' + ','.join(map(str, groups))
        return SolveLine.memo[key] if key in SolveLine.memo else None

    @staticmethod
    def save_result(springs, groups, result):
        key = springs + ' ' + ','.join(map(str, groups))
        SolveLine.memo[key] = result

    def __init__(self, springs: str, groups: list, start=False):
        self.springs = springs
        self.groups = groups
        self.start = start
        if self.start:
            print(springs, '\n', '  -', groups)

        self.is_sus = False

    def sus(self):
        self.is_sus = True
        return self

    def wide_slots(self):
        return [g for g in self.springs.split('.') if len(g)]

    def optimise(self):
        O = Optimise(self.springs, self.groups)
        while True:
            if sum(self.groups) == 0 or self.springs.count('?') == 0:
                break

            optimisers = [O.trim_sides, O.remove_edge_groups,
                          O.extend_side_groups, O.trim_redundant_edge_groups]

            for o in optimisers:
                o()
                if O.improved:
                    break
            else:
                if len(self.wide_slots()) == 1:
                    O.remove_visible_side_groups()

            if not O.improved:
                break
            O.improved = False

        self.springs, self.groups = O.output()

    def calc(self) -> int:
        if sum(self.groups) - self.springs.count('#') < 0:
            return 0

        if not self.is_sus:
            self.optimise()

        res = SolveLine.has_result(self.springs, self.groups)
        if res is not None:
            if self.start:
                print('   - Result =', res, '\n')
            return res

        res = self.calc_single() if len(self.wide_slots()) <= 1 else self.calc_multiple()
        SolveLine.save_result(self.springs, self.groups, res)
        if self.start:
            print('   - Result =', res, '\n')
        return res

    def calc_single(self) -> int:
        if len(self.groups) == 0:
            return 1

        return brute_force(self.springs, self.groups)

    def calc_multiple(self) -> int:
        total = 0
        num_in_first = 0
        ws = self.wide_slots()

        for num_in_first in range(len(self.groups) + 1):
            nums = self.groups[:num_in_first]
            if sum(nums) + len(nums) - 1 > len(ws[0]):
                break

            popped = SolveLine(ws[0], nums).sus()
            rest = SolveLine('.'.join(ws[1:]),
                             self.groups[num_in_first:]).sus()
            total += popped.calc() * rest.calc()
            # print('total', '.'.join(ws[1:]), self.groups[num_in_first:])

        return total


with open('input/day-12.txt', 'r') as f:
    lines = f.read().split('\n')
    print(sum(SolveLine(*parse_line(l), True).calc() for l in lines))
    # SolveLine('???.######.#####.?????', [1, 6, 5, 1], True).calc()
    print("\n".join(f"{k}\t{v}" for k, v in SolveLine.memo.items() if v))
