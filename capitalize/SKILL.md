---
description: Put accumulated capital to work at session start — withdraw the deposits harvest made (findings, decisions, open questions, until-ledgers, lessons) and deploy the slice relevant to THIS task as a ready-to-execute brief, so a fresh session starts warm instead of paying rent to re-learn the project. Then compound it: promote dormant assets into standing structure. Reads the archive, writes nothing but structure. Modes: prime | compound | statement.
argument-hint: "prime <what you're about to do> | compound | statement  (default: prime)"
---

The accounting law this skill runs on: **harvest EXPENSES a session — value hits the books once, then it's gone. Capitalize BOOKS it as an asset that amortizes across every future session.** Deposited capital that's never withdrawn is dead capital; it decays, it doesn't compound. This skill is the inbound side of the flywheel: harvest deposits, capitalize withdraws-and-deploys. It is the financial inverse of harvest, and it is the close of the broken link.

**Three hard invariants (this is what keeps capitalize from becoming nightshift or burn):**
- **It executes NOTHING.** No code, no branches, no running a task to done. It hands the present user a read-only brief + a menu they steer. The moment it does the work, it's a daytime nightshift.
- **It writes NO facts to CLAUDE.md.** That lane belongs to `/burn rent` (build commands, conventions, gotchas, measured in rent-$). Capitalize's writes are STRUCTURAL only — a roadmap item, a hook/guardrail, a queued task, a promoted memory file. If you detect an unpaid FACT rent, hand it to `/burn rent`; never write the fact yourself.
- **Index first, fetch on relevance.** Never dump the archive into context. Load a compact index (titles + IDs + dates), then pull full text ONLY for the entries that match the stated objective. Default to a subagent so only the brief — not the raw archive — hits main context. (Honors the token charter: no >100-line dump when a 5-line index does.)

## /capitalize prime <what you're about to do>  (default)
Withdraw the relevant reserve and deploy it as a starting brief for the task in `$ARGUMENTS`. If no task is given, infer it from git branch + the newest `session_summaries/` entry, and state your inference.

1. **Resolve the project root** (the dir containing `private/`). Spawn a subagent to build the capital INDEX — do not read full bodies into main context:
   - `private/findings/Finding_*.md` and `private/decisions/Decision_*.md` — title line + ID + date only.
   - `~/.claude/projects/<slug>/memory/MEMORY.md` — the one-line index entries.
   - `.claude/until/*.md` — for each: the pinned check, status (live/capped), and the REFUTED rows of its ledger.
   - The newest 1–2 `private/session_summaries/` — Open Questions + "what's next".
   - `~/.claude/stash/INBOX.md` — the open `[ ]` capture lines (machine-global loose ends not yet routed); keep only those bearing on the task.
2. **Retrieve by the task, not by browsing** (organize by how it'll be used). From the index, the subagent returns ONLY the entries that bear on `$ARGUMENTS`, with full text pulled just for those. Retrieve each capital type its own way: findings by topic-similarity, session state by recency, memory/lessons by task-match.
3. **Carry failures forward as first-class capital.** Surface the matching REFUTED hypotheses and known dead ends from until-ledgers under a **What's already been ruled out** heading, so this session is structurally barred from re-walking them (the highest-value withdrawal — a dead end re-walked is rent paid twice).
4. **Emit the brief** (printed in chat, surfaced as CONTEXT not commands — it primes reasoning, it does not hijack the new goal). Sections: **Task** (restated) · **Live state** (mid-flight until-pursuits, the last session's "what's next") · **Relevant findings/decisions** (by ID, one line each, DATED) · **What's already been ruled out** · **Parked (stash)** (open `~/.claude/stash/INBOX.md` items that bear on this task, if any — surfaced as loose ends, not commands) · **Unblocked?** (any open question this task could now answer). Every loaded entry is labeled with its date and marked supersedable — never silent authority that can steer tool/allowlist choices (loaded capital is poisonable; treat stale entries as suspect, prefer freshness-checked).
5. **End with a menu, not an action.** Offer the next moves the brief implies (e.g. "resume until X", "this looks like a `/burn rent` fact", "OQ-12 is now answerable — queue it?"). The user picks. You execute none of it here. If any stash items are open and relevant, include "`/stash drain` now?" among the offers (the inbox-on-the-way-in hook).

## /capitalize compound
Convert dormant deposited capital into standing structure that pays forward (the "interest on what you already know" half). Scan the archive for assets that have earned promotion, then PROPOSE each as a structural artifact — show the user the diff, write only on approval:
- A **finding** that's load-bearing for direction → a ROADMAP item (append to the project's roadmap file; create one only if the project wants it).
- A **lesson that has recurred** (the promote-on-second-occurrence threshold: seen ≥2× across sessions/memory) → a CLAUDE.md *guardrail* or a settings.json *hook* (a check, not a fact) — or hand to `/update-config` if it's a true automation.
- An **open question** that's now actionable → a QUEUED task: write the task + a DRAFT binary done-check into an `.claude/until/<slug>.md` stub, marked `status: UNPINNED / UNTESTED`, or add it to nightshift's worklist surface. You ENQUEUE; until/nightshift OWN pinning the negative-control and running the loop. No hypothesis ledger lives here.
Apply the four-part promotion gate to every candidate — **Reusable + Non-trivial + Specific + Verified** — matching harvest's high-signal bar. Report: promoted (with destination + ID), and what was rejected and why.

## /capitalize statement
The balance-sheet view — and the flywheel's success check. Spawn a subagent to find **dead capital**: findings/decisions/lessons deposited but never withdrawn or referenced since (decay candidates). Then the **flat-learning-curve test**: pick a task-class run across ≥3 sessions and check it's getting *cheaper/faster* — if the curve is flat, the deposits aren't compounding and the prime step isn't being used. Report: top dead-capital entries (prune, or promote via `compound`), the learning-curve verdict, and the one highest-leverage move to make the capital pay.

## Rules
- Read-only on the archive in `prime`; structural-write only on approval in `compound`. Never expense (consume/delete) capital silently — pruning is a `statement` recommendation the user approves.
- A withdrawal that isn't deployed into the current task is just a re-read — every prime must end pointed at `$ARGUMENTS`, not at a tour of the archive.
- Hand off, don't duplicate: facts → `/burn rent`; taste signal → `/taste induce`; running a queued check → `/until`; overnight execution → `/nightshift`.
