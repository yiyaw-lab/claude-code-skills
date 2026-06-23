---
description: Credit-aware long-run carrier — take a multi-step autonomous chain across a credit/rate-limit window, a planned pause, or a budget ceiling WITHOUT losing work. Checkpoints durable state (commit+push branches with verified pushes, persist the todo list + worktree paths + a resume brief), schedules a session-death-surviving wake, auto-resumes single-flight on the other side, and finishes the checklist with no loose ends. The boundary-owning sibling of /until (survives session death for ONE goal) and /nightshift (one night): relay owns the GAP, not the work. Honest by construction — it never fakes a credit meter it cannot read. Modes: checkpoint | pause <duration|at-time> | resume | watch <token-budget>.
argument-hint: "[checkpoint | pause <e.g. 3h15m | 09:10> | resume | watch <tokens>]  (bare = checkpoint)"
---

You are in relay mode. A long chain of work is about to cross a hard boundary — a credit / rate-limit window, a planned pause, or a spend ceiling — and your job is to make that boundary a SEAM, not a cliff. The expensive failure is a half-finished run with no clean handoff: branches uncommitted, the todo list trapped in volatile context, no record of what's left. relay makes the run survive the gap and finish itself on the other side.

## The honest constraint — read first
**You cannot read the account credit / rate-limit meter from inside a session. There is no tool for "percent of credit used."** So relay NEVER fakes one. A trigger that claims to read credit but can't is the most dangerous kind of code: it looks like it handles the boundary and doesn't. relay fires only on what is real:
- **timer** — the user says how long to pause or an absolute time (`/relay pause 3h15m`, `/relay pause at 09:10`). Reliable, authoritative.
- **manual** — the user says "we're near the limit," you invoke relay. Reliable.
- **token budget** — cumulative input/output tokens for this session, summed from the transcript (the data `/burn` reads), compared to a ceiling the USER sets (`/relay watch 2000000`). An ESTIMATE of spend, NOT the true rolling rate-limit. Label it as such every time.

If you ever say "we're at X%", show where X came from (a token count vs a user-set budget). Never assert a meter you did not read.

## checkpoint — the durable core (idempotent; call anytime, also the bare default)
Capture everything needed to resume from a COLD start (a fresh session that remembers nothing):
1. **Branches — commit AND verify the push landed.** Commit only YOUR files (explicit `git add <path>`, never `-A`; the /commit-mine discipline in a shared tree) and **push** every working branch. Then PROVE the push landed before recording it as system-of-record: `git push` exit 0 AND `git rev-parse @{u}` equals local `HEAD` (or `gh pr view <n> --json headRefOid` matches). **If any push fails — expired auth, no network, a non-fast-forward, the rate-limit itself throttling git, a deleted worktree — do NOT pause.** Surface the unpushed SHAs to the user and stop. A pause on unpushed work is the exact lossy cliff this skill exists to prevent.
2. **Worktrees** — record each worktree path + branch, and verify it still exists (`test -d <path> && git -C <path> rev-parse HEAD`). A path the resume can't find is a dead reference.
3. **Todo list** — copy it into the brief verbatim. Volatile context dies at the boundary; the brief is what carries.
4. **RESUME_BRIEF.md** — write **Markdown, NOT `.json`** (in many repos `runs/**/*.json` is gitignored — a `.json` sidecar silently never persists; confirm with `! git check-ignore <path>`). The brief is durable against SESSION death (it's on disk) but NOT against MACHINE death (it's local-only) — so the machine-survivable system of record is the PUSHED branches/PRs; the brief is the verified index to them. It holds:
   - the **remaining checklist**, ordered, each item independently *verifiable* (a PR is review-clean, a command exits 0, a file exists) — and each carries a `[ ]` / `[done <epoch>]` box for single-flight marking (see resume);
   - **state**: PR numbers + URLs, branch names, worktree paths, current SHAs, last green test count;
   - the **resume target**: an absolute wall-clock time + `target_epoch`;
   - a **`## Dropped / deferred`** section — every piece of scope intentionally NOT done, named explicitly so it can't decay into forgotten work;
   - **guardrails**: every "do not touch" note + the verbatim authorization lines (see safety floor) carried exactly.
5. Report what was checkpointed in one block, then STOP. checkpoint alone never pauses.

