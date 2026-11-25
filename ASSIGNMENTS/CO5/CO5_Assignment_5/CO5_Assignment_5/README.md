# CO5 Assignment 5 – Search, Complexity and Approximation Engineering

Student: SARAVANA H · Course: CSA06 Design and Analysis of Algorithms · Total: 50 marks

## Contents

| Path | Purpose |
|---|---|
| `Source_Code/Task_B1_Graph_Colouring/` | Backtracking graph colouring with instrumentation, validation tests, and the ordering comparison (B1) |
| `Source_Code/Task_B2_Adversarial_Search/` | Two same-size graphs with very different search cost (B2) |
| `Source_Code/Task_B3_Exact_vs_Approximation/` | Exact and greedy set cover, counterexample, and scalability experiment (B3) |
| `Source_Code/Task_B4_Bin_Packing/` | First Fit Decreasing with a challenge case and a 5,000-workload run (B4) |
| `Report/CO5_Assignment_5_Report.pdf` | Consolidated report: Part A solutions, Part B tasks, screenshots, and interpretation |
| `Report/screenshots/` | Screenshots (PNG) and captured program output (TXT) used in the report |
| `Report/build_report.py`, `Report/make_screenshots.py` | Scripts that regenerate the screenshots and the PDF |

## Assumptions

Values blank in the assignment PDF were assumed as follows: k = 3 colours (k = 4 in some B1.4 cases); n = 10 vertices for B2; bin capacity C = 10 (demo) and C = 100 (production run); set cover uses zones 0–7 and centres A–E from the B3.2 counterexample. Full details are in the report.

## Requirements

Python 3.8 or later. Part B uses only the standard library. The report needs `reportlab` and `Pillow`.

## Run

```bash
cd Source_Code/Task_B1_Graph_Colouring && python3 test_graph_colouring.py   # B1.1 tests
cd Source_Code/Task_B1_Graph_Colouring && python3 compare_orders.py         # B1.3 / B1.4
cd Source_Code/Task_B2_Adversarial_Search && python3 adversarial.py         # B2
cd Source_Code/Task_B3_Exact_vs_Approximation && python3 run_experiments.py # B3.1 / B3.3
cd Source_Code/Task_B4_Bin_Packing && python3 bin_packing.py                # B4
cd Report && python3 make_screenshots.py && python3 build_report.py         # regenerate report
```
