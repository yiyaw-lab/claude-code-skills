---
description: Sync a skill from ~/.claude/commands/<x>.md to the public skills repo (yiyaw-lab/agent-armor; local clone ~/code/claude-code-skills) as <x>/SKILL.md — disclosure+secrets gate first, README bookkeeping (badge count, playbook diagram, catalog row) handled, then a PR with CI green; merge only on explicit approval. Curated: only named skills, never a bulk export. Modes: <skill-name> | sweep | audit.
argument-hint: "<skill-name> | sweep | audit"
---

The law this skill runs on: **a public mirror rots silently.** The suite's skills are sharpened in place (~/.claude/commands — /hone edits them, lessons fold in), but the public copies in the skills repo update only when someone remembers — so the repo's contract ("this armor updates when my own workflow does") decays into stale copies and a wrong skill count. mirror makes that update a checked procedure: one command takes a named skill from the private commands dir to a reviewed PR on the public repo, with the disclosure gate and the README bookkeeping nobody remembers by hand.

**Three hard invariants:**
- **Curated, never bulk.** Mirror ONLY the skill(s) the user names, or already-public skills that drifted. Presence in ~/.claude/commands is NOT admission — the repo's bar is "survived contact with real work," and the user decides what's public (some skills stay private on purpose: personal pipelines, unproven drafts).
- **Nothing leaves the machine unscanned.** Before writing into the clone: a secrets scan (keys/tokens/bearer strings) and a disclosure scan (private paths, client/project names not already public, identifiers beyond the repo's own voice). A hit = stop and surface; never silently redact.
- **PR-gated; merge is a per-run human call.** Push a branch, open the PR, wait for the repo's validate-skills CI. Merge only when the user says so in THIS run (a standing "publish it" in the invocation counts). Never force-push, never commit to main directly.

## /mirror <skill-name>
1. **Sync the clone first:** `git -C ~/code/claude-code-skills pull --ff-only` — a mirror from a stale clone re-introduces what was already fixed upstream.
2. **Read the source** `~/.claude/commands/<x>.md` and run both scans (invariant 2).
3. **Transform = copy, honestly.** `<x>/SKILL.md` carries the same frontmatter (description, argument-hint) and body verbatim. Private-convention references (memory files, `private/` taxonomy, TASTE.md) STAY — the README already tells readers to swap in their own conventions; flag anything that would genuinely confuse a public reader rather than silently rewriting it. If the skill ships a script, copy it under `<x>/scripts/`.
4. **README bookkeeping** (the part nobody remembers): a NEW skill bumps the `skills-N` badge AND the prose count, joins its playbook-diagram line, and gets a catalog row in the section that owns it, written in that table's register. An UPDATE changes no counts. Badge, prose, diagram, and table must agree — CI validates skills, not the README; mirror owns that agreement.
5. **Branch, commit, PR:** branch `skill/<x>`, explicit `git add` of only the touched files (never `-A`), commit, push, `gh pr create`. Wait for the `validate` check; report its verdict + the PR URL.
6. **Merge on approval only** (invariant 3). After merging, confirm the default branch actually contains the change and report.

## /mirror sweep
For every repo dir with a same-named `~/.claude/commands/<x>.md`, diff `<x>/SKILL.md` against the command body. Report four buckets: **IN-SYNC** · **DRIFTED** (public copy stale — summarize what changed privately) · **PRIVATE-ONLY** (in commands, not mirrored — candidates; the user picks) · **REPO-ONLY** (mirrored but no local command — flag it, NEVER delete; it may be another machine's skill). Propose which drifted ones to sync; execute per approval, batched or per-skill as the user prefers.

## /mirror audit
Read-only: the same four-bucket report; propose nothing, write nothing.

## Rules
- **Lane discipline:** /publish owns yiya.dev content; /harmonize converges internal parts on a named standard; a skill-body EDIT is /hone's job. mirror owns exactly the cross-repo publication mechanics for the skills repo: scan → copy → README bookkeeping → PR.
- **Never delete on sweep;** REPO-ONLY is a flag, not a cleanup target.
- **Honest empty result:** nothing named and nothing drifted = say so and write nothing.
