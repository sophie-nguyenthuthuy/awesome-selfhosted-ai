#!/usr/bin/env python3
"""Health-check every entry against the GitHub API.

An entry is unhealthy if its repo:
  - no longer exists (dead),
  - is archived, or
  - has had no push in the last 12 months (stale).

Exit codes: 0 = all healthy, 1 = problems found, 2 = check aborted
(rate limit / network), so CI can distinguish "list is rotting" from
"checker couldn't run".
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

from common import ROOT, Entry, load_entries

STALE_DAYS = 365
API = "https://api.github.com/repos/{}"
GONE = {404, 410, 451}


class Aborted(Exception):
    pass


def fetch_repo(repo: str, token: str | None = None) -> tuple[int, dict]:
    req = urllib.request.Request(
        API.format(repo),
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-selfhosted-ai-health-check",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as e:
        return e.code, {}
    except (urllib.error.URLError, TimeoutError) as e:
        raise Aborted(f"network error fetching {repo}: {e}") from e


def classify(status: int, data: dict, now: datetime.datetime) -> tuple[str, str]:
    """Return (state, detail) where state is ok|dead|archived|stale|error."""
    if status in GONE:
        return "dead", "repository not found"
    if status in (403, 429):
        raise Aborted("GitHub API rate limit hit — set GITHUB_TOKEN and retry")
    if status != 200:
        return "error", f"unexpected HTTP {status}"
    if data.get("archived"):
        return "archived", "repository is archived"
    pushed_raw = data.get("pushed_at")
    if not pushed_raw:
        return "error", "no pushed_at in API response"
    pushed = datetime.datetime.fromisoformat(pushed_raw.replace("Z", "+00:00"))
    age = (now - pushed).days
    if age > STALE_DAYS:
        return "stale", f"last push {pushed:%Y-%m-%d} ({age} days ago)"
    return "ok", f"last push {pushed:%Y-%m-%d}"


def build_report(results: list[dict], now: datetime.datetime) -> str:
    problems = [r for r in results if r["state"] != "ok"]
    lines = [
        f"# Weekly health report — {now:%Y-%m-%d}",
        "",
        f"Checked **{len(results)}** entries: "
        f"{len(results) - len(problems)} healthy, {len(problems)} need attention.",
        "",
    ]
    if problems:
        lines += [
            "## Needs attention",
            "",
            "| Entry | Repo | Problem | Detail |",
            "|---|---|---|---|",
        ]
        for r in problems:
            lines.append(
                f"| {r['name']} | [{r['repo']}](https://github.com/{r['repo']}) "
                f"| **{r['state']}** | {r['detail']} |"
            )
        lines += [
            "",
            "For each entry above: fix the repo reference if it moved, or open a "
            "removal PR deleting its line from `data/entries.tsv`.",
        ]
    else:
        lines.append("Everything is alive. 🎉")
    lines += [
        "",
        "<details><summary>Full results</summary>",
        "",
        "| Entry | Repo | State | Detail |",
        "|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['name']} | {r['repo']} | {r['state']} | {r['detail']} |")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=str, help="write a markdown report to this path")
    parser.add_argument(
        "--repos", nargs="*",
        help="check only these owner/name repos (default: every entry in the list)",
    )
    args = parser.parse_args()

    entries = load_entries()
    if args.repos:
        by_repo = {e.repo.casefold(): e for e in entries}
        # A repo passed on the CLI that isn't in the TSV yet (a freshly added
        # PR line) is still checked, labeled by its own name.
        targets = [
            by_repo.get(r.casefold(), Entry("?", r, r, "?"))
            for r in args.repos
        ]
    else:
        targets = entries

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    now = datetime.datetime.now(datetime.timezone.utc)
    results = []
    try:
        for e in targets:
            status, data = fetch_repo(e.repo, token)
            state, detail = classify(status, data, now)
            results.append({"name": e.name, "repo": e.repo, "state": state, "detail": detail})
            marker = "✅" if state == "ok" else "❌"
            print(f"{marker} {e.repo}: {state} — {detail}")
    except Aborted as e:
        print(f"ABORTED: {e}", file=sys.stderr)
        return 2

    report = build_report(results, now)
    if args.report:
        path = pathlib.Path(args.report)
        if not path.is_absolute():
            path = ROOT / path
        path.write_text(report, encoding="utf-8")
    problems = [r for r in results if r["state"] != "ok"]
    print(f"\n{len(results)} checked, {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
