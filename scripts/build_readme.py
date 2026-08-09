#!/usr/bin/env python3
"""Generate README.md from data/*.tsv. Run with --check to verify it's in sync."""
from __future__ import annotations

import argparse
import sys

from common import README, load_categories, load_entries, slugify, sort_key

HEADER = """\
# Awesome Self-Hosted AI

> Open-source, self-hostable replacements for AI SaaS tools — **machine-checked**.
> Most awesome lists rot. This one can't: CI re-validates every entry weekly,
> flags anything dead, archived, or without a commit in the last 12 months,
> and opens an issue automatically.

[![CI](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/ci.yml)
[![Weekly health check](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/health.yml/badge.svg)](https://github.com/sophie-nguyenthuthuy/awesome-selfhosted-ai/actions/workflows/health.yml)
![Entries](https://img.shields.io/badge/entries-{count}-blue)

**Adding a tool is a one-line PR** — append one line to
[`data/entries.tsv`](data/entries.tsv) and CI does the rest
(schema check, liveness check, README regeneration).
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Contents

{toc}
"""

FOOTER = """\
## How the machine-checking works

- Entries live in [`data/entries.tsv`](data/entries.tsv) — one line per tool. This README is
  generated from it by [`scripts/build_readme.py`](scripts/build_readme.py); CI fails if they drift.
- [`scripts/validate.py`](scripts/validate.py) enforces the schema on every PR.
- [`scripts/check_health.py`](scripts/check_health.py) runs weekly against the GitHub API:
  a repo that 404s, is archived, or has had no push in **12 months** gets reported in an
  auto-filed issue. PRs that add a dead repo fail immediately.

## License

[CC0 1.0](LICENSE) — public domain.
"""

GENERATED_NOTE = (
    "<!-- GENERATED FILE — edit data/entries.tsv and run "
    "`python3 scripts/build_readme.py`, do not edit sections below by hand. -->\n"
)


def render() -> str:
    categories = load_categories()
    entries = load_entries()
    order = {c.slug: i for i, c in enumerate(categories)}
    entries = sorted(entries, key=lambda e: sort_key(e, order))

    toc = "\n".join(
        f"- [{c.title}](#{slugify(c.title)})" for c in categories
        if any(e.category == c.slug for e in entries)
    )
    out = [GENERATED_NOTE, HEADER.format(count=len(entries), toc=toc)]
    for c in categories:
        section = [e for e in entries if e.category == c.slug]
        if not section:
            continue
        out.append(f"## {c.title}\n\n*{c.blurb}*\n")
        for e in section:
            out.append(f"- **[{e.name}]({e.url})** — {e.description}")
        out.append("")
    out.append(FOOTER)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if README.md is out of date")
    args = parser.parse_args()

    content = render()
    if args.check:
        current = README.read_text(encoding="utf-8") if README.exists() else ""
        if current != content:
            print(
                "ERROR: README.md is out of date. Run `python3 scripts/build_readme.py` "
                "and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("OK: README.md is in sync with data/entries.tsv.")
        return 0
    README.write_text(content, encoding="utf-8")
    print(f"Wrote {README} ({len(content)} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
