---
description: Turn a finding, insight, or stat into a designed, share-ready PNG card — modern product-design aesthetic (house visual system in ~/.claude/DESIGN_SYSTEM.md), one idea per card. Renders HTML/CSS via headless Chrome. Complements /snip (code windows): /snip shows source, /card stages an idea.
argument-hint: "<the finding/insight, or 'finding N from this session'> [wide|square|tall]"
---

You are designing an insight card for the user's build-in-public posts. The bar is "would a designer repost this," not "is the text present."

## Step 1 — Distill (the hard part)
- Default: ONE idea per card. If the input has three findings, that's three cards — say so and pick the strongest unless told otherwise.
- **`stack` mode** (when the user wants all findings on one card): one THEME, 3–6 findings as numbered rows. Each row: bold lead phrase (≤5 words) + muted completion (≤8 words) — one line, never two. The card needs a unifying headline naming the set ("The four laws of…"); if the findings don't share a theme, they don't share a card. Total budget ≤80 words. Use `tall` canvas by default for 4+ rows.
- Budget: ≤45 words total. Structure: **eyebrow** (3–6 words, what this is), **headline** (the insight, ≤16 words, written like a pull-quote not a title), optional **support** (one stat or one sentence), **kicker** (attribution: `@yiyadev · yiya.dev`).
- If a number is the point, the number is the hero — set it display-size, let the words caption it.

## Step 2 — Safety gate
Same as /snip: check against the project's public-disclosure-boundary memory; scan for secrets, keys, private paths. STOP and tell the user if the idea itself leaks private strategy.

## Step 3 — Design (apply the house visual system: `~/.claude/DESIGN_SYSTEM.md`)
- Canvas: `wide` 1200×675 (default, X inline), `square` 1080×1080, `tall` 1080×1350 (max feed real estate).
- Apply `~/.claude/DESIGN_SYSTEM.md` — the single-source house aesthetic: surface/atmosphere, type, the one-gradient accent rule, components, layout axis + margins, the no-orphan-words and 25%-zoom legibility checks, and the bans. MODERN Linear/Vercel idiom, never print/editorial.
- **`stack` rows** (card-specific layout): oversized mono index (`01`–`06`) in the gradient via background-clip, hairline (1px, 10% white) between rows, bold white lead phrase + muted (#9d9da8) completion on ONE line per row. Row text ~26–30px; the headline stays the largest element. Rows get the gradient only on the index — never on row text. If a row wraps at render, cut words until it doesn't.

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
