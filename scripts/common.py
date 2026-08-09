"""Shared loading helpers for the data files. Stdlib only."""
from __future__ import annotations

import csv
import pathlib
from typing import NamedTuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATEGORIES_TSV = ROOT / "data" / "categories.tsv"
ENTRIES_TSV = ROOT / "data" / "entries.tsv"
README = ROOT / "README.md"

CATEGORY_FIELDS = ["slug", "title", "blurb"]
ENTRY_FIELDS = ["category", "name", "repo", "description"]


class Category(NamedTuple):
    slug: str
    title: str
    blurb: str


class Entry(NamedTuple):
    category: str
    name: str
    repo: str
    description: str

    @property
    def url(self) -> str:
        return f"https://github.com/{self.repo}"


def _read_tsv(path: pathlib.Path, fields: list[str]) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    if not rows or rows[0] != fields:
        raise ValueError(f"{path.name}: first line must be the header {chr(9).join(fields)!r}")
    return rows[1:]


def load_categories(path: pathlib.Path = CATEGORIES_TSV) -> list[Category]:
    return [Category(*row) for row in _read_tsv(path, CATEGORY_FIELDS)]


def load_entries(path: pathlib.Path = ENTRIES_TSV) -> list[Entry]:
    return [Entry(*row) for row in _read_tsv(path, ENTRY_FIELDS)]


def sort_key(entry: Entry, category_order: dict[str, int]) -> tuple[int, str]:
    return (category_order.get(entry.category, len(category_order)), entry.name.casefold())


def slugify(title: str) -> str:
    """GitHub heading anchor for the ASCII-only titles we use."""
    return "".join(c for c in title.lower() if c.isalnum() or c in " -").replace(" ", "-")
