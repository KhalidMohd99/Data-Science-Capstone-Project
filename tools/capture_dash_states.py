# -*- coding: utf-8 -*-
"""Capture the four Plotly-Dash dashboard states deterministically.

Each state starts its own server (different port, initial widget values set through
environment variables) so no fragile UI interaction is needed.

Outputs (assets/dash):
  dash_01_pie_all_sites.png               pie - successful launches per site
  dash_02_full_default.png                full dashboard, default state
  dash_03_pie_best_site.png               pie - KSC LC 39A (highest success ratio)
  dash_06_full_best_site.png              full dashboard, best site selected
  dash_04_scatter_all_sites_0_6000.png    scatter - all sites, payload [0, 6000] kg
  dash_05_scatter_all_sites_6000_16000.png scatter - all sites, payload [6000, 16000] kg
  dash_07_full_payload_filter.png         full dashboard, payload filter applied
"""
import io
import os
import socket
import subprocess
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from playwright.sync_api import sync_playwright

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
DASH_DIR = os.path.join(ROOT, "assets", "dash")
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")

# (state name, env overrides, port, [(file name, css selector or None for full page)])
STATES = [
    ("default", {}, 8061, [
        ("dash_01_pie_all_sites.png", "#success-pie"),
        ("dash_02_full_default.png", None),
    ]),
    ("best_site", {"DASH_INITIAL_SITE": "KSC LC 39A"}, 8062, [
        ("dash_03_pie_best_site.png", "#success-pie"),
        ("dash_06_full_best_site.png", None),
    ]),
    ("payload_low", {"DASH_INITIAL_MIN": "0", "DASH_INITIAL_MAX": "6000"}, 8063, [
        ("dash_04_scatter_all_sites_0_6000.png", "#payload-scatter"),
    ]),
    ("payload_high", {"DASH_INITIAL_MIN": "6000", "DASH_INITIAL_MAX": "16000"}, 8064, [
        ("dash_05_scatter_all_sites_6000_16000.png", "#payload-scatter"),
        ("dash_07_full_payload_filter.png", None),
    ]),
]


def wait_port(port, timeout=45):
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            s.settimeout(1)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(1)
    return False


os.makedirs(DASH_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 1000})

    for name, overrides, port, shots in STATES:
        env = os.environ.copy()
        env.update(overrides)
        env["DASH_PORT"] = str(port)
        print(f"state '{name}' on port {port} {overrides}")
        proc = subprocess.Popen([PY, "spacex_dash_app.py"], cwd=ROOT, env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            if not wait_port(port):
                print("  !! server did not start")
                continue
            page.goto(f"http://localhost:{port}", wait_until="networkidle", timeout=45000)
            page.wait_for_selector("#success-pie .js-plotly-plot", timeout=30000)
            page.wait_for_timeout(3000)
            print("  site-info   :", page.text_content("#site-info"))
            print("  payload-info:", page.text_content("#payload-info"))
            for fname, sel in shots:
                path = os.path.join(DASH_DIR, fname)
                if sel is None:
                    page.screenshot(path=path, full_page=True)
                else:
                    page.locator(sel).screenshot(path=path)
                print(f"  saved {fname} ({os.path.getsize(path) // 1024} KB)")
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except Exception:
                proc.kill()
            time.sleep(1.5)
        print()

    browser.close()

print("DASH STATES DONE")
