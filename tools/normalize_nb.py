# -*- coding: utf-8 -*-
"""Normalise notebooks to valid nbformat 4.5:
- markdown cells must not carry 'outputs' / 'execution_count'
- every cell gets a unique 'id' (nbformat 4.5 requires it)
- code cells keep 'outputs' + 'execution_count'
Validates each file with nbformat.validate before saving.
"""
import glob
import io
import json
import os
import sys
import uuid

import nbformat

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"


def normalise(path):
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    changed = False
    seen_ids = set()

    for cell in nb.get("cells", []):
        ctype = cell.get("cell_type")
        if ctype == "markdown":
            for bad in ("outputs", "execution_count"):
                if bad in cell:
                    del cell[bad]
                    changed = True
        elif ctype == "code":
            cell.setdefault("outputs", [])
            cell.setdefault("execution_count", None)
        cell.setdefault("metadata", {})
        cid = cell.get("id")
        if not isinstance(cid, str) or not cid or cid in seen_ids:
            cid = uuid.uuid4().hex[:8]
            cell["id"] = cid
            changed = True
        seen_ids.add(cid)

    nb["nbformat"] = 4
    nb["nbformat_minor"] = 5

    node = nbformat.from_dict(nb)
    nbformat.validate(node)

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
    return changed


files = sorted(glob.glob(os.path.join(ROOT, "*.ipynb")))
for path in files:
    try:
        changed = normalise(path)
        print(f"{'FIXED  ' if changed else 'OK     '} {os.path.basename(path)}")
    except Exception as exc:
        print(f"FAILED {os.path.basename(path)}: {exc}")
        raise
print("done")
