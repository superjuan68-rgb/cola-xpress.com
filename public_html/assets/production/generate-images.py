"""
ColaXpress Episode 01 — DALL-E 3 Image Generator
=================================================
Generates all 62 documentary images from the ep01-image-brief.
Saves directly to: assets/production/exports/documentary/

Requirements:
  pip install openai

Usage:
  Set your API key, then run:
  python assets/production/generate-images.py

  API key can be set three ways (checked in this order):
    1. Edit OPENAI_API_KEY at the top of this file
    2. Environment variable:  set OPENAI_API_KEY=sk-...
    3. The script will prompt you if neither is set

Cost estimate:
  62 images × $0.08  (standard, 1792×1024) = ~$4.96
  62 images × $0.120 (hd,       1792×1024) = ~$7.44

Options (edit below):
  QUALITY   "standard" or "hd"
  RESUME    True = skip images already saved (safe to re-run)
  START_AT  1–62, jump to a specific image number
  DELAY     seconds between API calls (13 = stays under 5/min limit)
"""

import os
import sys
import time
import base64
import json
from pathlib import Path

# ── CONFIG — edit these ──────────────────────────────────────────────
OPENAI_API_KEY = ""            # paste key here, or leave blank to use env var
QUALITY        = "standard"   # "standard" ($0.08) or "hd" ($0.12) per image
DELAY          = 13            # seconds between calls — safe for tier-1 rate limit
RESUME         = True          # skip already-generated files
START_AT       = 1             # set higher to jump into the list (e.g. 23 to resume)

OUT_DIR = Path(r"C:\Users\j-pre\OneDrive\Documents\public_html\assets\production\exports\documentary")
SIZE    = "1792x1024"          # native 16:9 DALL-E 3 size
# ────────────────────────────────────────────────────────────────────


# ── Style appended to every prompt ───────────────────────────────────
BASE = (
    "cinematic documentary photography, dark moody atmosphere, "
    "shallow depth of field, teal LED accent lighting, near-black background, "
    "desaturated muted color grade with slightly lifted shadows, "
    "Sony A7S III 85mm f/1.4 lens, photorealistic, "
    "no text no labels no watermarks no bright studio lighting"
)

# ── Consistent subject descriptions ──────────────────────────────────
VGROW = (
    "VIVOSUN vGrow smart grow box, matte black vertical cabinet "
    "18 inches wide 48 inches tall, single front door with large rectangular "
    "viewing window, premium appliance aesthetic, faint teal LED seam glow at door edges"
)
APT = (
    "minimalist modern apartment, charcoal gray walls, "
    "dark herringbone wood floor, single large window with blurred night city view, "
    "considered furniture no clutter"
)


