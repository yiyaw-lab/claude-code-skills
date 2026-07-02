---
title: "Worldly Moral Feature Ideas"
saved_at: "2026-07-02"
source: "conversation"
tags:
  - product-strategy
  - moral-reasoning
  - critical-thinking
  - current-events
  - family-learning
auto_fire:
  trigger_when:
    - "User asks for feature ideas grounded in a methodology, evidence, or research database."
    - "User asks to make family or education prompts more moral, worldly, current-events-aware, civically relevant, or critical-thinking oriented."
    - "User asks for dinner conversation improvements involving dilemmas, societal tensions, future readiness, or perspective-taking."
  avoid_when:
    - "The request asks for live news coverage, partisan advocacy, or reactive commentary."
    - "The request is implementation-only with no strategy or product design component."
    - "The request involves age-inappropriate, fear-based, or ideologically prescriptive content."
  confidence_threshold: "medium"
  suggested_mode: "silent_reference"
---

# Worldly Moral Feature Ideas

## Original Prompt

> then draw from the database and suggest any new features or improve existing features (maybe the dinner convo could be tied to current events/moral dilemmas/societal tensions to stay relevant and interesting) to best support our families to raise exceptionally moral, curious, worldly, critically-thinking children

## Augmented Reusable Prompt

Use the evidence-informed methodology database for `[PROJECT]` to propose new features and improvements that help families raise children who are morally grounded, curious, worldly, intellectually humble, and strong critical thinkers.

Focus areas:
- Moral reasoning and values reflection.
- Epistemic honesty, uncertainty calibration, and source sense.
- Perspective-taking across disagreement.
- Systems thinking and tradeoff reasoning.
- Creative problem-solving and future readiness.
- Parent-mediated family conversation, especially dinner-table prompts.

Explore whether dinner conversation should include a carefully curated "world context" layer based on current events, moral dilemmas, civic tensions, technological change, or societal tradeoffs.

Constraints:
- Do not turn the product into a child-facing news feed.
- Avoid partisan framing, fear-based content, sensational news, and age-inappropriate topics.
- Prefer "current-event adjacent" prompts: neutral, durable issue cards inspired by the world, not live reactive news summaries.
- Keep parents in control of sensitivity level and topic preferences.
- Preserve SMS simplicity and avoid adding app-like complexity unless the payoff is clear.
- Ground recommendations in the methodology database and state which technique each feature draws from.

Deliverables:
- Prioritized feature list with rationale.
- Risks and guardrails for each feature.
- Smallest shippable version.
- Data or schema needed, if any.
- How the feature would personalize over time.
- Example prompts/messages for at least three age bands.

Success criteria:
- Features should make families' conversations richer without making parents feel lectured.
- Children should practice thinking, not receive ideology.
- The system should become more personalized, culturally aware, and morally serious while staying warm and practical.

## Reuse Notes

- Reuse for product strategy passes that should translate a methodology database into concrete features.
- Strong fit for education, family, civic-learning, and AI companion products.
- Customize the values, age bands, and sensitivity boundaries before reuse.
- Auto-fire as background strategy context for relevant feature ideation; surface it explicitly only when it changes the recommendation.
