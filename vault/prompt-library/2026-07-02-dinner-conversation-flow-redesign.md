---
title: "Dinner Conversation Flow Redesign"
saved_at: "2026-07-02"
source: "conversation"
tags:
  - product-design
  - family-learning
  - sms-flow
  - dinner-conversation
  - lifecycle-nudge
auto_fire:
  trigger_when:
    - "User asks to design or redesign a lifecycle flow using stored family or child personalization."
    - "User asks to add opt-in, nudge, setup, or reactivation messaging for an existing live user base."
    - "User asks to turn methodology or research data into a product flow."
  avoid_when:
    - "The request is only a one-off copy tweak or support reply."
    - "The request would send production messages without an explicit authorized send path."
    - "The request is unrelated to family learning, onboarding, lifecycle messaging, or parent-mediated experiences."
  confidence_threshold: "high"
  suggested_mode: "ask_first"
---

# Dinner Conversation Flow Redesign

## Original Prompt

> once the database is robust, redesign the dinner conversation flow drawing from database's insights - and for current users who didn't get to opt in for the dinner conversation feature, send them a text to nudge them to set it up

## Augmented Reusable Prompt

Redesign the dinner conversation flow for `[PROJECT]` using the existing evidence-informed methodology database and the product's stored family/child personalization data.

Objectives:
- Turn dinner conversation into a distinct family-level experience, not a generic quest or child assignment.
- Draw from the methodology database to generate prompts that support curiosity, epistemic honesty, perspective-taking, moral reasoning, and critical thinking.
- Use each family's known context: child profiles, ages, interests, past quests, child responses, parent feedback, successful patterns, avoidances, and preferred settings.
- Preserve core product metrics by keeping dinner conversation separate from quest completion unless the product explicitly supports dinner-response tracking.
- Add a compliant opt-in path for existing users who never saw the dinner conversation setup.

Required deliverables:
- Updated data model or state design for dinner opt-in status, dinner time, setup prompt history, and nudge tracking.
- Updated onboarding/SMS flow for new families.
- A safe current-user nudge mechanism that dry-runs before sending and only targets eligible opted-in users.
- Dinner prompt generation logic that uses the methodology database and family personalization.
- Guardrails for SMS compliance, opt-out, rate limiting, and avoiding medical/therapeutic/developmental guarantees.
- Verification plan covering local validation, build/type checks, and production rollout steps.

Quality bar:
- Dinner prompts should feel table-ready, warm, concise, and parent-mediated.
- Do not make dinner prompts feel like homework, quizzes, therapy, or performance tasks.
- Do not send production messages until there is a reviewable, authorized, dry-run path.
- Document the operator path for dry run, send, and rollback.

## Reuse Notes

- Reuse for any feature that turns stored personalization and methodology data into a new lifecycle flow.
- Replace `[PROJECT]` with the app or repo name.
- If the product has live users, keep the nudge path opt-in, auditable, and dry-run-first.
- Auto-fire only when the request clearly involves lifecycle flow design or user messaging; ask first before any production send.