# ── All 62 image prompts ─────────────────────────────────────────────
IMAGES = [

    # ═══ ACT I — COMPLEXITY MONTAGE ════════════════════════════════
    {
        "num": 1, "slug": "nutrient-bottles",
        "prompt": (
            "row of 8 different cannabis nutrient bottles crowded on a dark shelf, "
            "different heights colors and labels, nutrient solution visible through glass, "
            "blurred grow tent visible in background bokeh, "
            f"{BASE}"
        ),
    },
    {
        "num": 2, "slug": "ph-pen-macro",
        "prompt": (
            "extreme macro close-up of pH meter electrode metal tip with single water "
            "droplet clinging to it, completely dark background, sharp droplet detail, "
            "dramatic single side light source, clinical and demanding, "
            f"{BASE}"
        ),
    },
    {
        "num": 3, "slug": "phone-alert-vpd",
        "prompt": (
            "smartphone screen at 2:47 AM in total darkness, grow monitoring app "
            "notification alert on lock screen, urgent red notification badge, "
            "phone screen glow the only light in dark bedroom, "
            f"{BASE}"
        ),
    },
    {
        "num": 4, "slug": "phone-alert-ph-drift",
        "prompt": (
            "smartphone lock screen at 2:47 AM with two stacked grow app push "
            "notifications about pH drift and reservoir check, dark room, "
            "phone screen glow only light source, interrupted sleep implied, "
            f"{BASE}"
        ),
    },
    {
        "num": 5, "slug": "grow-tent-rigged",
        "prompt": (
            "close-up of grow tent corner showing silver duct tape patching ducting, "
            "small clip fan zip-tied at an awkward angle, improvised DIY rigging, "
            "dark green canvas tent wall, visible wear, practical not designed, "
            f"{BASE}"
        ),
    },
    {
        "num": 6, "slug": "grow-journal",
        "prompt": (
            "hand-written grow journal notebook open, daily pH and EC readings logged "
            "with dates corrections and arrows, dense notes on graph paper, "
            "ballpoint pen resting on page, dim warm desk lamp light, dark background, "
            f"{BASE}"
        ),
    },
    {
        "num": 7, "slug": "tds-meter",
        "prompt": (
            "TDS PPM meter being dipped into hydroponic reservoir, digital display "
            "showing 847 ppm, hands partially visible, green tinted nutrient water "
            "surface with light reflections, macro close-up, "
            f"{BASE}"
        ),
    },
    {
        "num": 8, "slug": "grow-tent-chaos",
        "prompt": (
            "interior of traditional cannabis grow tent, cluttered improvised setup, "
            "multiple nutrient bottles on floor, ducting runs in all directions, "
            "extension cords timers and equipment everywhere, HPS or LED light above, "
            "the before picture, "
            f"{BASE}"
        ),
    },

    # ═══ ACT I — vGROW INTRODUCTION ════════════════════════════════
    {
        "num": 9, "slug": "vgrow-hero",
        "prompt": (
            f"{VGROW}, centered in completely dark minimalist room, "
            "single subtle overhead light from above, premium product photography "
            "lighting, isolated object portrait, faint teal glow at door seams, "
            f"{BASE}"
        ),
    },
    {
        "num": 10, "slug": "vgrow-night-glow",
        "prompt": (
            f"{VGROW} in completely dark apartment room at night, "
            "teal LED light seeping through door edges is the only light in frame, "
            "soft teal pool on floor below unit, dark walls barely visible, "
            "calm and autonomous, "
            f"{BASE}"
        ),
    },
    {
        "num": 11, "slug": "phone-canopy-nominal",
        "prompt": (
            "smartphone lock screen at 2:47 AM showing a single calm notification "
            "reading Canopy nominal all environmental parameters within target range, "
            "clean minimal notification design, teal blue color accent, "
            "dark room, peaceful contrast to earlier alerts, "
            f"{BASE}"
        ),
    },
    {
        "num": 12, "slug": "sleeping-vgrow-background",
        "prompt": (
            "person sleeping peacefully in bed, dark bedroom at night, "
            f"{VGROW} visible in soft focus background glowing faint teal, "
            "grower sleeping while system runs, 2AM, undisturbed rest, "
            "blurred foreground figure sharp background unit, "
            f"{BASE}"
        ),
    },

    # ═══ ACT II — THE IDEA ═════════════════════════════════════════
    {
        "num": 13, "slug": "vgrow-in-living-room",
        "prompt": (
            f"{VGROW} placed in clean minimalist living room, {APT}, "
            "the unit looks like designer furniture not growing equipment, "
            "evening ambient light, bookshelf visible, wide establishing shot, "
            f"{BASE}"
        ),
    },
    {
        "num": 14, "slug": "espresso-machine",
        "prompt": (
            "matte black precision espresso machine on dark stone kitchen counter, "
            "hand pouring freshly ground coffee beans into portafilter, "
            "close-up detail, moody kitchen lighting, premium domestic appliance, "
            f"{BASE}"
        ),
    },
    {
        "num": 15, "slug": "espresso-pour",
        "prompt": (
            "macro photography of rich dark espresso stream pouring into small ceramic "
            "cup with golden crema forming on top, dramatic side lighting, "
            "black background, the craft result, "
            f"{BASE}"
        ),
    },
    {
        "num": 16, "slug": "camera-darkroom-print",
        "prompt": (
            "modern mirrorless camera resting in hand on dark wood table, "
            "beside it an aged darkroom photograph print slightly yellowed, "
            "analog and digital side by side, single side light, "
            f"{BASE}"
        ),
    },
    {
        "num": 17, "slug": "vgrow-window-close",
        "prompt": (
            f"close-up of {VGROW} viewing window, rectangular dark tinted glass "
            "panel with faint teal LED magnetic seal glow at edges, "
            "plant silhouette barely visible inside, mysterious premium design detail, "
            f"{BASE}"
        ),
    },
    {
        "num": 18, "slug": "vgrow-door-portrait",
        "prompt": (
            f"{VGROW} front door full vertical view, dark matte black faux leather "
            "surface texture, large rectangular viewing window glowing faint teal, "
            "subtle handle on right side, dark background, "
            f"{BASE}"
        ),
    },
    {
        "num": 19, "slug": "roots-macro-dense",
        "prompt": (
            "extreme macro close-up of cannabis DWC hydroponic root mass day 32, "
            "dense pure white roots branching and filling entire frame, "
            "water droplets on roots, dark teal water visible beneath, "
            "almost architectural organic structure, clean healthy roots, "
            f"{BASE}"
        ),
    },
    {
        "num": 20, "slug": "roots-in-water",
        "prompt": (
            "cannabis DWC hydroponic roots viewed at water line from side angle, "
            "white roots visible below dark teal-tinted reservoir water surface, "
            "small air bubbles rising, macro photography, "
            f"{BASE}"
        ),
    },

    # ═══ ACT III — THE REVEAL ══════════════════════════════════════
    {
        "num": 21, "slug": "vgrow-texture-macro",
        "prompt": (
            "extreme macro of matte black faux leather surface texture, "
            "premium material grain detail, subtle crosshatch weave pattern visible, "
            "dramatic raking light from one side, luxury material close-up, "
            "no other context, "
            f"{BASE}"
        ),
    },
    {
        "num": 22, "slug": "vent-grille-macro",
        "prompt": (
            "macro close-up of precision aluminum ventilation grille, clean parallel "
            "slots cut into dark anodized metal, single directional light casting "
            "deep shadows into the slots, premium engineering detail, "
            f"{BASE}"
        ),
    },
    {
        "num": 23, "slug": "door-cracking-open",
        "prompt": (
            f"{VGROW} front door cracked open exactly one inch, brilliant white "
            "interior LED light blazing through the narrow gap, extreme contrast "
            "between matte black exterior and intense white interior glow, "
            "anticipation of the reveal, "
            f"{BASE}"
        ),
    },
    {
        "num": 24, "slug": "door-half-open",
        "prompt": (
            f"{VGROW} door open halfway showing interior, white highly reflective "
            "interior walls partially visible, Samsung LED grow light bar at top "
            "emitting bright warm white light, healthy green cannabis plant partially "
            "visible inside, door swung to right, dramatic light pour, "
            f"{BASE}"
        ),
    },
    {
        "num": 25, "slug": "interior-full-reveal",
        "prompt": (
            f"straight-on view directly inside open {VGROW}, white highly reflective "
            "mirror-like interior walls, Samsung LM301H LED grow light board at top "
            "emitting intense warm white full-spectrum light, healthy green cannabis "
            "plant centered in DWC hydroponic net cup, brilliant interior illumination, "
            "door fully open, "
            f"{BASE}"
        ),
    },
    {
        "num": 26, "slug": "samsung-led-macro",
        "prompt": (
            "macro close-up of Samsung LM301H EVO LED grow light board, "
            "individual warm white LED diode chips in grid array on white PCB, "
            "emitting intense full-spectrum light, technical precision beauty, "
            f"{BASE}"
        ),
    },
    {
        "num": 27, "slug": "app-vpd-screen",
        "prompt": (
            "smartphone displaying grow monitoring app, VPD reading 1.1 kPa large and "
            "prominent, smooth 24-hour chart line holding flat with no spikes, "
            "temperature 76F humidity 62% secondary metrics, teal UI accent color, "
            "phone held in hand against dark background, "
            f"{BASE}"
        ),
    },
    {
        "num": 28, "slug": "vpd-graph-close",
        "prompt": (
            "extreme close-up of smartphone screen showing VPD environmental chart, "
            "perfectly smooth flat line at 1.1 for 24 hours, zero variation, "
            "teal graph on dark app background, data visualization, "
            f"{BASE}"
        ),
    },
    {
        "num": 29, "slug": "living-room-full-wide",
        "prompt": (
            f"wide shot of {APT}, {VGROW} in left corner glowing teal, "
            "large window with blurred city lights on right, dark couch bookshelves, "
            "grow unit indistinguishable from designer furniture, domestic normalcy, "
            "the definitive it belongs here shot, "
            f"{BASE}"
        ),
    },
    {
        "num": 30, "slug": "person-reading-unit-bg",
        "prompt": (
            f"person sitting on dark couch reading book, {APT}, "
            f"{VGROW} glowing teal in background, person ignoring the unit, "
            "ordinary evening, domestic normalcy, medium wide, "
            f"{BASE}"
        ),
    },

    # ═══ ACT IV — THE EVIDENCE — GROWTH ARC ════════════════════════
    {
        "num": 31, "slug": "seedling-day01",
        "prompt": (
            "cannabis seedling in rockwool cube placed in DWC net cup, "
            "just germinated with tiny white root tip barely visible, "
            "white reflective grow box interior, LED light above, day 1, close-up, "
            f"{BASE}"
        ),
    },
    {
        "num": 32, "slug": "cotyledons-day03",
        "prompt": (
            "cannabis seedling cotyledons day 3, two small round seed leaves just "
            "emerged, slightly fuzzy surface, hydroponic DWC grow, "
            "white interior lighting from above, macro, tiny new plant, "
            f"{BASE}"
        ),
    },
    {
        "num": 33, "slug": "first-true-leaves-day07",
        "prompt": (
            "cannabis seedling day 7, first true serrated leaves emerging between "
            "cotyledons, pale healthy green, white grow box interior, warm LED, "
            "macro close-up, "
            f"{BASE}"
        ),
    },
    {
        "num": 34, "slug": "roots-water-day07",
        "prompt": (
            "cannabis DWC roots at day 7, small clean white root system just reaching "
            "reservoir water level, viewed from side, white roots against teal "
            "nutrient water below, early growth, "
            f"{BASE}"
        ),
    },
    {
        "num": 35, "slug": "canopy-topdown-day14",
        "prompt": (
            "cannabis plant day 14 vegetative stage, top-down bird's eye view, "
            "multiple leaf sets forming symmetrical canopy, deep green healthy leaves, "
            "no tip burn no yellowing, white grow box interior, viewed from directly above, "
            f"{BASE}"
        ),
    },
    {
        "num": 36, "slug": "root-mass-day14",
        "prompt": (
            "cannabis DWC root mass at day 14, dense white roots branching and "
            "spreading in reservoir, clean healthy white no discoloration, "
            "teal nutrient water, dramatic lighting on roots, "
            f"{BASE}"
        ),
    },
    {
        "num": 37, "slug": "one-top-off",
        "prompt": (
            "hand pouring water from measuring container into hydroponic DWC reservoir "
            "access port inside grow cabinet, close-up, single deliberate action, "
            "teal interior light, one top-off in two weeks, minimal intervention, "
            f"{BASE}"
        ),
    },
    {
        "num": 38, "slug": "roots-extreme-macro",
        "prompt": (
            "extreme macro cannabis DWC roots, individual root hairs and fine "
            "branching filaments in sharp focus, pure white healthy roots, "
            "water droplets, almost abstract organic texture, dark water background, "
            f"{BASE}"
        ),
    },
    {
        "num": 39, "slug": "plant-side-day28",
        "prompt": (
            "cannabis plant day 28 mid-vegetative, full bushy canopy, deep green "
            "healthy leaves, multiple nodes, even symmetrical growth, "
            "inside white reflective grow box, side angle showing height, "
            "DWC reservoir at base, "
            f"{BASE}"
        ),
    },
    {
        "num": 40, "slug": "leaf-macro-day28",
        "prompt": (
            "extreme macro cannabis leaf surface day 28, perfect deep green, "
            "sharp serrated edge, no tip burn no yellowing no claw, "
            "fine leaf texture and veins visible, healthy unstressed vegetative leaf, "
            f"{BASE}"
        ),
    },
    {
        "num": 41, "slug": "canopy-topdown-day28",
        "prompt": (
            "cannabis plant day 28 top-down view, lush even green canopy filling frame, "
            "perfect symmetrical growth, multiple developing bud sites forming, "
            "viewed directly from above inside grow cabinet, "
            f"{BASE}"
        ),
    },

    # ═══ FLOWER ARC ════════════════════════════════════════════════
    {
        "num": 42, "slug": "first-pistils-day35",
        "prompt": (
            "cannabis plant node showing first white pistils forming, "
            "transition to flower day 35, warm red-orange bloom LED spectrum, "
            "white hair-like pistils emerging at stem junction, macro close-up, "
            f"{BASE}"
        ),
    },
    {
        "num": 43, "slug": "interior-bloom-spectrum",
        "prompt": (
            f"inside open {VGROW}, LED running warm red bloom spectrum, "
            "pink-orange interior glow on reflective white walls, "
            "cannabis plant in early flower below, "
            "warm tones contrasting earlier white veg light, "
            f"{BASE}"
        ),
    },
    {
        "num": 44, "slug": "early-flower-week6",
        "prompt": (
            "cannabis plant week 6 early flower, multiple small bud sites forming "
            "along branches, white pistils extending, main cola beginning to swell, "
            "warm bloom spectrum light inside grow box, "
            f"{BASE}"
        ),
    },
    {
        "num": 45, "slug": "bud-site-macro-week6",
        "prompt": (
            "cannabis bud site close-up week 6, calyxes beginning to stack, "
            "white pistils extending outward, first fine trichomes appearing on "
            "sugar leaves, macro, warm bloom light, "
            f"{BASE}"
        ),
    },
    {
        "num": 46, "slug": "mid-flower-week7",
        "prompt": (
            "cannabis plant week 7 mid-flower, buds swelling on main cola and branches, "
            "pistils turning orange and amber at tips, trichomes visible to naked eye, "
            "inside grow cabinet bloom light, full mid-flower development, "
            f"{BASE}"
        ),
    },
    {
        "num": 47, "slug": "trichomes-week7",
        "prompt": (
            "cannabis trichomes extreme macro week 7, clear and milky white trichome "
            "heads on glandular stalks, bud surface, microscope-level macro, "
            "crystalline glandular structures, single trichomes in sharp focus, "
            f"{BASE}"
        ),
    },
    {
        "num": 48, "slug": "late-flower-week8",
        "prompt": (
            "cannabis plant week 8 late flower, dense mature buds on cola and branches, "
            "mostly orange amber pistils, heavy sugar leaf trichome frost, "
            "filling grow box interior nearly touching LED, harvest approaching, "
            f"{BASE}"
        ),
    },
    {
        "num": 49, "slug": "trichomes-harvest-ready",
        "prompt": (
            "cannabis trichomes harvest-ready macro, mix of milky white and amber "
            "trichome heads with some clear still visible, bud surface, "
            "peak harvest window, crystalline structures in sharp focus, "
            f"{BASE}"
        ),
    },
    {
        "num": 50, "slug": "final-cola",
        "prompt": (
            "cannabis main cola week 8 harvest ready, dense frosted mature buds, "
            "heavy trichome coverage giving crystalline frosty appearance, "
            "orange amber pistils, deep green possible purple hues, "
            "teal accent backlight, the 60-day payoff, "
            f"{BASE}"
        ),
    },

    # ═══ HARVEST ═══════════════════════════════════════════════════
    {
        "num": 51, "slug": "harvest-scissors",
        "prompt": (
            "sharp stainless steel pruning scissors at base of cannabis main stem, "
            "harvest moment, macro, teal interior light, deliberate precise position, "
            "contrast of dark scissors against vivid green stem, "
            f"{BASE}"
        ),
    },
    {
        "num": 52, "slug": "branch-in-led-light",
        "prompt": (
            "hand holding freshly harvested cannabis branch up against bright LED "
            "backlight, trichomes sparkling and catching the light, fresh cut, "
            "inside grow cabinet, warm white LED from behind, glistening resin, "
            f"{BASE}"
        ),
    },
    {
        "num": 53, "slug": "trim-tray-layout",
        "prompt": (
            "trim tray top-down view, freshly harvested cannabis buds laid out, "
            "multiple colas on stems, dark tray, teal and warm accent light "
            "catching trichomes, fresh harvest display, "
            f"{BASE}"
        ),
    },
    {
        "num": 54, "slug": "drying-rack",
        "prompt": (
            "cannabis branches hanging upside down on drying rack in dark room, "
            "silhouettes of drying buds faintly backlit by single teal light, "
            "3-4 days into dry, patience and process, dark moody atmosphere, "
            f"{BASE}"
        ),
    },
    {
        "num": 55, "slug": "curing-jars",
        "prompt": (
            "two wide-mouth glass mason jars filled with dried cannabis buds on dark "
            "surface, slight condensation on glass, buds clearly visible inside, "
            "curing process, single side light catching trichomes, "
            f"{BASE}"
        ),
    },
    {
        "num": 56, "slug": "jar-open",
        "prompt": (
            "open glass mason jar with cured cannabis buds, lid placed beside it, "
            "buds at top of jar, slight moisture shimmer, dark background, "
            "warm side light catching trichomes, the cure, "
            f"{BASE}"
        ),
    },
    {
        "num": 57, "slug": "final-bud-in-hand",
        "prompt": (
            "one perfect cured cannabis bud held between two fingers, "
            "backlit by teal light, trichomes sparkling, amber and orange pistils, "
            "heavy resin coverage, dark background, macro, "
            "the craft result, 60 days in one frame, "
            f"{BASE}"
        ),
    },

    # ═══ ACT V — THE MANIFESTO ═════════════════════════════════════
    {
        "num": 58, "slug": "vgrow-closed-fullcircle",
        "prompt": (
            f"{VGROW}, closed front view, dark minimalist room, "
            "teal LED seam glow at door edges, same composition as hero shot, "
            "full circle return, system running autonomously, nothing to do, "
            f"{BASE}"
        ),
    },
    {
        "num": 59, "slug": "espresso-callback",
        "prompt": (
            "matte black precision espresso machine close-up, same composition as "
            "Act II, the tool that enables craft not replaces it, moody kitchen, "
            f"{BASE}"
        ),
    },
    {
        "num": 60, "slug": "camera-callback",
        "prompt": (
            "modern mirrorless camera held in hand, callback composition, "
            "dark background, the craft tool in the craftsperson's hand, "
            f"{BASE}"
        ),
    },
    {
        "num": 61, "slug": "vgrow-closer-optional",
        "prompt": (
            f"{VGROW} slightly closer than hero shot, teal LED seam glow "
            "filling more of frame, dark surroundings, machine breathing quietly, "
            "minimal powerful presence, 'It's optional', "
            f"{BASE}"
        ),
    },
    {
        "num": 62, "slug": "vgrow-final-fade",
        "prompt": (
            f"{VGROW} in dark apartment at night, teal LED glow pooling on floor, "
            "system running quietly and autonomously, only light source in frame, "
            "peaceful final image, last frame before fade to black, "
            f"{BASE}"
        ),
    },
]


