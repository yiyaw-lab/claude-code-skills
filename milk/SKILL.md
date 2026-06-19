---
description: Tap ONE rich asset for durable yield — point it at a deep-research report, a competitor repo, a paper/PDF, a long thread, or a codebase you're holding RIGHT NOW, and squeeze every durable drop (findings, decisions, saveable prompts, postable snippets, lessons, open questions) WITHOUT ending the session. Routes the yield into your existing capital stores so the squeeze feeds the flywheel. Re-milkable: the same asset keeps producing as you revisit it. Modes: asset | consolidate.
argument-hint: "asset <path|url|description> | consolidate [N sessions]  (default: asset)"
---

The cash-cow law this skill runs on: **a productive asset yields a recurring stream — you draw from it, you don't slaughter it.** harvest reaps the SESSION-field once at end-of-cycle; milk taps a discrete ASSET, now, mid-session, again whenever it produces more. The asset is the cow; you don't consume it, you milk it. The non-negotiable that keeps it on the flywheel and not strip-mining: **every drop DEPOSITS into the same stores harvest writes to** — so milk feeds capitalize.

**The ONE rule that keeps this from being a dump:** nothing enters a durable store unless it clears the four-part gate — **Reusable + Non-trivial + Specific + Verified** — AND a "search existing first" check. Before writing any finding/decision/lesson, grep the existing store for a near-duplicate; if one exists, UPDATE it, don't add a twin. A milk run that produces 20 raw notes has failed; one that deposits 3 gated, deduped, addressable assets has succeeded.

**Two guards on scope (this is what keeps milk distinct from harvest and taste):**
- **Not the ambient session.** Milk is for a DISCRETE asset you point at. If `$ARGUMENTS` is effectively "this session" at session end, REFUSE and redirect to `/harvest` — that's harvest's job, and milk must not grade the session, touch `build_log.md`, or advance the session counter.
- **Not taste, not facts.** If you hit strong taste signal (the asset reveals how the user judges), hand off to `/taste induce` — don't write TASTE.md. If you hit a re-learned project fact, hand to `/burn rent`.

## /milk asset <path|url|description>  (default)
Squeeze one external/internal asset for durable value. **Progressive summarization, not one-shot** — distill in passes so a 200-msg thread or a 40-page PDF doesn't collapse to mush:
1. **Locate + chunk.** Resolve the asset (a file, a URL to fetch, a repo path, a pasted thread). Large asset → chunk it; spawn subagents per chunk so the raw bytes never sit in main context — only distilled returns do.
2. **Analyze along fixed value dimensions** (the same every run, so yield is comparable): architecture/structure · non-obvious patterns worth stealing · gotchas/failure-modes · reusable ideas · claims worth verifying · prompts/code worth saving.
3. **Distill in layers** per chunk: gist → the bolded core → the ONE deployable move. Keep the deployable move; that's the yield, the rest is scaffolding.
4. **Gate, dedupe, then ROUTE the yield into existing stores** (this is the differentiator vs a generic analyzer — it doesn't dead-end in chat):
   - durable learning → `private/findings/Finding_<NNN>_*.md` (next free ID), TAGGED with the source asset, in the established `## What Was Learned / ## Evidence / ## Implications` shape.
   - a choice this asset forces/settles → `private/decisions/Decision_<NNN>_*.md`.
   - a recurring/architectural lesson → the project `memory/` (+ a MEMORY.md index line).
   - an open question the asset raises → stage for `/capitalize compound` (a queued task), don't pin it here.
   - publishable gold (a clean reusable pattern → `/snip`; a stat/insight that lands → `/card`) — stage the draft, disclosure + secrets gate FIRST, nothing auto-posts.
   - a prompt worth reusing → `/prompt save`.
5. **Report + re-milk pointer.** What was deposited (paths + IDs), what was gated out and why, what was handed off. Note where the asset still has unmilked yield, so a later `/milk asset <same>` resumes from there rather than re-squeezing the top.

## /milk consolidate [N sessions]
The cross-session yield: roll up what N sessions of deposits ADD UP TO — the synthesis step the archive lacks (MEMORY.md is an index, not a thesis). Spawn a subagent to read the per-session `findings/`+`decisions/` across the newest N (default the project's full set), then apply the four-verb consolidation vocabulary, surfacing each for approval (never auto-commit):
- **NEW** — an emergent truth no single session states but several imply (theory-grade; the "what is now true" layer).
- **UPDATE** — supersede a stale finding/decision with a freshness-checked newer one.
- **DELETE** — prune refuted/contradicted capital, BUT carry the failure forward as a "don't re-try" note (a dead end is high-value capital, not noise).
- **PROMOTE** — elevate the repeatedly-useful (≥2 occurrences) into a standing artifact via `/capitalize compound` (roadmap/guardrail/queued task).
Gate every promotion (Reusable+Non-trivial+Specific+Verified). Report the new higher-order truths, the supersessions, and the prune-with-carry-forward list.

## Rules
- Squeeze, don't slaughter: the source asset is never consumed or altered; milk only reads it and deposits derivatives.
- Re-runnable by design: a re-milk of the same asset must extend, not duplicate — `search existing first` makes that real.
- Mid-session always; never requires the session to end. If you find yourself grading the session, you're in harvest's lane — stop and redirect.
