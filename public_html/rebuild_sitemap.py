import os, re

base   = r'C:\Users\j-pre\OneDrive\Documents\public_html'
domain = 'https://cola-xpress.com'

# ── 1. Ground-truth page -> images from HTML ─────────────────────
scan_dirs = ['', 'grow', 'learn', 'guides', 'equipment', 'watch']
page_images = {}
for d in scan_dirs:
    folder = os.path.join(base, d) if d else base
    if not os.path.isdir(folder):
        continue
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(folder, fname)
        with open(fpath, encoding='utf-8') as f:
            html = f.read()
        imgs = sorted(set(re.findall(r'assets/images/([a-zA-Z0-9_./-]+\.(?:webp|png))', html)))
        rel = (d + '/' + fname).lstrip('/')
        page_images[rel] = imgs

# ── 2. Lastmod map from old sitemap ──────────────────────────────
with open(os.path.join(base, 'sitemap.xml'), encoding='utf-8') as f:
    old = f.read()

lastmods = {}
# Parse each <url> block individually to avoid multi-value unpacking
url_blocks = re.findall(r'<url>(.*?)</url>', old, re.DOTALL)
for block in url_blocks:
    loc_m = re.search(r'<loc>(.*?)</loc>', block)
    mod_m = re.search(r'<lastmod>(.*?)</lastmod>', block)
    if loc_m and mod_m:
        rel = loc_m.group(1).replace(domain, '').lstrip('/')
        lastmods[rel] = mod_m.group(1).strip()

# ── 3. Build ordered URL list (preserve sitemap order) ───────────
ordered_urls = []
for block in url_blocks:
    loc_m = re.search(r'<loc>(.*?)</loc>', block)
    if loc_m:
        rel = loc_m.group(1).replace(domain, '').lstrip('/')
        if rel not in ordered_urls:
            ordered_urls.append(rel)

# Add any scanned pages not already present
for rel in page_images:
    if rel not in ordered_urls:
        ordered_urls.append(rel)

# ── 4. Extra pages (in sitemap, no images, not scanned) ──────────
extra_lastmod = {
    'grow/beginner-mistakes-small-space-grows.html': '2026-04-21',
    'grow/vpd-chart-cannabis.html':                  '2026-05-10',
    'guides/about.html':   '2026-05-06',
    'guides/contact.html': '2026-05-06',
    'guides/faq.html':     '2026-04-21',
    'guides/search.html':  '2026-05-06',
}

# ── 5. Generate sitemap XML ───────────────────────────────────────
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
]

for rel in ordered_urls:
    url  = domain + '/' + rel if rel else domain + '/'
    url  = url.replace('//', '/').replace('https:/', 'https://')
    date = lastmods.get(rel) or extra_lastmod.get(rel, '2026-05-10')
    imgs = page_images.get(rel, [])

    lines.append('  <url>')
    lines.append(f'    <loc>{url}</loc>')
    lines.append(f'    <lastmod>{date}</lastmod>')
    for img in imgs:
        img_url = f'{domain}/assets/images/{img}'
        lines.append('    <image:image>')
        lines.append(f'      <image:loc>{img_url}</image:loc>')
        lines.append('    </image:image>')
    lines.append('  </url>')

lines.append('</urlset>')
out = '\n'.join(lines) + '\n'

with open(os.path.join(base, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(out)

# ── 6. QC report ─────────────────────────────────────────────────
total_img_entries = out.count('<image:loc>')
total_urls = len(url_blocks)

print(f'Sitemap rebuilt successfully.')
print(f'  URLs:              {total_urls}')
print(f'  Image entries:     {total_img_entries}')

img_dir = os.path.join(base, 'assets', 'images')
all_disk = set(f for f in os.listdir(img_dir) if f.endswith(('.webp', '.png')))
in_sitemap = set(re.findall(r'assets/images/([^<\n]+\.(?:webp|png))', out))
missing = all_disk - in_sitemap

print(f'  On-disk images:    {len(all_disk)}')
print(f'  In sitemap:        {len(in_sitemap)}')
print(f'  Missing from sitemap: {len(missing)}')
if missing:
    for m in sorted(missing):
        print(f'    MISSING: {m}')
else:
    print('  Coverage: 100% -- all images indexed.')
