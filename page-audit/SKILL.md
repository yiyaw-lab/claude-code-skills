---
description: Audit a local HTML page's layout and rendering the trustworthy way. Measured facts (overflow, element widths) via an instrumented iframe harness, then screenshots via modern headless Chrome with animations neutralized. Use before diagnosing any visual bug, and instead of eyeballing headless screenshots.
argument-hint: "<path-to-html> [widths, default 390,768,1440]"
allowed-tools: Bash, Read, Write
---

You are auditing a local HTML page. The core rule: **measurements are facts; screenshots are testimony.** Headless rendering betrays you in version-dependent ways: older headless builds handled `--window-size` inconsistently for screenshots, viewport-relative units (svh/vh) balloon in tall capture windows, and IntersectionObserver reveals race the shutter. Version history matters when reading old advice: new headless became the default for bare `--headless` in Chrome 112, and Chrome 132 removed `--headless=old` entirely (old headless survives only as the separate `chrome-headless-shell` binary). The harness below sidesteps the window-size question entirely: width is pinned by an iframe, not the browser window, so it returns the same numbers on any Chrome that can run JS. Facts first, pictures second, and neither is believed unconditionally: both have artifact catalogues below.

## Step 1 - Measure (facts)
Run the bundled harness against the page at each target width (default `390,768,1440`; honor `$ARGUMENTS`):
```
python3 ~/claude-code-skills/page-audit/scripts/measure_page.py <page.html> --widths 390,768,1440
```
Mechanics, so you can interpret its output: it wraps the page in a fixed-width iframe (so media queries apply per width regardless of the browser window), renders via `--dump-dom` under `--virtual-time-budget=5000` with a 1.8s in-page settle, and reports per width: `scrollWidth` vs viewport (horizontal overflow) and every element whose bounding rect exceeds the viewport by more than 2px after rounding to whole pixels (tag.class, right edge, width; capped at 20 offenders, so bleeds that round to 2px or less never appear in the list). It finds Chrome automatically (`CHROME_BIN` overrides). If the harness errors, fix the invocation; do not fall back to eyeballing.

### When the MEASUREMENT lies (check before filing an overflow bug)
| Measured symptom | Likely false positive |
|---|---|
| OVERFLOW, but an ancestor has `overflow: hidden`/`clip` | Clipped decoration. The user can never see or scroll to it. Confirm ancestor overflow before filing. |
| Offender is an animated element (entrance OR autoplay) | Animations never advance under `--dump-dom` virtual time; everything measures at its `from` state, often off-canvas by design. |
| Offenders in below-fold reveal sections | The iframe viewport is 900px tall; IntersectionObserver reveals below that never fire, so below-fold geometry is the pre-reveal (often transformed) state. |

Decision rule: a measurement beats a screenshot for geometry, but an OVERFLOW verdict still needs a user-visibility confirm. Clipped by an ancestor, or an animation start state? Then it's an artifact, not a bug.

### What "clean" does NOT mean
The harness measures horizontal overflow only. Vertical overlap, z-index collisions, zero-height collapses, and contrast are invisible to it. "clean" means "no horizontal overflow at these widths", nothing more. That's what Step 2's screenshots are for.

### Scope
- The harness resolves its argument as a local file path; `http(s)` URLs are not accepted. It runs Chrome with `--allow-file-access-from-files`, so pages built by `fetch()` of local files or ES-module imports DO measure their full JS-built layout under `file://`. For served apps, audit the built static page with the harness and point Step 2's screenshots at the dev server URL.
- Attribution blindness: the verdict (scrollWidth) sees everything; the offender scan (`querySelectorAll` + bounding rects) does not. **OVERFLOW with an EMPTY offenders list** means the offender is invisible to the element scan. Verified causes: overflowing inline text, e.g. a long unbroken string whose block's rect stays at viewport width (the most common mobile overflow bug); a wide `::before`/`::after` pseudo-element; a shadow-DOM-hosted element; or, when the scrollWidth delta is only 1-2px, a bleed that rounded under the offender threshold. The verdict is trustworthy; attribution needs DevTools.
- The inverse state also occurs: **"clean" WITH offenders listed** means the listed elements are clipped by an ancestor (`overflow: hidden` keeps scrollWidth at viewport width). That is the clipped-decoration row of the false-positive table, already confirmed: no user-visible bug.

## Step 2 - Render (pictures, done right)
Only after the measurements, capture visuals with modern headless and animations neutralized:
```
CHROME="${CHROME_BIN:-$(command -v google-chrome || echo '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')}"
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=1 \
  --force-prefers-reduced-motion --hide-scrollbars \
  --window-size=1440,900 --screenshot=/tmp/audit-desktop.png "file://<abs-path>"
```
Repeat at 390x844 for mobile. For below-the-fold content prefer one tall capture (e.g. 1440x4500) and remember: any `svh/vh`-sized section stretches with the capture window. That's an artifact, not a bug. `--force-prefers-reduced-motion` makes pages with reveal animations show everything instantly (if the page handles reduced motion; if sections are still blank, that is a finding about the page's reduced-motion path, not proof of broken layout). Anchor fragments (`page.html#section`) do not reliably scroll in headless; don't use them as evidence of anything.

## Step 3 - Read the screenshots with the Read tool and report
- Lead with the measured verdict (overflow or clean, per width), then visual observations.
- Arbitrate every discrepancy through the two catalogues: a screenshot symptom that a measurement contradicts is presumed a screenshot artifact; an OVERFLOW that fails the user-visibility confirm is presumed a measurement artifact. Say which, explicitly.
- If the user reported a visual bug the audit can't reproduce, say "not reproduced under measurement" rather than inventing a cause.

## When the SCREENSHOT lies (check before claiming a bug)
| Symptom in screenshot | Likely artifact |
|---|---|
| Text clipped at right edge, but scrollWidth == viewport | Headless window-size handling; trust the measurement |
| Giant empty void above/below a hero | svh/vh section scaled to a tall capture window |
| Sections blank/black mid-page | Reveal transitions raced the shutter (use --force-prefers-reduced-motion) |
| Anchor screenshot shows the top of the page | Headless didn't scroll to the fragment |
