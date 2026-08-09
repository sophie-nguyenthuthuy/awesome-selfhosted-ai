#!/usr/bin/env python3
"""Validate data/entries.tsv and data/categories.tsv.

Every rule here exists so a one-line PR either merges clean or fails with a
message that says exactly how to fix it.
"""
from __future__ import annotations

import re
import sys

from common import ENTRIES_TSV, CATEGORIES_TSV, load_categories, load_entries, sort_key

REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DESCRIPTION_MIN, DESCRIPTION_MAX = 20, 120


def validate() -> list[str]:
    errors: list[str] = []
    try:
        categories = load_categories()
        entries = load_entries()
    except ValueError as e:
        return [str(e)]

    slugs = [c.slug for c in categories]
    if len(set(slugs)) != len(slugs):
        errors.append(f"{CATEGORIES_TSV.name}: duplicate category slugs")
    order = {slug: i for i, slug in enumerate(slugs)}

    seen_repos: dict[str, int] = {}
    seen_names: dict[str, int] = {}
    for i, e in enumerate(entries, start=2):  # line numbers, 1-based + header
        where = f"{ENTRIES_TSV.name}:{i} ({e.name or e.repo or 'blank'})"
        if not all([e.category, e.name, e.repo, e.description]):
            errors.append(f"{where}: all four fields are required")
            continue
        if e.category not in order:
            errors.append(f"{where}: unknown category {e.category!r} — see {CATEGORIES_TSV.name}")
        if not REPO_RE.match(e.repo):
            errors.append(f"{where}: repo must be 'owner/name' (no https://github.com/ prefix)")
        key = e.repo.casefold()
        if key in seen_repos:
            errors.append(f"{where}: duplicate repo (already on line {seen_repos[key]})")
        seen_repos.setdefault(key, i)
        nkey = e.name.casefold()
        if nkey in seen_names:
            errors.append(f"{where}: duplicate name (already on line {seen_names[nkey]})")
        seen_names.setdefault(nkey, i)
        if not DESCRIPTION_MIN <= len(e.description) <= DESCRIPTION_MAX:
            errors.append(
                f"{where}: description must be {DESCRIPTION_MIN}-{DESCRIPTION_MAX} chars "
                f"(got {len(e.description)})"
            )
        if e.description and e.description[0].islower():
            errors.append(f"{where}: description should start with a capital letter")
        if e.description.endswith("."):
            errors.append(f"{where}: description should not end with a period")

    expected = sorted(entries, key=lambda e: sort_key(e, order))
    if entries != expected:
        for i, (got, want) in enumerate(zip(entries, expected), start=2):
            if got != want:
                errors.append(
                    f"{ENTRIES_TSV.name}: entries must be grouped by category "
                    f"(in {CATEGORIES_TSV.name} order) and sorted by name within each — "
                    f"first mismatch at line {i}: found {got.name!r}, expected {want.name!r}"
                )
                break
    return errors


def main() -> int:
    errors = validate()
    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    if errors:
        print(f"\n{len(errors)} problem(s) found.", file=sys.stderr)
        return 1
    print(f"OK: {len(load_entries())} entries, {len(load_categories())} categories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
