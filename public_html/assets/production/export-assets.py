"""
ColaXpress Brand Asset Exporter
================================
Exports all brand HTML files to production-ready PNG/image files.

Requirements:
  pip install playwright pillow
  playwright install chromium

Usage:
  python export-assets.py

Output files (in assets/production/exports/):
  thumbnail-ep01.png      — 1280x720 YouTube thumbnail
  hud-overlay.png         — 440px HUD widget (transparent bg)
  shorts-card-a.png       — 1080x1920 quote card
  shorts-card-b.png       — 1080x1920 data card
  shorts-card-c.png       — 1080x1920 hook card
  yt-banner.png           — 2560x1440 YouTube channel banner (full bleed)
  yt-profile.png          — 800x800 channel profile picture / CX monogram
  yt-watermark.png        — 150x150 in-video watermark (transparent bg)
  fb-cover.png            — 1640x624 Facebook page cover photo
  brand-sheet.pdf         — Full brand reference (PDF)
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# -- Paths ----------------------------------------------------------
BASE_DIR   = Path(r"C:\Users\j-pre\OneDrive\Documents\public_html")
BRAND_DIR  = BASE_DIR / "assets" / "brand"
OUT_DIR    = BASE_DIR / "assets" / "production" / "exports"
DOC_DIR    = OUT_DIR / "documentary"
SERVER_URL = "http://localhost:7720"  # must match .claude/launch.json port

OUT_DIR.mkdir(parents=True, exist_ok=True)
DOC_DIR.mkdir(parents=True, exist_ok=True)

# -- Export targets -------------------------------------------------
EXPORTS = [
    {
        "name": "thumbnail-ep01",
        "url": f"{SERVER_URL}/assets/brand/thumbnail-ep01.html",
        "viewport": {"width": 1280, "height": 720},
        "selector": ".canvas",        # crop to just the canvas element
        "output": "thumbnail-ep01.png",
        "scale": 1,
    },
    {
        "name": "hud-overlay",
        "url": f"{SERVER_URL}/assets/brand/hud-overlay.html",
        "viewport": {"width": 900, "height": 600},
        "selector": ".hud",           # crop to just the HUD widget
        "output": "hud-overlay.png",
        "scale": 2,                   # 2x for retina-quality composite
    },
    {
        "name": "shorts-card-a",
        "url": f"{SERVER_URL}/assets/brand/shorts-card.html",
        "viewport": {"width": 1100, "height": 560},
        "selector": ".variant-a",
        "output": "shorts-card-a.png",
        "scale": 4,                   # 4x: 270px -> 1080px (1080x1920 production)
    },
    {
        "name": "shorts-card-b",
        "url": f"{SERVER_URL}/assets/brand/shorts-card.html",
        "viewport": {"width": 1100, "height": 560},
        "selector": ".variant-b",
        "output": "shorts-card-b.png",
        "scale": 4,
    },
    {
        "name": "shorts-card-c",
        "url": f"{SERVER_URL}/assets/brand/shorts-card.html",
        "viewport": {"width": 1100, "height": 560},
        "selector": ".variant-c",
        "output": "shorts-card-c.png",
        "scale": 4,
    },

    # ── YouTube channel assets ──────────────────────────────────────
    {
        "name": "yt-banner",
        "url": f"{SERVER_URL}/assets/brand/yt-banner.html",
        "viewport": {"width": 1280, "height": 720},
        "selector": ".canvas",
        "output": "yt-banner.png",
        "scale": 2,          # 1280x720 → 2560x1440 (YouTube banner spec)
    },
    {
        "name": "yt-profile",
        "url": f"{SERVER_URL}/assets/brand/yt-profile.html",
        "viewport": {"width": 800, "height": 800},
        "selector": ".canvas",
        "output": "yt-profile.png",
        "scale": 1,          # native 800x800 (YouTube profile spec)
    },
    {
        "name": "yt-watermark",
        "url": f"{SERVER_URL}/assets/brand/yt-watermark.html",
        "viewport": {"width": 150, "height": 150},
        "selector": ".canvas",
        "output": "yt-watermark.png",
        "scale": 1,          # native 150x150 (YouTube watermark spec)
        "transparent": True,
    },

    # ── Documentary stills — 1920x1080 → exports/documentary/ ───────
    *[
        {
            "name": f"still-{slug}",
            "url": f"{SERVER_URL}/assets/brand/stills/still-{slug}.html",
            "viewport": {"width": 1920, "height": 1080},
            "selector": ".canvas",
            "output": f"still-{slug}.png",
            "out_dir": DOC_DIR,          # route stills to documentary subfolder
            "scale": 1,
        }
        for slug in [
            "00-black",
            "01-opening",
            "02-enclosure",
            "03-complexity",
            "04-phone-night",
            "05-door-open",
            "06-notification",
            "07-vpd-display",
            "08-roots",
            "09-living-room",
            "10-beat-slept",
            "11-beat-one",
            "12-day-01",
            "13-day-07",
            "14-day-14",
            "15-day-28",
            "16-act1",
            "17-act2",
            "18-act3",
            "19-act4",
            "20-act5",
            "21-main-title",
            "22-see-you",
        ]
    ],

    # ── Facebook channel assets ─────────────────────────────────────
    {
        "name": "fb-cover",
        "url": f"{SERVER_URL}/assets/brand/fb-cover.html",
        "viewport": {"width": 820, "height": 312},
        "selector": ".canvas",
        "output": "fb-cover.png",
        "scale": 2,          # 820x312 → 1640x624 (Facebook cover spec)
    },
]

# -- Main export function -------------------------------------------
async def export_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=1)

        for job in EXPORTS:
            print(f"\n>> Exporting: {job['name']}")

            page = await context.new_page()
            await page.set_viewport_size(job["viewport"])

            # Wait for fonts + layout
            await page.goto(job["url"], wait_until="networkidle")
            await page.wait_for_timeout(1500)  # allow Google Fonts to load

            out_path = job.get("out_dir", OUT_DIR) / job["output"]

            # Screenshot the specific element (cropped export)
            element = page.locator(job["selector"]).first
            await element.screenshot(
                path=str(out_path),
                scale="device",   # uses device_scale_factor=1
                type="png",
                omit_background=job.get("transparent", False),
            )

            # If scale > 1, upscale using Pillow
            scale = job.get("scale", 1)
            if scale > 1:
                try:
                    from PIL import Image
                    img = Image.open(out_path)
                    w, h = img.size
                    img_scaled = img.resize((w * scale, h * scale), Image.LANCZOS)
                    img_scaled.save(out_path, "PNG", optimize=True)
                    print(f"   Scaled {w}x{h} -> {w*scale}x{h*scale}")
                except ImportError:
                    print("   [!] Pillow not installed — skipping scale-up.")
                    print("       pip install Pillow  to enable upscaling.")

            file_size = out_path.stat().st_size / 1024
            print(f"   Saved: {out_path.name}  ({file_size:.0f} KB)")
            await page.close()

        # -- Brand sheet PDF ----------------------------------------
        print(f"\n-> Exporting: brand-sheet (PDF)")
        page = await context.new_page()
        await page.set_viewport_size({"width": 1400, "height": 900})
        await page.goto(f"{SERVER_URL}/assets/brand/brand-sheet.html", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        pdf_path = OUT_DIR / "brand-sheet.pdf"
        await page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        pdf_size = pdf_path.stat().st_size / 1024
        print(f"   Saved: brand-sheet.pdf  ({pdf_size:.0f} KB)")
        await page.close()

        await browser.close()

    # -- Summary ---------------------------------------------------
    print(f"\n{'-'*50}")
    print(f"Export complete.\n")
    print(f"Brand assets  ->  {OUT_DIR}")
    for f in sorted(OUT_DIR.iterdir()):
        if f.is_file():
            size_kb = f.stat().st_size / 1024
            print(f"  {f.name:<35} {size_kb:>6.0f} KB")
    print(f"\nDocumentary stills  ->  {DOC_DIR}")
    for f in sorted(DOC_DIR.iterdir()):
        if f.is_file():
            size_kb = f.stat().st_size / 1024
            print(f"  {f.name:<35} {size_kb:>6.0f} KB")
    print(f"{'-'*50}\n")

    print("Upload checklist:")
    print("  yt-banner.png       -> YouTube Studio > Customization > Branding > Banner image")
    print("  yt-profile.png      -> YouTube Studio > Customization > Branding > Picture")
    print("  yt-watermark.png    -> YouTube Studio > Customization > Branding > Video watermark")
    print("  fb-cover.png        -> Facebook Page > Edit Profile > Cover Photo (1640x624)")
    print("  yt-profile.png      -> Facebook Page > Edit Profile > Profile Picture (reuse same file)")
    print("  thumbnail-ep01.png  -> YouTube thumbnail (upload when publishing Ep01)")
    print("  hud-overlay.png     -> Import into Premiere/DaVinci, composite Screen @ 90%")
    print("  shorts-card-a/b/c   -> Shorts end cards -- import into short clip edits")
    print("  brand-sheet.pdf     -> Send to freelancers with their brief\n")

# -- Entry point ----------------------------------------------------
if __name__ == "__main__":
    # Check server is running first
    import urllib.request
    try:
        urllib.request.urlopen(SERVER_URL, timeout=3)
    except Exception:
        print(f"\n[ERROR] Preview server not running at {SERVER_URL}")
        print("Start it first:")
        print("  python -m http.server 7720 --directory \"C:\\Users\\j-pre\\OneDrive\\Documents\\public_html\"")
        print("Then run this script again.\n")
        raise SystemExit(1)

    asyncio.run(export_all())
