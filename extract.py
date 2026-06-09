#!/usr/bin/env python3
"""
extract.py  --  Phase 4 one-time migration.
Carves every current public_html/*.html page into a source file under src/pages/
that contains ONLY the per-page parts (verbatim head SEO/JSON-LD + verbatim <main>
+ the active nav label). Shared chrome (head boilerplate, header, footer) is owned
by src/_partials and src/_data/site.json. Re-running build.py must reproduce the
current site (proven by verify_rebuild.py).

Deny-list principle: only the lines proven identical across all 51 pages are
treated as boilerplate and dropped. Anything unrecognized in <head> is preserved
verbatim, so no SEO/JSON-LD can ever be silently lost.
"""
import os, re, json, sys

PUB = "/home/user/cola-xpress.com/public_html"
SRC = "/home/user/cola-xpress.com/src"

# --- shared head boilerplate (prefix-stripped, whitespace-stripped canonical) ---
BP_EXACT = {
 '<meta charset="utf-8" />',
 '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
 '<link rel="icon" href="favicon.ico" />',
 '<link rel="icon" type="image/svg+xml" href="favicon.svg" />',
 '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png" />',
 '<link rel="icon" type="image/png" sizes="48x48" href="favicon-48.png" />',
 '<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png" />',
 '<link rel="manifest" href="site.webmanifest" />',
 '<meta name="theme-color" content="#151515" />',
 '<meta property="og:site_name" content="ColaXpress" />',
 '<link rel="preconnect" href="https://fonts.googleapis.com" />',
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />',
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />',
}
BP_REGEX = [
 re.compile(r'^<link rel="stylesheet" href="style\.css\?v=\d+" />$'),
 re.compile(r'^<script defer src="script\.js\?v=\d+"></script>$'),
]

def is_boilerplate(line):
    s = line.strip().replace("../", "")
    if s in BP_EXACT:
        return True
    return any(r.match(s) for r in BP_REGEX)

def pages():
    for dp, dirs, files in os.walk(PUB):
        if ".claude" in dp.split(os.sep) or "/assets" in dp + "/":
            dirs[:] = [d for d in dirs if d not in (".claude", "assets")]
            continue
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.relpath(os.path.join(dp, fn), PUB)

def extract_head_content(head_inner):
    """Return per-page head content verbatim, with boilerplate lines removed and
    JSON-LD blocks preserved as opaque units."""
    # protect multiline ld+json blocks
    blocks = []
    def stash(m):
        blocks.append(m.group(0))
        return f"\x00LD{len(blocks)-1}\x00"
    protected = re.sub(r'<script type="application/ld\+json">.*?</script>',
                       stash, head_inner, flags=re.DOTALL)
    out = []
    for line in protected.splitlines():
        if "\x00LD" in line:
            # restore the ld+json block verbatim (it's its own line/region)
            def unstash(m): return blocks[int(m.group(1))]
            out.append(re.sub(r'\x00LD(\d+)\x00', unstash, line))
            continue
        if not line.strip():
            continue
        if is_boilerplate(line):
            continue
        out.append(line)
    return "\n".join(out)

def main():
    errors = []
    n = 0
    for rel in sorted(pages()):
        fp = os.path.join(PUB, rel)
        t = open(fp, encoding="utf-8").read()

        m_head = re.search(r"<head>(.*?)</head>", t, re.DOTALL)
        m_header = re.search(r"<header>.*?</header>", t, re.DOTALL)
        m_main = re.search(r"<main>.*?</main>", t, re.DOTALL)
        m_footer = re.search(r"<footer>.*?</footer>", t, re.DOTALL)
        if not all([m_head, m_header, m_main, m_footer]):
            errors.append(f"{rel}: missing one of head/header/main/footer"); continue

        # nothing meaningful must live between header/main/footer except whitespace
        between1 = t[m_header.end():m_main.start()].strip()
        between2 = t[m_main.end():m_footer.start()].strip()
        if between1 or between2:
            errors.append(f"{rel}: unexpected content between chrome and main "
                          f"(b1={between1[:40]!r} b2={between2[:40]!r})"); continue

        # active nav label (verbatim from current header)
        am = re.search(r'class="active"[^>]*>([^<]+)</a>', m_header.group(0))
        active = am.group(1).strip() if am else ""

        head_content = extract_head_content(m_head.group(1))
        main_block = m_main.group(0)

        # blog page wraps the embed in a div, not <main>; capture the real main-ish
        # region: everything from the first <main or <div class="container blog-embed
        # Actually main is always <main>..</main>; the blog embed lives INSIDE <main>.

        out = (f"<!--ACTIVE:{active}-->\n"
               f"<!--BEGIN-HEAD-->\n{head_content}\n<!--END-HEAD-->\n"
               f"<!--BEGIN-MAIN-->\n{main_block}\n<!--END-MAIN-->\n")
        dest = os.path.join(SRC, "pages", rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(out)
        n += 1

    print(f"Extracted {n} pages -> {SRC}/pages")
    if errors:
        print(f"\n!!! {len(errors)} ERRORS:")
        for e in errors:
            print("  ", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
