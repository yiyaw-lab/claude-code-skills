---
description: Commit ONLY this session's work out of a shared dirty tree where parallel agent sessions have uncommitted edits in the same files. Positive hunk selection, staged-snapshot test (checkout-index + suite), and a foreign-symbol check before every commit. Use whenever git status shows modifications you didn't all make.
argument-hint: "[test command] (optional; auto-detected from the repo if omitted)"
allowed-tools: Bash, Read, Write, Edit
---

You are landing this session's changes from a working tree that peer sessions also write to. Two failure modes have actually happened and this procedure exists to prevent both: (1) `git add <file>` swept a peer's unfinished hunks into a commit; (2) a *subtractive* hunk-split (dropping only the peer hunks you knew about) swept an **unknown** peer's hunks into main without their dependencies. The result was dangling references that no test caught, because lazy imports and daemon threads don't fire under unittest.

## Step 0 - Inventory: mine vs theirs, per file
- `git fetch origin` first. Stale remote-tracking refs poison every comparison below, including the push-rejection diagnosis in Step 4.
- `git status --short` and `git log --oneline -5` (a peer may have just committed; re-derive, don't assume).
- Bind `<base>`: the remote branch you will push to (`git rev-parse --abbrev-ref @{upstream}`, falling back to `origin/main`).
- Build YOUR edit list from what you actually did this session (files you Edited/Wrote). For each modified file, decide: **wholly mine**, **wholly theirs** (touch nothing), or **mixed**.
- For mixed files, `git diff <base> -- <file>` and identify your hunks **positively**, by matching against edits you made. Never subtract hunks you recognize as someone else's: a peer whose work you haven't seen is exactly the peer you can't subtract.

## Step 1 - Stage
- Wholly-mine files: `git add <path>` (explicit paths, never `-A`/`-a`).
- Mixed files: hand-write a minimal patch containing only your hunks, then `git apply --cached --check mine.patch` before `git apply --cached mine.patch`. The working tree (peers' edits) stays untouched, and your patch's context lines must match the INDEX, not the working tree. That is why peers' uncommitted edits never belong in your patch: the index doesn't have them.
- To select hunks mechanically, select YOURS by number (positive selection):
  ```
  git diff <base> -- <file> > full.diff
  awk '/^@@/{h++} h==2 || h==5 || /^diff|^index|^---|^\+\+\+/' full.diff > mine.patch
  ```
  `h==N` keeps hunk N. The inverse form (`h!=N`, "drop the hunks I recognize") is the subtractive split that caused incident (2) above. Do not use it.
  One known leak: a dropped hunk that deletes a line beginning with `--` matches the header regex and bleeds into your patch as a fake `---` line. `--check` rejects the corrupt patch with a filename/header error; when you see that error, hand-remove the leaked line. The mandated `--check` exists to catch exactly this.
- **Entangled hunks.** When one hunk interleaves your edit and a peer's (you both touched the same function), hunk selection is too coarse. Edit the hunk body by hand: keep your `+` lines, delete the peer's `+` lines, restore the peer's `-` lines to plain context, then recount BOTH sides of the `@@` header. The Step 2 snapshot test is your net for miscounts. If you cannot separate authorship with confidence, do not guess: leave the file uncommitted and flag it in the report.
- If the repo's default branch is checked out, branch first.

## Step 2 - Prove the STAGED SNAPSHOT stands alone
Run the bundled checker (it exports the index via `checkout-index` and tests THAT, not the working tree):
```
bash ~/agent-armor/commit-mine/scripts/staged_check.sh [test command]
```
A red run has four causes. Triage in this order before touching the staging:
1. **Untracked-but-required files.** `checkout-index` exports tracked files only. Anything `??` in `git status` (artifacts you generated this session, fixtures you never added) is absent from the snapshot, and the failure looks identical to a staging gap. If your staged code needs it and it's yours, `git add` it.
2. **node_modules is absent** for the same reason. The test command runs with its cwd inside the snapshot, so link dependencies in:
   `bash .../staged_check.sh bash -c 'ln -s "<abs-repo-path>/node_modules" node_modules && npm test --silent'`
3. **A real staging-dependency gap**: you staged a consumer without its provider (or vice versa). Fix the staging, re-run.
4. **Suite cost.** When landing multiple commits, pass a scoped test command per intermediate commit and run the full suite once against the final staged state. Don't pay a 20-minute suite per commit.

One more checker honesty note: when no test command is given and none auto-detects, the checker prints a warning but **exits 0**. That is "nothing tested", not "proven standalone". In automation, always pass an explicit test command.

**Known blind spot, check by hand:** the suite can't catch references that only fire at runtime (lazy imports, daemon-thread targets, entrypoint wiring). Grep the staged additions for every symbol/module they call and confirm each is either staged or already in HEAD.

## Step 3 - Foreign-symbol check
The checker prints staged added lines (first 200; if your diff is larger, review `git diff --cached` in full). Scan them against your edit list: **any added symbol, import, or comment you don't recognize as yours is a peer's hunk. Unstage it** (`git restore --staged <file>` and re-split). Do not rationalize an unfamiliar line as "probably fine."

Binary files are invisible to this review: no added lines are printed, and hunk-splitting doesn't apply. Treat any modified binary you didn't generate as a peer's.

## Step 4 - Commit in logical stages, then push
- One coherent commit per concern; subject + body explaining why; the repo's trailer conventions.
- Repeat Step 2 per commit when committing in stages (scoped test command; full suite on the last).
- On push rejection: `git fetch origin` again, then `git log <branch>..origin/<branch>`. If histories are disjoint (a bot or peer pushed), `git rebase --autostash origin/<branch>` replays your commits; on a clean replay the autostash re-applies and the peers' dirty tree is restored. Never force-push a shared branch.
- **If the replay conflicts**, the peers' uncommitted edits are now held in the rebase autostash, which does NOT appear in `git stash list`; its commit SHA is recorded at `.git/rebase-merge/autostash`. Two safe exits: resolve and `git rebase --continue` (the autostash re-applies at the end), or `git rebase --abort` (restores the peers' edits; verified). Never `git reset --hard` or switch branches mid-rebase: that is how a peer's work gets stranded, which is the exact incident class this skill exists to prevent. If the rebase ends any other way (`git rebase --quit`, a dead session), git converts the autostash into a regular `stash@{0}: autostash` entry; recover with `git stash pop` once the tree is conflict-free, or `git stash apply <SHA from the file above>` as the last resort.

## When NOT to use this
- This skill is damage control for a tree that is already shared. If sessions are long-lived, or two sessions keep colliding in the same hot files, give each session its own `git worktree` and this entire procedure disappears. Surgery is for when you're already cut.
- If more than a couple of files need entangled-hunk surgery, coordination (let one session land first) is cheaper and safer than surgery.
- Binary-heavy work defeats both the patch-splitting and the foreign-symbol review. Don't share a tree for it.

## Report
List per commit: hash, files, and which were hunk-split. Note anything left intentionally uncommitted (peers' work, inseparable hunks) so the user knows the tree isn't dirty by accident.
