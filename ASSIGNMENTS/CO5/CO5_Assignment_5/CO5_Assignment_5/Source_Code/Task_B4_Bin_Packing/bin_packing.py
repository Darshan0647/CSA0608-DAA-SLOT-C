"""
Task B4 - Bin packing under a production constraint.

Workload demands d_i satisfy 0 < d_i <= C (server capacity), identical servers.
Goal: minimise the number of servers used with no server over capacity.

Strategy (B4.1): First Fit Decreasing (FFD)
  1. Sort workloads by demand, largest first.
  2. Place each workload on the FIRST open server with enough remaining capacity.
  3. If no open server fits, open a new server.
  Running time: O(n log n) for the sort plus O(n * s) for the placement scan,
  where s is the number of servers opened.

Exact reference (B4.2): depth-first branch and bound over the same items.
  Used only on small inputs to check how far FFD is from optimal.
"""
import math
import random
import time


def first_fit_decreasing(demands, capacity):
    """Return a list of servers; each server is a dict with 'items' and 'remaining'."""
    for d in demands:
        if not 0 < d <= capacity:
            raise ValueError(f"demand {d} must satisfy 0 < d <= {capacity}")
    servers = []
    for d in sorted(demands, reverse=True):          # 1. sort, largest first
        for s in servers:                            # 2. first server that fits
            if s["remaining"] >= d:
                s["items"].append(d)
                s["remaining"] -= d
                break
        else:                                        # 3. none fits: open a server
            servers.append({"items": [d], "remaining": capacity - d})
    return servers


def exact_min_servers(demands, capacity):
    """Branch and bound. Exact, exponential in the worst case; small n only."""
    items = sorted(demands, reverse=True)
    lower_bound = math.ceil(sum(items) / capacity)
    best = [len(items)]                               # trivial upper bound: one item per server
    loads = []

    def dfs(i):
        if len(loads) >= best[0]:                     # prune: cannot beat the incumbent
            return
        if i == len(items):
            best[0] = len(loads)
            return
        if best[0] == lower_bound:                    # already optimal: stop early
            return
        seen = set()
        for j in range(len(loads)):
            if loads[j] + items[i] <= capacity and loads[j] not in seen:
                seen.add(loads[j])                    # skip symmetric (equal-load) bins
                loads[j] += items[i]
                dfs(i + 1)
                loads[j] -= items[i]
        loads.append(items[i])                        # open a new server
        dfs(i + 1)
        loads.pop()

    dfs(0)
    return best[0], lower_bound


def report(servers, capacity):
    print(f"  Servers used: {len(servers)}")
    for idx, s in enumerate(servers, 1):
        used = capacity - s["remaining"]
        print(f"  Server {idx:>3}: workloads={s['items']}  used={used:<4} remaining={s['remaining']}")


def verify(servers, demands, capacity):
    placed = sorted(d for s in servers for d in s["items"])
    assert placed == sorted(demands), "every workload must be assigned exactly once"
    for s in servers:
        assert sum(s["items"]) <= capacity, "server over capacity"
        assert s["remaining"] == capacity - sum(s["items"])


if __name__ == "__main__":
    C = 10
    print("=" * 78)
    print("DEMO 1 - 10 workloads, capacity C = 10")
    print("=" * 78)
    demo = [7, 5, 4, 4, 3, 3, 2, 6, 5, 1]
    servers = first_fit_decreasing(demo, C)
    verify(servers, demo, C)
    report(servers, C)
    print()

    print("=" * 78)
    print("CHALLENGE (B4.2) - input where FFD is NOT optimal, C = 10")
    print("=" * 78)
    hard = [4, 4, 3, 3, 3, 3]
    ffd = first_fit_decreasing(hard, C)
    verify(ffd, hard, C)
    print("  FFD trace: 4,4 -> server 1 (full at 8, a 3 cannot fit)")
    print("             3,3,3 -> server 2 (load 9); last 3 -> server 3")
    report(ffd, C)
    opt, lb = exact_min_servers(hard, C)
    print(f"  Exact optimum: {opt} servers (lower bound ceil(sum/C) = {lb})")
    print(f"  FFD optimal? {len(ffd) == opt}   Excess servers: {len(ffd) - opt}")
    print("  Optimal packing: {4,3,3} and {4,3,3}, each exactly 10")
    print()

    print("=" * 78)
    print("PRODUCTION-SCALE RUN - 5,000 workloads, capacity C = 100")
    print("=" * 78)
    rng = random.Random(42)
    big = [rng.randint(1, 60) for _ in range(5000)]
    t0 = time.perf_counter()
    big_servers = first_fit_decreasing(big, 100)
    elapsed = time.perf_counter() - t0
    verify(big_servers, big, 100)
    lb = math.ceil(sum(big) / 100)
    total_remaining = sum(s["remaining"] for s in big_servers)
    print(f"  Workloads        : {len(big)}")
    print(f"  Total demand     : {sum(big)}")
    print(f"  Servers used     : {len(big_servers)}")
    print(f"  Lower bound      : {lb}  (ceil(total demand / C))")
    print(f"  Gap to bound     : {len(big_servers) - lb} server(s)  "
          f"({(len(big_servers) - lb) / lb:.2%} above the bound)")
    print(f"  Unused capacity  : {total_remaining}")
    print(f"  Run time         : {elapsed * 1000:.2f} ms")
    print(f"  Workloads on first 3 servers: "
          f"{[len(s['items']) for s in big_servers[:3]]} items each")
