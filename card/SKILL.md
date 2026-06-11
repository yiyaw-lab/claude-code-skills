---
description: Turn a finding, insight, or stat into a designed, share-ready PNG card — editorial typography, house palette, one idea per card. Renders HTML/CSS via headless Chrome. Complements /snip (code windows): /snip shows source, /card stages an idea.
argument-hint: "<the finding/insight, or 'finding N from this session'> [wide|square|tall]"
---

You are designing an insight card for the user's build-in-public posts. The bar is "would a designer repost this," not "is the text present."

## Step 1 — Distill (the hard part)
- ONE idea per card. If the input has three findings, that's three cards — say so and pick the strongest unless told otherwise.
- Budget: ≤45 words total. Structure: **eyebrow** (3–6 words, what this is), **headline** (the insight, ≤16 words, written like a pull-quote not a title), optional **support** (one stat or one sentence), **kicker** (attribution: `@yiyadev · yiya.dev`).
- If a number is the point, the number is the hero — set it display-size, let the words caption it.

## Step 2 — Safety gate
Same as /snip: check against the project's public-disclosure-boundary memory; scan for secrets, keys, private paths. STOP and tell the user if the idea itself leaks private strategy.

## Step 3 — Design (house system: MODERN product aesthetic — Linear/Vercel school, not editorial/serif)
- Canvas: `wide` 1200×675 (default, X inline), `square` 1080×1080, `tall` 1080×1350 (max feed real estate).
- Background: near-black (#0a0a0f), plus atmosphere: ONE soft radial glow in the accent hue (≤14% opacity, off-canvas origin) and/or a faint dot-grid masked to fade (rgba(255,255,255,0.05), 28px). Subtle — texture, not decoration.
- Type: heavy geometric sans for the headline (-apple-system / SF Pro Display, weight 700, tracking -0.03em, line-height ~1.08), SF Mono for eyebrow + kicker. No serifs. Max 3 sizes.
- Accent: ONE gradient per card (e.g. peach #fab387 → pink #f5a0c0 → lavender #b4befe) applied via background-clip:text to the key phrase, or to the hero number, or a small dot — never to body text or backgrounds.
- Components: eyebrow as a glassy pill (1px rgba-white border, blur-tint fill, mono uppercase, gradient dot); inline terms as rounded chips matching; hairline (1px, 14% white) for the kicker rule.
- Layout: strong left axis, generous margins (≥8%). NO orphan words on headline wraps — tune size/max-width until lines break clean. Bans: clip-art, emoji, drop shadows, serif fonts, more than one gradient.
- Legibility check: headline must read at 25% zoom (feed thumbnail). If it doesn't, cut words, not point size.
- The user's bar is "modern" — when in doubt, reference the current 2026 product-design idiom (Linear, Vercel, Stripe marketing pages), never print/editorial.

## Step 4 — Render
- Bundle dir per the /snip convention: `~/build-in-public/snippets/<YYYY-MM-DD>_<slug>/` containing `card.html` and `card.png`.
- Render at 2x:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --screenshot=card.png --window-size=<W>,<H> --force-device-scale-factor=2 \
    --default-background-color=00000000 --hide-scrollbars card.html
  ```
- **Look at the PNG yourself (Read it) before showing the user.** If the hierarchy is mushy, the text crowds an edge, or it reads like a slide, fix and re-render. Never ship a card you haven't seen.

## Step 5 — Bundle + open
- Write `post.md` (draft caption ≤280 chars — the card carries the substance, the caption just frames it) with `Status: draft`.
- Add the `- [ ]` line to `~/build-in-public/snippets/INDEX.md`.
- `open` the PNG and report the bundle path.
