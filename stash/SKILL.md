---
description: Zero-friction capture inbox for the thought worth keeping that flies past mid-task — park it in one line, keep working, drain it later into the gated skill that owns its destination. The missing low-friction front door to the flywheel (capture is trivial; the DRAIN is the product). Modes: <note> (capture) | drain | list.
argument-hint: "[<note to capture> | drain | list]  (bare text = capture)"
allowed-tools: Read, Edit, Write, Bash
---

The law this skill runs on: **an inbox nobody drains is dead capital.** The rest of the suite is high-signal by construction — milk/harvest gate on four criteria, snip/card render, prompt compiles a template, until pins a done-check — so it has no low-friction front door for the thought that lands mid-task and would otherwise be lost or derail you. stash is that door: capture in one line and keep moving; the expensive routing (to a finding, an /until stub, /milk, /burn, /taste, /snip…) is DEFERRED to a drain pass. It owns capture-and-park and NO promotion logic — the drain hands each item to the skill that already owns its destination. Capture is trivial; the drain is the whole product.

**Three hard invariants:**
- **It is a WAITING ROOM, not a store.** The durable homes (a project's `private/findings`, `private/decisions`, `.claude/until` stubs, `~/.claude` memory, the build-in-public pool) stay the ONLY homes for promoted capital. `~/.claude/stash/INBOX.md` holds only not-yet-triaged intent. Empty-when-drained is the health signal (a fat inbox is debt, not riches).
- **An item leaves the inbox ONLY by landing in a durable store.** Flip a line to `[x]` only once you have MOVED it somewhere real (append the destination). Never check-in-place — a checked-but-unpromoted line is a lie (the rule /snip's index enforces).
- **No promotion logic of its own.** The drain reuses the family's four-part gate (Reusable + Non-trivial + Specific + Verified) and routes to the owning skill. stash never invents a new store, gate, or destination.

## /stash <note>  (default — capture)
Park one thing in ~2 seconds and return to the task. NO analysis, NO gating at capture time — deferring cognition is the entire point.
1. Ensure the inbox exists: `mkdir -p ~/.claude/stash` (file `~/.claude/stash/INBOX.md`). It is machine-global on purpose, so capture works the instant a thought lands even if you are in the wrong repo.
2. Pick a one-word **route-hint** (advisory; the drain re-judges) — any term from the routing table in `## /stash drain` below, which is the single source for the hint vocabulary and where each term routes. Use the user's hint if they gave one.
3. Dedupe: grep the open `[ ]` lines for a near-match; if the same thought is already parked, UPDATE that line rather than twin it (milk's search-existing-first rule).
4. Append ONE line via the current UTC time (`date -u +"%Y-%m-%d %H:%M"`), then stop:
   `- [ ] <YYYY-MM-DD HH:MM> [<hint>] <one forward-looking line> :: src=<file:line | url | "session" | repo>`
   The body is a pointer or a hunch ("revisit X", "verify claim Y", "competitor Z does W"), NOT a finished finding — if you can write the finding now you do not stash it, you /milk or /harvest it.
5. Confirm in one line ("Stashed. N open.") and return to what you were doing.

## /stash drain
The triage pass — the skill's real product. Empty the inbox by routing each parked item to the skill that owns its destination.
1. Read the open `[ ]` lines in `~/.claude/stash/INBOX.md`.
2. For EACH, apply the four-part gate (Reusable + Non-trivial + Specific + Verified) to decide PROMOTE vs DROP, then route by its (re-judged) destination — stash owns the move-out, not the promotion logic. Use the line's `src=` to pick the right project for a per-project store (the inbox is machine-global; the stores are per-project):
   - **finding / decision** → write via /harvest's conventions (next free `Finding_NNN`/`Decision_NNN` in that project's `private/`, same section shape).
   - **until** → write a `.claude/until/<slug>.md` stub at `status: UNPINNED / UNTESTED` (the exact artifact /capitalize compound emits — stash is a second on-ramp to it).
   - **read** → leave a queued `/milk asset <x>` pointer; do NOT squeeze it inline.
   - **memory / fact / taste / snip / card / prompt / skill** → HAND OFF to the owning skill (write memory directly / /burn rent / /taste / /snip / /card / /prompt save / /hone). Name the handoff; never write CLAUDE.md, TASTE.md, or another skill's store directly (the lane discipline /hone and /capitalize enforce).
3. Flip each promoted line to `[x]` with its destination appended (`-> Finding_037`); DROP a dead one with a one-word reason (stale/dupe/trivial) and, if it was a real dead end, carry it forward as a don't-retry note rather than erasing it silently (milk's prune-with-carry-forward).
4. Report: promoted (with destination), handed off (to which skill), dropped (reason). The inbox should end at or near zero open lines.

## /stash list
Read-only. Print the open `[ ]` lines grouped by route-hint, and flag any older than ~14 days as decay candidates (drain-or-drop) so an un-drained inbox is a visible debt, not invisible rot. Writes nothing.

## Rules
- **Capture is ungated; the drain is gated.** Never gate or distill at capture time (that defeats the front door); always gate at drain time (that protects the stores).
- **Waiting room, never a store:** an item leaves only by landing somewhere durable; never check-in-place; the durable stores remain the only homes for promoted capital.
- **No new store, gate, or destination:** the drain reuses the four-part gate and routes to existing skills. A project fact → /burn rent; a preference → /taste; a finished finding → /milk or /harvest (if you could write it now, you would not stash it).
- **Empty-when-drained is health:** report the open count; a growing inbox is debt. (The drain can also be nudged at the flywheel's edges — /capitalize prime surfacing task-relevant open items on the way in, /harvest reminding you to drain on the way out — but /stash list + /stash drain stand alone so it never rots even unwired.)
- **Honest dedupe and drops:** update a re-stashed thought, do not twin it; a dropped dead end is carried forward as don't-retry, never silently erased.
