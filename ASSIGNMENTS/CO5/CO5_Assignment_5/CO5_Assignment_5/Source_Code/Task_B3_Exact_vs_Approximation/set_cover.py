"""
Task B3 - Exact vs Approximate Emergency Service Set Cover.

Zones   : universe U = {0, ..., m-1}  (emergency-response zones)
Centres : candidate sets S_1..S_c      (each centre serves a subset of zones)
Goal    : choose the fewest centres whose union covers U.

Solution A (exact)  : enumerate centre subsets in increasing size; the first
                      size that covers U is optimal.
Solution B (greedy) : repeatedly pick the centre covering the most still-
                      uncovered zones (ties -> lowest index).

Zones and centres are stored as bitmasks so that each set operation is O(1).
Effort is counted, not timed: exact = subsets examined, greedy = centre
evaluations (coverage counts computed).
"""
import itertools
import random


class Instance:
    def __init__(self, m, sets, name="instance"):
        self.m = m
        self.name = name
        self.full = (1 << m) - 1
        self.names = [s[0] for s in sets]
        self.masks = []
        for _, zones in sets:
            mask = 0
            for z in zones:
                if not 0 <= z < m:
                    raise ValueError(f"zone {z} out of range")
                mask |= 1 << z
            self.masks.append(mask)
        union = 0
        for mk in self.masks:
            union |= mk
        if union != self.full:
            raise ValueError("instance is not coverable: some zone has no centre")


def exact_cover(inst):
    """Return (chosen centre indices, effort) where effort = subsets examined."""
    effort = 0
    c = len(inst.masks)
    for size in range(1, c + 1):
        for combo in itertools.combinations(range(c), size):
            effort += 1
            union = 0
            for i in combo:
                union |= inst.masks[i]
            if union == inst.full:
                return list(combo), effort
    raise RuntimeError("unreachable for a coverable instance")


def greedy_cover(inst):
    """Return (chosen centre indices, effort) where effort = centre evaluations."""
    uncovered = inst.full
    chosen = []
    effort = 0
    while uncovered:
        best, best_gain = None, -1
        for i, mk in enumerate(inst.masks):          # scan every centre
            effort += 1
            gain = bin(mk & uncovered).count("1")    # currently uncovered zones it covers
            if gain > best_gain:                     # strict '>' keeps lowest index on ties
                best, best_gain = i, gain
        if best_gain == 0:
            raise RuntimeError("no centre covers a remaining zone")
        chosen.append(best)                          # selection
        uncovered &= ~inst.masks[best]               # state update
    return chosen, effort                            # termination: uncovered == 0


def is_cover(inst, chosen):
    union = 0
    for i in chosen:
        union |= inst.masks[i]
    return union == inst.full


def random_instance(m, c, density, seed, name):
    """Random coverable instance: each zone is guaranteed at least one centre."""
    rng = random.Random(seed)
    sets = [[z for z in range(m) if rng.random() < density] for _ in range(c)]
    for z in range(m):
        if not any(z in s for s in sets):
            rng.choice(sets).append(z)
    return Instance(m, [(f"C{i+1}", s) for i, s in enumerate(sets)], name)


def show(inst, chosen):
    return "{" + ", ".join(inst.names[i] for i in chosen) + "}"


if __name__ == "__main__":
    # Counterexample from B3.2 (the greedy bait is C; A and B are the optimum)
    zones = 8
    sets = [
        ("A", [0, 1, 2, 3]),
        ("B", [4, 5, 6, 7]),
        ("C", [0, 1, 4, 5, 6]),
        ("D", [2, 7]),
        ("E", [3, 7]),
    ]
    inst = Instance(zones, sets, "counterexample")
    ex, ex_eff = exact_cover(inst)
    gr, gr_eff = greedy_cover(inst)
    print("Counterexample instance (8 zones, 5 centres)")
    print(f"  Exact  : {show(inst, ex)}  size={len(ex)}  subsets examined={ex_eff}")
    print(f"  Greedy : {show(inst, gr)}  size={len(gr)}  evaluations={gr_eff}")
    print(f"  Greedy is optimal? {len(gr) == len(ex)}")
