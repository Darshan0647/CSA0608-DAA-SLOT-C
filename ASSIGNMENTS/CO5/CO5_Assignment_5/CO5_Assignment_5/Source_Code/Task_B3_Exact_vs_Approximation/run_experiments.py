"""Task B3.1 - B3.3: correctness on small instances and scalability experiment."""
from set_cover import Instance, exact_cover, greedy_cover, random_instance, is_cover, show

print("B3.1 - Correctness on three small (random, unselected) instances")
print("-" * 86)
print(f"{'Instance':<10}{'Zones':>6}{'Centres':>8}{'Exact size':>12}{'Greedy size':>13}{'Same?':>8}   Exact cover / Greedy cover")
print("-" * 86)
small = [random_instance(8, 7, 0.35, 101, "S1"),
         random_instance(10, 8, 0.30, 202, "S2"),
         random_instance(12, 9, 0.30, 303, "S3")]
for inst in small:
    ex, _ = exact_cover(inst)
    gr, _ = greedy_cover(inst)
    assert is_cover(inst, ex) and is_cover(inst, gr)
    same = "yes" if len(ex) == len(gr) else "no"
    print(f"{inst.name:<10}{inst.m:>6}{len(inst.masks):>8}{len(ex):>12}{len(gr):>13}{same:>8}   "
          f"{show(inst, ex)} / {show(inst, gr)}")
print()

print("B3.3 - Scalability (effort counted, not timed)")
print("-" * 86)
print(f"{'Zones':>6}{'Centres':>9}{'Exact effort':>14}{'2^centres':>14}{'Greedy effort':>15}{'Exact cover':>13}{'Greedy cover':>14}")
print("-" * 86)
for m, c in [(10, 8), (12, 10), (14, 12), (16, 14), (18, 16), (20, 18), (22, 20), (24, 22), (26, 24)]:
    inst = random_instance(m, c, 0.3, 1000 + m, f"N{m}")
    ex, ex_eff = exact_cover(inst)
    gr, gr_eff = greedy_cover(inst)
    print(f"{m:>6}{c:>9}{ex_eff:>14,}{2**c:>14,}{gr_eff:>15,}{len(ex):>13}{len(gr):>14}")
print()
print("Exact effort = subsets examined before the first cover of minimum size is found.")
print("2^centres = worst-case number of subsets (exact search with no early stop).")
