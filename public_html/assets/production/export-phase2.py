"""
Phase 2 Visual Asset Exporter
==============================
Exports all 5 Phase-2 chart HTML files to 1200x630 PNGs.
Output goes to both assets/images/ (site use) and
assets/production/exports/ (archive copy).

Requirements:
  pip install playwright pillow
  playwright install chromium

Usage:
  python export-phase2.py
  (preview server must be running on port 7720)
"""

import asyncio, io, urllib.request
from pathlib import Path
from PIL import Image

BASE_DIR   = Path(r"C:\Users\j-pre\OneDrive\Documents\public_html")
SERVER_URL = "http://localhost:7720"
PROD_DIR   = BASE_DIR / "assets" / "production"
IMG_DIR    = BASE_DIR / "assets" / "images"
EXP_DIR    = PROD_DIR / "exports"
EXP_DIR.mkdir(parents=True, exist_ok=True)

EXPORTS = [
    {
        "name":   "grow-stage-timeline",
        "page":   "assets/production/grow-stage-timeline.html",
        "output": "cannabis-grow-stage-timeline.png",
    },
    {
        "name":   "dwc-nutrient-schedule",
        "page":   "assets/production/dwc-nutrient-schedule.html",
        "output": "dwc-nutrient-schedule-by-stage.png",
    },
    {
        "name":   "trichome-stages",
        "page":   "assets/production/trichome-stages.html",
        "output": "trichome-stages-cannabis-chart.png",
    },
    {
        "name":   "drying-curing-environment",
        "page":   "assets/production/drying-curing-environment.html",
        "output": "cannabis-drying-curing-environment-chart.png",
    },
    {
        "name":   "light-schedule-chart",
        "page":   "assets/production/light-schedule-chart.html",
        "output": "cannabis-light-schedule-12-12-vs-18-6.png",
    },
]

async def export_all():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=2)

        results = []

        for job in EXPORTS:
            print(f"\n>> {job['name']}")
            url = f"{SERVER_URL}/{job['page']}"

            page = await context.new_page()
            await page.set_viewport_size({"width": 1200, "height": 630})
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(2000)   # fonts + canvas paint

            raw = await page.screenshot(full_page=False, scale="device", type="png")
            await page.close()

            # Downscale 2x -> 1x
            img = Image.open(io.BytesIO(raw))
            w, h = img.size
            img_1x = img.resize((w // 2, h // 2), Image.LANCZOS)
            print(f"   {w}x{h} -> {img_1x.width}x{img_1x.height}")

            out_img = IMG_DIR  / job["output"]
            out_exp = EXP_DIR  / job["output"]

            img_1x.save(str(out_img), "PNG", optimize=True, compress_level=7)
            img_1x.save(str(out_exp), "PNG", optimize=True, compress_level=7)

            kb = out_img.stat().st_size // 1024
            print(f"   assets/images/{job['output']}  ({kb} KB)")
            results.append((job["output"], kb))

        await browser.close()

    print(f"\n{'='*52}")
    print("Phase 2 Export Complete")
    print(f"{'='*52}")
    for name, kb in results:
        print(f"  {name:<48}  {kb:>4} KB")
    print(f"\nAll PNGs saved to:  assets/images/")
    print(f"Archive copies in:  assets/production/exports/")
    print()


if __name__ == "__main__":
    try:
        urllib.request.urlopen(SERVER_URL, timeout=3)
    except Exception:
        print(f"\n[ERROR] Preview server not running at {SERVER_URL}")
        print("Start it first:")
        print('  python -m http.server 7720 --directory '
              '"C:\\Users\\j-pre\\OneDrive\\Documents\\public_html"')
        raise SystemExit(1)

    asyncio.run(export_all())
