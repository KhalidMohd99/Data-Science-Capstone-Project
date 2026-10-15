# -*- coding: utf-8 -*-
"""Probe the Dash 3.x DOM: dropdown options + range slider structure."""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1400, "height": 1000})
    pg.goto("http://localhost:8050", wait_until="networkidle")
    pg.wait_for_timeout(3500)

    # ---- dropdown
    pg.click("#site-dropdown")
    pg.wait_for_timeout(900)
    print("options:", pg.evaluate(
        "() => Array.from(document.querySelectorAll('[role=option], .dash-dropdown-option, li'))"
        ".slice(0,15).map(e => e.tagName + '|' + (e.getAttribute('role')||'') + '|' + e.className + '|' + e.textContent.trim().slice(0,30))"))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)

    # ---- slider
    print("\n#payload-slider outer:", pg.eval_on_selector("#payload-slider", "el => el.tagName + '|' + el.className"))
    print("slider children:", pg.evaluate("""() => {
        const root = document.querySelector('#payload-slider');
        if (!root) return 'no root';
        const walk = (el, d) => {
            if (d > 3) return [];
            let out = [];
            for (const c of el.children) {
                out.push('  '.repeat(d) + c.tagName + '.' + c.className + ' role=' + (c.getAttribute('role')||'') + ' aria=' + (c.getAttribute('aria-valuenow')||''));
                out = out.concat(walk(c, d + 1));
            }
            return out;
        };
        return walk(root, 0).slice(0, 40).join('\\n');
    }"""))
    b.close()
