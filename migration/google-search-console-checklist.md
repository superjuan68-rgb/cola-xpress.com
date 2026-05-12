# Google Search Console — Migration Checklist

**Old canonical:** `https://colaxpress.cannahustle.nyc/`
**New canonical:** `https://www.cola-xpress.com/`

Do these IN ORDER. Skipping or reordering loses ranking equity.

---

## Phase 0 — Before you touch DNS or redirects

- [ ] **Crawl the old site** (Screaming Frog or `wget --mirror`) and export all indexed URLs to `migration/url-mapping.csv`.
- [ ] **Export GSC data from the old property:**
  - Performance → Pages → Export (last 16 months)
  - Pages → Indexed pages → Export
  - Sitemaps → note every submitted sitemap URL
  - Links → Top linking sites + Top linked pages → Export
  - Save all CSVs in `migration/exports/old-domain/` for the record.
- [ ] **Snapshot rankings** for your top 50 target keywords (Ahrefs, Semrush, or manual). You need a baseline to detect regression.

---

## Phase 1 — Deploy the new site at the new canonical

- [ ] New site live and crawlable at `https://www.cola-xpress.com/`.
- [ ] Every page has a self-referential `<link rel="canonical">` to its `https://www.cola-xpress.com/...` URL (see `templates/canonical-head-snippet.html`).
- [ ] `https://www.cola-xpress.com/sitemap.xml` exists and returns 200.
- [ ] `https://www.cola-xpress.com/sitemap-images.xml` exists and returns 200.
- [ ] `robots.txt` references both sitemaps (see `templates/robots.txt`).
- [ ] Internal links use the **new** canonical (no hardcoded `colaxpress.cannahustle.nyc` anywhere — `grep -r "cannahustle.nyc" public_html/` should return zero hits except in the old `.htaccess`).
- [ ] OpenGraph `og:url` and Twitter `twitter:url` point to the new domain.
- [ ] HTTPS valid, HSTS header set.
- [ ] Test 20 random redirects manually: `curl -I https://colaxpress.cannahustle.nyc/<path>` should return `301` with `Location: https://www.cola-xpress.com/<path>`.

---

## Phase 2 — Search Console setup

- [ ] **Add the NEW property** (Domain property, not URL prefix): `cola-xpress.com`
  - Verify via DNS TXT record (preferred — covers all subdomains + protocols).
- [ ] **Keep the OLD property verified** (`colaxpress.cannahustle.nyc`). Do NOT delete it. You need it active for Change of Address and for monitoring residual traffic.
- [ ] **Submit the new sitemap:** Search Console → Sitemaps → enter `sitemap.xml` and `sitemap-images.xml`.
- [ ] **In the OLD property:** Settings → Change of Address → select the new property → run the validation. Google will check that:
  - The old site 301s to the new site.
  - The new site is verified in your account.
  - Both properties are reachable.
- [ ] Once validation passes, **submit** the change of address.

---

## Phase 3 — Force recrawl

- [ ] **URL Inspection tool** on the new property, for each top 20 page:
  - Paste the new URL → Test live URL → Request indexing.
- [ ] **Submit the sitemap on the OLD property too** — temporarily — so Google sees the 301s faster. Remove after 30 days.
- [ ] **Internal links audit:** any link still pointing at `colaxpress.cannahustle.nyc` is forcing an extra 301 hop. Fix at the source.
- [ ] **Backlink outreach:** identify the top 20 external backlinks (from the GSC export in Phase 0) and request the link owners update to the new domain. 301s pass equity but direct links are stronger.

---

## Phase 4 — Monitor for 90 days

Check both properties every 3 days for the first 30 days, weekly after that.

- [ ] **Coverage / Pages report (new property):** indexed count should rise as old property's falls. Total indexed across both should stay flat or grow.
- [ ] **Coverage report (old property):** look for `Page with redirect` — this is the GOOD state. Watch for `Soft 404`, `Crawled - currently not indexed`, `Redirect error` — these are the bad states.
- [ ] **Performance report:** total clicks + impressions across both properties combined should stay flat or grow. A 10–20% temporary drop in the first 2–4 weeks is normal; a sustained 30%+ drop after week 6 means something is broken.
- [ ] **Core Web Vitals:** ensure the new domain isn't worse than the old (CDN, image formats, lazy loading).
- [ ] **Manual actions / Security issues:** check both properties weekly.

---

## Phase 5 — Long tail (6–12 months)

- [ ] Keep the OLD hosting + redirects live for **at least 12 months** (Google recommends minimum 180 days; 12 months is the safe number for full equity consolidation).
- [ ] After 12 months and once `colaxpress.cannahustle.nyc` shows zero impressions in GSC, you can decommission the old hosting — but **keep the DNS record + redirect rule** pointing to the new domain forever if possible.

---

## What "success" looks like

- New property indexed page count ≥ 95% of old property's peak indexed page count.
- Combined organic clicks within 5% of pre-migration baseline by day 60.
- Top 20 target keyword rankings within ±3 positions of pre-migration baseline by day 90.
- Zero `Redirect error` or `Soft 404` entries on the old property.