# ── Helpers ──────────────────────────────────────────────────────────
def get_api_key():
    if OPENAI_API_KEY:
        return OPENAI_API_KEY
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    key = input("\nOpenAI API key not found. Paste it here: ").strip()
    if not key:
        print("[ERROR] No API key provided. Exiting.")
        sys.exit(1)
    return key


def save_manifest(out_dir, results):
    """Save a JSON manifest of all generated images with prompts and filenames."""
    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n   Manifest saved: {manifest_path.name}")


# ── Main ─────────────────────────────────────────────────────────────
def main():
    from openai import OpenAI

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    api_key = get_api_key()
    client  = OpenAI(api_key=api_key)

    total   = len(IMAGES)
    cost_each = 0.08 if QUALITY == "standard" else 0.12
    to_run  = [img for img in IMAGES if img["num"] >= START_AT]

    if RESUME:
        to_run = [
            img for img in to_run
            if not (OUT_DIR / f"img-{img['num']:02d}-{img['slug']}.png").exists()
        ]

    print(f"\n{'='*58}")
    print(f"  ColaXpress Ep01 — DALL-E 3 Generator")
    print(f"{'='*58}")
    print(f"  Quality    : {QUALITY}  ({SIZE})")
    print(f"  Images     : {len(to_run)} of {total} to generate")
    print(f"  Est. cost  : ${len(to_run) * cost_each:.2f}")
    print(f"  Output     : {OUT_DIR}")
    print(f"  Delay      : {DELAY}s between calls")
    if RESUME:
        skipped = total - len(to_run)
        if skipped:
            print(f"  Resuming   : {skipped} already done, skipping")
    print(f"{'='*58}\n")

    if not to_run:
        print("Nothing to generate — all images already exist.\n")
        return

    print(f"Generate {len(to_run)} image(s) for ~${len(to_run)*cost_each:.2f}? [y/N]: y")
    # AUTO_CONFIRM — user approved this run

    results  = []
    failures = []

    for i, img in enumerate(to_run, 1):
        num    = img["num"]
        slug   = img["slug"]
        fname  = f"img-{num:02d}-{slug}.png"
        fpath  = OUT_DIR / fname
        prompt = img["prompt"]

        print(f"\n[{i}/{len(to_run)}] #{num:02d} {slug}")
        print(f"         {prompt[:90]}...")

        for attempt in range(1, 4):  # up to 3 tries
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=SIZE,
                    quality=QUALITY,
                    response_format="b64_json",
                    n=1,
                )
                img_bytes = base64.b64decode(response.data[0].b64_json)
                with open(fpath, "wb") as f:
                    f.write(img_bytes)

                kb = fpath.stat().st_size / 1024
                revised = response.data[0].revised_prompt or ""
                print(f"         Saved: {fname}  ({kb:.0f} KB)")

                results.append({
                    "num": num, "slug": slug, "file": fname,
                    "original_prompt": prompt,
                    "revised_prompt": revised,
                    "kb": round(kb, 1),
                })
                break

            except Exception as e:
                err = str(e)
                print(f"         [!] Attempt {attempt} failed: {err[:120]}")
                if attempt < 3:
                    print(f"         Retrying in 20s...")
                    time.sleep(20)
                else:
                    print(f"         [SKIPPED] #{num:02d} after 3 failures.")
                    failures.append({"num": num, "slug": slug, "error": err})

        # Rate limit buffer — wait between calls
        if i < len(to_run):
            time.sleep(DELAY)

    # Save manifest
    all_results = results + [{"num": f["num"], "slug": f["slug"], "file": None, "error": f["error"]} for f in failures]
    all_results.sort(key=lambda x: x["num"])
    save_manifest(OUT_DIR, all_results)

    # Final summary
    print(f"\n{'='*58}")
    print(f"  Done.  {len(results)} generated, {len(failures)} failed.")
    print(f"  Total spent: ~${len(results) * cost_each:.2f}")
    print(f"  Output: {OUT_DIR}")
    if failures:
        print(f"\n  Failed images (re-run with START_AT to retry):")
        for f in failures:
            print(f"    #{f['num']:02d} {f['slug']} — {f['error'][:80]}")
    print(f"{'='*58}\n")


if __name__ == "__main__":
    main()
