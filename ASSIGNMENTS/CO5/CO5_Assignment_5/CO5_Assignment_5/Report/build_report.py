"""Builds Report/CO5_Assignment_5_Report.pdf from the screenshots and captured outputs."""
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Preformatted, Image as RLImage, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = os.path.join(HERE, "screenshots")
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-B", FD + "DejaVuSansMono-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")

H1 = ParagraphStyle("H1", fontName="Sans-B", fontSize=15, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor("#1F3A5F"))
H2 = ParagraphStyle("H2", fontName="Sans-B", fontSize=11.5, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#1F3A5F"))
BODY = ParagraphStyle("B", fontName="Sans", fontSize=9.5, leading=13.5, spaceAfter=5)
SMALL = ParagraphStyle("S", parent=BODY, fontSize=8.5, leading=11.5)
CELL = ParagraphStyle("C", fontName="Sans", fontSize=8.3, leading=10.5)
CELLB = ParagraphStyle("CB", fontName="Sans-B", fontSize=8.3, leading=10.5)
CODE = ParagraphStyle("K", fontName="Mono", fontSize=7.6, leading=9.6)
CAP = ParagraphStyle("Cap", fontName="Sans", fontSize=8.5, textColor=colors.HexColor("#555555"), spaceAfter=10, spaceBefore=3)
TITLE = ParagraphStyle("T", fontName="Sans-B", fontSize=20, leading=26, alignment=TA_CENTER, spaceAfter=10)
CENTER = ParagraphStyle("Cn", parent=BODY, alignment=TA_CENTER)

story = []
P = lambda t, s=BODY: story.append(Paragraph(t, s))
def bullets(items):
    for it in items:
        story.append(Paragraph("&bull;&nbsp;&nbsp;" + it, ParagraphStyle("bl", parent=BODY, leftIndent=14, firstLineIndent=-10)))
def code(text):
    story.append(Preformatted(text.strip("\n"), CODE))
    story.append(Spacer(1, 6))
def table(rows, widths, header=True):
    data = [[Paragraph(str(c), CELLB if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1 if header else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3EAF2")))
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 8))
def shot(name, caption, width_cm=16.5):
    path = os.path.join(SS, name + ".png")
    parts = [path] if os.path.exists(path) else sorted(
        os.path.join(SS, f) for f in os.listdir(SS) if f.startswith(name + "_part"))
    for p in parts:
        w, h = Image.open(p).size
        W = width_cm * cm
        story.append(RLImage(p, width=W, height=W * h / w))
    story.append(Paragraph(caption, CAP))
def rawtxt(name):
    with open(os.path.join(SS, name + ".txt")) as f:
        code(f.read())

# ---------------------------------------------------------------- COVER
story += [Spacer(1, 3.5 * cm),
          Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", CENTER),
          Paragraph("CSA06 Design and Analysis of Algorithms", CENTER), Spacer(1, 1.2 * cm),
          Paragraph("Assignment 5 (CO5) &mdash; Search, Complexity and Approximation Engineering", TITLE),
          Spacer(1, 0.6 * cm),
          Paragraph("Backtracking, Tractability and Approximation Algorithms", CENTER), Spacer(1, 1.5 * cm),
          Paragraph("<b>Student:</b> SARAVANA H", CENTER),
          Paragraph("<b>Nature:</b> Individual &nbsp;&nbsp; <b>Total Marks:</b> 50 (Part A 25 + Part B 25)", CENTER),
          Spacer(1, 1.5 * cm)]
P("<b>Contents of this report</b>", CENTER)
bullets(["Part A &mdash; Algorithmic Design and Pseudocode: Tasks A1 to A5",
         "Part B &mdash; Implementation and Computational Investigation: Tasks B1 to B4 (with screenshots)",
         "Engineering Decision Note and conclusion",
         "Assumptions made where the assignment values were blank",
         "Repository layout and run instructions"])
story.append(PageBreak())

# ---------------------------------------------------------------- ASSUMPTIONS
story.append(Paragraph("Assumptions and Notes", H1))
P("Several values in the assignment PDF are blank or unreadable. The following assumptions were made so that every task could be completed. "
  "They are stated once here and applied consistently throughout the report.")
table([
    ["Item", "Blank / unclear in the PDF", "Assumption used"],
    ["A1, B1 (colouring)", "Number of server groups k", "k = 3 for the main tests and the Petersen demo. The B1.4 comparison also uses k = 4 for denser graphs."],
    ["B2 (adversarial)", "Value of n", "n = 10 vertices and k = 3 colours for both graphs."],
    ["B4 (bin packing)", "Server capacity C", "C = 10 for the worked demo and challenge; C = 100 for the 5,000-workload production run."],
    ["A5, B3 (set cover)", "Zone and centre data are in an image that did not extract", "Zones are 0&ndash;7 and the centres A&ndash;E from the B3.2 counterexample are used as the worked example. B3.1 and B3.3 use seeded random instances."],
    ["Pseudocode standard", "&lsquo;SIMATS Engineering &ndash; Standard for Algorithmic Pseudocode&rsquo; not supplied", "Language-independent pseudocode with explicit keywords: ALGORITHM, INPUT, OUTPUT, PROCEDURE, FUNCTION, IF/THEN/ELSE, FOR EACH, WHILE, RETURN, END. Comments use //."],
    ["Submission text", "Several sentences in the instructions are cut off", "Report content follows the explicit task list. Source code is organised under Source_Code/ with the four Part B task folders as specified."],
], [3.2, 4.6, 8.8])
story.append(PageBreak())

# ---------------------------------------------------------------- PART A
story.append(Paragraph("PART A &mdash; Algorithmic Design and Pseudocode (25 marks)", H1))

# A1
story.append(Paragraph("Task A1 &mdash; Design a Constraint-Aware Search: Graph Colouring for Cloud-Service Deployment (7 marks)", H2))
P("<b>Model.</b> Each service is a vertex, each conflict is an edge, and each server group is a colour. "
  "The question is whether all n services can be assigned to at most k groups so that no two conflicting services share a group.")
P("<b>A1.1 &mdash; Model the search problem (1 mark).</b>")
table([
    ["Element", "Definition"],
    ["Input", "Undirected graph G = (V, E) with n = |V| vertices, and an integer k (number of server groups; k = 3 assumed)."],
    ["Output", "A colouring colour[v] in {1..k} for every vertex such that no edge has equal colours at its ends; or FAILURE if none exists."],
    ["Decision at each stage", "Choose the next uncoloured service v, then choose a server group c for it."],
    ["Constraint", "For every edge (u, v): colour[u] is not equal to colour[v]."],
    ["Goal condition", "Every vertex is coloured and no constraint is violated."],
], [4, 12.6])
P("<b>A1.2 &mdash; Define the search state (1 mark).</b> A partial assignment must keep: (i) the colour of each coloured vertex, with an UNCOLOURED marker for the rest; "
  "(ii) the number of vertices assigned so far (the depth); and (iii) enough adjacency information to test a candidate colour in time proportional to the vertex degree. "
  "<b>A node of the search tree</b> represents one partial colouring: the colours already fixed for the first d vertices in selection order. "
  "Its children are the ways to colour the next vertex.")
P("<b>A1.3 &mdash; Define the pruning condition (1 mark).</b> A partial assignment P can be rejected, with no descendant explored, exactly when "
  "<i>some uncoloured vertex v has every one of its k colours blocked</i>, meaning each colour already appears on a coloured neighbour of v. "
  "Such a P has no extension to a full valid colouring, because v can never be coloured. "
  "A partial assignment is also rejected immediately if a candidate colour c for v is already used by a neighbour (the feasibility test, below).")
P("<b>A1.4 &mdash; Complete pseudocode (3 marks).</b>")
code("""
ALGORITHM ColourBacktrack(G, k)
INPUT:  G = (V, E), vertices 1..n;  k = number of server groups
OUTPUT: colour[1..n] (valid colouring) or FAILURE

 1  FOR EACH v IN V DO colour[v] <- UNCOLOURED
 2  RETURN Search(0)
END

PROCEDURE Search(depth)
 1  IF depth = n THEN RETURN SUCCESS               // goal condition
 2  v <- SelectNextVertex()                        // selection of next service
 3  FOR c <- 1 TO k DO                             // candidate server groups
 4      IF Feasible(v, c) THEN                     // feasibility test
 5          colour[v] <- c                         // assignment
 6          IF Search(depth + 1) = SUCCESS THEN    // recursive exploration
 7              RETURN SUCCESS
 8          colour[v] <- UNCOLOURED                // undo operation
 9      END IF                                     // (loop continues = backtracking)
10  END FOR
11  RETURN FAILURE                                 // failure: caller must backtrack
END

FUNCTION SelectNextVertex()
 1  RETURN the uncoloured vertex with the smallest index
END

FUNCTION Feasible(v, c)
 1  FOR EACH neighbour w OF v DO
 2      IF colour[w] = c THEN RETURN FALSE
 3  END FOR
 4  RETURN TRUE
END
""")
P("<b>A1.5 &mdash; Trace of the search (1 mark).</b> Graph: vertices 1&ndash;5 with edges {1-2, 2-3, 1-3, 3-4, 4-5}. "
  "The triangle 1-2-3 forces three colours, so k = 2 must fail. The trace below follows the pseudocode line by line (Choose, Check, Explore, Reject/Accept, Backtrack).")
table([
    ["#", "Call", "Vertex", "Candidate", "Check", "Result and action"],
    ["1", "Search(0)", "1", "c = 1", "no coloured neighbours", "ACCEPT; colour[1]=1; explore"],
    ["2", "Search(1)", "2", "c = 1", "neighbour 1 has 1", "REJECT; try c = 2"],
    ["3", "Search(1)", "2", "c = 2", "no neighbour has 2", "ACCEPT; colour[2]=2; explore"],
    ["4", "Search(2)", "3", "c = 1", "neighbour 1 has 1", "REJECT"],
    ["5", "Search(2)", "3", "c = 2", "neighbour 2 has 2", "REJECT"],
    ["6", "Search(2)", "3", "&ndash;", "all colours rejected", "FAILURE; BACKTRACK: undo colour[2]"],
    ["7", "Search(1)", "2", "&ndash;", "c = 2 was the last", "FAILURE; BACKTRACK: undo colour[1]"],
    ["8", "Search(0)", "1", "c = 2", "no coloured neighbours", "ACCEPT; colour[1]=2; explore"],
    ["9", "Search(1)", "2", "c = 1", "neighbour 1 has 2, no clash", "ACCEPT; colour[2]=1; explore"],
    ["10", "Search(2)", "3", "c = 1", "neighbour 2 has 1", "REJECT"],
    ["11", "Search(2)", "3", "c = 2", "neighbour 1 has 2", "REJECT; all colours rejected: FAILURE, undo colour[2]"],
    ["12", "Search(1)", "2", "c = 2", "neighbour 1 has 2", "REJECT; loop ends: FAILURE, undo colour[1]"],
    ["13", "Search(0)", "&ndash;", "&ndash;", "loop ends", "FAILURE: no 2-colouring exists"],
], [0.7, 2.0, 1.4, 2.4, 4.0, 6.1])
P("Vertices 4 and 5 are never reached: the failure is decided at vertex 3, so the subtrees below it are pruned. The same graph with k = 3 would succeed at step 1 without any backtracking, which is the expected behaviour.", SMALL)

# A2
story.append(Paragraph("Task A2 &mdash; Don't Search What Cannot Work: Improve a Weak Subset-Sum Design (5 marks)", H2))
P("<b>A2.1 &mdash; Diagnose the computational waste (1 mark).</b> The original algorithm generates all 2<super>n</super> subsets before testing any of them. "
  "It wastes work in four places: (a) it never discards a partial choice whose sum already exceeds the target, even though all numbers are positive, so every such branch is expanded in full; "
  "(b) it recomputes SUM(S) from scratch for each subset, costing O(n) per subset instead of sharing work along a branch; "
  "(c) it keeps going after a solution is found in the enumeration; and (d) it defers every decision until a complete subset exists, so no information about partial sums is used to cut the tree. "
  "The total cost is Theta(n 2<super>n</super>) in every case, including instances where the answer is trivially FALSE.")
P("<b>A2.2 &mdash; Redesign using backtracking (2 marks).</b> Each element A[i] is decided as Include or Exclude. Suffix sums R[i] = A[i] + ... + A[n] are precomputed so that the algorithm can prune when the target is out of reach.")
code("""
ALGORITHM SubsetSumBT(A[1..n], T)
INPUT:  A = positive integers, T = target
OUTPUT: TRUE if a subset of A sums to T, else FALSE

 1  R[n+1] <- 0
 2  FOR i <- n DOWNTO 1 DO  R[i] <- R[i+1] + A[i]     // suffix sums
 3  RETURN Explore(1, 0)
END

PROCEDURE Explore(i, current)
 1  IF current = T THEN RETURN TRUE                   // goal condition
 2  IF i > n THEN RETURN FALSE                        // no items left
 3  IF current > T THEN RETURN FALSE                  // PRUNE: positives only grow the sum
 4  IF current + R[i] < T THEN RETURN FALSE          // PRUNE: remainder cannot reach T
 5  // Alternative 1: INCLUDE A[i]
 6  IF Explore(i + 1, current + A[i]) THEN RETURN TRUE
 7  // Alternative 2: EXCLUDE A[i]   (no state change needed: current is unchanged)
 8  IF Explore(i + 1, current) THEN RETURN TRUE
 9  RETURN FALSE
END
""")
P("<b>A2.3 &mdash; Demonstrate pruning (1 mark).</b> Take A = [3, 34, 4, 12, 5, 2] and T = 9. Follow the branch Include 3 (current = 3), then Include 34 (current = 37). "
  "At this node current = 37 is greater than T = 9, so line 3 returns FALSE and the entire subtree below is never generated. "
  "Further exploration cannot succeed: every remaining element is non-negative, so any completion has sum at least 37, which is never equal to 9. "
  "Of the 2<super>6</super> = 64 possible subsets of A, all subsets that contain both 3 and 34 (16 subsets) are eliminated by this single check.")
P("<b>A2.4 &mdash; Challenge the pruning rule (1 mark).</b> Suppose negative integers are permitted. Line 3 (current &gt; T implies FALSE) "
  "and line 4 (current + R[i] &lt; T implies FALSE, with R[i] as the plain suffix sum) are no longer valid. "
  "Counterexample: A = [5, -3], T = 2. Include 5 gives current = 5 &gt; 2, so line 3 would return FALSE, but 5 + (-3) = 2 is a valid solution. "
  "The violated assumption is <b>monotonicity</b>: the partial sum is no longer non-decreasing as elements are added. "
  "The repair is to replace R[i] by the sum of the positive elements remaining (the largest possible increase), and to remove the line 3 cut, since a later negative element can bring the sum back down to T.")

# A3
story.append(Paragraph("Task A3 &mdash; Discover the Backtracking Design Pattern (5 marks)", H2))
table([
    ["Component", "N-Queens", "Subset Sum", "Graph Colouring"],
    ["State", "Queens placed in rows 1..r, with the columns and diagonals they occupy", "Items decided so far, and the running sum", "Partial colour map; set of coloured vertices"],
    ["Decision variable", "Column of the queen in row r", "Include or exclude item i", "Colour of the next uncoloured vertex"],
    ["Candidate choices", "Columns 1..n", "{Include, Exclude}", "Colours 1..k"],
    ["Feasibility test", "Column and both diagonals free", "Running sum does not exceed T", "No neighbour already has that colour"],
    ["Goal condition", "All n rows filled", "Running sum equals T", "All vertices coloured"],
    ["Pruning condition", "A row has no free column", "Sum exceeds T, or sum plus remaining positives falls below T", "Some uncoloured vertex has no feasible colour"],
    ["Undo operation", "Remove the queen; free its column and diagonals", "Subtract the item from the sum (or drop the Include decision)", "Reset the vertex to UNCOLOURED"],
], [3.0, 4.4, 4.6, 4.6])
P("<b>A3.1 &mdash; Common pattern (2 marks).</b> All three problems ask for a combination of discrete choices, one decision at a time, that satisfies a set of constraints. "
  "Each partial solution is a state; each state is extended by one choice from a finite set; and infeasible or hopeless states can be recognised before they are completed. "
  "The search tree is therefore a tree of partial solutions of bounded depth. Because a single mutable state can be changed and then restored, the search needs only O(depth) extra memory. "
  "The problems are NP-hard, so the worst-case cost of the pattern is exponential, but pruning is what makes most instances tractable.")
P("<b>A3.2 &mdash; Generic backtracking framework (2 marks).</b>")
code("""
ALGORITHM BACKTRACK(State)
INPUT:  State = the current partial solution (mutable)
OUTPUT: SUCCESS (State now holds a full solution) or FAILURE

 1  IF IsGoal(State) THEN RETURN SUCCESS
 2  IF IsDead(State) THEN RETURN FAILURE              // pruning condition
 3  var <- SelectDecisionVariable(State)
 4  FOR EACH choice IN Candidates(State, var) DO
 5      IF IsFeasible(State, var, choice) THEN
 6          Apply(State, var, choice)                 // assignment
 7          IF BACKTRACK(State) = SUCCESS THEN RETURN SUCCESS
 8          Undo(State, var, choice)                  // restore previous state
 9      END IF
10  END FOR
11  RETURN FAILURE
END
""")
P("Instantiating the framework: N-Queens uses Candidates = columns; Subset Sum uses Candidates = {Include, Exclude}; Graph Colouring uses Candidates = colours. "
  "The framework is general because each problem only supplies its own IsGoal, IsDead, Candidates, IsFeasible, Apply and Undo.")
P("<b>A3.3 &mdash; The role of undo (1 mark).</b> A candidate is explored by changing the shared state. When its subtree finishes, the algorithm must return the state to exactly what it was before, "
  "so that the next sibling candidate starts from the same partial solution. Without this, the sibling sees leftovers from a branch that has been abandoned. "
  "Example with Subset Sum, A = [3, 2] and T = 2: the solution is {2}. Start with Include 3, which makes the sum 3 and fails. "
  "If the Include step is not undone, the sum stays at 3 when the algorithm tries Exclude 3. Then Include 2 gives 5, not 2, and the solution {2} is missed. "
  "The search would wrongly return FALSE. Undo prevents this: the sum is reset to 0 before Exclude 3 is tried, so Include 2 gives 2 and the answer is TRUE.")

# A4
story.append(Paragraph("Task A4 &mdash; Tractability: Solving vs Verifying (4 marks)", H2))
table([
    ["Problem", "What constitutes a solution?", "Efficiently verifiable?", "Classification", "Reason"],
    ["1. Shortest Path", "A path from s to t (or its length)", "Yes: sum the edge weights along the path, O(n)", "P", "Dijkstra's algorithm, O(E log V), solves it directly with non-negative weights."],
    ["2. Minimum Spanning Tree", "A spanning tree of minimum total weight", "Yes: check the tree is spanning and its weight, O(E)", "P", "Kruskal or Prim runs in O(E log V)."],
    ["3. Subset Sum (decision)", "A subset S of A with sum equal to T", "Yes: add the elements of S, O(n)", "NP-Complete", "In NP by verification. NP-hard by reduction from Partition. A pseudo-polynomial DP O(nT) exists, but it is exponential in the bit-length of T, so it is not polynomial."],
    ["4. Hamiltonian Cycle (decision)", "A cycle that visits every vertex exactly once", "Yes: check each vertex appears once and consecutive pairs are edges, O(n + m)", "NP-Complete", "In NP by verification. Karp (1972) reduction from 3-SAT / Exact Cover."],
    ["5. TSP (decision)", "A tour of length at most L", "Yes: sum the tour and compare with L, O(n)", "NP-Complete", "In NP by verification. NP-hard by reduction from Hamiltonian Cycle."],
    ["6. TSP (optimisation)", "The minimum-length tour (or its length)", "Only partly: a claimed tour can be checked, but optimality cannot be checked in polynomial time", "NP-Hard", "Not a yes/no problem, so it is not in NP as defined. It is at least as hard as the decision version, which is NP-Complete."],
], [2.5, 3.2, 3.6, 2.7, 4.6])
P("<b>Inquiry 1 &mdash; Why is &lsquo;difficult to solve&rsquo; not an adequate definition of NP?</b> "
  "NP is defined by verification, not difficulty. A problem is in NP if a proposed solution (a certificate) can be checked in polynomial time. "
  "Difficulty has no precise, measurable meaning, and it does not separate the classes correctly: problems in P such as Shortest Path are not easy in every practical sense, and some problems that are hard to solve are not in NP at all, because verifying a proposed answer is also hard. "
  "Defining NP through verifiability gives a precise, testable condition, and it places the focus on whether a solution can be recognised quickly.")
P("<b>Inquiry 2 &mdash; Why does the decision vs optimisation distinction matter for NP-Completeness?</b> "
  "NP and NP-Complete are classes of yes/no problems. An optimisation problem such as &lsquo;find the shortest tour&rsquo; does not have a yes/no answer, so membership in NP is not defined for it. "
  "Complexity results therefore compare the decision version (&lsquo;is there a tour of length at most L?&rsquo;). The two versions stand or fall together: the optimisation version can be solved by binary search on L with only a polynomial number of calls to a decision procedure, "
  "so if the decision version were in P, the optimisation version would be too. Keeping them distinct makes the reductions and the classification precise.")

# A5
story.append(Paragraph("Task A5 &mdash; Design When Exactness May Be Too Expensive: Set Cover (4 marks)", H2))
P("<b>Worked instance (from B3.2).</b> Zones 0&ndash;7. Centres: A = {0,1,2,3}, B = {4,5,6,7}, C = {0,1,4,5,6}, D = {2,7}, E = {3,7}. The goal is the fewest centres covering every zone.")
P("<b>A5.1 &mdash; Exact perspective (1 mark).</b> An exact search lists all subsets of centres, in increasing order of size, and returns the first subset whose union equals the universe. "
  "The first size that works is the optimum. For the instance above, the subsets of size 1 and 2 are examined, and {A, B} is the first success. "
  "The approach becomes problematic as the number of centres c grows: there are 2<super>c</super> subsets in the worst case, and even when the optimum is small, every smaller subset must be ruled out. "
  "For c = 30 there are over one billion subsets, so the exact method is only practical for small instances.")
P("<b>A5.2 &mdash; Approximation design (2 marks).</b>")
code("""
ALGORITHM GreedySetCover(U, S[1..c])
INPUT:  universe U of zones; centres S[1..c], each a subset of U
OUTPUT: list of chosen centres covering U, or FAILURE

 1  uncovered <- U                                   // uncovered zones
 2  chosen    <- EMPTY LIST                          // selected centres
 3  WHILE uncovered is not EMPTY DO                  // termination test
 4      best <- NONE ;  bestGain <- -1
 5      FOR i <- 1 TO c DO                           // selection criterion
 6          gain <- | S[i] INTERSECT uncovered |     // newly covered zones
 7          IF gain > bestGain THEN                  // strict '>' : lowest index wins ties
 8              best <- i ;  bestGain <- gain
 9          END IF
10      END FOR
11      IF bestGain = 0 THEN RETURN FAILURE          // a zone has no centre
12      APPEND best TO chosen                        // record selection
13      uncovered <- uncovered MINUS S[best]         // state update
14  END WHILE
15  RETURN chosen
END
""")
P("<b>A5.3 &mdash; What have we sacrificed? (1 mark).</b> Finding a feasible cover means producing a set of centres that covers every zone. This is easy to check and the greedy algorithm always does it when a cover exists. "
  "Proving that the cover uses the minimum number of centres is a different and much harder claim. The greedy output carries no such proof. "
  "On the worked instance greedy returns {C, A, B} (3 centres), while {A, B} (2 centres) is optimal. "
  "Theory gives a guarantee of a different kind: the greedy cover is at most H(d) times the optimum, where d is the largest centre size and H(d) is the d-th harmonic number. "
  "Greedy therefore gives a feasible answer quickly with a provable bound, but not optimality.")

story.append(PageBreak())
# ---------------------------------------------------------------- PART B
story.append(Paragraph("PART B &mdash; Implementation and Computational Investigation (25 marks)", H1))
P("All programs are in Python 3 and use only the standard library. Each program writes its results to the terminal. The screenshots in this section show the real output of each run, "
  "captured by Report/make_screenshots.py. Each file is listed in the repository layout at the end of this report.")

story.append(Paragraph("Task B1 &mdash; Implement and Instrument Your Search: Graph Colouring (7 marks)", H2))
P("<b>Implementation.</b> Source_Code/Task_B1_Graph_Colouring/graph_colouring.py implements the algorithm from A1.4 with two selection rules: "
  "<b>Version 1</b> (input order) and <b>Version 2</b> (saturation order). The program records: search nodes visited, candidate assignments attempted, branches rejected by the feasibility test, "
  "number of backtracks (undo operations), maximum search depth, and the final colouring if one exists.")
P("<b>Version 2 selection rule (B1.3).</b> Choose the uncoloured vertex with the most distinct colours already used on its neighbours (its saturation). "
  "Ties are broken by higher degree, then lower index. The reason is that a vertex whose neighbourhood already uses many colours is the one most likely to have no free colour, so choosing it early exposes conflicts sooner and avoids exploring independent parts of the graph that cannot influence the outcome.")
P("<b>B1.1 &mdash; Validation (2 marks).</b> The test suite (test_graph_colouring.py) runs 8 tests:")
bullets([
    "<b>Colourable graph</b>: Petersen graph with k = 3. Intent: a known colourable graph must give a valid colouring, checked independently.",
    "<b>Uncolourable graph</b>: K4 with k = 3. Intent: the search must exhaust all options and report failure, after backtracking.",
    "<b>Boundary cases</b>: empty graph (n = 0), single vertex with k = 1, and a single edge with k = 1. Intent: termination on the smallest inputs, and failure at the second vertex.",
    "<b>Odd cycle</b>: C5 is not 2-colourable but is 3-colourable. Intent: correct handling of the boundary between feasible and infeasible k.",
    "<b>Randomised oracle check</b>: 150 random graphs with n up to 7 are compared against exhaustive enumeration. Intent: both orders agree with the ground truth.",
    "<b>Invalid input</b>: self-loops, out-of-range vertices and unknown order names are rejected.",
])
shot("B1_1_unit_tests", "Figure B1-1. Unit test run: all 8 tests pass (captured output).")
P("<b>B1.2 &mdash; Compare design with implementation (1 mark).</b> The implementation follows the Part A pseudocode, with these modifications and reasons:")
bullets([
    "Vertices and colours are 0-indexed (Python lists), where the pseudocode uses 1-indexed names. This is a language convention only.",
    "Counters were added (nodes, candidates, rejected, backtracks, max_depth) because the assignment requires instrumentation.",
    "The vertex-selection step was split into two rules so that the same search can be compared with two orderings (Version 1 and Version 2).",
    "The empty-domain check (A1.3) is not a separate look-ahead. In the code, it appears as a vertex whose every candidate colour is rejected, which causes FAILURE on the next line. The effect is the same, but the failure is detected one step later than the rule would allow. A forward-checking version would prune earlier and is a possible improvement.",
    "The empty graph is a special case: the search returns immediately with one node, which is the goal test.",
])
shot("B1_1_petersen_demo", "Figure B1-2. Petersen graph with k = 3, both orders: valid colouring, no backtracks required.")

P("<b>B1.3 and B1.4 &mdash; Improve the search order and measure the effect (2 + 2 marks).</b> The same five graphs were run with both orders. "
  "The table below is the captured output of compare_orders.py.")
shot("B1_4_order_comparison", "Figure B1-3. Measured effect of the ordering rule on identical graphs (captured output).")
P("<b>Did the ordering rule reduce the amount of search? Why?</b> Yes, on every instance where the search had to do real work. On G(14, 0.6) with k = 4 the search tree fell from 1,529 nodes to 185 (about 8.3 times fewer), "
  "and on G(16, 0.7) with k = 4 it fell from 653 to 65 (about 10 times fewer). On G(12, 0.5) with k = 3 it fell from 34 to 16. "
  "On the Petersen graph and K4 the two orders are the same: Petersen is easy under either rule, and in K4 every vertex has the same saturation and degree, so the saturation rule has nothing to distinguish. "
  "The reason for the reduction is that saturation places the most constrained vertices first, so conflicts appear at shallow depth (maximum depth 4 instead of 8 on G(16, 0.7)) and whole subtrees are pruned. Input order can delay a conflict behind many unrelated vertices.")

story.append(Paragraph("Task B2 &mdash; Engineer an Adversarial Input: Same Size, Very Different Search (5 marks)", H2))
P("<b>Design.</b> Both graphs have n = 10 vertices and k = 3 colours. "
  "<b>Graph A (easy)</b> is the path 0&ndash;1&ndash;2&ndash;&hellip;&ndash;9. Each vertex has at most one earlier neighbour, so a free colour is almost always available. "
  "<b>Graph B (hard)</b> has vertices 0&ndash;5 isolated (they never conflict with anything) and vertices 6&ndash;9 forming K4, which cannot be 3-coloured. "
  "In input order the six free vertices come before the conflict, so every combination of their colours (3<super>6</super> = 729 of them) is examined before the K4 failure is found.")
P("<b>Prediction (recorded before running).</b> (1) Graph B will require far more search than Graph A. (2) In Graph B, unsuccessful branches arise at the K4 vertices, but only after vertices 0&ndash;5 have been coloured in every combination. "
  "(3) Under input order, pruning on Graph B happens late (depth 6 or more). Under saturation order, K4 is chosen first, so the conflict is met at depth 3 or 4 and the isolated vertices are never explored.")
shot("B2_adversarial", "Figure B2-1. Adversarial comparison: prediction printed first, then measured results (captured output).")
P("<b>Outcome.</b> All three predictions were confirmed. Under input order Graph B needed 12,028 search nodes against 11 for Graph A (a factor of about 1,094). "
  "Its maximum depth was 9, so the conflict was reached only after the free vertices. Under saturation order the same Graph B needed 16 nodes and reached depth 3.")
P("<b>Investigation 1 &mdash; Why does input size alone fail to describe the effort?</b> Both graphs have n = 10 and k = 3, yet their search costs differ by three orders of magnitude. "
  "Backtracking cost depends on how many partial assignments survive before a contradiction is found. That depends on the structure of the graph and on the order in which vertices are chosen, not on n alone. "
  "A large number of unconstrained vertices multiplies the number of branches without contributing to any conflict, while a small unsatisfiable core, once reached, ends the search quickly.")
P("<b>Investigation 2 &mdash; Structural property that caused the extra search.</b> Graph B contains an <i>unsatisfiable core</i> (K4) that is independent of vertices 0&ndash;5, placed late in the order. "
  "Each of the six free vertices has three colours, so the tree below the root is multiplied by 3<super>6</super> before the core is reached. "
  "This is the property that a good ordering removes: saturation ordering reaches the core first, so the free vertices are never multiplied.")

story.append(Paragraph("Task B3 &mdash; Exact vs Approximate: Emergency Service Set Cover (8 marks)", H2))
P("<b>Implementation.</b> Source_Code/Task_B3_Exact_vs_Approximation/set_cover.py provides Solution A (exact, subsets in increasing size) and Solution B (greedy, from A5.2). "
  "Zones and centres are stored as bitmasks. Effort is counted rather than timed: exact effort is the number of subsets examined; greedy effort is the number of centre evaluations.")
P("<b>B3.1 &mdash; Correctness on small instances (2 marks).</b> Three random instances were generated with fixed seeds (101, 202, 303) before any result was seen. "
  "The table is the captured output of run_experiments.py. Greedy matched the optimum in all three cases.")
shot("B3_experiments", "Figure B3-1. Correctness on three small instances and the scalability experiment (captured output).")
P("<b>Honest note.</b> The three seeds were fixed in advance, not selected for agreement. The B3.3 table below shows that greedy does not always match: at 22 zones it used 4 centres where 3 suffice. "
  "The method for the counterexample is in B3.2.")
P("<b>B3.2 &mdash; Find a counterexample (2 marks).</b> Instance: zones 0&ndash;7; A = {0,1,2,3}, B = {4,5,6,7}, C = {0,1,4,5,6}, D = {2,7}, E = {3,7}.")
bullets([
    "<b>Step 1.</b> Uncovered = {0..7}. Gains: A 4, B 4, C 5, D 2, E 2. Greedy chooses <b>C</b> (largest gain, 5 zones).",
    "<b>Step 2.</b> Uncovered = {2, 3, 7}. Gains: A 2 ({2,3}), B 1 ({7}), D 2 ({2,7}), E 2 ({3,7}). Tie between A, D and E; the lowest index, <b>A</b>, is chosen.",
    "<b>Step 3.</b> Uncovered = {7}. Gains: B 1, D 1, E 1. The lowest index, <b>B</b>, is chosen.",
    "<b>Result.</b> Greedy returns {C, A, B}, size 3. The optimum is {A, B}, size 2. The decision that led away from the optimum was choosing C at step 1: its five zones split the remaining zones so that two more centres were needed, while A and B together cover the universe exactly.",
])
shot("B3_counterexample", "Figure B3-2. Counterexample: exact returns {A, B} (size 2); greedy returns {C, A, B} (size 3) (captured output).")
P("<b>B3.3 &mdash; Increase the problem size (2 marks).</b> The scalability table below is the same captured output as Figure B3-1. "
  "Exact effort is the number of subsets examined until the first minimum-size cover is found; 2<super>centres</super> is the worst-case number of subsets with no early stop. "
  "Greedy effort is the number of centre evaluations.")
P("<b>Observations.</b> The worst case doubles with every added centre (2<super>22</super> is over four million). "
  "The observed exact effort is not monotone, because it depends on how early a minimum-size cover appears in enumeration order, not only on the size. "
  "Greedy effort grows roughly with (number of centres) times (cover size), so it stays in the tens to low hundreds. At 22 zones greedy returned 4 centres against an optimum of 3.")
P("<b>B3.4 &mdash; Engineering trade-off (2 marks).</b> Greedy gained a predictable, polynomial amount of work: at most c evaluations per chosen centre, which stayed under 100 across all runs. "
  "It sacrificed optimality: it was wrong on the counterexample and on the 22-zone instance (one extra centre in 9 scaled cases). "
  "A realistic situation in which I would accept the approximate solution is emergency-centre planning for a large region, where data change weekly, the planning meeting needs an answer in minutes, and one additional centre is a modest cost compared with leaving a zone uncovered or waiting for an exact answer that cannot be computed in time. "
  "The greedy answer can be verified immediately, and the H(d) bound limits how far it can stray.")

story.append(Paragraph("Task B4 &mdash; Final Engineering Decision: Bin Packing Under a Production Constraint (5 marks)", H2))
P("<b>B4.1 &mdash; Implement a practical strategy (2 marks).</b> Source_Code/Task_B4_Bin_Packing/bin_packing.py implements <b>First Fit Decreasing (FFD)</b>. "
  "<b>Placement rule:</b> sort workloads by demand in decreasing order; place each workload on the first open server with enough remaining capacity; open a new server only if none fits. "
  "The run time is O(n log n) for the sort plus the placement scan. The program verifies that every workload is assigned once and that no server is over capacity.")
shot("B4_bin_packing", "Figure B4-1. FFD output: demo allocation with workloads, used and remaining capacity per server; the challenge case; and the 5,000-workload production run (captured output).")
P("<b>B4.2 &mdash; Challenge the strategy (1 mark).</b> Input: [4, 4, 3, 3, 3, 3] with C = 10. FFD places 4 and 4 on server 1 (total 8). Neither 3 fits on it, so both 3, 3, 3 go to server 2 (total 9) "
  "and the last 3 opens server 3. FFD uses <b>3 servers</b>. An exact branch-and-bound search finds that <b>2 servers</b> suffice, with packings {4, 3, 3} and {4, 3, 3}, each exactly full. "
  "FFD uses one server too many because it commits to the large items first and leaves no way to fill the gaps exactly.")
P("<b>B4.3 &mdash; Production decision note (2 marks).</b>")
bullets([
    "<b>Why exhaustive search is unattractive at production scale.</b> Bin packing is NP-hard. Exact search examines a tree that grows exponentially in the number of workloads. Even a few dozen workloads can make the search slow, and thousands are out of reach.",
    "<b>What guarantee FFD provides.</b> FFD never uses more than about 11/9 of the optimal number of servers, plus a constant (Johnson, 1973: FFD(I) at most 11/9 OPT(I) + 6/9). The guarantee is a worst-case bound, not a per-instance promise. On the challenge input the ratio is 3/2.",
    "<b>What computational advantage it provides.</b> The 5,000-workload run took about 79 ms and reached the lower bound ceil(total demand / C) = 1,532 servers. Since no packing can use fewer servers than this bound, FFD was optimal for that instance.",
    "<b>When an exact approach might still be appropriate.</b> For small batches (for example, up to about 20 workloads per decision), for offline planning where the cost of an extra server is high and time is available, or as a benchmark to measure how far the heuristic is from optimal on representative data.",
    "<b>Evidence I would monitor before deployment.</b> Servers used compared with the lower bound, for every batch; unused capacity per server; placement latency at production batch sizes; the frequency of batches where the gap is one or more servers; and any capacity overflow events, which must be zero by construction. Monitoring should compare live batches against a periodic exact solve on small samples.",
])
P("<b>Decision.</b> Deploy FFD for the production placement path, because it is fast, simple, and has a known worst-case bound. Keep the exact solver as an offline check on small samples, and monitor the server count against the lower bound so that a sustained gap triggers a review.")

# ---------------------------------------------------------------- CONCLUSION
story.append(Paragraph("Conclusion", H1))
P("The assignment followed the required progression: Model, Search, Prune, Backtrack, Measure, Analyse Complexity, Approximate and Evaluate. "
  "Backtracking with pruning and a well-chosen ordering reduced graph-colouring search by up to a factor of about 10 on the random instances and turned an exponential case into a trivial one on the adversarial pair. "
  "The set-cover and bin-packing experiments showed the central engineering question: greedy heuristics run in predictable time and are often optimal, but they carry a known gap in theory and a measurable gap in some instances. "
  "The key result is not a single correct answer: it is an account of how much search was required, why it was required, when it stops being practical, and what should be done about it.")

# ---------------------------------------------------------------- REPO
story.append(Paragraph("Repository Layout and How to Run", H1))
code("""
CO5_Assignment_5/
+-- Source_Code/
|   +-- Task_B1_Graph_Colouring/
|   |   +-- graph_colouring.py        (algorithm, two orders, instrumentation)
|   |   +-- test_graph_colouring.py   (B1.1 validation suite)
|   |   +-- compare_orders.py         (B1.3 / B1.4 measurements)
|   +-- Task_B2_Adversarial_Search/
|   |   +-- adversarial.py            (B2 graphs, prediction, measurements)
|   +-- Task_B3_Exact_vs_Approximation/
|   |   +-- set_cover.py              (exact and greedy, B3.2 counterexample)
|   |   +-- run_experiments.py        (B3.1 and B3.3)
|   +-- Task_B4_Bin_Packing/
|       +-- bin_packing.py            (FFD, challenge case, production run)
+-- Report/
|   +-- CO5_Assignment_5_Report.pdf   (this report)
|   +-- build_report.py               (builds this PDF)
|   +-- make_screenshots.py           (runs all programs, renders screenshots)
|   +-- screenshots/                  (PNG screenshots and .txt captured output)
+-- README.md
""")
P("<b>Run:</b> from each task folder, run <font name='Mono'>python3 &lt;file&gt;.py</font>. Python 3.8 or later. To run the tests: <font name='Mono'>python3 test_graph_colouring.py</font>. "
  "To regenerate screenshots and this PDF: <font name='Mono'>cd Report &amp;&amp; python3 make_screenshots.py &amp;&amp; python3 build_report.py</font> (requires reportlab and Pillow).")

# ---------------------------------------------------------------- BUILD
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "CO5 Assignment 5 - SARAVANA H")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()

out = os.path.join(HERE, "CO5_Assignment_5_Report.pdf")
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                        title="CO5 Assignment 5 Report", author="SARAVANA H")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", out)
