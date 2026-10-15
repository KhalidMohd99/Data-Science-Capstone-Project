# -*- coding: utf-8 -*-
"""List every %%sql cell of the SQL notebook with its result columns, so the 10 queries
can be mapped to template slides 24-33 in the right order."""
import io
import json
import re
import sys

OUT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story\sql_cells.txt"
f = open(OUT, "w", encoding="utf-8")


def p(*a):
    print(*a, file=f)


nb = json.load(open(r"C:\Users\khali\Downloads\Claud_IBM-capstone-story\04-SQL Notebook for Peer .ipynb",
                    encoding="utf-8"))
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])
    if c["cell_type"] == "markdown":
        t = src.strip()
        if re.search(r"TASK|Task|task", t):
            p(f"[{i}] MD: {t[:150]}")
        continue
    if "%%sql" in src:
        outs = c.get("outputs", [])
        cols = []
        for o in outs:
            h = o.get("data", {}).get("text/html")
            if h:
                h = "".join(h) if isinstance(h, list) else h
                cols = re.findall(r"<th[^>]*>(.*?)</th>", h)
        p(f"---- [{i}] %%sql out={len(outs)} cols={cols[:12]}")
        p(src.strip()[:400])
        p()
f.close()
print("written")
