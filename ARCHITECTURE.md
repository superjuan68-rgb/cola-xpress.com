# ColaXpress — Site Architecture & Component Inventory

> **Status:** Architecture Freeze proposal (v1, 2026-06-07).
> **Purpose:** One source of truth for navigation, information architecture,
> components, SEO patterns, and design tokens. Every page inherits from this.
> Nothing in `public_html/` should deviate from this document without updating
> it first.

This file is internal (it lives at the repo root, outside `public_html/`, so it
is never served or indexed).

---

## 1. Why this document exists

The site is **51 hand-authored static HTML pages with no build step**. There is
no shared layer for the header, nav, or footer — each page carries its own copy.
That is the single structural weakness behind every "Frankenstein" symptom.

Concrete proof, measured 2026-06-07:

| Layer | Measured state | Verdict |
|---|---|---|
| Build system / templating | None. 51 standalone documents. | **Root cause** |
| Primary navigation | Was **5 orderings** → unified → reduced to the **lean 6-item nav** on 2026-06-07. | Fixed, but still duplicated in 51 files |
| Footer | Was **29 distinct variants**; unified to 1 canonical footer on 2026-06-07 (Phase 1). | Fixed |
| `script.js` cache version | 47 pages on `?v=10`, 4 on `?v=11` | Drift → stale-cache risk |
| `style.css` cache version | Uniform `?v=14` | Healthy |
| Taxonomy (Learn vs Guides) | 10 of 14 `/learn/` articles mark **Guides** active; 4 mark **Learn** | IA confusion |
| SEO meta (canonical/OG/Twitter/JSON-LD) | 51/51 complete | **Strength — do not disturb** |
| Design tokens / CSS | 1 stylesheet, consistent component classes; inline `style=` on only 9 pages | Mostly healthy |

**Takeaway:** This is *not* a redesign problem. The visual design system is in
good shape. The problem is the absence of a **single source of truth for shared
chrome**. Adding one nav item required editing 51 files — that is the symptom to
eliminate.

---

## 2. Frozen Primary Navigation

**Shipped & frozen (6 items, ratified + applied 2026-06-07):**

```
Home · Grow System · Equipment · Learn · Blog · About
```

Guides, Watch, FAQ, Search, and Contact were demoted out of the primary nav and
now live only in the canonical footer. This list is **frozen**. New sections do
not get bolted into the nav ad hoc — they require a deliberate edit to this
document first.

---

## 3. Information Architecture (target)

```
Home
├─ Grow System            (money)
├─ Equipment              (money)
├─ Learn                  (authority hub)
│   ├─ Craft cannabis
│   ├─ Harvest & trichomes
│   ├─ Drying
│   ├─ Curing
│   └─ Light cycles / troubleshooting
├─ Blog                   (authority — Soro-embedded feed)
├─ Watch                  (authority — video)
└─ Trust
    ├─ About
    ├─ Contact
    ├─ FAQ
    └─ Legal (NY home-grow law, landlord rules)
```

### Taxonomy fix needed: "Learn" vs "Guides"

Today both exist and overlap. `/guides/` holds About, Contact, FAQ, Search, the
index, **plus** two legal articles. `/learn/` holds 14 educational articles —
but 10 of them light up **Guides** in the nav, not Learn. Pick one owner for
educational content (recommended: **Learn** is the authority hub; **Guides**
becomes Trust/utility only) and make the active-state match the URL.

---

## 4. Content Hierarchy

| Tier | Pages | Goal | SEO posture |
|---|---|---|---|
| **Money** | Home, Grow System, Equipment | Convert / affiliate | High-intent keywords, internal links inbound |
| **Authority** | Learn (+ articles), Blog, Watch | Rank, build trust, feed Money pages | Topic clusters, dense internal linking |
| **Trust** | About, Contact, FAQ, Legal | Credibility, compliance | Low competition, schema (Org, FAQ) |

Internal-link rule: Authority pages link **down to** Money pages; Money pages
link **across** to supporting Authority pages. Trust pages link to everything.

---

## 5. Component Inventory

These are the reusable blocks. Today they are copy-pasted; the goal (§6) is to
source each from **one** template. Reference implementations are the hub pages
(`learn/index.html`, `grow/index.html`).

