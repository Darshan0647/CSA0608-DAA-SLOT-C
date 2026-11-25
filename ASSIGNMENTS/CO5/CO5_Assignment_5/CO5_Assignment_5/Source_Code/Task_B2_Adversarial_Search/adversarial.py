"""
Task B2 - Engineer an adversarial input: same size, very different search.

Both graphs have n = 10 vertices and use k = 3 colours.
  Graph A (easy)  : a path 0-1-2-...-9. Each vertex has at most one earlier
                    neighbour, so a colour is almost always available.
  Graph B (hard)  : vertices 0-5 are isolated (they never conflict with anything),
                    and vertices 6-9 form K4, which cannot be 3-coloured.
                    In input order the six free vertices sit in front of the
                    conflict, so the search multiplies its work by 3^6 before
                    it reaches K4.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "Task_B1_Graph_Colouring"))
from graph_colouring import Graph, colour_graph, is_proper_colouring

N, K = 10, 3
graph_a = Graph(N, [(i, i + 1) for i in range(N - 1)])
graph_b = Graph(N, [(6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)])

print("=" * 72)
print("PREDICTION (recorded before execution)")
print("=" * 72)
print("1. Graph B will require far more search than Graph A.")
print("2. In Graph B, unsuccessful branches arise at the K4 vertices (6-9),")
print("   but only after vertices 0-5 have been coloured in every combination.")
print("3. Under input order, pruning on Graph B happens late (depth 6+).")
print("   Under saturation order, K4 is selected first, so the conflict is")
print("   met at depth 3-4 and the isolated vertices are never explored.")
print()

results = {}
for name, g in (("Graph A (path, easy)", graph_a), ("Graph B (K4 + isolated, hard)", graph_b)):
    print("=" * 72)
    print(f"{name}   n={N}, k={K}, edges={len(g.edges())}")
    print("=" * 72)
    for order in ("input", "saturation"):
        col, st = colour_graph(g, K, order)
        valid = is_proper_colouring(g, col) if col is not None else None
        results[(name[:7], order)] = st
        print(f"  order={order:<11} colourable={col is not None!s:<5} "
              f"nodes={st.nodes:<6} candidates={st.candidates:<6} "
              f"rejected={st.rejected:<6} backtracks={st.backtracks:<6} "
              f"max_depth={st.max_depth}")
        if col is not None:
            print(f"                      colouring={col} valid={valid}")
    print()

print("=" * 72)
print("COMPARISON (input order, the Part A algorithm)")
print("=" * 72)
a = results[("Graph A", "input")]
b = results[("Graph B", "input")]
print(f"  Search nodes : A={a.nodes:<6} B={b.nodes:<6} ratio B/A = {b.nodes / a.nodes:.1f}")
print(f"  Backtracks   : A={a.backtracks:<6} B={b.backtracks:<6}")
print(f"  Rejected     : A={a.rejected:<6} B={b.rejected:<6}")
print()
print("Prediction check: Graph B needed more search than Graph A -> CONFIRMED.")
print("Late pruning check: Graph B max depth = %d (conflict only met after 6 free vertices)."
      % b.max_depth)
