#!/usr/bin/env python3
"""
seed_sitemap.py -- one-time: capture the current hand-built sitemap.xml into
src/_data/sitemap.json so the generator (build_sitemap.py) can preserve every
<lastmod> and <image:image> entry. Keyed by page relative path so it maps onto
src/pages. Phase 6A carries images forward verbatim; Phase 6B will discover them.
"""
import os, json, re
import xml.etree.ElementTree as ET

PUB = "/home/user/cola-xpress.com/public_html"
OUT = "/home/user/cola-xpress.com/src/_data/sitemap.json"
DOMAIN = "https://cola-xpress.com/"

SM = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
IM = "{http://www.google.com/schemas/sitemap-image/1.1}"

def rel_of(loc):
    assert loc.startswith(DOMAIN), loc
    path = loc[len(DOMAIN):]
    return path if path else "index.html"

def main():
    tree = ET.parse(os.path.join(PUB, "sitemap.xml"))
    root = tree.getroot()
    data = {}
    order = []
    dups = []
    for url in root.findall(f"{SM}url"):
        loc = url.findtext(f"{SM}loc").strip()
        rel = rel_of(loc)
        lastmod = (url.findtext(f"{SM}lastmod") or "").strip()
        imgs = [im.findtext(f"{IM}loc").strip()
                for im in url.findall(f"{IM}image") if im.findtext(f"{IM}loc")]
        if rel in data:
            dups.append((rel, loc))
            # same page, multiple <loc>: keep the most recent lastmod and the
            # richest image set so nothing is lost in the dedup.
            prev = data[rel]
            data[rel] = {
                "lastmod": max(prev["lastmod"], lastmod),
                "images": imgs if len(imgs) > len(prev["images"]) else prev["images"],
            }
            continue
        data[rel] = {"lastmod": lastmod, "images": imgs}
        order.append(rel)
    payload = {"order": order, "pages": data}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(payload, open(OUT, "w"), indent=2)
    total_imgs = sum(len(v["images"]) for v in data.values())
    print(f"Seeded {len(data)} unique URLs, {total_imgs} image entries -> {OUT}")
    if dups:
        print(f"\nDeduplicated {len(dups)} entry(ies) (same page, multiple <loc>):")
        for rel, loc in dups:
            print(f"  rel={rel}  dropped duplicate loc={loc}")

if __name__ == "__main__":
    main()