| Component | Markup anchor | Notes / canonical source |
|---|---|---|
| **Head / SEO block** | `<head>` | canonical, OG, Twitter, favicons, manifest, JSON-LD. 51/51 consistent — codify, don't change. |
| **Header + desktop nav** | `<nav aria-label="Primary navigation">` | Unified 2026-06-07. 10 items. |
| **Mobile nav** | `<div class="nav-mobile">` | Must mirror desktop nav exactly. |
| **Footer** | `<footer>` | ⚠️ **29 variants — needs a single canonical footer.** |
| **Hero** | `.page-hero` / `.page-hero-card` | 50 uses (~1/page). Stable. |
| **Card** | `.card`, `.surface-card` | Primary content unit. Many modifiers: `card-eyebrow`, `card-title`, `card-desc`, `card-status`, `card-type`, `card-spec`. |
| **Grids** | `.guide-grid`, `.card-grid`, `.split-grid` | Layout containers. |
| **Summary strip** | `.summary-strip` / `.summary-pill` | Intro pill row. |
| **Buttons** | `.btn` (×30), `.btn-secondary` (×3) | Only 2 variants — keep it that way. |
| **CTA** | `.hero-actions`, `.cta-good` | Call-to-action clusters. |
| **Related reading** | `.related-reading` / `.related-links` | Internal-link block at page foot. |

### Design tokens (source of truth = `public_html/style.css`, `?v=14`)
- **Typography:** Cormorant Garamond (display) + Manrope (body), loaded from
  Google Fonts with `preconnect`.
- **Theme color:** `#151515`.
- **Spacing / widths:** `.container` controls section width; do not hand-roll
  inline widths. (9 pages currently carry inline `style=` — migrate into CSS.)

---

## 6. The structural fix: one source of truth for shared chrome

The header, nav, footer, and `<head>` SEO block must come from **one place** so a
change propagates without touching 51 files. Options, cheapest first:

1. **Static build step (recommended).** A tiny Node/Eleventy (or even a 50-line
   Python) generator: author pages as content + a shared layout/partial set,
   build to `public_html/`. No runtime dependency, output stays pure static.
   - Pros: real templating, partials (`_header`, `_footer`, `_head`), data-driven
     nav, automatic sitemap. Industry-standard.
   - Cons: introduces a build/deploy step (one-time setup).
2. **HTML includes via a generator script we already control.** Extend the
   ad-hoc Python approach (like the nav-normalizer used 2026-06-07) into a
   maintained `build.py` that injects partials from `/_partials/`.
   - Pros: minimal tooling, no new framework.
   - Cons: home-grown; less standard than Eleventy.
3. **Server-Side Includes (SSI) / edge includes.** If the host supports SSI
   (`<!--#include -->`).
   - Pros: no build step.
   - Cons: host-dependent; fragile across migrations; not great for SEO tooling.

**Recommendation:** Option 1 (Eleventy) or Option 2 if we want to stay
dependency-free. Either way, after migration: **nav, footer, and head live in one
partial each**, and adding a page never edits another page again.

---

## 7. Phased remediation plan (no redesign, low risk)

- **Phase 0 — Freeze (this doc).** Ratify nav + IA (§2, §8). ✅ Lean 6-item nav
  ratified 2026-06-07.
- **Phase 1 — Canonical footer.** ✅ Done 2026-06-07. 29 variants → 1 footer that
  carries every destination (incl. the items demoted from the lean nav, so the
  pending nav reduction orphans nothing). Crawl: 1482 refs, 0 broken.
- **Phase 1b — Apply lean nav.** ✅ Done 2026-06-07. Primary nav reduced to the
  6 ratified items on all 51 pages; demoted links live in the canonical footer.
  Educational `/learn/*` articles remapped active-state Guides → **Learn** (11
  pages), resolving most of the Phase 3 taxonomy drift. Pages whose section left
  the nav (Watch, FAQ, Search, Guides index/legal/Contact) carry no active
  highlight. Crawl: 1482 refs, 0 broken.
- **Phase 2 — Asset-version single source.** Fix `script.js ?v=10` vs `?v=11`;
  define versions in one place.
- **Phase 3 — Taxonomy cleanup.** Resolve Learn-vs-Guides ownership; fix
  active-state to match URL section.
- **Phase 4 — Introduce the build/partial layer** (§6). Migrate the 51 pages to
  inherit head/header/nav/footer from partials. After this, chrome edits are
  one-file changes.
- **Phase 5 — Inline-style cleanup.** Move the 9 pages' inline `style=` into CSS.

Each phase is independently shippable and reversible.

---

## 8. Open decisions (need owner sign-off)

1. **Primary nav shape:** keep the shipped 10-item nav, or adopt the lean 6-item
   nav (moving Guides/Watch/FAQ/Search/Contact into the footer)? Everything
   downstream (footer unification, taxonomy) depends on this.
2. **Learn vs Guides ownership:** make Learn the sole educational hub and demote
   Guides to Trust/utility? (Recommended.)
3. **Build approach:** Eleventy (standard) vs maintained `build.py` (dependency-
   free)?

Until these are answered, Phases 1–4 are blocked on #1 and #3.
