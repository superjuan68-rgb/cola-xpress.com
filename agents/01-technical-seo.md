# Agent 01 — Technical SEO

**Role:** Find every technical reason Google is not ranking, indexing, or
crawling pages correctly. Verify the 301 migration is intact.

**Inputs required:**
- Screaming Frog crawl of the new domain (or `wget --mirror` output)
- `migration/url-mapping.csv` filled in
- GSC Coverage report export (both old and new property)
- The deployed `.htaccess` or `nginx.conf` from production
- A list of the top 20 pages by traffic

---

## Checks

### A. Migration integrity (run first, blocks everything else)
1. For each row in `url-mapping.csv`:
   `curl -sI -o /dev/null -w "%{http_code} %{redirect_url}\n" "https://colaxpress.cannahustle.nyc{old_path}"`
   Expect: `301 https://www.cola-xpress.com{new_path}`
2. No redirect chains (max one 301 hop). Test with `curl -sILo /dev/null`.
3. New canonical resolves: `https://www.cola-xpress.com/{path}` returns 200.
4. `www` and `non-www` of NEW domain: non-www must 301 to www.
5. HTTP must 301 to HTTPS on both domains.

### B. Indexability
1. `<meta name="robots">` and `X-Robots-Tag` header on every important page.
2. `robots.txt` does not block CSS/JS/image directories.
3. `noindex` is absent from pages that should rank.
4. Canonical tag matches the request URL (no cross-canonical loops).
5. `hreflang` only if multi-locale (likely N/A here).

### C. Crawlability
1. Internal links use the new domain exclusively.
2. No links to 404, 410, or 5xx.
3. XML sitemap submitted, valid, ≤50k URLs / ≤50MB per file.
4. `lastmod` in sitemap is accurate.
5. Pagination: `?page=2` is reachable from page 1 (no JS-only pagination).

### D. Structured data
1. Organization schema on homepage — validates in Rich Results Test.
2. Product / LocalBusiness / Article schema where applicable.
3. Breadcrumb schema on deep pages.
4. No schema errors in GSC `Enhancements`.

### E. Core Web Vitals
1. LCP <2.5s on top 10 pages (mobile, 4G throttle).
2. CLS <0.1.
3. INP <200ms.
4. TTFB <600ms.

### F. Server hygiene
1. HSTS header present with `max-age >= 15552000`.
2. HTTPS cert valid for ≥30 days.
3. `Content-Encoding: gzip` or `br` for HTML.
4. HTTP/2 or HTTP/3 enabled.

---

## Scoring rubric (0-100)

Start at 100. Subtract:
- 20 per failing check in section A (migration is critical)
- 5 per failing check in sections B, C
- 3 per failing check in sections D, E
- 1 per failing check in section F

---

## Output format

```
[TECHNICAL SEO] severity=blocker
location: https://colaxpress.cannahustle.nyc/shop
evidence: curl returns 200 (not 301) — redirect not deployed
fix: add per-path override OR confirm OLD-DOMAIN.htaccess deployed
impact: shop page indexes on both domains, splitting equity
effort: 5 min
```
