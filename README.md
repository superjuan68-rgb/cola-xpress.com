# cola-xpress.com — Site Audit & Migration Workspace

Working branch: `claude/site-audit-migration-IKDNa`

**Old canonical:** `https://colaxpress.cannahustle.nyc/`
**New canonical:** `https://www.cola-xpress.com/`

This repo is the operational memory for the migration + ongoing audit cycles.
It does NOT yet contain the production site code — once you push `public_html`
into this repo, the audit agents have something concrete to audit against.

---

## What's here

```
migration/
  apache/
    OLD-DOMAIN.htaccess         # drop on colaxpress.cannahustle.nyc
    NEW-DOMAIN.htaccess         # drop on www.cola-xpress.com (above WP block)
  nginx/
    OLD-DOMAIN.conf             # nginx alternative for old domain
    NEW-DOMAIN.conf             # nginx alternative for new domain
  templates/
    robots.txt                  # for new domain
    sitemap-images.xml          # image sitemap stub
    canonical-head-snippet.html # canonical + OG + schema head template
  url-mapping.csv               # source-of-truth for per-URL 301s (FILL THIS IN)
  google-search-console-checklist.md   # phased GSC migration runbook

agents/
  ORCHESTRATOR.md               # master prompt to run a full audit
  01-technical-seo.md
  02-image-seo-domination.md
  03-visual-ux.md
  04-customer-likeability.md
  05-content-authority.md
  06-competitor-intelligence.md
```

---

## Deploy order (do NOT reorder)

1. **Fill in `migration/url-mapping.csv`** with every old URL. Source the list
   from GSC export + Screaming Frog crawl.
2. **Push the new site live at `https://www.cola-xpress.com/`** with canonical
   tags, sitemap, robots.txt, and `migration/apache/NEW-DOMAIN.htaccess` (or
   the nginx equivalent) deployed.
3. **Verify** with `curl -I` that the new canonical resolves to 200 and that
   non-www / http variants 301 to the canonical.
4. **Deploy `migration/apache/OLD-DOMAIN.htaccess`** on the old hosting.
   Add per-URL overrides for any slugs that changed.
5. **Verify** redirects: pick 20 old URLs, `curl -I` each one, confirm 301 →
   correct new URL (no chains, no soft 404s).
6. **Search Console:** follow `migration/google-search-console-checklist.md`
   from Phase 0 onward.
7. **Run the orchestrator audit** (`agents/ORCHESTRATOR.md`) once the new site
   is stable, with rendered HTML + Screaming Frog crawl as inputs.

---

## What this repo does NOT do

- It does not auto-deploy. You (or your devops) deploy the configs.
- It does not auto-monitor GSC. Hook up the GSC API separately if you want
  scheduled monitoring — the SOPs describe what to monitor.
- It does not give Claude persistent memory across sessions. The repo IS the
  memory: commit findings to `audits/YYYY-MM-DD-<scope>.md` and feed them
  back in next session.

---

## Next concrete step

Push your `public_html` into this repo (on its own commit) so the audit
agents have real files to read. Once that's in, run:

```
# from this repo, on the audit branch
@agents/ORCHESTRATOR.md  with inputs from public_html/
```
