"""Task B1.3 / B1.4 - Compare Version 1 (input order) with Version 2 (saturation order)."""
import random
from graph_colouring import Graph, colour_graph, is_proper_colouring

PETERSEN = Graph(10, [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),
                      (5,7),(7,9),(9,6),(6,8),(8,5)])
K4 = Graph(4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)])


def random_graph(n, p, seed):
    rng = random.Random(seed)
    return Graph(n, [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p])


CASES = [
    ("Petersen, k=3",        PETERSEN,                  3),
    ("K4, k=3 (infeasible)", K4,                        3),
    ("G(12,0.5), k=3",       random_graph(12, 0.5, 7),  3),
    ("G(14,0.6), k=4",       random_graph(14, 0.6, 11), 4),
    ("G(16,0.7), k=4",       random_graph(16, 0.7, 5),  4),
]

header = f"{'Instance':<22}{'Order':<12}{'Nodes':>7}{'Cands':>7}{'Rejected':>10}{'Backtracks':>12}{'MaxDepth':>10}  {'Result':<16}"
print(header)
print("-" * len(header))
for name, g, k in CASES:
    for order in ("input", "saturation"):
        col, st = colour_graph(g, k, order)
        result = "colourable" if col is not None else "NOT colourable"
        if col is not None:
            assert is_proper_colouring(g, col)
        print(f"{name:<22}{order:<12}{st.nodes:>7}{st.candidates:>7}{st.rejected:>10}"
              f"{st.backtracks:>12}{st.max_depth:>10}  {result:<16}")
    print("")
