---
description: Apply the razor — raze a target to the simplest sufficient form by QUESTIONING every requirement and DELETING whole parts/processes before any optimization (Musk's Algorithm: question → delete → simplify → accelerate → automate; idiot index; the best part is no part). A "should this EXIST at all" scythe, not a tidy-up. Deletion is the judgment act. Modes: <target> (scan+propose) | audit | apply. Alias: /elonize.
argument-hint: "<path|module|feature|process to raze> | audit | apply  (default: scan + propose)"
allowed-tools: Read, Edit, Write, Bash
---

The law this skill runs on: **the best part is no part; the best process is no process.** Occam's razor in code — *entities must not be multiplied beyond necessity*. Where /simplify tidies what stays and /code-review hunts bugs in what stays, raze attacks the prior question: should this part, this requirement, this step EXIST at all? It runs Musk's Algorithm in strict order — question requirements, DELETE, and only then simplify/accelerate/automate — because optimizing a thing that should not exist is the most expensive mistake there is. Deletion is the judgment ("generation is free, judgment isn't"); raze makes the cut the product.

**Three hard invariants:**
- **Delete before optimize — never the reverse.** The steps run in order; you may not simplify/accelerate/automate a part until it has survived the delete pass. Refusing to polish a deletion candidate is itself the core safety rule.
- **Propose-on-approval, never auto-delete.** Default mode emits a kill-list and writes nothing. Cuts land only in `apply`, only on individually-approved entries (no bulk "yes to all" — one wrong bulk delete is unrecoverable), one kill per commit, tests green between each. Branch-only, reversible by git.
- **The ≥80 genuinely-unused gate.** No part is proposed for deletion below 80/100 unused-confidence, and 80 demands real evidence: the import/usage graph traced from REAL entrypoints (never a stale audit), zero live callers, and a trial cut that leaves the build + tests green. Zero test coverage = HIGH-RISK, manual proof required, never auto-trusted.

## /raze <target>  (default — scan + propose)
Run the Algorithm as ordered evidence passes (fan the reads to scout subagents; only the candidate list returns).
1. **Pin + budget.** Restate the target as an inventory of PARTS (functions, files, flags, config keys, deps, abstraction layers, doc sections, CI/build steps, pipeline stages, even whole skills). Set the add-back budget (default ~10%). Negative control: if nothing is a deletion candidate, you were handed lean code — stop and redirect to /simplify.
2. **Question the requirements (make them less dumb).** For each part, trace WHY it exists to a named owner (git blame, the introducing PR/ticket, the constraint it cites). Flag every requirement whose only authority is a confident assertion with no live consumer — those are the most dangerous because the least questioned. Compute the idiot index (part cost ÷ irreducible essential cost) where measurable.
3. **Delete (the core act).** Hardest-to-justify first, decide KILL or KEEP. KILL: no entrypoint reaches it (proven by import graph), its requirement died in step 2, speculative flexibility nobody asked for, redundant layers/flags. Build the KILL-LIST ordered by (idiot index × deletion-safety); each entry: the part · why it dies · the import-graph/call-site proof it's unused · UNUSED-CONFIDENCE 0-100 (floor 80 to propose) · blast radius (and is it tested?) · the exact cut (diff) · an explicit ADD-BACK BET.
4. **Hand off the survivors — do NOT re-roll.** Only now is optimization allowed, and it is not raze's lane: route surviving code to /simplify (reuse/altitude/efficiency) and /code-review (correctness on the new edges each deletion created). Token-fat → /burn. Name the handoffs; don't re-implement them.
5. **Accelerate, then automate — last, survivors only.** For surviving PROCESS targets, recommend cycle-time cuts before automation (automating waste just makes it faster); surface as recommendations, never auto-install.
6. **Report + route.** Emit the kill-list (proposed ≥80 / watching <80 / refused), the idiot-index leaderboard, the unanswered "why does this exist?" requirements, and the lane handoffs. Honest-empty: if nothing clears the 80 gate, say so and cut nothing — a manufactured deletion is worse than none.

## /raze audit
Read-only. Produce the kill-list + idiot-index leaderboard + the requirements ledger (every part whose only authority is an unbacked assertion), and propose/write NOTHING. The "what would I cut, and why" preview — mirrors /hone audit.

## /raze apply
Execute ONLY pre-approved kills from a prior scan. One kill = one commit; run the target's pinned check (tests/build/the app per /run) with real output BEFORE the next cut. A red check halts immediately, reverts that single cut, and reports — never proceeds through a broken state. A deletion that breaks the check is ADDED BACK and logged as a restore (paid-for tuition: record WHY, so a future raze does not re-kill it). Record each landed kill + its add-back bet to `~/.claude/raze/cuts.md` so the realized add-back rate can be graded later (closes the loop the way /hone closes grade→improvement).

## Rules
- **Order is law:** question → delete → simplify → accelerate → automate. Never optimize a part that has not survived deletion.
- **Refuse-list (never cut, regardless of confidence):** security/allowlist/auth gates (never trust the model to self-limit), the logging/observability net, the tests themselves (deleting the test that would catch a bad delete is the cardinal sin), secrets handling, anything outward-facing or irreversible outside git. Chesterton's fence: a part whose purpose cannot be traced is WATCHED, not cut — unknown reason is a reason to keep.
- **The add-back rate is the two-sided grade:** restores ÷ kills. Well above ~10% = you cut wrong (tighten the gate); near 0% = you were timid (you became /simplify); a small non-zero rate = aggressive enough yet safe. Net parts/lines deleted is the product — a session that nets +lines has not razed.
- **Lane discipline:** raze deletes; /simplify optimizes the survivors; /code-review checks the new edges; /burn cuts tokens. Hand off, don't duplicate.
- **Shared-tree safety:** branch-only, explicit `git add <path>` (never -A), no history rewrite on a shared branch; an adversarial /code-review pass must try to refute each cut before any PR.

Alias: `/elonize` runs this skill. **raze** is the razor (delete to the simplest sufficient form — the self-documenting verb); **elonize** is the broader basket of first-principles/Algorithm moves of which the razor is one. As more of those principles get encoded, they live here.
