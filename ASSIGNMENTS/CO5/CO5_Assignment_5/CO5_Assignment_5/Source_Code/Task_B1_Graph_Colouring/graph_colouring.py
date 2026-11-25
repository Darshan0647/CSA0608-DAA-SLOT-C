"""
Task B1 - Backtracking Graph Colouring with search instrumentation.

Problem : Can the vertices of an undirected graph G be coloured with at most k
          colours so that no two adjacent vertices share a colour?

Version 1 (input order)  : vertices are chosen in the order 0, 1, ..., n-1.
Version 2 (saturation)   : the next vertex is the uncoloured vertex with the most
                           distinct colours already used by its neighbours
                           (the "most constrained" vertex). Ties are broken by
                           higher degree, then by lower index.
"""
from dataclasses import dataclass


@dataclass
class Stats:
    nodes: int = 0          # search-tree nodes visited (calls to search)
    candidates: int = 0     # (vertex, colour) pairs attempted
    rejected: int = 0       # candidates refused by the feasibility test
    backtracks: int = 0     # undo operations performed
    max_depth: int = 0      # deepest partial assignment reached

    def as_dict(self):
        return {"nodes": self.nodes, "candidates": self.candidates,
                "rejected": self.rejected, "backtracks": self.backtracks,
                "max_depth": self.max_depth}


class Graph:
    def __init__(self, n, edges=()):
        if n < 0:
            raise ValueError("n must be non-negative")
        self.n = n
        self.adj = [set() for _ in range(n)]
        for u, v in edges:
            if not (0 <= u < n and 0 <= v < n):
                raise ValueError(f"edge ({u},{v}) out of range")
            if u == v:
                raise ValueError("self-loops are not allowed")
            self.adj[u].add(v)
            self.adj[v].add(u)

    def edges(self):
        return sorted({(min(u, v), max(u, v)) for u in range(self.n) for v in self.adj[u]})


def is_proper_colouring(graph, colour):
    """True if every vertex is coloured and no edge joins two equal colours."""
    if any(c < 0 for c in colour):
        return False
    return all(colour[u] != colour[v] for u in range(graph.n) for v in graph.adj[u])


def colour_graph(graph, k, order="input"):
    """
    Decide k-colourability by backtracking.
    Returns (colouring or None, Stats).
    colouring[v] is a colour in 0..k-1, or None if no colouring exists.
    """
    if order not in ("input", "saturation"):
        raise ValueError("order must be 'input' or 'saturation'")

    colour = [-1] * graph.n          # -1 means "uncoloured"
    stats = Stats()

    def select_vertex():
        uncoloured = [v for v in range(graph.n) if colour[v] == -1]
        if not uncoloured:
            return None
        if order == "input":
            return uncoloured[0]
        # Saturation rule: maximise distinct neighbour colours, then degree, then index.
        def key(v):
            sat = len({colour[w] for w in graph.adj[v] if colour[w] != -1})
            return (-sat, -len(graph.adj[v]), v)
        return min(uncoloured, key=key)

    def feasible(v, c):
        return all(colour[w] != c for w in graph.adj[v])

    def search(depth):
        stats.nodes += 1
        stats.max_depth = max(stats.max_depth, depth)
        v = select_vertex()
        if v is None:                       # goal: every vertex coloured
            return True
        for c in range(k):                  # candidate colours
            stats.candidates += 1
            if not feasible(v, c):          # feasibility test / pruning
                stats.rejected += 1
                continue
            colour[v] = c                   # assign
            if search(depth + 1):           # explore
                return True
            colour[v] = -1                  # undo
            stats.backtracks += 1           # backtrack
        return False                        # failure: no colour fits v

    found = search(0)
    return (colour if found else None), stats


if __name__ == "__main__":
    # Quick demonstration on the Petersen graph (3-colourable, not 2-colourable)
    outer = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
    petersen = Graph(10, outer + spokes + inner)
    for order in ("input", "saturation"):
        col, st = colour_graph(petersen, 3, order)
        print(f"Petersen graph, k=3, order={order}")
        print(f"  colouring : {col}")
        print(f"  valid     : {is_proper_colouring(petersen, col)}")
        print(f"  stats     : {st.as_dict()}")