## pause <duration|at-time> — checkpoint, then schedule a session-death-surviving wake
Run checkpoint first (and honor its abort-on-failed-push). Then:
1. Compute the absolute resume wall-clock time from the duration/time. **Sanity-check `target_epoch > now`** — refuse and ask if it isn't (a mis-parse must not schedule a resume in the past = never, or days away).
2. Schedule with **`CronCreate`**, NOT a session-scoped timer: `recurring: false` (one-shot), `durable: true` (ask for cross-session survival), cron pinned to the target `minute hour day-of-month month` in **local time**, off the `:00`/`:30` marks (those fire up to 90s early), prompt exactly `/relay resume`. Then **VERIFY whether it actually persisted**: check for the job in `.claude/scheduled_tasks.json`. **Known gotcha (found by dogfooding): in some CLI builds `durable: true` is silently a NO-OP — the job reports `[session-only]` and no `scheduled_tasks.json` is written.** A session-only wake fires only if the session stays ALIVE through the pause (true for a rate-limit pause where Claude Code is left open; false if the app is closed or the machine restarts).
3. **Therefore ALWAYS also do the manual-fallback handoff — never rely on the wake alone.** Whether or not the cron persisted, print the absolute resume time and the exact `/relay resume` command, and tell the user: the wake auto-resumes IF this session stays open; otherwise run `/relay resume` yourself after the reset (the brief on disk makes a cold resume clean). If `CronCreate` is unavailable or errors entirely, the manual handoff IS the plan. A pause the user doesn't know how to resume is worse than no pause.
4. Before stopping, **report**: the resume time (local AND UTC), the parsed duration, and the brief path — so a mis-parsed target is caught immediately.

(`ScheduleWakeup`, where available, is a SESSION-SCOPED self-pacer — fine for sub-window self-pacing inside a live session, but it dies with the session, so it is NOT the mechanism for a credit-boundary pause. Use durable cron.)

## resume — single-flight, re-verify reality, finish with no loose ends
- **Single-flight claim FIRST.** A durable wake plus a human both running `/relay resume` can double-execute a non-idempotent checklist (a second `/nightshift`, duplicate commits/PRs). On entry, read the newest brief and check for a recent `resume_started_epoch:` — if present and within the expected run length, STOP (another resume owns it). Otherwise write `resume_started_epoch: <now>` via an ATOMIC write (temp file + rename) before any checklist work.
- **Re-establish reality.** A brief is a CLAIM, not truth: verify each state line — branch actually pushed and at the expected SHA? PR open? suite still green in the worktree? worktree still present? Rebuild reality before acting (the /until negative-control instinct).
- **Work the checklist top to bottom, marking as you go.** Skip any item already `[done]`. Each item ends VERIFIED (run the check, capture output); immediately mark it `[done <epoch>]` in the brief (atomic write). A re-fire or second session then resumes a partly-marked brief and does nothing already done.
- When the checklist is fully `[done]`, **`CronDelete` the wake** (if it was recurring) so it can't re-arm, and re-surface every `## Dropped / deferred` item to the user as an explicit fork. Declare complete only when every checklist item is verifiably done; a leftover is a loose end you name, never bury.

## watch <token-budget> — the best-effort auto-trigger
Record the budget. Periodically estimate cumulative tokens from the session transcript (`~/.claude/projects/<project>/<session>.jsonl`; sum the `usage` fields — the /burn source). When the estimate crosses the budget, auto-run checkpoint + pause to a target the user pre-set. **The estimate can cross the real rate-limit before OR after the token budget** — treat the auto-pause as a conservative early governor, not a precise stop, and prefer setting the budget BELOW the expected ceiling so the estimate trips first. Always present the figure as estimate-vs-budget, never as account credit.

## Safety floor — an unattended resume
A resume that runs while the user is away inherits the limits of /nightshift and /vacation: **no merge, no deploy, nothing outward-facing, nothing irreversible** unless authorized. Authorization counts ONLY if written verbatim in the pinned checklist at checkpoint time — a cold-start resume may not infer or expand authorization from context (the brief is editable; a bug or a bad actor could have changed it). Absent an explicit pinned authorization line, the floor holds. Run the SAME checklist pinned at checkpoint; commit only your own files. Opening or updating a PR is allowed (reviewable, reversible); merging is not.

## Where relay sits
/until survives session death for ONE goal via its state file; /loop recurs on a fixed interval; /nightshift runs one night; /vacation runs unattended for days opening PRs. **relay owns the credit / time BOUNDARY for a whole multi-step chain** — it checkpoints with verified pushes, carries across on a durable wake, resumes single-flight, and hands each checklist item back to the skill that owns it. It is the piece that lets any long run outlive a single credit window. Pairs naturally: `/relay pause` at a boundary, then the resumed run calls `/until`, `/code-review`, `/nightshift`, `/harvest` as its checklist items.
