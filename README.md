# claude-code-skills

Working skills from my Claude Code setup. Every one of them runs my actual day: they have shipped real branches, caught real bugs, and billed real tokens. A skill lands in this repo only after it has survived contact with my own work.

I'm [yiya](https://yiya.dev), a non-traditional engineer building in public on [X @yiyadev](https://x.com/yiyadev). I work on a few projects ([Synapi](https://synapi.app) is one), but the machine I care most about is a company brain plus a factory that builds itself. These skills are its working parts, and the build log for all of them is on X.

The common thread: **agents are cheap, verification is the product.** Most of these skills exist to make an agent prove its work instead of describe it. Pinned done-checks with negative controls. Fresh-context reviewers told to refute, not approve. Measured token economics instead of vibes. Staged-snapshot tests instead of "looks right." The first overnight run of `/nightshift` shipped 6 of 6 tasks at $11.52 per shipped task, and the one defect of the night was caught by exactly this discipline: an agent gamed its own done-check and the adversarial reviewer refused it.

## Skills, by function

Seventeen skills, grouped by what they actually do. They compose into one loop — *verify the work, bank what's durable, sharpen the tools, ship the gold* — but each runs standalone.

```
  claude-code-skills · by function
  ───────────────────────────────────────────────────────────────────
  VERIFICATION & PURSUIT       make the agent prove its work
     until · nightshift · commit-mine · page-audit
  ───────────────────────────────────────────────────────────────────
  THE SESSION FLYWHEEL         capital in and out of every session
     harvest → capitalize → milk · stash · burn
  ───────────────────────────────────────────────────────────────────
  JUDGMENT & SELF-IMPROVEMENT  the suite grades and sharpens itself
     grade-session · hone · taste
  ───────────────────────────────────────────────────────────────────
  KEEP IT LEAN & CURRENT       cut what shouldn't exist, track the edge
     raze (alias: elonize) · frontier
  ───────────────────────────────────────────────────────────────────
  BUILD-IN-PUBLIC & AUTHORING  turn work into shareable craft
     card · snip · prompt
  ───────────────────────────────────────────────────────────────────
```

### Verification & pursuit — make the agent prove its work
| Skill | What it does |
|-------|--------------|
| [until](until/) | Goal-pursuit engine: pin a verifiable objective, then attempt, verify, adjust until it is done. Negative-control checks so a passing test means something, a hypothesis ledger that forbids re-testing refuted ideas, git checkpoints, and a forced escalation ladder ending in fresh-context subagents. Survives session death via a state file. |
| [nightshift](nightshift/) | The night shift. Call it at bedtime: it builds its own worklist across your active repos, executes under an absolute safety contract (branches only, nothing irreversible, nothing outward-facing), double-verifies every task with a pinned binary done-check plus a fresh-context reviewer told to refute it, and leaves a 2-minute morning brief with measured dollars-per-shipped-task economics. |
| [commit-mine](commit-mine/) | Commit only this session's work out of a dirty tree that parallel agent sessions are also editing. Positive hunk selection, a staged-snapshot test that runs the suite against the index rather than the working tree, and a foreign-symbol check before every commit. Ships the checker script. |
| [page-audit](page-audit/) | Audit a local HTML page the trustworthy way: measurements are facts, screenshots are testimony. An instrumented iframe harness reports overflow and element widths per viewport before any screenshot, then modern headless Chrome captures with animations neutralized. Includes a catalogue of headless-rendering artifacts that look like bugs and aren't. |

### The session flywheel — capital in and out of every session
| Skill | What it does |
|-------|--------------|
| [harvest](harvest/) | Reap an ending session for everything durable, so the next run starts richer: full transcript, durable findings/decisions docs, a candid graded report card (delegated to `grade-session`), a build-log entry, banked memory lessons, then an auto-staged build-in-public `/card` or `/snip` of the session's most shareable gold (disclosure-gated). A python script does the mechanical half; the model does the interpretive half from what it just lived. |
| [capitalize](capitalize/) | The inbound half of the flywheel: at session start, withdraw the capital `harvest` deposited (findings, decisions, until-ledgers, ruled-out dead ends) and deploy the slice relevant to THIS task as a ready brief, so a fresh session starts warm instead of paying rent to re-learn the project. Executes nothing; ends in a menu you steer. Modes: prime / compound / statement. |
| [milk](milk/) | Tap ONE rich asset mid-session — a deep-research report, a competitor repo, a paper, a long thread — and squeeze every durable drop (findings, decisions, saveable prompts, lessons) into your stores, without ending the session. Four-part gate + search-existing-first dedupe. Re-milkable. |
| [stash](stash/) | Zero-friction capture inbox for the thought that flies past mid-task: park it in one line, keep working, drain it later into the gated skill that owns its destination. A waiting room, not a store — an item leaves only by landing somewhere durable. Capture is trivial; the drain is the product. |
| [burn](burn/) | Token-economics engine: audit where a session's tokens actually went (with real-$ math from transcript usage), pay down "session rent" by writing re-learned facts where they load once, and install structural spend disciplines — built on agentic billing mechanics, not "be concise" tips. Modes: audit / rent / charter. |

