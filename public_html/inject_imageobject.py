"""
ImageObject Schema Injector
============================
Adds @type:ImageObject structured data to every content page
that references images from assets/images/.

Injects a single consolidated ImageObject (or @graph list) block
AFTER the existing BreadcrumbList schema script on each page.
Skips pages that already have ImageObject schema.
Produces a QC report at the end.
"""

import os, re, json

BASE   = r'C:\Users\j-pre\OneDrive\Documents\public_html'
DOMAIN = 'https://cola-xpress.com'

SCAN_DIRS = ['', 'grow', 'learn', 'guides', 'equipment', 'watch']

# ── helpers ───────────────────────────────────────────────────────

def slug_to_name(slug):
    """Convert filename slug to a readable title."""
    name = slug.replace('-', ' ').replace('_', ' ')
    name = re.sub(r'\.(webp|png|jpg)$', '', name, flags=re.I)
    # Capitalize each word
    name = ' '.join(w.capitalize() for w in name.split())
    return name

def extract_images(html):
    """
    Return list of dicts with keys: src, alt, width, height.
    Only assets/images/ references.
    """
    pattern = re.compile(
        r'<img\s[^>]*src=["\']([^"\']*assets/images/[^"\']+)["\'][^>]*>',
        re.DOTALL | re.IGNORECASE
    )
    results = []
    for m in pattern.finditer(html):
        tag = m.group(0)
        src_full = m.group(1)
        # normalise to just the filename
        filename = src_full.split('assets/images/')[-1]

        alt_m   = re.search(r'alt=["\']([^"\']*)["\']', tag)
        width_m = re.search(r'width=["\'](\d+)["\']', tag)
        height_m= re.search(r'height=["\'](\d+)["\']', tag)

        results.append({
            'filename': filename,
            'alt':    alt_m.group(1)   if alt_m    else '',
            'width':  int(width_m.group(1))  if width_m  else 1200,
            'height': int(height_m.group(1)) if height_m else 630,
        })
    # deduplicate preserving order
    seen, unique = set(), []
    for r in results:
        if r['filename'] not in seen:
            seen.add(r['filename'])
            unique.append(r)
    return unique

def build_imageobject_block(page_url, images):
    """Build a JSON-LD script tag containing all ImageObjects for the page."""
    if len(images) == 1:
        img = images[0]
        obj = {
            "@context": "https://schema.org",
            "@type":    "ImageObject",
            "contentUrl": f"{DOMAIN}/assets/images/{img['filename']}",
            "name":        slug_to_name(img['filename']),
            "description": img['alt'],
            "url":         page_url,
            "width":       img['width'],
            "height":      img['height'],
        }
        payload = json.dumps(obj, indent=6, ensure_ascii=False)
    else:
        graph = []
        for img in images:
            graph.append({
                "@type":       "ImageObject",
                "contentUrl":  f"{DOMAIN}/assets/images/{img['filename']}",
                "name":        slug_to_name(img['filename']),
                "description": img['alt'],
                "url":         page_url,
                "width":       img['width'],
                "height":      img['height'],
            })
        obj = {
            "@context": "https://schema.org",
            "@graph":   graph,
        }
        payload = json.dumps(obj, indent=6, ensure_ascii=False)

    return f'    <script type="application/ld+json">\n      {payload}\n    </script>'

# ── anchor: inject after BreadcrumbList block ─────────────────────
# Pattern: end of last ld+json script before </head>
INJECT_ANCHOR = re.compile(
    r'(</script>)(\s*\n\s*</head>)',
    re.IGNORECASE
)

# ── main ──────────────────────────────────────────────────────────

updated   = []
skipped   = []
no_images = []

for d in SCAN_DIRS:
    folder = os.path.join(BASE, d) if d else BASE
    if not os.path.isdir(folder):
        continue
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith('.html'):
            continue
        rel  = (d + '/' + fname).lstrip('/')
        path = os.path.join(folder, fname)

        with open(path, encoding='utf-8') as f:
            html = f.read()

        # Skip if already has ImageObject
        if 'ImageObject' in html:
            skipped.append(rel)
            continue

        images = extract_images(html)
        if not images:
            no_images.append(rel)
            continue

        # Build page URL
        if rel == 'index.html':
            page_url = DOMAIN + '/'
        else:
            page_url = DOMAIN + '/' + rel
            # Normalize section index pages to directory form
            page_url = re.sub(r'/(grow|learn|guides|equipment|watch)/index\.html$', r'/\1/', page_url)

        schema_block = build_imageobject_block(page_url, images)

        # Find the LAST </script> before </head> and inject after it
        # Locate </head>
        head_close = html.lower().rfind('</head>')
        if head_close == -1:
            skipped.append(rel + ' [no </head>]')
            continue

        # Find last </script> before </head>
        last_script_end = html.rfind('</script>', 0, head_close)
        if last_script_end == -1:
            skipped.append(rel + ' [no </script> before </head>]')
            continue

        insert_pos = last_script_end + len('</script>')
        new_html = html[:insert_pos] + '\n' + schema_block + html[insert_pos:]

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        updated.append((rel, len(images)))

# ── QC report ─────────────────────────────────────────────────────
print('=' * 56)
print('ImageObject Schema Injection — QC Report')
print('=' * 56)
print(f'\nPages updated:       {len(updated)}')
print(f'Pages already done:  {len(skipped)}')
print(f'Pages no images:     {len(no_images)}')

print(f'\nUpdated ({len(updated)}):')
for rel, n in updated:
    print(f'  {rel}  ({n} image{"s" if n>1 else ""})')

if skipped:
    print(f'\nSkipped (already had schema or error):')
    for s in skipped:
        print(f'  {s}')

# Verify injection
errors = []
for rel, _ in updated:
    path = os.path.join(BASE, rel.replace('/', os.sep))
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'ImageObject' not in content:
        errors.append(rel)

print(f'\nVerification:')
if errors:
    for e in errors:
        print(f'  FAIL: {e}')
else:
    print(f'  All {len(updated)} pages verified — ImageObject schema present.')

print('\nDone.')
