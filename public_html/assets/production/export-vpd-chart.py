"""
VPD Chart Exporter
==================
Exports vpd-chart.html to:
  assets/images/vpd-chart-cannabis-by-stage.png   (1200x630 site image)
  assets/production/exports/vpd-chart-og.png      (1200x630 OG preview copy)

Requirements:
  pip install playwright pillow
  playwright install chromium

Usage:
  python export-vpd-chart.py
  (preview server must be running on port 7720)
"""

import asyncio, urllib.request
from pathlib import Path

BASE_DIR   = Path(r"C:\Users\j-pre\OneDrive\Documents\public_html")
SERVER_URL = "http://localhost:7720"
PAGE_URL   = f"{SERVER_URL}/assets/production/vpd-chart.html"

OUT_IMAGES = BASE_DIR / "assets" / "images" / "vpd-chart-cannabis-by-stage.png"
OUT_EXPORT = BASE_DIR / "assets" / "production" / "exports" / "vpd-chart-og.png"
OUT_EXPORT.parent.mkdir(parents=True, exist_ok=True)


async def export():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=2)   # 2x => crisp

        page = await context.new_page()
        await page.set_viewport_size({"width": 1200, "height": 630})
        await page.goto(PAGE_URL, wait_until="networkidle")
        await page.wait_for_timeout(1800)    # fonts + canvas paint

        # Screenshot full body (1200x630 at 2x => 2400x1260 raw)
        raw_bytes = await page.screenshot(
            full_page=False,
            scale="device",
            type="png",
        )
        await browser.close()

    # Downscale 2x -> 1x via Pillow (sharp result)
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(raw_bytes))
    w, h = img.size
    print(f"   Raw screenshot: {w}x{h}")

    img_1x = img.resize((w // 2, h // 2), Image.LANCZOS)
    print(f"   Final size:     {img_1x.width}x{img_1x.height}")

    img_1x.save(str(OUT_IMAGES), "PNG", optimize=True, compress_level=7)
    img_1x.save(str(OUT_EXPORT), "PNG", optimize=True, compress_level=7)

    print(f"\n   Saved site image:  {OUT_IMAGES.relative_to(BASE_DIR)}")
    print(f"          {OUT_IMAGES.stat().st_size // 1024} KB")
    print(f"   Saved export copy: {OUT_EXPORT.relative_to(BASE_DIR)}")
    print(f"          {OUT_EXPORT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    try:
        urllib.request.urlopen(SERVER_URL, timeout=3)
    except Exception:
        print(f"\n[ERROR] Preview server not running at {SERVER_URL}")
        print("Start it first:")
        print("  python -m http.server 7720 --directory "
              "\"C:\\Users\\j-pre\\OneDrive\\Documents\\public_html\"")
        raise SystemExit(1)

    print(f"Exporting VPD chart from {PAGE_URL} ...")
    asyncio.run(export())
    print("\nDone.")
