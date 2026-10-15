# -*- coding: utf-8 -*-
"""Extract presentation assets from executed notebooks:
- assets/eda/*.png     -> chart images from the EDA visualization notebook
- assets/ml/*.png      -> confusion matrices + accuracy chart from the ML notebook
- assets/sql/*.html    -> saved SQL result tables from the SQL notebook
"""
import base64
import html as html_mod
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
ASSETS = os.path.join(ROOT, "assets")


def cell_text(cell):
    return "".join(cell["source"])


def save_png(out_dir, name, b64data):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64data))
    print(f"  saved {os.path.relpath(path, ROOT)} ({os.path.getsize(path)//1024} KB)")


# ------------------------------------------------------------- EDA charts
print("EDA visualization charts:")
nb = json.load(open(os.path.join(ROOT, "jupyter-labs-eda-dataviz-v2.ipynb"), encoding="utf-8"))
labels = {
    21: "00_payload_vs_flightnumber_reference",
    25: "01_task1_flightnumber_vs_launchsite",
    29: "02_task2_payload_vs_launchsite",
    34: "03_task3_success_rate_vs_orbit",
    38: "04_task4_flightnumber_vs_orbit",
    42: "05_task5_payload_vs_orbit",
    48: "06_task6_yearly_success_trend",
}
found = 0
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    for o in cell.get("outputs", []):
        png = o.get("data", {}).get("image/png")
        if png:
            label = labels.get(i, f"cell{i:02d}")
            save_png(os.path.join(ASSETS, "eda"), label + ".png", png)
            found += 1
print(f"  total: {found}\n")

# ---------------------------------------------------------- ML notebook
print("ML notebook images:")
os.makedirs(os.path.join(ASSETS, "ml"), exist_ok=True)
nb = json.load(open(os.path.join(ROOT, "Modul-04_SpaceX_Machine Learning Prediction_Part_5 (1).ipynb"), encoding="utf-8"))
n = 0
last_label = "output"
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = cell_text(cell)
    for o in cell.get("outputs", []):
        png = o.get("data", {}).get("image/png")
        if png:
            # guess what this image is from the source code around it
            if "accuracy" in src.lower() and ("bar" in src.lower() or "plot" in src.lower()):
                label = "accuracy_comparison"
            elif "confusion_matrix" in src or "ConfusionMatrixDisplay" in src:
                m = re.search(r"(Logistic|SVM|Decision|KNN|RandomForest|AdaBoost|Bagging)\w*", src)
                label = "confusion_matrix_" + (m.group(1).lower() if m else f"cell{i:02d}")
            elif "countplot" in src or "value_counts" in src:
                label = f"cell{i:02d}_plot"
            else:
                label = f"cell{i:02d}_output"
            n += 1
            save_png(os.path.join(ASSETS, "ml"), f"{n:02d}_{label}.png", png)
    # also capture printed accuracy tables
    for o in cell.get("outputs", []):
        if o.get("output_type") == "stream" and "ccuracy" in "".join(o.get("text", [])):
            txt = "".join(o["text"])
            out = os.path.join(ASSETS, "ml", "accuracy_report.txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"  saved accuracy_report.txt ({len(txt)} chars)")
print(f"  total images: {n}\n")

# ------------------------------------------------------------- SQL tables
print("SQL result tables:")
nb = json.load(open(os.path.join(ROOT, "04-SQL Notebook for Peer .ipynb"), encoding="utf-8"))
os.makedirs(os.path.join(ASSETS, "sql"), exist_ok=True)
n = 0
task_no = 0
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = cell_text(cell)
    if not src.strip().startswith("%%sql"):
        continue
    if "%sql SELECT" not in src.replace("\n", " ") and "%%sql" in src:
        pass
    html_out = None
    for o in cell.get("outputs", []):
        h = o.get("data", {}).get("text/html")
        if h:
            html_out = "".join(h) if isinstance(h, list) else h
    if html_out is None:
        continue
    task_no += 1
    # first line comment / query text for the title
    first = next((ln.strip() for ln in src.splitlines() if ln.strip() and not ln.strip().startswith("%%sql")), "Query")
    title = first.lstrip("#").strip()[:90]
    query = html_mod.escape(src.replace("%%sql", "").strip())
    page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
 body {{ font-family: Segoe UI, Arial, sans-serif; margin: 18px; background: #fff; color: #111; }}
 h3 {{ font-size: 15px; margin: 0 0 10px; color: #0f62fe; }}
 pre.query {{ background:#f4f4f4; padding:8px 10px; font-size:12px; border-left:3px solid #0f62fe; white-space:pre-wrap; }}
 table {{ border-collapse: collapse; font-size: 13px; margin-top: 10px; }}
 th, td {{ border: 1px solid #d2d2d2; padding: 4px 10px; text-align: left; }}
 th {{ background: #e0e0e0; }}
</style></head><body>
<h3>SQL Result {task_no}</h3>
<pre class="query">{query}</pre>
{html_out}
</body></html>"""
    out = os.path.join(ASSETS, "sql", f"query_{task_no:02d}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    n += 1
    print(f"  saved query_{task_no:02d}.html  <- {title}")
print(f"  total: {n}")
print("\ndone")
