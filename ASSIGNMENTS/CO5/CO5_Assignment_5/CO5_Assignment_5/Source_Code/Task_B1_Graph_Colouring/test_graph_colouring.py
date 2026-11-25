"""Task B1.1 - Validation test suite for the graph colouring implementation."""
import itertools
import random
import unittest
from graph_colouring import Graph, colour_graph, is_proper_colouring

PETERSEN = Graph(10, [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),
                      (5,7),(7,9),(9,6),(6,8),(8,5)])
K4 = Graph(4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)])
C5 = Graph(5, [(0,1),(1,2),(2,3),(3,4),(4,0)])


def brute_force_colourable(graph, k):
    """Independent oracle: try every colour assignment (small graphs only)."""
    for cols in itertools.product(range(k), repeat=graph.n):
        if is_proper_colouring(graph, list(cols)):
            return True
    return False


class TestGraphColouring(unittest.TestCase):
    def test_colourable_petersen_k3(self):
        # Intent: a known colourable graph must yield a valid colouring.
        for order in ("input", "saturation"):
            col, _ = colour_graph(PETERSEN, 3, order)
            self.assertIsNotNone(col)
            self.assertTrue(is_proper_colouring(PETERSEN, col))

    def test_uncolourable_k4_k3(self):
        # Intent: K4 needs 4 colours, so k=3 must be rejected by exhaustive search.
        for order in ("input", "saturation"):
            col, st = colour_graph(K4, 3, order)
            self.assertIsNone(col)
            self.assertGreater(st.backtracks, 0)

    def test_boundary_empty_graph(self):
        # Intent: zero vertices is trivially colourable (edge-case termination).
        col, st = colour_graph(Graph(0), 1)
        self.assertEqual(col, [])
        self.assertEqual(st.nodes, 1)

    def test_boundary_single_vertex_one_colour(self):
        # Intent: smallest non-trivial colourable case with k = 1.
        col, _ = colour_graph(Graph(1), 1)
        self.assertEqual(col, [0])

    def test_boundary_one_edge_one_colour(self):
        # Intent: an edge with k = 1 must fail immediately at the second vertex.
        col, st = colour_graph(Graph(2, [(0, 1)]), 1)
        self.assertIsNone(col)
        self.assertEqual(st.max_depth, 1)

    def test_odd_cycle_needs_three(self):
        # Intent: C5 is not 2-colourable but is 3-colourable.
        self.assertIsNone(colour_graph(C5, 2)[0])
        self.assertIsNotNone(colour_graph(C5, 3)[0])

    def test_agrees_with_brute_force_on_random_graphs(self):
        # Intent: both search orders must agree with an independent oracle.
        rng = random.Random(2024)
        for _ in range(150):
            n = rng.randint(1, 7)
            edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
            g = Graph(n, edges)
            k = rng.randint(1, 3)
            expected = brute_force_colourable(g, k)
            for order in ("input", "saturation"):
                col, _ = colour_graph(g, k, order)
                self.assertEqual(col is not None, expected)
                if col is not None:
                    self.assertTrue(is_proper_colouring(g, col))

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            Graph(2, [(0, 0)])
        with self.assertRaises(ValueError):
            Graph(2, [(0, 5)])
        with self.assertRaises(ValueError):
            colour_graph(C5, 3, order="random")


if __name__ == "__main__":
    unittest.main(verbosity=2)
