"""
Runs every Part B program, saves its real stdout to a .txt file, and renders
terminal-style PNG screenshots into Report/screenshots/.
Run from the Report folder:  python3 make_screenshots.py
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "Source_Code")
OUT = os.path.join(HERE, "screenshots")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MAX_LINES = 42

RUNS = [
    ("B1_1_petersen_demo",   "Task_B1_Graph_Colouring", ["python3", "graph_colouring.py"]),
    ("B1_1_unit_tests",      "Task_B1_Graph_Colouring", ["python3", "test_graph_colouring.py"]),
    ("B1_4_order_comparison","Task_B1_Graph_Colouring", ["python3", "compare_orders.py"]),
    ("B2_adversarial",       "Task_B2_Adversarial_Search", ["python3", "adversarial.py"]),
    ("B3_counterexample",    "Task_B3_Exact_vs_Approximation", ["python3", "set_cover.py"]),
    ("B3_experiments",       "Task_B3_Exact_vs_Approximation", ["python3", "run_experiments.py"]),
    ("B4_bin_packing",       "Task_B4_Bin_Packing", ["python3", "bin_packing.py"]),
]

def render(title, text, path, lines_per_img=MAX_LINES):
    font = ImageFont.truetype(FONT, 15)
    bold = ImageFont.truetype(BOLD, 15)
    cw = font.getlength("M")
    lh = 21
    all_lines = text.rstrip("\n").split("\n")
    chunks = [all_lines[i:i+lines_per_img] for i in range(0, len(all_lines), lines_per_img)] or [[""]]
    for part, lines in enumerate(chunks, 1):
        width = int(max(len(l) for l in lines + [title]) * cw) + 60
        width = max(width, 700)
        height = 46 + lh * len(lines) + 24
        img = Image.new("RGB", (width, height), (30, 30, 30))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, width, 34], fill=(60, 60, 60))
        for i, col in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
            d.ellipse([12 + i*20, 10, 24 + i*20, 22], fill=col)
        suffix = f" (part {part}/{len(chunks)})" if len(chunks) > 1 else ""
        d.text((96, 8), title + suffix, font=bold, fill=(220, 220, 220))
        y = 46
        for l in lines:
            d.text((18, y), l, font=font, fill=(204, 230, 204) if l.strip() else (30,30,30))
            y += lh
        img.save(path if len(chunks) == 1 else path.replace(".png", f"_part{part}.png"))
    return len(chunks)

for name, folder, cmd in RUNS:
    res = subprocess.run(cmd, cwd=os.path.join(SRC, folder), capture_output=True, text=True)
    output = res.stdout + (("\n[stderr]\n" + res.stderr) if res.stderr.strip() else "")
    with open(os.path.join(OUT, name + ".txt"), "w") as f:
        f.write(output)
    prompt = f"$ cd {folder} && {' '.join(cmd)}"
    n = render(prompt, output, os.path.join(OUT, name + ".png"))
    print(f"{name:<24} exit={res.returncode}  images={n}  lines={output.count(chr(10))}")
