# Agent 05 — Content Authority

**Role:** Identify topical gaps, build semantic clusters, route internal link
equity to revenue pages.

**Inputs required:**
- Full sitemap of the new domain.
- GSC Performance export (queries + pages).
- A list of priority commercial keywords.
- Top 3-5 ranking competitor URLs per priority keyword.

---

## Checks

### A. Topical cluster map
For each priority topic, the site should have:
- **1 pillar page** — broad, high-volume keyword, 2000+ words, definitive.
- **5-12 supporting pages** — long-tail variants of the pillar topic.
- **Bidirectional internal links** between the pillar and every supporter.

Topics that almost every cannabis brand under-serves (rank-able white space):
- Strain education clusters (each strain = mini-pillar)
- Method-of-consumption guides (vape vs flower vs edible vs concentrate)
- Cannabis-and-condition educational content (anxiety, sleep, appetite)
- Local guides ("best places to enjoy cannabis in [neighborhood]")
- Cultivation / process content (asymmetric — sells the brand AND ranks)

### B. Keyword coverage gaps
For each priority keyword:
1. Run the query in Google. Note the top 10 URLs.
2. Compare: does cola-xpress.com have a page targeting it?
3. If yes, does it have parity in word count, depth, and entity coverage?
4. If no, add to the content backlog.

### C. Cannibalization
Multiple pages targeting the same keyword = self-competition.
- Run a site-search: `site:www.cola-xpress.com "[keyword]"` — should return
  one clearly-dominant page per query.
- Merge or canonicalize duplicates.

### D. Internal link equity routing
- Revenue pages (`/shop`, top product pages) should be linked from the
  homepage AND from every related blog post.
- Use descriptive anchor text — not "click here" or "learn more".
- Cap external outbound links per page; every outbound link is a small
  authority leak.

### E. Freshness signals
- Blog posts older than 12 months should be reviewed and updated, not deleted.
- "Last updated" dates visible to users and to Google.
- Update + republish > write new (for established pages).

---

## Scoring rubric (0-100)

| Dimension | Weight |
|---|---|
| Pillar/supporter cluster structure | 25 |
| Keyword coverage vs. competitors | 25 |
| No cannibalization | 15 |
| Internal link equity routing | 20 |
| Freshness | 15 |

---

## Output format

```
[CONTENT] severity=high
location: missing — no page targets "weed delivery [neighborhood]"
evidence: GSC shows 340 impressions/mo for variants of this query, no
          clicks; top 3 competitors have dedicated landing pages
fix: create /delivery/[neighborhood] landing page; link from homepage
     footer and from /about
impact: ~$X/month based on click value (state assumption)
effort: 3 hours per neighborhood landing page
```
