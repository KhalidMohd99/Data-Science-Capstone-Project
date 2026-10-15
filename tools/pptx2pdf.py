# -*- coding: utf-8 -*-
"""Convert PPTX to PDF using PowerPoint COM (Microsoft PowerPoint must be installed)."""
import io
import os
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
PPTX = os.path.join(ROOT, "Data Science Capstone Project Report.pptx")
PDF = os.path.join(ROOT, "Data Science Capstone Project Report.pdf")

try:
    import win32com.client as win32
except Exception as exc:
    print("win32com not available:", exc)
    sys.exit(1)

ppt = win32.Dispatch("PowerPoint.Application")
try:
    ppt.Visible = False
except Exception:
    ppt.Visible = True
try:
    pres = ppt.Presentations.Open(PPTX)
    pres.SaveAs(PDF, FileFormat=32)  # 32 = ppSaveAsPDF
    pres.Close()
    print("PDF saved:", PDF)
    print("exists?", os.path.exists(PDF))
except Exception as exc:
    print("conversion failed:", exc)
finally:
    try:
        ppt.Quit()
    except Exception:
        pass
    time.sleep(1)
