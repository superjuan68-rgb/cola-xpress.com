# Agent 04 — Customer Likeability

**Role:** Audit how the site FEELS to a first-time visitor. Trust, legitimacy,
emotional clarity, perceived professionalism.

**Inputs required:**
- Rendered homepage and 2-3 deeper pages.
- About / Contact / FAQ / Policies pages.
- Any customer reviews shown on-site or off-site.

---

## Checks

### A. Trust signals (cannabis is high-trust-required)
- Licensing displayed (state license # visible in footer + on legal pages).
- Lab results (COA) accessible from every product page.
- Physical address or service area stated explicitly. Vague = sketchy.
- Real photos of staff / facility / products (no stock).
- Verifiable customer reviews — quantity AND recency matter.
- Press mentions or partnerships, if real. Never fake.

### B. Tone & voice consistency
- Same brand voice on homepage, product pages, blog, emails, support replies.
- Cannabis-industry literate without being meme-coded.
- Avoid the two failure modes:
  - "Corporate beige" — feels like every other delivery brand
  - "Stoner stereotype" — feels juvenile, suppresses premium pricing power

### C. Onboarding friction
- New visitor can answer in 10 seconds:
  - "Do you deliver to me?"
  - "How long does it take?"
  - "What's the minimum?"
  - "Is this legal?"
- Age gate is fast and respectful, not adversarial.
- First-purchase guidance (what to order, recommended products).

### D. Professionalism red flags
- Typos, mismatched fonts, broken layouts → instant trust killer.
- Outdated copyright year in footer.
- Lorem ipsum or template placeholders ANYWHERE.
- Broken links, missing favicons, broken social icons.
- Default "Hello world!" type artifacts from CMS install.

### E. Emotional response (first 5 seconds)
- Does the page feel premium, legit, calm, knowledgeable?
- Or does it feel cluttered, anxious, untrustworthy, generic?
- The 5-second test: show someone the homepage, hide it, ask:
  "What do they sell? Would you buy from them? Why?"

---

## Scoring rubric (0-100)

| Dimension | Weight |
|---|---|
| Trust signals (license, lab, reviews, address) | 30 |
| Tone consistency | 15 |
| Onboarding clarity | 20 |
| Professionalism (no red flags) | 20 |
| Emotional response | 15 |

---

## Output format

```
[LIKEABILITY] severity=blocker
location: https://www.cola-xpress.com/  (footer)
evidence: no state license number visible; service area not stated
fix: add license # and "Serving [neighborhood list]" to footer + About page
impact: cannabis buyers screen for licensure within 10 seconds; this alone
        suppresses conversion ~20-40% vs. licensed competitors
effort: 15 min
```