### Judgment & self-improvement — the suite grades and sharpens itself
| Skill | What it does |
|-------|--------------|
| [grade-session](grade-session/) | The report card, standalone: two candid graded tables (your prompting, the agent's performance) plus a coach note for each side. Straight A's count as failed grading. No dependencies; prints in chat. Also the single source `/harvest` delegates its grading to. |
| [hone](hone/) | Closes the grade→improvement loop: reads the accumulated `grade-session` report cards, finds failures that RECUR across sessions, and proposes surgical edits to the skill bodies that caused them — writing only on approval. The suite's self-improvement layer (recurrence-gated, propose-on-approval, lane-disciplined). Modes: sweep / audit / `<skill>`. |
| [taste](taste/) | Distill your revealed taste from real session transcripts into an enforceable personal rubric, then apply it as a pre-delivery filter. Mines what you actually corrected and accepted — never what you say you prefer. Modes: induce / apply / audit. |

### Keep it lean & current — cut what shouldn't exist, track the edge
| Skill | What it does |
|-------|--------------|
| [raze](raze/) | Apply the razor: question every requirement, then DELETE whole parts/processes before any optimization (Musk's Algorithm; "the best part is no part"). A "should this EXIST at all" scythe, not a tidy-up. Propose-on-approval, a ≥80 unused-confidence gate, branch-only, graded by a two-sided add-back rate. Alias: `/elonize`. |
| [frontier](frontier/) | "Am I at the frontier?" — for any SURFACE (design, model stack, infra, content...), audit where your work has fallen behind the live current standard (benchmarked against that surface's frontier exemplars) and, on approval, provision the current frontier toolchain. The external standard-SETTER: discovers live (no baked-in tool list), adopts under raze's additive-safety contract. Modes: audit / plan / apply / refresh. |

### Build-in-public & authoring — turn work into shareable craft
| Skill | What it does |
|-------|--------------|
| [card](card/) | Stages one insight as a designed, share-ready PNG in a modern product aesthetic (gradient accents, glassy pills, ambient glow), rendered from HTML/CSS via headless Chrome. Reads the house visual system from `DESIGN_SYSTEM.md`. `/snip` shows source; `/card` stages an idea. |
| [snip](snip/) | Turns any file or snippet into a build-in-public bundle: disclosure-boundary and secrets check first, then a freeze-rendered PNG in a house style, a draft post caption, and a posted/not-posted index. |
| [prompt](prompt/) | Prompt library plus compiler: save frequent prompts as parameterized templates, invoke them by name (type 3 words, run the 80-word version), or refine a draft for effect per token by front-loading your acceptance criteria. Ships with starter templates. |

## Start here

If you take one skill, take `until`: it changes what "done" means for everything else you run. If you take two, add `nightshift`, which runs its tasks as until-style pursuits while you sleep. If agents step on each other in one repo, `commit-mine` is the painkiller. And if you want the compounding system, the flywheel is `harvest` → `capitalize` (deposit at session end, withdraw at the next start), with `hone` quietly sharpening the skills themselves from their own report cards.

## Install

Each skill folder has a `SKILL.md` and sometimes a `scripts/` directory or example data file.

```sh
# the skill (as a slash command)
cp harvest/SKILL.md ~/.claude/commands/harvest.md

# its script, if it has one
mkdir -p ~/.claude/scripts
cp harvest/scripts/session_to_markdown.py ~/.claude/scripts/

# card and frontier reference a house visual system — grab the example
cp DESIGN_SYSTEM.md ~/.claude/DESIGN_SYSTEM.md
# frontier also reads an editable per-surface map
mkdir -p ~/.claude/frontier && cp frontier/surfaces.md ~/.claude/frontier/surfaces.md
```

Some skills reference my personal conventions: a `private/` folder taxonomy, memory files, a `TASTE.md` rubric, a `DESIGN_SYSTEM.md`. Those references are the load-bearing part. Swap in your own conventions and the skills get sharper, not weaker; a verification loop tuned to nobody verifies nothing.

These are shared as working parts, not a maintained library. Issues and PRs are welcome, and the contract is honest: this repo updates when my own workflow does.
