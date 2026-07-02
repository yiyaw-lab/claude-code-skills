---
title: "Pre-Enrichment Decision Policy"
saved_at: "2026-07-02"
source: "conversation"
tags:
  - prompt-enrichment
  - agent-workflow
  - decision-policy
  - prompt-library
  - codex-behavior
auto_fire:
  trigger_when:
    - "User asks when or how Codex should pre-enrich a prompt before implementing."
    - "User asks for automatic prompt augmentation, prompt routing, or agent behavior policies."
    - "A broad or high-impact prompt appears under-specified but has clear strategic intent."
  avoid_when:
    - "The user gives a precise implementation request that should be executed literally."
    - "The user is debugging an urgent failure and enrichment would slow the fix."
    - "The enrichment would change the user's latest instruction instead of clarifying it."
  confidence_threshold: "high"
  suggested_mode: "silent_reference"
pre_enrichment:
  enrich_when:
    - "The request is strategic, multi-step, research-heavy, architectural, or product/design oriented."
    - "The user intent is clear but compressed, with implied quality bars or validation needs."
    - "A saved prompt pattern matches at high confidence and no guardrail blocks it."
  skip_when:
    - "The request is a direct command, exact code edit, narrow bug fix, or specific correction."
    - "The user explicitly asks not to expand scope."
    - "Pre-enrichment would introduce unrequested production, compliance, or external-send behavior."
  default_behavior: "internal"
---

# Pre-Enrichment Decision Policy

## Original Prompt

> can u make it so codex auto decides when to pre-enrich a prompt

## Augmented Reusable Prompt

Design an agent-side decision policy for `[AGENT_OR_WORKSPACE]` that determines when a user prompt should be pre-enriched before execution.

Objective:
- Let the agent improve broad or compressed prompts before acting, without making the workflow slower, noisier, or less faithful to the user's intent.
- Keep pre-enrichment mostly internal unless the expanded interpretation changes scope, adds risk, or requires confirmation.

Decision policy:
- Execute literally when the user gives a precise implementation request, direct command, urgent debugging task, or specific correction.
- Internally enrich when the user intent is clear but compressed, and the task is broad, strategic, research-heavy, architectural, product/design-oriented, or multi-step.
- Show a brief enriched frame when it materially affects sequencing, validation, deliverables, or the definition of success.
- Ask first when there are multiple plausible interpretations or when the enriched version would affect production systems, external sends, money, accounts, compliance, private data, or destructive operations.

Retrieval behavior:
- Check saved prompt metadata for matching `trigger_when` and `enrich_when` signals.
- Respect `avoid_when` and `skip_when` before applying a saved prompt.
- Use at most one or two saved prompt patterns unless the user asks for a broader strategy pass.
- Let the newest user instruction, current repo context, and safety/tooling rules override saved prompts.

Output behavior:
- Do not show the full augmented prompt by default.
- If pre-enrichment shapes the work, mention the chosen frame briefly.
- If confidence is medium, present the saved prompt as a candidate or ask one clarification.

Success criteria:
- The agent produces deeper work on broad prompts without drifting from the ask.
- The user does not have to manually request prompt augmentation every time.
- The system remains conservative around irreversible, external, or production-impacting actions.

## Reuse Notes

- Reuse when building prompt libraries, agent operating procedures, Codex skills, or internal AI workflow policies.
- Customize `[AGENT_OR_WORKSPACE]` and the production-risk categories for the environment.
- Keep pre-enrichment invisible by default; only surface it when it materially changes the work.
