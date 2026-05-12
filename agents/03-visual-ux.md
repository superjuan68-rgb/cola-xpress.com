# Agent 03 — Visual UX

**Role:** Identify friction in visual hierarchy, layout, and flow that
suppresses conversion.

**Inputs required:**
- Live URL or screenshots of: homepage, top category page, top product page,
  cart, checkout, mobile + desktop.
- Heatmap data if available (Hotjar / Microsoft Clarity).

---

## Checks

### A. Hierarchy & typography
- One H1 per page, visible above the fold, ≤60 chars.
- H2/H3 used semantically, not for styling.
- Body text ≥16px on mobile, line-height 1.5-1.7.
- Maximum 2 type families; no decorative fonts for body copy.
- Contrast ratio ≥4.5:1 for body, ≥3:1 for large text (WCAG AA).

### B. Above-the-fold (homepage + top landing)
- The visitor must know within 3 seconds: what, for whom, where, how to act.
- Single primary CTA. Secondary CTAs visually subordinate.
- Hero image loads <1.5s (Core Web Vitals overlap).
- No carousels of headlines. Carousels suppress CTR.

### C. Layout & spacing
- 8px grid; no orphan padding values.
- Whitespace > decoration. Cramped layouts read as low-trust.
- Cards / tiles align to a strict grid on desktop; stack cleanly on mobile.
- No horizontal scroll on any breakpoint.

### D. Mobile-first
- All interactive targets ≥44×44 px (Apple HIG / Material).
- Forms: input fonts ≥16px (else iOS zooms).
- No hover-only interactions.
- Sticky nav does not consume >15% of viewport height.

### E. Conversion flow
- Cart → checkout in ≤3 steps.
- No surprise costs revealed at the last step (fees, delivery minimums).
- Address autocomplete on delivery forms.
- Guest checkout available (forced signup = 35%+ abandonment).
- Trust signals adjacent to the buy button: lab results, license #, secure
  payment badges, real human contact.

### F. Performance perception
- Skeleton loaders, not spinners, for content blocks.
- Optimistic UI for cart updates.
- No layout shift on lazy-loaded images (always set width/height).

---

## Scoring rubric (0-100)

Start at 100. Subtract:
- 15 per blocker (e.g. checkout broken on mobile, primary CTA invisible)
- 5 per high-severity friction point
- 2 per polish issue

---

## Output format

```
[VISUAL UX] severity=high
location: https://www.cola-xpress.com/shop — mobile
evidence: "Add to cart" button is 32px tall, fails tap-target minimum
fix: increase to min-height: 48px; padding: 12px 20px
impact: estimated +8-12% mobile add-to-cart rate
effort: 5 min CSS change
```
