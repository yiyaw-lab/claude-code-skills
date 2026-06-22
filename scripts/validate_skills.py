#!/usr/bin/env python3
"""Validate the agent-armor skill suite — make the repo prove its own thesis.

The thesis here is "make an agent prove its work, not describe it." This script
is that practice turned on the repo itself: it refuses to take the suite's word
that it is well-formed and instead checks it. Stdlib only (no PyYAML).

Checks, run over every */SKILL.md in the repo root:
  1. FRONTMATTER — each SKILL.md opens with a YAML frontmatter block delimited
     by `---` lines, that block parses, and it carries the identifying keys a
     Claude Code skill needs: a non-empty `description` in the frontmatter, and
     a `name` — which by Claude Code convention is the skill's folder name. The
     folder name must be a valid skill slug (lowercase / digits / hyphens). A
     SKILL.md with no parseable frontmatter, or with an empty/absent
     `description`, FAILS.
  2. SCRIPTS COMPILE — every */scripts/*.py compiles under `py_compile`.
  3. SKILL LINKS — no SKILL.md markdown-links to a sibling skill directory that
     does not exist.

Exit non-zero on any failure; print a per-check report either way.

Usage:
  python3 scripts/validate_skills.py        # from the repo root
"""
from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Valid skill-name slug: lowercase letters, digits, hyphens (the folder name,
# which Claude Code uses as the skill's `name`).
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Matches markdown links whose target is a bare sibling directory, e.g. `](until/)`.
DIR_LINK_RE = re.compile(r"\]\((?!https?://|/|#)([A-Za-z0-9._-]+)/\)")


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """Parse a leading `---`-delimited YAML frontmatter block with a stdlib-only
    line parser sufficient for this suite's flat `key: value` frontmatter.

    Returns (mapping, None) on success, or (None, error_message) on failure.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "no opening '---' frontmatter delimiter on line 1"

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "no closing '---' frontmatter delimiter"

    mapping: dict[str, str] = {}
    last_key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        # Continuation line (folded/indented value) for the previous key.
        if last_key is not None and (raw.startswith((" ", "\t"))) and ":" not in raw.split("#", 1)[0]:
            mapping[last_key] = (mapping[last_key] + " " + raw.strip()).strip()
            continue
        if ":" not in raw:
            return None, f"frontmatter line is not 'key: value': {raw!r}"
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip()
        # Strip a single layer of matching surrounding quotes.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        mapping[key] = value
        last_key = key
    return mapping, None


def check_frontmatter(skill_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for sf in skill_files:
        rel = sf.relative_to(REPO_ROOT)
        text = sf.read_text(encoding="utf-8")
        mapping, err = parse_frontmatter(text)
        if err is not None:
            errors.append(f"{rel}: {err}")
            continue
        # `description` must be present and non-empty in the frontmatter.
        if not mapping.get("description"):
            errors.append(f"{rel}: missing or empty required frontmatter key 'description'")
        # `name` is the folder name by Claude Code convention; require it to be a
        # valid skill slug. If the frontmatter also declares `name`, honor that.
        name = mapping.get("name") or sf.parent.name
        if not SLUG_RE.match(name):
            errors.append(f"{rel}: skill name {name!r} is not a valid slug (lowercase/digits/hyphens)")
    return errors


def check_scripts_compile(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for py in sorted(repo_root.glob("*/scripts/*.py")):
        rel = py.relative_to(repo_root)
        try:
            py_compile.compile(str(py), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{rel}: does not compile: {exc.msg.strip()}")
    return errors


def check_skill_links(skill_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for sf in skill_files:
        rel = sf.relative_to(REPO_ROOT)
        text = sf.read_text(encoding="utf-8")
        for target in DIR_LINK_RE.findall(text):
            candidate = REPO_ROOT / target
            if not candidate.is_dir():
                errors.append(f"{rel}: links to skill directory '{target}/' which does not exist")
    return errors


def main() -> int:
    skill_files = sorted(REPO_ROOT.glob("*/SKILL.md"))
    if not skill_files:
        print("FAIL: no */SKILL.md files found — is this the repo root?")
        return 1

    py_scripts = sorted(REPO_ROOT.glob("*/scripts/*.py"))

    print(f"agent-armor skill validator — repo root: {REPO_ROOT}")
    print(f"found {len(skill_files)} skill(s), {len(py_scripts)} script(s)\n")

    checks = [
        ("frontmatter (name + description)", check_frontmatter(skill_files)),
        ("scripts compile", check_scripts_compile(REPO_ROOT)),
        ("skill directory links", check_skill_links(skill_files)),
    ]

    failed = False
    for label, errors in checks:
        if errors:
            failed = True
            print(f"FAIL  {label} ({len(errors)} problem(s)):")
            for e in errors:
                print(f"        - {e}")
        else:
            print(f"PASS  {label}")

    print()
    if failed:
        print("RESULT: FAIL — fix the problems above.")
        return 1
    print(f"RESULT: PASS — all {len(skill_files)} skills validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
