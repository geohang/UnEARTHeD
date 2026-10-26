"""Capture the figure-mode panels of index.html for print.

A development tool: the page never loads it. It renders #figure/entry
(panel a), #figure/agent-trace (panel b) and #figure/interface (both panels
stacked, with one footer) at 862 logical pixels wide and writes, for each,
to figures/:

  <name>.png  raster at a device scale factor of 3 (about 2,590 pixels across,
              enough for print at 6.5 inches; --scale raises it)
  <name>.pdf  vector: text, outlines and the map stay sharp at any size
  <name>.svg  vector, converted from the PDF when Poppler's pdftocairo is found

Usage, from the repository root:

    pip install playwright
    python -m playwright install chromium      # or pass --channel msedge / chrome
    python tools/capture_figures.py [--channel msedge] [--scale 3] [--pdftocairo PATH]

The page is opened from disk, so no server and no network are needed.
"""

from __future__ import annotations

import argparse
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "index.html").as_uri()
OUT = ROOT / "figures"
WIDTH = 862
ROUTES = {"entry": "#figure/entry", "agent-trace": "#figure/agent-trace", "interface": "#figure/interface"}


def png_size(path: Path) -> tuple[int, int]:
    """Width and height from the PNG header."""
    with path.open("rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--channel", default=None,
                        help="use an installed browser (msedge, chrome) instead of Playwright's Chromium")
    parser.add_argument("--scale", type=float, default=3, help="device scale factor of the PNG (default 3)")
    parser.add_argument("--pdftocairo", default=shutil.which("pdftocairo"),
                        help="path to Poppler's pdftocairo, for the SVG copies (default: found on PATH)")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel=args.channel)
        # Figure mode ignores prefers-color-scheme; light is set here too so captures are reproducible.
        context = browser.new_context(viewport={"width": WIDTH, "height": 1000},
                                      device_scale_factor=args.scale, color_scheme="light")
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.emulate_media(media="screen")
        for name, route in ROUTES.items():
            page.goto(PAGE + route)
            panel = page.locator(".fig-panel")
            panel.wait_for()
            page.evaluate("document.fonts.ready")
            box = panel.bounding_box()
            png = OUT / f"{name}.png"
            panel.screenshot(path=str(png), animations="disabled")
            w, h = png_size(png)
            print(f"{png.relative_to(ROOT)}: {w} x {h} px "
                  f"({box['width']:.0f} x {box['height']:.0f} logical px at {args.scale:g}x)")
            # The panel starts at the top of the page, so a page of its size holds exactly the panel.
            pdf = OUT / f"{name}.pdf"
            page.pdf(path=str(pdf), width=f"{WIDTH}px", height=f"{math.ceil(box['y'] + box['height'])}px",
                     print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                     page_ranges="1")
            print(f"{pdf.relative_to(ROOT)}: vector, page {WIDTH / 96:.2f} x {math.ceil(box['height']) / 96:.2f} in")
            if args.pdftocairo:
                svg = OUT / f"{name}.svg"
                subprocess.run([args.pdftocairo, "-svg", str(pdf), str(svg)], check=True)
                print(f"{svg.relative_to(ROOT)}: vector, from the PDF")
        browser.close()
    if not args.pdftocairo:
        print("pdftocairo not found: SVG copies skipped (the PDFs are vector).")
    if errors:
        print("Console errors:", *errors, sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
