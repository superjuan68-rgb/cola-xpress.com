#!/usr/bin/env python3
"""
build_sitemap.py -- Phase 6A. Generate public_html/sitemap.xml from src/pages.

  - page discovery:     one <url> per page under src/pages/
  - <loc>:              each page's own canonical URL (= canonical validation)
  - <lastmod>:          from the seed (src/_data/sitemap.json); new pages fall
                        back to the source file's git last-commit date, then today
  - <image:image>:      carried forward verbatim from the seed (Phase 6B will
                        replace this with real per-page image discovery)
  - validation:         every <loc> resolves to a built page AND equals its
                        page canonical; reports stale/missing. Fails loudly.

Run after build.py.   python3 build_sitemap.py
"""
import os, re, json, sys, subprocess, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PAGES = os.path.join(ROOT, "src", "pages")
SEED = json.load(open(os.path.join(ROOT, "src", "_data", "sitemap.json")))
OUT = os.path.join(ROOT, "public_html", "sitemap.xml")
DOMAIN = "https://cola-xpress.com/"

def discover():
    rels = []
    for dp, _, files in os.walk(SRC_PAGES):
        for fn in files:
            if fn.endswith(".html"):
                rels.append(os.path.relpath(os.path.join(dp, fn), SRC_PAGES))
    return set(rels)

def canonical_of(rel):
    txt = open(os.path.join(SRC_PAGES, rel), encoding="utf-8").read()
    m = re.search(r'<link rel="canonical" href="([^"]+)"', txt)
    if not m:
        raise ValueError(f"{rel}: no canonical tag")
    return m.group(1).strip()

def git_date(rel):
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", f"src/pages/{rel}"],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
        return out or datetime.date.today().isoformat()
    except Exception:
        return datetime.date.today().isoformat()

def main():
    pages = discover()
    seed_pages = SEED["pages"]
    seed_order = SEED["order"]

    # validation
    errors = []
    for rel in pages:
        loc = canonical_of(rel)
        expected = DOMAIN if rel == "index.html" else DOMAIN + rel
        if loc != expected:
            errors.append(f"{rel}: canonical {loc!r} != expected {expected!r}")
    stale = [r for r in seed_pages if r not in pages]
    if stale:
        errors.append(f"seed has entries with no page: {stale}")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  ", e)
        sys.exit(1)

    # order: seed order first (preserves current sitemap order), new pages appended
    ordered = [r for r in seed_order if r in pages] + sorted(pages - set(seed_order))

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for rel in ordered:
        loc = canonical_of(rel)
        info = seed_pages.get(rel, {})
        lastmod = info.get("lastmod") or git_date(rel)
        images = info.get("images", [])
        out.append("  <url>")
        out.append(f"    <loc>{loc}</loc>")
        out.append(f"    <lastmod>{lastmod}</lastmod>")
        for img in images:
            out.append("    <image:image>")
            out.append(f"      <image:loc>{img}</image:loc>")
            out.append("    </image:image>")
        out.append("  </url>")
    out.append("</urlset>")
    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    total_imgs = sum(len(seed_pages.get(r, {}).get("images", [])) for r in ordered)
    print(f"Wrote {OUT}: {len(ordered)} urls, {total_imgs} image entries")

if __name__ == "__main__":
    main()
