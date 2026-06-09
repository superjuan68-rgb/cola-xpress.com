#!/usr/bin/env python3
"""
build.py  --  ColaXpress single-source-of-truth static builder (stdlib only).

Composes each page in src/pages/ with the shared chrome in src/_partials/ and the
site-wide data in src/_data/site.json, writing finished HTML to the output dir
(default: public_html/). Edit nav/footer/versions ONCE in site.json or a partial;
rebuild; every page updates.

  python build.py                 # build into public_html/
  python build.py --out /tmp/dist # build into a temp dir (for verification)
"""
import os, re, json, sys, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

def load(p): return open(p, encoding="utf-8").read()

SITE = json.load(open(os.path.join(SRC, "_data", "site.json"), encoding="utf-8"))
HEAD_T = load(os.path.join(SRC, "_partials", "head.html")).rstrip("\n")
HEADER_T = load(os.path.join(SRC, "_partials", "header.html")).rstrip("\n")
FOOTER_T = load(os.path.join(SRC, "_partials", "footer.html")).rstrip("\n")

def link_for(target, page_dir):
    tdir = os.path.dirname(target)
    if tdir == page_dir:
        return os.path.basename(target)
    return ("../" if page_dir else "") + target

def build_header(page_dir, active):
    logo = link_for("index.html", page_dir)
    desk, mob = [], []
    for it in SITE["nav"]:
        href = link_for(it["target"], page_dir)
        cls = ' class="active"' if it["label"] == active else ""
        desk.append(f'            <li><a href="{href}"{cls}>{it["label"]}</a></li>')
        mob.append(f'          <a href="{href}"{cls}>{it["label"]}</a>')
    return (HEADER_T.replace("{{LOGO_HREF}}", logo)
                    .replace("{{PRIMARY_NAV}}", "\n".join(desk))
                    .replace("{{MOBILE_NAV}}", "\n".join(mob)))

def build_footer(page_dir):
    logo = link_for("index.html", page_dir)
    links = [f'            <a href="{link_for(it["target"], page_dir)}">{it["label"]}</a>'
             for it in SITE["footer_links"]]
    return (FOOTER_T.replace("{{LOGO_HREF}}", logo)
                    .replace("{{BRAND_TAGLINE}}", SITE["brand_tagline"])
                    .replace("{{FOOTER_LINKS}}", "\n".join(links))
                    .replace("{{COPYRIGHT}}", SITE["copyright"])
                    .replace("{{DISCLAIMER}}", SITE["disclaimer"]))

def build_head(page_dir, head_content):
    prefix = "" if page_dir == "" else "../"
    return (HEAD_T.replace("{{PREFIX}}", prefix)
                  .replace("{{CSS_VER}}", SITE["css_ver"])
                  .replace("{{JS_VER}}", SITE["js_ver"])
                  .replace("{{HEAD_CONTENT}}", head_content))

SRCPAGE_RE = re.compile(
    r"<!--ACTIVE:(?P<active>[^>]*)-->\s*"
    r"<!--BEGIN-HEAD-->\n(?P<head>.*?)\n<!--END-HEAD-->\s*"
    r"<!--BEGIN-MAIN-->\n(?P<main>.*?)\n<!--END-MAIN-->", re.DOTALL)

def src_pages():
    base = os.path.join(SRC, "pages")
    for dp, _, files in os.walk(base):
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.relpath(os.path.join(dp, fn), base)

def compose(rel):
    txt = load(os.path.join(SRC, "pages", rel))
    m = SRCPAGE_RE.search(txt)
    if not m:
        raise ValueError(f"{rel}: source markers not found")
    active = m.group("active").strip()
    head_content = m.group("head")
    main_block = m.group("main")
    page_dir = os.path.dirname(rel) if rel != "index.html" else ""

    head_inner = build_head(page_dir, head_content)
    header = build_header(page_dir, active)
    footer = build_footer(page_dir)

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        f"{head_inner}\n"
        "  </head>\n"
        "  <body>\n"
        f"{header}\n"
        "\n"
        f"    {main_block}\n"
        "\n"
        f"{footer}\n"
        "  </body>\n"
        "</html>\n"
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "public_html"))
    args = ap.parse_args()
    n = 0
    for rel in sorted(src_pages()):
        html = compose(rel)
        dest = os.path.join(args.out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(html)
        n += 1
    print(f"Built {n} pages -> {args.out}")

if __name__ == "__main__":
    main()
