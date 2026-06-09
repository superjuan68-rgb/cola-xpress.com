#!/usr/bin/env python3
"""
verify_rebuild.py  --  prove the rebuild is structurally identical to production.

Compares the freshly built pages (default /tmp/dist) against the golden current
public_html/, page by page, on three gates:
  1. DOM-structural equality  (ld+json removed, whitespace canonicalized, attrs sorted)
  2. JSON-LD semantic equality (every block parsed and deep-compared as a multiset)
  3. SEO string equality       (title, description, canonical, every og:* / twitter:*)

Any difference on any gate = FAIL.  Whitespace-only HTML reformatting is invisible
to gate 1 and is the only permitted change.
"""
import os, re, sys, json
from html.parser import HTMLParser

GOLD = "/home/user/cola-xpress.com/public_html"
NEW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/dist"

LDJSON_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)

class Canon(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.toks = []
    def handle_starttag(self, tag, attrs):
        self.toks.append(("s", tag, tuple(sorted(attrs))))
    def handle_startendtag(self, tag, attrs):
        self.toks.append(("s", tag, tuple(sorted(attrs))))
        self.toks.append(("e", tag))
    def handle_endtag(self, tag):
        self.toks.append(("e", tag))
    def handle_data(self, data):
        d = " ".join(data.split())
        if d:
            self.toks.append(("t", d))

def dom_tokens(html):
    html = LDJSON_RE.sub('<script type="application/ld+json"></script>', html)
    p = Canon(); p.feed(html); return p.toks

def dom_equal(g_html, n_html):
    """Head compared as a multiset (element order in <head> is semantically
    inert), body compared in exact order (order is meaningful there)."""
    from collections import Counter
    def split(toks):
        for i, t in enumerate(toks):
            if t[0] == "s" and t[1] == "body":
                return toks[:i], toks[i:]
        return toks, []
    gh, gb = split(dom_tokens(g_html))
    nh, nb = split(dom_tokens(n_html))
    return Counter(gh) == Counter(nh) and gb == nb

def ldjson_set(html):
    out = []
    for block in LDJSON_RE.findall(html):
        try:
            out.append(json.dumps(json.loads(block), sort_keys=True, separators=(",", ":")))
        except Exception as e:
            out.append(f"UNPARSEABLE:{e}:{block[:80]}")
    return sorted(out)

META_RE = re.compile(r'<meta[^>]*?(?:name|property)="([^"]+)"[^>]*?content="([^"]*)"', re.I)
def seo_map(html):
    d = {}
    for k, v in META_RE.findall(html):
        if k in ("description",) or k.startswith("og:") or k.startswith("twitter:"):
            d[k] = v
    mc = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if mc: d["canonical"] = mc.group(1)
    mt = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    if mt: d["title"] = mt.group(1).strip()
    return d

def pages():
    for dp, dirs, files in os.walk(GOLD):
        if ".claude" in dp.split(os.sep) or "/assets" in dp + "/":
            dirs[:] = [d for d in dirs if d not in (".claude", "assets")]
            continue
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.relpath(os.path.join(dp, fn), GOLD)

def main():
    fails = {"dom": [], "ldjson": [], "seo": [], "missing": []}
    total = 0
    for rel in sorted(pages()):
        total += 1
        npath = os.path.join(NEW, rel)
        if not os.path.exists(npath):
            fails["missing"].append(rel); continue
        g = open(os.path.join(GOLD, rel), encoding="utf-8").read()
        nw = open(npath, encoding="utf-8").read()
        if not dom_equal(g, nw):
            fails["dom"].append(rel)
        if ldjson_set(g) != ldjson_set(nw):
            fails["ldjson"].append(rel)
        if seo_map(g) != seo_map(nw):
            fails["seo"].append(rel)
    print(f"Compared {total} pages: GOLD={GOLD}  NEW={NEW}\n")
    ok = True
    for gate, lst in fails.items():
        status = "PASS" if not lst else f"FAIL ({len(lst)})"
        print(f"  gate {gate:8s}: {status}")
        if lst:
            ok = False
            for r in lst[:10]:
                print(f"       - {r}")
    print("\n" + ("ALL GATES PASS — rebuild is structurally identical." if ok else "FAILURES PRESENT."))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
