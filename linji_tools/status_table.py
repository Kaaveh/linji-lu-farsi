"""Build the chapter status table for the README from fa/ front matter.

`status:` in each fa/ file is the single source of truth for progress. Keeping
a hand-written table in the README instead guarantees it goes stale, and a
stale progress table is worse than none -- it tells contributors a chapter is
free when someone is halfway through it.

Usage:
    tools/status_table.py            # print the table
    tools/status_table.py --write    # splice it into README.md
    tools/status_table.py --check    # exit non-zero if README is out of date
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


import regex

from . import _md

REPO = _md.REPO

BEGIN = "<!-- BEGIN status table -->"
END = "<!-- END status table -->"

CONFIG = _md.config("status_table")

# The status labels, and the order the table and the progress summary render
# them in -- both are the project's, not this script's, so they come from
# [tool.status_table.statuses]. TOML preserves the order it is written in.
STATUSES = CONFIG.get("statuses", {})

# Markup to strip out of a heading before it lands in a table cell, from
# [tool.status_table] heading_markup. Optional: a project whose headings are
# plain prose needs none.
HEADING_MARKUP = regex.compile(CONFIG["heading_markup"]) if CONFIG.get("heading_markup") else None


def heading_of(doc: _md.Document, markup=None) -> str:
    """The first heading's text, with `markup` stripped out of it.

    `markup` is a compiled pattern, defaulting to [tool.status_table]
    heading_markup. A project whose headings are plain prose needs none.
    """
    pattern = HEADING_MARKUP if markup is None else markup
    for block in _md.iter_blocks(doc):
        if block.kind == "heading":
            text = block.text.lstrip("#")
            return (pattern.sub("", text) if pattern else text).strip()
    return ""


def sort_key(path: Path):
    stem = path.stem
    return (not stem.isdigit(), int(stem) if stem.isdigit() else 0, stem)


def collect(fa_dir: Path) -> list[tuple[str, str, str]]:
    """(filename, heading, status) for every chapter."""
    rows = []
    for path in sorted(fa_dir.glob("*.md"), key=sort_key):
        doc = _md.read(path)
        rows.append((path.name, heading_of(doc), doc.status or "untranslated"))
    return rows


def render(rows: list[tuple[str, str, str]], repo_url: str) -> str:
    done = sum(1 for _, _, s in rows if s in ("translated", "reviewed"))
    total = len(rows)
    percent = round(100 * done / total) if total else 0

    fa_done = _md.to_persian_digits(done)
    fa_total = _md.to_persian_digits(total)
    fa_percent = _md.to_persian_digits(percent)

    # The summary stays visible; the 75 rows go behind a disclosure triangle.
    # A table that long at the top of the README pushes everything anyone
    # actually needs -- rights, contributing, build -- below the fold.
    lines = [
        f"**{fa_done} از {fa_total} بخش ({fa_percent}٪)**",
        "",
        "<details>",
        f"<summary>Per-section status ({total} files)</summary>",
        "",
        "| بخش | عنوان | وضعیت |",
        "|---|---|---|",
    ]
    for name, heading, status in rows:
        label = STATUSES.get(status, f"❓ {status}")
        link = f"[`{name}`]({repo_url}/blob/main/fa/{name})"
        lines.append(f"| {link} | {heading} | {label} |")
    lines += ["", "</details>"]
    return "\n".join(lines)


def splice(readme: str, table: str) -> str:
    start = readme.find(BEGIN)
    end = readme.find(END)
    if start == -1 or end == -1:
        raise ValueError(f"README.md is missing the {BEGIN} / {END} markers")
    return readme[: start + len(BEGIN)] + "\n\n" + table + "\n\n" + readme[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="update README.md in place")
    parser.add_argument("--check", action="store_true", help="fail if README.md is stale")
    parser.add_argument("--fa", type=Path, default=REPO / "fa")
    parser.add_argument("--readme", type=Path, default=REPO / "README.md")
    parser.add_argument("--repo-url", default=CONFIG.get("repo_url", ""))
    args = parser.parse_args(argv)

    table = render(collect(args.fa), args.repo_url)

    if not (args.write or args.check):
        print(table)
        return 0

    readme = args.readme.read_text(encoding="utf-8")
    try:
        updated = splice(readme, table)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if updated != readme:
            print("README.md status table is out of date — run `just status-write`", file=sys.stderr)
            return 1
        print("status table: up to date")
        return 0

    args.readme.write_text(updated, encoding="utf-8")
    print(f"status table: updated {args.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
