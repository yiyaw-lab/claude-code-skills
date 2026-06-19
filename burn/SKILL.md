---
description: Token-economics engine — audit where a session's tokens actually went (with $ math from real transcript usage data), pay down "session rent," and enforce structural spend disciplines that cut cost without touching quality. Built on agentic billing mechanics, not "be concise" tips. Modes: audit | rent | charter.
argument-hint: "audit [session|N sessions] | rent | charter"
---

Four laws this skill runs on — they're how agentic billing actually works, not generic advice:

1. **Main context is a subscription, not a purchase.** Every token read into the main loop is re-billed on every subsequent turn (fully, whenever the prompt cache misses). A 5k-token file read in turn 3 of a 40-turn session can cost 35× its size. Subagents pay once: they read in their own context and return only conclusions.
2. **Output is ~5× the price of input.** The agent's own verbosity is the most expensive text in the room. Long final reports the user skims cost more than the file reads that produced them.
3. **Every avoidable round-trip re-bills the conversation.** A clarifying question the agent could have answered itself = a whole extra turn of context, plus a likely cache expiry during the human delay (5-min TTL). Questions are the most expensive tokens in the system.
4. **Every session pays rent.** The fixed cost of re-learning the project — re-reading the same configs, re-discovering the same conventions — is billed at session start, every session, until the knowledge is written down where sessions load it.

## /burn audit [N sessions | session]
Write a quick python script over `~/.claude/projects/**/*.jsonl` (newest N, default 3). Assistant records carry `.message.usage` — `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`. Measure:
- **Spend shape**: total in/out/cache-read per session; cache hit rate; turns that paid full re-read (cache miss after a gap).
- **Law-1 violations**: tool_result bytes landed in main context, grouped by tool; files Read more than once (path-level dedup); large reads that never changed a decision.
- **Law-2**: output tokens per assistant turn; flag the long-report tail.
- **Law-3**: agent questions that the next user message answered with information already available in the session.
- **Law-4**: facts re-discovered across sessions of the same project (same files re-read on day 1 of every session).
Get CURRENT per-token pricing before computing $ — use the claude-api skill or docs; NEVER hardcode prices from memory. Report: $ by category, the top 3 leaks, and the one structural change that saves the most.

## /burn rent
Pay down session rent for the current project: diff "what this session had to re-learn" against CLAUDE.md / memory. Anything re-discovered (build commands, conventions, gotchas, where things live) gets written into CLAUDE.md — tersely, it's loaded every session, so it has its own carrying cost: only facts that save more than they weigh. Report what was added and the estimated rent reduction.

## /burn charter
Install (or update) a `## Token discipline` section in the project's CLAUDE.md encoding the structural rules — these save spend WITHOUT quality loss because each cuts tokens that don't change decisions, never tokens that do:
- **Fan-out reads go to subagents**; only conclusions enter the main loop. Never paste >100 lines into main context when a subagent could return the 5-line answer. (Quality guard: ambiguous/critical code gets a FULL subagent read, not a skim — the saving is in placement, not depth.)
- **Cheapest sufficient verification**: prefer the single failing test over the suite, `--quiet`/`tail` over full logs, targeted greps over directory dumps. (Quality guard: never skip verification — downgrade its verbosity, not its existence.)
- **Batch independent tool calls in one turn**; batch questions to the user into one ask (each separate ask = one re-billed conversation + one cache expiry).
- **Don't re-read what the harness tracks**: no Read-after-Edit verification, no re-Read of files already in context.
- **Final reports state decisions and evidence, not narrative**: what changed, what's verified, what's next. Length budget scales with what the user will act on, not with how much work was done.
- **Never economize on**: verification existing, reading code you're about to change, surfacing failures honestly. A wrong answer is the most expensive token sequence possible — one bad merge buys a year of file reads.

## Rules
- Quality is the constraint, not the variable: every recommendation must name what it deliberately does NOT cut.
- Measure before prescribing — audit findings drive charter emphasis, not vibes.
- Savings claims get real numbers from usage data, never estimates presented as measurements.
