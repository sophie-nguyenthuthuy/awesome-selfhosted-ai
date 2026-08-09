# Contributing

Adding a tool is **one line**. Everything else is automated.

## Add a tool

1. Open [`data/entries.tsv`](data/entries.tsv).
2. Add one tab-separated line in the right category section, alphabetically by name:

   ```
   category<TAB>Name<TAB>owner/repo<TAB>Short description
   ```

   Example:

   ```
   pinecone	LanceDB	lancedb/lancedb	Embedded vector database for multimodal AI, built on Lance
   ```

3. Open a PR. Don't touch `README.md` by hand — run `python3 scripts/build_readme.py`
   and commit the regenerated file (CI fails if it drifts).

CI will reject the PR with an exact error message if the line is malformed,
out of order, a duplicate, or points at a dead/archived repo.

## Acceptance criteria

- **Self-hostable end to end.** A cloud offering may exist, but the full product must run on your own hardware.
- **Open source** (OSI license) or source-available with self-hosting clearly permitted — the entry description should say "source-available" in that case.
- **Actually replaces the section's SaaS** — not a library that merely relates to it.
- **Alive**: not archived, pushed to within the last 12 months. CI enforces this weekly, forever.

## Removing entries

When the weekly health check files an issue, anyone can send a PR deleting the
flagged line (or fixing the `owner/repo` reference if the project moved). This
is the whole point of the list — removals are as welcome as additions.

## Local checks

```
python3 scripts/validate.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s tests
GITHUB_TOKEN=... python3 scripts/check_health.py   # optional, hits the GitHub API
```

No dependencies — everything is Python 3.10+ stdlib.
