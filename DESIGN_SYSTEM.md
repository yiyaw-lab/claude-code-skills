# House visual system

The single-source house aesthetic for rendered visual artifacts — insight cards today, and any future render skill (slide decks, hero images). Extracted from `/card` so the look lives in ONE place and stays consistent. Idiom: MODERN product design — Linear / Vercel / Stripe-marketing school, NOT print / editorial / serif.

## Surface
Background near-black (#0a0a0f), plus atmosphere: ONE soft radial glow in the accent hue (≤14% opacity, off-canvas origin) and/or a faint dot-grid masked to fade (rgba(255,255,255,0.05), 28px). Subtle — texture, not decoration.

## Type
Heavy geometric sans for the headline (-apple-system / SF Pro Display, weight 700, tracking -0.03em, line-height ~1.08); SF Mono for eyebrow + kicker. No serifs. Max 3 sizes.

## Accent
ONE gradient per artifact (e.g. peach #fab387 → pink #f5a0c0 → lavender #b4befe), applied via background-clip:text to the key phrase, the hero number, or a small dot — NEVER to body text or backgrounds.

## Components
Eyebrow as a glassy pill (1px rgba-white border, blur-tint fill, mono uppercase, gradient dot); inline terms as rounded chips matching; hairline (1px, 14% white) for rules.

## Layout
Strong left axis, generous margins (≥8%). NO orphan words on headline wraps — tune size/max-width until lines break clean.

## Legibility
The headline must read at 25% zoom (feed thumbnail). If it does not, cut words, not point size.

## Bans
Clip-art, emoji, drop shadows, serif fonts, more than one gradient.

When in doubt, reference the current 2026 product-design idiom (Linear, Vercel, Stripe marketing pages), never print/editorial.
