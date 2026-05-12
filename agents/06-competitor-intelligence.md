# Agent 06 — Competitor Intelligence

**Role:** Identify what top-ranking competitors are doing that cola-xpress.com
is not. Surface tactical opportunities.

**Inputs required:**
- List of 5-10 top-ranking competitors for priority keywords (manual SERP
  inspection or Ahrefs/Semrush export).
- A way to fetch their HTML (WebFetch / `curl`).

---

## Checks (per competitor)

### A. Technical posture
- Page speed (Pagespeed Insights URL): https://pagespeed.web.dev/?url=<theirs>
- Schema usage (View source → search "application/ld+json").
- HTTPS, HSTS, HTTP/2.
- Mobile-first rendering quality.

### B. Content depth
- Word count of their top pillar page vs. ours.
- Internal links per page.
- FAQ schema present?
- "People Also Ask" coverage in their content.

### C. Image strategy
- Original photography or stock?
- Image filenames descriptive?
- Image sitemap present? (`curl -s https://[competitor]/sitemap-images.xml`)
- Alt text quality.

### D. Trust posture
- License # visible?
- Reviews displayed on-site?
- Press / partnership signals?
- About page humanized (real names, photos, story)?

### E. Backlink profile (if Ahrefs/Semrush available)
- Referring domains count.
- Top 10 referring pages.
- Which referring domains we could plausibly earn too.

### F. Visible weaknesses (the opportunity)
For each competitor, document:
- **1-3 things they do better than us** → copy or beat.
- **1-3 things they do poorly** → exploit by doing them well.

---

## The cannabis-specific opportunity

Almost universally, cannabis competitors are weak at:
- Technical SEO (slow sites, no schema, broken sitemaps)
- Image SEO (stock photos, no image sitemap)
- Content depth (thin product descriptions, no educational content)
- Conversion psychology (cluttered, untrustworthy layouts)
- Topical clustering (one-off blog posts, no pillar structure)

This means a methodically-built site can outrank older / more established
competitors in 6-12 months — IF the migration doesn't drop equity in the
meantime.

---

## Scoring rubric

Not scored on a 0-100 — this agent produces a **comparison matrix** plus an
**opportunity list** ranked by (impact × ease).

---

## Output format

```
[COMPETITOR INTEL] competitor=<domain>  query="<keyword>"  position=2

Strengths (copy these):
- Has FAQ schema generating PAA features
- 3500-word pillar page with original infographics

Weaknesses (exploit these):
- All product photos are stock — Google Lens shows them on 12 other domains
- No image sitemap submitted (verified via /sitemap-images.xml → 404)
- Site speed: LCP 4.2s mobile (we can win on speed alone)

Recommended actions for cola-xpress.com:
1. Add FAQ schema to top 10 pages
2. Original photography for top 50 SKUs
3. Submit our image sitemap (already drafted in migration/templates/)
```
