# -*- coding: utf-8 -*-
"""Print a one-line summary of every cell in a notebook (for inspection)."""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

path = sys.argv[1]
nb = json.load(open(path, encoding="utf-8"))
print(f"FILE: {path}")
print(f"total cells: {len(nb['cells'])}")
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])
    if c["cell_type"] == "markdown":
        first = src.strip().split("\n")[0][:100]
        print(f"[{i}] MD  : {first}")
    else:
        outs = c.get("outputs", [])
        errs = [o for o in outs if o.get("output_type") == "error"]
        err = ""
        if errs:
            err = f" ERROR={errs[0]['ename']}: {errs[0]['evalue'][:70]}"
        ec = c.get("execution_count")
        head = src.strip().replace("\n", " / ")[:150]
        print(f"[{i}] CODE exec={ec} outs={len(outs)}{err} :: {head}")

if len(sys.argv) > 2:  # dump full source of specific cells
    for arg in sys.argv[2:]:
        idx = int(arg)
        print(f"\n===== FULL SOURCE [{idx}] =====")
        print("".join(nb["cells"][idx]["source"]))
        print(f"===== OUTPUTS [{idx}] =====")
        print(json.dumps(nb["cells"][idx].get("outputs", []), ensure_ascii=False)[:800])
