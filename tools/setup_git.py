# -*- coding: utf-8 -*-
"""Initialize git repo, add all files, commit, add remote, and produce push commands."""
import io
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
REPO = "https://github.com/KhalidMohd99/Data-Science-Capstone-Project"

def run(cmd):
    proc = subprocess.Popen(cmd, cwd=ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print(">>>", cmd)
    if out.strip():
        print(out.decode('utf-8', errors='ignore'))
    if err.strip():
        print("ERR:", err.decode('utf-8', errors='ignore'))
    print("---")
    return proc.returncode

if not os.path.exists(os.path.join(ROOT, ".git")):
    run("git init")
run("git add .")
run('git commit -m "Add Data Science Capstone project: notebooks, dashboard, EDA/ML assets, SQL results, maps, PPTX/PDF, and scripts"')
run(f"git remote remove origin 2>NUL; git remote add origin {REPO}.git")
print("=== PUSH COMMANDS (run manually if credentials not cached) ===")
print(f"cd /d {ROOT}")
print("git branch -M main")
print("git push -u origin main")
