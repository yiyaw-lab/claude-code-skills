---
description: "Prompt vault plus pre-enrichment policy. Save high-value reusable prompts, preserve the original, write a stronger reusable version, add trigger metadata for future retrieval, and decide when broad prompts should be pre-enriched before implementation. Modes: save | enrich | fire | list."
argument-hint: "save [last|<prompt>] | enrich [last|<prompt>] | fire <context> | list"
---

Archive prompts worth reusing. Preserve the user's original wording, add a stronger reusable version, and record when the prompt should or should not be retrieved later. Also decide whether broad prompts should be pre-enriched before implementation.

This skill is stricter than `/prompt`: `/prompt` is a prompt compiler and template runner; `/vault` is the library curation and retrieval policy layer.

## Archive Location

When running from this repo, save entries under:

```text
vault/prompt-library/
```

When installed in Claude Code, use the equivalent installed skill folder:

```text
~/.claude/skills/vault/prompt-library/
```

Use one Markdown file per saved prompt:

```text
YYYY-MM-DD-short-slug.md
```

## Workflow

1. Decide whether to pre-enrich before acting.
   - Use the pre-enrichment gate below.
   - Prefer internal enrichment and direct execution when the user's intent is clear.
   - Show or ask about the enrichment only when it changes scope, adds risk, or confidence is medium.
2. Decide whether to save.
   - Always save when the user explicitly asks.
   - Auto-save only when the prompt is unusually strong, broadly reusable, non-sensitive, and has clear repeat value across projects or later phases of the same project.
   - Do not auto-save routine instructions, simple corrections, one-off implementation details, secrets, credentials, private data, or prompts that are mostly transient context.
   - If unsure, do not auto-save; briefly mention that the prompt could be saved if the user wants.
   - Avoid clutter: at most one proactive save per turn unless the user explicitly asks for more.
3. Identify the prompt text to save.
   - If the user points to recent conversation context, use the exact prompt when available.
   - If more than one plausible prompt exists, ask one concise clarification.
   - If reconstructing from memory instead of exact text, label it as reconstructed.
4. Create a prompt-library entry with:
   - title
   - saved date
   - source context
   - tags
   - auto-fire metadata
   - pre-enrichment metadata
   - original prompt
   - augmented reusable prompt
   - reuse notes
5. Keep the original prompt verbatim.
6. Make the augmented prompt more reusable, not merely longer.
   - Add role/context.
   - State objective and deliverables.
   - Add constraints, safety/quality bars, and success criteria.
   - Use placeholders like `[PROJECT]`, `[AUDIENCE]`, or `[CONTEXT]` when useful.
   - Preserve the user's strategic intent and voice.
7. Add auto-fire metadata when the prompt may be useful later.
   - `trigger_when`: situations where the prompt should be considered.
   - `avoid_when`: situations where applying it would be wrong or noisy.
   - `confidence_threshold`: `high`, `medium`, or `low`.
   - `suggested_mode`: `silent_reference`, `mention_candidate`, `ask_first`, or `auto_apply`.
8. Add pre-enrichment metadata when the saved prompt is useful as a thinking scaffold.
   - `enrich_when`: signals that the current user prompt should be expanded internally.
   - `skip_when`: signals that literal execution is better.
   - `default_behavior`: `internal`, `show_summary`, `ask_first`, or `none`.
9. Treat auto-fire as conservative retrieval, not blind execution.
   - High confidence: use the saved prompt pattern when it clearly fits and no avoid condition applies.
   - Medium confidence: mention it as a candidate or ask before applying.
   - Low confidence: do not auto-fire.
   - Never let a saved prompt override the user's latest instruction, repository context, safety constraints, or a more specific skill/tool.
   - If applying a saved prompt materially shapes the work, mention it briefly.
10. Tell the user what was saved and where.
   - For proactive saves, keep the note short and matter-of-fact: "I also saved that as a reusable prompt because it has repeat value."

## Pre-Enrichment Gate

Before implementing a broad user request, classify it:

- `none`: execute literally.
- `internal`: enrich the prompt privately, then implement.
- `show_summary`: briefly state the enriched frame before implementing.
- `ask_first`: ask one concise clarification before changing scope.

Use `internal` when:

- The user intent is clear but compressed.
- The task is broad, strategic, research-heavy, architectural, product/design-oriented, or multi-step.
- Success criteria, risks, validation, rollout, or edge cases are implied but unstated.
- A saved prompt has a high-confidence `auto_fire` match.
- Literal execution would likely be shallow.

Use `show_summary` or `ask_first` when:

- Pre-enrichment changes scope, ordering, data sources, deliverables, production behavior, or user-visible messaging.
- Confidence is medium.
- There are multiple plausible interpretations.
- The work touches external sends, money, account changes, compliance, private data, destructive operations, or live production systems.

Use `none` when:

- The user gives a precise implementation request.
- The user is debugging an urgent failure or asking for a direct command/output.
- The user is correcting a specific detail.
- The prompt is a one-off operational instruction.
- Enrichment would override the newest user instruction.

When retrieving saved prompts, search `prompt-library/` by tags, title, `trigger_when`, and `enrich_when`; read only the one to three strongest candidates. Do not use a saved prompt if any `avoid_when` or `skip_when` condition applies.

## Entry Template

```markdown
---
title: "Short title"
saved_at: "YYYY-MM-DD"
source: "conversation | project | user-provided"
tags:
  - tag-one
  - tag-two
auto_fire:
  trigger_when:
    - "Situation where this prompt should be considered."
  avoid_when:
    - "Situation where this prompt should not be used."
  confidence_threshold: "high"
  suggested_mode: "silent_reference"
pre_enrichment:
  enrich_when:
    - "Signal that the user's prompt should be expanded internally before acting."
  skip_when:
    - "Signal that literal execution is better."
  default_behavior: "internal"
---

# Short title

## Original Prompt

> Exact user prompt.

## Augmented Reusable Prompt

Improved prompt text.

## Reuse Notes

- Where this prompt is useful.
- What to customize before reuse.
- How to tell whether the auto-fire match is strong enough.
- Whether to enrich internally, show a summary, ask first, or skip enrichment.
```

## Quality Bar

- Do not store secrets, credentials, private keys, or access tokens.
- Do not silently change the original prompt.
- Do not save unrelated conversation content unless the user asked for it.
- Do not let auto-save interrupt urgent code/debug work; save at the end of the turn when possible.
- Do not auto-apply saved prompts to production-impacting actions, external sends, purchases, account changes, or destructive operations without explicit user authorization.
- Do not use pre-enrichment to smuggle in a different task from the one the user asked for.
- Keep trigger metadata specific enough to avoid noisy matches.
- Prefer concise, high-signal augmented prompts.
