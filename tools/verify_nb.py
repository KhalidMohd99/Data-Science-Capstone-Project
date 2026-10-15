# -*- coding: utf-8 -*-
"""Verify executed notebooks: errors, executed cells, PNG outputs, printed streams, CSV files."""
import glob
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"

files = sys.argv[1:] or [
    "jupyter-labs-eda-dataviz-v2.ipynb",
    "02-jupyter-labs-webscraping.ipynb",
    "launch_site_location.ipynb",
]

for f in files:
    path = os.path.join(ROOT, f)
    nb = json.load(open(path, encoding="utf-8"))
    errs = imgs = execd = code_cells = 0
    texts = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        code_cells += 1
        if c.get("execution_count"):
            execd += 1
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                errs += 1
                print(f"  ERROR cell {i}: {o['ename']}: {o['evalue'][:120]}")
            data = o.get("data", {})
            if "image/png" in data:
                imgs += 1
            if o.get("output_type") == "stream":
                t = "".join(o["text"]).strip()
                if t:
                    texts.append(f"cell {i}: {t[:220]}".replace("\n", " / "))
    print(f"{f}: code_cells={code_cells} executed={execd} errors={errs} png_outputs={imgs}")
    for t in texts[:10]:
        print("   |", t)
    print()

print("CSV files:")
for p in sorted(glob.glob(os.path.join(ROOT, "*.csv"))):
    print("  ", os.path.basename(p), os.path.getsize(p), "bytes")
