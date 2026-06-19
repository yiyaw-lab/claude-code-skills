---
description: Close the grade→improvement loop — read accumulated grade-session report cards, find failures that RECUR across sessions, and propose surgical edits to the skill bodies that caused them; write only on approval. The suite's self-improvement layer (grade-session diagnoses per session; hone sharpens across sessions). Modes: sweep | audit | <skill-name>.
argument-hint: "[sweep | audit | <skill-name>] (default: sweep)"
allowed-tools: Read, Edit, Write, Bash
---

The law this skill runs on: **a grade nobody acts on is a diagnosis with no treatment.** /grade-session writes a candid report card every session, /harvest files it — but nothing ever edits the skill that earned the bad grade, so the suite repeats the same failure forever. hone is the feedback wire: it reads the accumulated coach/agent notes, finds the failures that RECUR, and sharpens the skill body that caused each one. It hones PATTERNS, not incidents — one bad grade is noise; the same bad grade twice is a defect in the instructions.

**Three hard invariants (this is what keeps hone from becoming taste, capitalize, or burn):**
- **It edits skill BODIES only** — the procedural steps/rules in `~/.claude/commands/*.md`. A project FACT goes to `/burn rent` (never write CLAUDE.md here); a user PREFERENCE goes to `/taste` (never write TASTE.md here). Cross a lane and you've duplicated another skill.
- **Propose, write only on approval.** Every edit is surfaced as a unified diff + its grade evidence before anything is written. Never auto-edit a skill. Surgical hunks only — add a guard step, tighten a rule, fix a default; never rewrite a body.
- **Recurrence-gated.** A skill is honed only for a failure seen across **≥2 sessions** (the same promote-on-second-occurrence bar capitalize/taste use). A one-off stays watched, not actioned.

## /hone sweep  (default)
Run the full loop: grades in, approved skill edits out.

1. **Gather the graded report cards.** Spawn a subagent so only the extracted grades — not the full summaries — hit main context. It reads the newest N (default 5) `private/session_summaries/*-summary.md`, pulls each `# Session Evaluation` block (the two grade tables + **Coach Note** + **Agent Note**), and the `feedback`-type entries in `~/.claude/projects/<slug>/memory/MEMORY.md`. Returns: per session, the sub-A grades with their one-line notes, plus both notes verbatim. If fewer than 2 graded sessions exist, stop and say so — there is not enough signal yet (run /harvest to accumulate it).
2. **Cluster into recurring failure modes.** Group the low grades + notes by the UNDERLYING failure (e.g. "over-read into main context", "review missed state-machine edges", "asked a question it could have answered"), not by wording. Keep only modes that recur across **≥2 sessions**; everything else is reported as watched, not actioned.
3. **Route each cluster by lane — do NOT cross lanes:**
   - a recurring **skill-method** failure (the skill's own steps/rules permitted it) → hone's lane (step 4).
   - a re-learned **project fact** → hand to `/burn rent`. a **taste/preference** signal → hand to `/taste`. Name the handoff; write neither file yourself.
   - a one-off or fuzzy note → leave it; list it under "watching".
4. **Map to the target skill + draft the smallest edit that closes it.** For each in-lane cluster, find the skill `.md` whose step or rule would have prevented the recurrence, and draft the minimal surgical change — a new guard step, a tightened rule, a corrected default. Never a rewrite. (hone MAY target its own body; if so, flag it loudly.)
5. **Gate every proposed edit on the four-part promotion gate** — **Reusable** (helps beyond the one session), **Non-trivial** (the skill genuinely lacked it), **Specific** (a concrete step/rule, not "be better"), **Verified** (traceable to ≥2 dated grade moments). Reject the rest with reasons.
6. **Propose, then write only what's approved.** Show each edit as a unified diff against its skill + the grade evidence (which sessions, which exact notes drove it). Apply only the approved hunks. Report: **applied** (path + the failure it closes), **rejected** (reason), **handed off** (to /burn or /taste), **watching** (sub-threshold).

## /hone audit
The read-only backlog — the flat-learning-curve check for the skill suite itself. Run steps 1–3 of sweep, then STOP: list each recurring failure mode with its recurrence count + the sessions, the skill it implicates, and its lane (hone edit / →/burn / →/taste / watching). Propose and write nothing. Use this to see whether grades are actually feeding back, or whether the same complaint keeps recurring un-fixed.

## /hone <skill-name>
Scope the sweep to one skill: gather only the grade moments that bear on `<skill-name>` (its name, its outputs, the work it ran), then run steps 2–6 for that skill alone. Use when one skill keeps under-delivering and you want to sharpen it now without a full sweep.

## Rules
- **Patterns, not incidents:** never edit a skill from a single session's note. A defect is recurrence (≥2 sessions); below that it is watched, not written.
- **Lane discipline:** hone writes ONLY skill-body method/logic. Project fact → `/burn rent`; user preference → `/taste`; the grades themselves are `/grade-session`'s and are read-only canonical input — never re-grade, re-live, or edit the archive.
- **Propose-on-approval, surgical, reversible:** always surface the unified diff + evidence; write only approved hunks; smallest change that closes the failure; never rewrite a whole body. (`~/.claude/commands/` may be outside git — the diff IS the safety record, so keep edits inspectable.)
- **Self-edits are announced:** an edit to `hone.md` itself is allowed (it is the point) but must be flagged explicitly, never slipped in.
- **Honest empty result:** if nothing clears the recurrence + four-part gate, say so and write nothing. A manufactured edit is worse than none.
- **Quality is the constraint, not the variable:** every edit must make the skill catch a real recurring failure; never trade a skill's correctness or clarity for brevity.
