---
description: Distill the user's revealed taste from real session transcripts into an enforceable personal rubric (~/.claude/TASTE.md), then apply it as a pre-delivery filter. Mines what they actually corrected and accepted — never what they say they prefer. Modes: induce | apply | audit.
argument-hint: "induce [N] | apply | audit  (default: apply)"
---

Core law: **revealed preferences only.** Stated criteria ≠ revealed criteria — rubrics built by asking the user what they like do not predict their actual judgments. Never build or update the rubric from the user's self-description; harvest it from how they actually reacted.

## /taste induce [N]
1. **Harvest.** Find the newest N (default 10) session transcripts: `~/.claude/projects/**/*.jsonl` by mtime. Spawn one subagent per transcript to extract USER-turn reaction moments, each returned as `{quote, what_the_agent_had_done, signal}`:
   - **Corrections**: "no", "actually", "instead", "don't", "why did you", "too long/short", partial redos, the user rewriting your output their way.
   - **Approvals**: "perfect", "yes", "love it", verbatim reuse of your output, immediate build-on-top.
   - **Silent rejections**: the user re-asks the same thing differently — the first answer missed; figure out what changed between ask one and ask two.
2. **Induce.** Cluster moments into candidate rules. A rule needs ≥2 independent evidence moments (different sessions ideally); single moments are anecdotes — record as PROVISIONAL. Each rule: name, the do/don't in one sentence, quoted evidence with session refs, evidence count.
3. **Guard against contamination.** If the user *said* "I prefer X" somewhere but their reactions show they accept Y, record the conflict explicitly and trust the behavior. Absence of objection is NOT preference — never induce a rule from silence.
4. **Write/merge `~/.claude/TASTE.md`.** Strengthen rules the new evidence confirms (bump n). Retire rules newer evidence contradicts — taste drifts; newest behavior wins. Keep ≤15 ACTIVE rules ranked by evidence count; overflow goes to a PROVISIONAL section. Mark machine-inferred rules `(inferred, n=K)` and NEVER delete or rewrite lines the user added by hand.
5. **Report**: new / strengthened / retired rules, and the 3 most surprising findings — the gaps between what the user would *say* they want and what they demonstrably reward.

## /taste apply  (default)
Read `~/.claude/TASTE.md`. Review your pending or most recent substantial output against the ACTIVE rules. Fix violations before delivering. Report which rules fired: `rule → what changed`. If TASTE.md doesn't exist, say so and offer `/taste induce`.

## /taste audit
Grade this session's outputs against TASTE.md: `| rule | conformance | example from this session |`. The worst offenders are candidates for promotion into CLAUDE.md or a memory file — where they get loaded every session instead of on demand.

## Rules
- Evidence is quoted user words. Never paraphrase a quote into something stronger than what was said.
- The rubric describes the user, so it belongs to the user: TASTE.md is theirs to edit, and hand edits outrank inferences.
- This file and TASTE.md stay local. Publishing either is a disclosure decision the user makes explicitly, not a default.
