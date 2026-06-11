---
description: Goal-pursuit engine — attempt, verify, adjust until a pinned objective is verifiably done. Negative-control verification, a hypothesis ledger that forbids re-testing refuted ideas, git checkpoints, and a forced escalation ladder (switch layers → fresh-context subagent → attack the goal itself). Survives session death via a state file. (For time-based recurrence, use the built-in /loop instead.)
argument-hint: "<objective> [-- <verify command>] [max=N] | resume"
---

You are in goal-pursuit mode. You do not end your turn until the objective is VERIFIED accomplished or a stop condition fires. "Should work now" is not a stopping state.

## Step 0 — Pin the goal, then prove the check can fail
- Restate the objective as a binary, observable check: a command's exit code, a file's state, a passing test, a visible behavior. If `$ARGUMENTS` contains `-- <verify>`, that IS the check. `max=N` caps iterations (default 10).
- **Negative control: run the check BEFORE doing any work.** If it already passes, the goal is mis-pinned — stop and re-pin. A check that can't fail can't verify anything.
- NEVER weaken the check mid-run. The check pinned here is the check you finish on.
- Create the state file `.claude/until/<goal-slug>.md` in the project: the pinned check, the brief (what's known, what's ruled out), and the ledger below. Update it EVERY iteration — this is what makes the pursuit survive compaction, crashes, and session ends. `/until resume` = read the newest state file and continue from its ledger, not from scratch.

## The hypothesis ledger
Maintain in the state file:
`| iter | hypothesis | layer | action | check result | status: REFUTED / CONFIRMED / UNTESTED |`
- One hypothesis per iteration, falsifiable, named BEFORE acting.
- **A REFUTED hypothesis is dead. Re-testing it is forbidden** — variants count as re-tests unless you can say what evidence distinguishes them.
- Tag each hypothesis with its layer: `code | config | environment | dependency | data | assumption`. You'll need this for escalation.

## Each iteration
1. **Checkpoint** — before any risky change: `git stash push` or a WIP commit. A failed fix must be rolled back, not layered under the next fix. Compounding half-fixes is how loops corrupt the workspace.
2. **Act** — smallest change that tests the hypothesis.
3. **Verify** — run the pinned check for real; capture output. A pass must be reproduced once (re-run, clean state if cheap) before you trust it — flaky passes are how loops end in false victory.
4. **Record** — update the ledger + state file. Failed experiment? Roll back to checkpoint before iterating.

## The escalation ladder — strategy shifts are forced, not optional
- **3 consecutive REFUTED in the same layer** → that layer is probably innocent. Next hypothesis MUST come from a different layer.
- **5 consecutive REFUTED** → your context is now part of the problem: you're anchored on dead hypotheses. Write a clean brief (symptom, check, ledger summary, what's ruled out — NOT your theories) and spawn a fresh-context subagent on it. Its naivety is the asset; do not contaminate the brief with your favorite suspect.
- **7 consecutive REFUTED** → attack the goal itself: spawn an adversarial subagent to argue the check is testing the wrong thing, the bug is upstream of where you're looking, or the objective hides a false assumption. If it lands, re-pin WITH THE USER (this is the one allowed check change — explicit, never silent).
- **Cap reached** → write the handoff: state file finalized, brief sharpened, "what I'd try next" listed. A future `/until resume` — yours or another agent's — starts from iteration N, not zero.

## Stop conditions — never declare false success
- ✅ Check passes, reproduced → report what worked + verifying output.
- 🛑 Thrashing: no new falsifiable hypothesis exists in any layer.
- 🛑 Cap (default 10).
- 🛑 User-blocked: needs credentials, a decision, money, or hardware only the user has — name it precisely.

## Final report
✅ or 🛑 · the verified evidence (real output, not paraphrase) · iterations used · the ledger · state-file path. On 🛑: the exact resume command.
