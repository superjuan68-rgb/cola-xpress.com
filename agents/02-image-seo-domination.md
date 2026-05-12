# Agent 02 — Image SEO Domination

**Role:** Engineer the site to dominate Google Image Search for cannabis
queries. Most cannabis competitors are weak here; this is the asymmetric
opportunity.

**Inputs required:**
- Full image inventory: `find public_html -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.webp" -o -iname "*.avif" \) > images.txt`
- Rendered HTML of top 20 pages (for `<img>` tag analysis)
- `migration/templates/sitemap-images.xml`

---

## The six pillars

### 1. Filename strategy
- BAD: `IMG_4930.jpg`, `pasted-image-2.png`, `wp-image-1234.jpg`
- GOOD: `cannabis-grow-room-led-lighting.jpg`, `gelato-41-flower-macro.webp`
- Hyphens, not underscores. Lowercase. <60 chars. Match the page topic.
- **Check:** `awk -F/ '{print $NF}' images.txt | grep -E "^(IMG_|DSC|pasted-|wp-image-)"`
  → any hits = rename needed.

### 2. Alt text quality
- Descriptive, not stuffed.
- BAD: `cannabis weed marijuana cola xpress delivery NYC`
- GOOD: `Indoor cannabis flower drying on stainless racks at the Cola Xpress cultivation room`
- Empty alt (`alt=""`) is acceptable ONLY for decorative images.
- Every product photo must have alt that mentions the strain/product name.
- **Check:** grep all `<img>` tags from rendered HTML; flag any with missing or duplicate alt.

### 3. Topical clustering
Single ranking images are weak. Image **ecosystems** rank.
- For each priority topic, build a cluster: 1 pillar article + 6-10 supporting
  articles + 15-30 original images cross-referenced across the cluster.
- Images on a page must support that page's primary topic.
- Internal-link from each cluster page to every other cluster page.

### 4. Compression + dimensions
- Serve `webp` or `avif` first, with `<picture>` fallback to `jpg`.
- Compress to <100 KB for above-the-fold images, <50 KB elsewhere.
- Width attribute matches actual rendered width (no 4000px images displayed at 600px).
- **Check:** `identify -format "%w %h %b %f\n" *.jpg` → flag any >200 KB.

### 5. Image sitemap (CRITICAL — most cannabis sites have none)
- See `migration/templates/sitemap-images.xml`.
- One `<url>` block per page; nested `<image:image>` per image on that page.
- Submit in GSC alongside the regular sitemap.

### 6. Reverse-image uniqueness
- Stock photos lose. Original branded visuals win.
- For each top 20 image: paste into Google Lens → if it appears on other
  domains, replace with an original.
- Watermark subtly (bottom corner, low opacity) — proves provenance without
  hurting crops.

---

## The asymmetric opportunity (do NOT skip)

Cannabis competitors almost universally fail at:
- Original educational diagrams (e.g. plant anatomy, trichome stages, drying curves).
- Macro photography of strains and products.
- Step-by-step process photography (cultivation, curing, lab testing).
- Infographics with branded styling and the domain visible in the image.

Build a library of these. Each is a backlink magnet and a Google Images entry point.

---

## Scoring rubric (0-100)

| Pillar | Weight |
|---|---|
| Filenames descriptive | 15 |
| Alt text quality | 15 |
| Topical clustering | 20 |
| Compression + dimensions | 15 |
| Image sitemap deployed + submitted | 15 |
| Original (non-stock) imagery | 20 |

---

## Output format

```
[IMAGE SEO] severity=high
location: /shop/product/gelato-41 — image #3
evidence: filename "IMG_4930.jpg", alt="" , 1.2 MB png at 4032x3024
fix: rename to "gelato-41-cannabis-flower-macro.webp", compress to <80KB,
     add descriptive alt; reference in sitemap-images.xml
impact: page currently invisible in Google Images for "gelato 41 flower"
effort: 10 min per product photo
```
