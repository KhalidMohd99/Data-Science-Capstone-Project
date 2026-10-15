# -*- coding: utf-8 -*-
"""Headless (Playwright) screenshot capture for the capstone presentation.

Dashboard states
  dash_01_pie_all_sites.png              pie: successful launches per site (slide 39)
  dash_02_full_default.png               full dashboard, default state
  dash_03_pie_best_site.png              pie: KSC LC 39A (highest success ratio, slide 40)
  dash_06_full_best_site.png             full dashboard with the best site selected
  dash_04_scatter_all_sites_0_6000.png   scatter, ALL sites, payload [0, 6000]  (slide 41a)
  dash_05_scatter_all_sites_6000_16000.png scatter, ALL sites, payload [6000, 16000] (slide 41b)
  dash_07_full_payload_filter.png        full dashboard with the payload filter applied

Maps: assets/maps/map_1..3.png
SQL : assets/sql/query_01..10.png
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from playwright.sync_api import Page, sync_playwright

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
DASH_DIR = os.path.join(ROOT, "assets", "dash")
MAP_DIR = os.path.join(ROOT, "assets", "maps")
SQL_DIR = os.path.join(ROOT, "assets", "sql")


def shot(target, path, full_page=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(target, Page):
        target.screenshot(path=path, full_page=full_page)
    else:  # Locator
        target.screenshot(path=path)
    print(f"  saved {os.path.relpath(path, ROOT)} ({os.path.getsize(path) // 1024} KB)")


def goto_retry(page, url, tries=6, wait="networkidle"):
    for i in range(tries):
        try:
            page.goto(url, wait_until=wait)
            return True
        except Exception as exc:
            print(f"  retry {i + 1}/{tries}: {exc.__class__.__name__}")
            page.wait_for_timeout(3000)
    raise RuntimeError(f"could not load {url}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 1000})

    def select_site(name):
        page.click("#site-dropdown")
        page.wait_for_timeout(700)
        page.click(f"label.dash-dropdown-option:has-text('{name}')")
        page.wait_for_timeout(2300)

    def set_range(lo, hi):
        page.fill(".dash-range-slider-min-input", str(lo))
        page.keyboard.press("Enter")
        page.wait_for_timeout(1200)
        page.fill(".dash-range-slider-max-input", str(hi))
        page.keyboard.press("Enter")
        page.wait_for_timeout(2300)

    # ------------------------------------------------------------- DASHBOARD
    print("Dash dashboard:")
    goto_retry(page, "http://localhost:8050")
    page.wait_for_selector("#success-pie .js-plotly-plot", timeout=30000)
    page.wait_for_timeout(2500)

    pie = page.locator("#success-pie")
    scatter = page.locator("#payload-scatter")

    # state 1: default (all sites, full payload range) -> slide 39
    print("  default state:", page.text_content("#site-info"), "|", page.text_content("#payload-info"))
    shot(pie, os.path.join(DASH_DIR, "dash_01_pie_all_sites.png"))
    shot(page, os.path.join(DASH_DIR, "dash_02_full_default.png"), full_page=True)

    # state 2: best site selected -> slide 40
    select_site("KSC LC 39A")
    print("  best-site state:", page.text_content("#site-info"))
    shot(pie, os.path.join(DASH_DIR, "dash_03_pie_best_site.png"))
    shot(page, os.path.join(DASH_DIR, "dash_06_full_best_site.png"), full_page=True)

    # state 3: all sites + payload [0, 6000] -> slide 41a
    select_site("All Sites")
    set_range(0, 6000)
    print("  payload [0,6000]:", page.text_content("#payload-info"))
    shot(scatter, os.path.join(DASH_DIR, "dash_04_scatter_all_sites_0_6000.png"))

    # state 4: all sites + payload [6000, 16000] -> slide 41b
    set_range(6000, 16000)
    print("  payload [6000,16000]:", page.text_content("#payload-info"))
    shot(scatter, os.path.join(DASH_DIR, "dash_05_scatter_all_sites_6000_16000.png"))
    shot(page, os.path.join(DASH_DIR, "dash_07_full_payload_filter.png"), full_page=True)

    # ------------------------------------------------------------- MAPS
    print("Folium maps:")
    for name in ("map_1_all_launch_sites", "map_2_launch_outcomes", "map_3_site_proximity"):
        goto_retry(page, f"file:///{os.path.join(MAP_DIR, name)}.html".replace("\\", "/"))
        page.wait_for_timeout(2500)
        shot(page, os.path.join(MAP_DIR, f"{name}.png"), full_page=True)

    # ------------------------------------------------------------- SQL
    print("SQL tables:")
    for i in range(1, 11):
        path = os.path.join(SQL_DIR, f"query_{i:02d}.html")
        if not os.path.exists(path):
            continue
        goto_retry(page, f"file:///{path}".replace("\\", "/"), wait="load")
        page.wait_for_timeout(400)
        shot(page, os.path.join(SQL_DIR, f"query_{i:02d}.png"))

    browser.close()

print("ALL SCREENSHOTS DONE")
