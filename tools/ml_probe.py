# -*- coding: utf-8 -*-
"""Map ML notebook outputs to models, extract exact accuracies, build assets/ml/accuracy_comparison.png."""
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
NB = os.path.join(ROOT, "Modul-04_SpaceX_Machine Learning Prediction_Part_5 (1).ipynb")
ML = os.path.join(ROOT, "assets", "ml")

nb = json.load(open(NB, encoding="utf-8"))

print("=== cells with text streams mentioning accuracy ===")
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    for o in c.get("outputs", []):
        if o.get("output_type") == "stream":
            t = "".join(o["text"])
            if "ccuracy" in t or "best" in t.lower():
                print(f"[cell {i}] {t.strip()[:400]}")
                print()

print("=== cells containing confusion_matrix (model identification) ===")
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    if "confusion_matrix" in src or "ConfusionMatrixDisplay" in src:
        m = re.findall(r"(Logistic\s*Regression|SVM|Decision\s*Tree|KNN|Random\s*Forest|AdaBoost|Bagging)", src, re.I)
        has_png = any("image/png" in o.get("data", {}) for o in c.get("outputs", []))
        print(f"[cell {i}] png={has_png} models_mentioned={m} | {src.strip()[:90].replace(chr(10), ' / ')}")

print("\n=== model test accuracy cells (search for .score / accuracy_score) ===")
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    if "accuracy_score" in src or ".score(" in src:
        outs = []
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream":
                outs.append("".join(o["text"]).strip())
            elif "text/plain" in o.get("data", {}):
                d = o["data"]["text/plain"]
                outs.append(("".join(d) if isinstance(d, list) else d).strip())
        print(f"[cell {i}] {src.strip()[:100].replace(chr(10), ' / ')}")
        for t in outs:
            print(f"        -> {t[:200]}")
