---
description: "Schema-first publisher for yiya.dev. Turn one durable, public-safe artifact from a Claude Code session into a typed content entry, after disclosure checks, a secrets scan, and the four-part quality gate. Reads live yiyaw-lab/yiyadev schemas, proves the entry with npm run build, then opens a PR or compare URL. Never merges. Modes: <artifact|path> | sweep | draft."
argument-hint: "<artifact|path> | sweep | draft <artifact|path>"
allowed-tools: Bash, Read, Write, Edit, Grep
---

Publish is the public-facing sibling of the `harvest` -> `milk` -> `vault` flywheel. It promotes only the few artifacts that are safe, specific, reusable, and verified enough to belong on yiya.dev. It never invents work and never merges its own PR.

## Non-Negotiables

- Run disclosure and secrets checks before rendering anything public.
- Publish receipts, not strategy. Redact or reject private project details, internal IDs, credentials, customer/user data, unshipped plans, and private taxonomy.
- Enforce the four-part gate: `Reusable`, `Non-trivial`, `Specific`, `Verified`. Reject with named reasons when any part fails.
- Read the live `yiyaw-lab/yiyadev` content files before writing. Treat every schema shown below as a snapshot, not authority.
- Prove every content edit with `npm run build` before opening a PR.
- Open a PR or provide a compare URL. Never push to `main`, merge, enable auto-merge, or batch unrelated artifacts.

## Target Repo Setup

Use an existing checkout first. Prefer `YIYADEV_REPO`, then `~/code/yiyadev`, then `~/yiyadev`, then `/tmp/yiyadev`.

```sh
target="${YIYADEV_REPO:-$HOME/code/yiyadev}"
if [ ! -d "$target/.git" ] && [ -d "$HOME/yiyadev/.git" ]; then target="$HOME/yiyadev"; fi
if [ ! -d "$target/.git" ] && [ -d "/tmp/yiyadev/.git" ]; then target="/tmp/yiyadev"; fi
if [ ! -d "$target/.git" ]; then
  if command -v gh >/dev/null 2>&1; then
    gh repo clone yiyaw-lab/yiyadev "$target"
  else
    git clone https://github.com/yiyaw-lab/yiyadev.git "$target"
  fi
fi
git -C "$target" fetch origin main
git -C "$target" checkout main
git -C "$target" pull --ff-only
```

If the private clone or push fails because credentials are unavailable, stop with the exact files/patch prepared and the GitHub compare URL that should be opened after authentication. Do not claim a PR exists unless it does.

## Live Schema Snapshot

Always re-read `src/content/*.ts`; this snapshot was checked on 2026-07-02 and may drift.

- `src/content/guides.ts`
  ```ts
  export type Guide = { title: string; body: string[] };
  export const guides: Guide[] = [];
  ```
  Use for reusable lessons and hard-won operating principles. Body is tight editorial prose, usually 2-4 paragraphs.

- `src/content/code.ts`
  ```ts
  export type CodeRepo = { title: string; note: string; href: string; tags: string[] };
  export const code: CodeRepo[] = [];
  ```
  Use only for public repos with real receipts in `href` and `tags`.

- `src/content/tools.ts`
  ```ts
  export type Tool = { name: string; note: string; get: string; href: string; tags: string[] };
  export const tools: Tool[] = [];
  ```
  Use only for small public builder tools. `get` is the human install/use line.

- `src/content/writing.ts`
  ```ts
  export type WritingCategory =
    | "Prior" | "Prediction" | "Pattern" | "Rethought"
    | "Replicated" | "Remains" | "Recursion" | "Unfalsifiable";
  export type Essay = {
    slug: string;
    title: string;
    dek: string;
    category: WritingCategory;
    date: string;
    readTime: string;
    href?: string;
    origin?: string;
    syndicated?: { platform: string; url: string }[];
    body?: string;
    tags?: string[];
    shelfLife?: "perishable" | "perennial";
    draft?: boolean;
  };
  export const essays: Essay[] = [];
  ```
  Use for substantial notes or essays. Prefer an on-site `body`; use `href`/`origin` only when the canonical piece lives elsewhere.

- `src/content/track-record.ts`
  ```ts
  export type TrackRecordStatus = "open" | "hit" | "partial" | "miss";
  export type TrackRecordEntry = {
    id: string;
    stated: string;
    claim: string;
    domain: "research" | "engineering" | "product";
    status: TrackRecordStatus;
    resolution?: string;
    resolved?: string;
    source?: string;
    sourceLabel?: string;
    draft?: boolean;
  };
  export const trackRecord: TrackRecordEntry[] = [];
  ```
  Use for dated bets and scored outcomes. `open` is allowed only for a real dated prediction. `hit`, `partial`, and `miss` require `resolution`, `resolved`, and evidence.

## Mode: `<artifact|path>`

1. Resolve one artifact. It can be a harvested finding, decision, session summary, build-log entry, scored prediction, shipped public repo, or explicit path. Read it fully.
2. Run the disclosure boundary and secrets scan. Search for API keys, tokens, `.env` content, credentials, private absolute paths, emails, customer/user data, private strategy, internal taxonomy, and unshipped plans.
3. Apply the four-part gate:
   - `Reusable`: useful beyond this one session.
   - `Non-trivial`: not generic advice or filler.
   - `Specific`: includes a concrete pattern, number, date, commit, test, repo, or outcome.
   - `Verified`: traceable to a real receipt.
4. Classify the artifact to exactly one target file: `guides`, `code`, `tools`, `writing`, or `track-record`.
5. Re-read the target file and nearby entries. Match its object shape, ordering, imports, trailing commas, and voice.
6. Create a branch in the `yiyadev` checkout:
   ```sh
   slug="<short-kebab-slug>"
   git -C "$target" checkout -B "publish/$slug"
   ```
7. Insert one typed entry. Keep the PR one artifact wide.
8. Run:
   ```sh
   cd "$target"
   npm ci --silent 2>/dev/null || npm install --silent
   npm run build
   ```
   Fix malformed entries until the build is green. Never open a red PR.
9. Commit and push:
   ```sh
   git -C "$target" add src/content
   git -C "$target" commit -m "Publish <short title>"
   git -C "$target" push -u origin "publish/$slug"
   ```
10. Open review without merging:
   ```sh
   if command -v gh >/dev/null 2>&1; then
     gh -R yiyaw-lab/yiyadev pr create --base main --head "publish/$slug" \
       --title "Publish <short title>" \
       --body "<source artifact, gate verdicts, validation command, and do-not-merge reminder>"
   else
     echo "Open PR: https://github.com/yiyaw-lab/yiyadev/compare/main...publish/$slug?expand=1"
   fi
   ```

## Mode: `sweep`

Scan the newest harvest outputs and propose candidates. Do not write files until the user picks one.

For each candidate, report:
- source artifact and receipt
- disclosure/secrets verdict
- four-part gate verdict
- target content file
- rendered draft object

If no candidate clears the bar, say so and open no PR. One excellent item beats a batch of weak ones.

## Mode: `draft <artifact|path>`

Run resolve, disclosure scan, gate, classification, live schema read, and rendering. Print the exact typed object and target file. Do not commit, push, or open a PR. If useful, temporarily insert and run `npm run build`, then revert the local draft before stopping.

## Voice

Match yiya.dev: austere, editorial, claim-free, receipts over adjectives. No hype, no vanity metrics, no generic AI boilerplate. If the artifact cannot be written without overclaiming, reject it.
