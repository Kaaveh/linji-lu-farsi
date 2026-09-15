#!/usr/bin/env python3
"""This book's note apparatus, carried across gTranslator and verified.

The round-trip itself is general and lives in `linji_tools.anchors`, which knows
nothing about Watson's markup. This file is the half that does: the token
pattern, the Persian form each token takes, and the two irregularities the book
turns out to have. Roughly a hundred lines of knowledge about one text.

The book's 253 notes resolve through 1,012 inline markup tokens that sit
mid-sentence:

    ...to the lecture seat.<a id="m2-2"></a>[<sup>²</sup>](#n2-2)

Google Translate's Advanced model does not mangle these -- it *deletes* them,
every one, silently. Measured on source/42.md: ten tokens in, zero out. What it
does preserve is bracketed numeric sentinels, in place, including mid-sentence,
so `strip` swaps the tokens out and `restore` puts them back where the model
left the sentinels:

    tools/anchors.py strip   source/42.md               -o /tmp/42.en.md
    <gTranslator on /tmp/42.en.md>                      -o /tmp/42.fa.md
    tools/anchors.py restore source/42.md /tmp/42.fa.md -o fa/42.md
    tools/anchors.py --check

Anchor ids are re-emitted from source/, never from the translation, so they
cannot drift.

Headings go through the same mechanism, because every heading in the book is
structural rather than prose -- 69 `### <number>`, 66 `#### Notes`, 4
`## Part ...` and 6 named front/back-matter titles, and not one of them needs
translating:

    ### 42        ->  # ۴۲            (fa/ opens at level 1)
    #### Notes    ->  ## یادداشت‌ها
    ## Part One:  ->  dropped          (lives in _quarto.yml as a part: entry,
                                        which is the declared parity offset -1)
    ## Preface    ->  # پیش‌گفتار      ([tool.book.titles] in pyproject.toml)

Note markers become Persian digits, and the source's raw `<sup>` wrapper is
replaced by Pandoc's native superscript -- `[<sup>²</sup>](#n2-2)` becomes
`[^۲^](#n2-2)`. This is not cosmetic. Pandoc passes raw `<sup>` through to HTML
but *drops* it for LaTeX, so with the wrapper the PDF sets every one of the 253
markers at full size, inline with the body text. `^۲^` compiles to
`\\textsuperscript{۲}` for LaTeX and back to `<sup>۲</sup>` for HTML, so one form
is correct in all three outputs. Caught by reading the typeset page, invisible
in the Markdown.

Usage:
    tools/anchors.py strip SOURCE -o OUT
    tools/anchors.py restore SOURCE DRAFT -o OUT
    tools/anchors.py --check
"""

from __future__ import annotations

from functools import partial
from pathlib import Path

import regex
from linji_tools import _md, anchors as engine
from linji_tools._md import to_persian_digits

REPO = Path(__file__).resolve().parent.parent

# source/ files with no translation to pair against, from [tool.book] exclude.
EXCLUDE = set(_md.config("book").get("exclude", []))

# The Persian headings for the six non-numbered files, from [tool.book.titles].
TITLES = _md.config("book").get("titles", {})

NOTES_HEADING = "یادداشت‌ها"

# What `restore` writes. The pipeline produces the published text in one pass --
# strip, translate, restore, normalise -- with no hand-revision stage after it,
# so there is no later step to promote a `draft` or a `translated` into place.
# The output is the edition, and its status says so.
FINAL_STATUS = "reviewed"

SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")

# Precedence matters: a note opener is an anchor followed by its list number, so
# it has to be tried before any barer anchor pattern would match.
TOKEN = regex.compile(
    r"""
      (?P<ref><a\ id="m[^"]*"></a>\[<sup>(?P<sup>[^<]*)</sup>\]\((?P<refdest>[^)]*)\))
    | (?P<note><a\ id="n[^"]*"></a>(?P<num>\d+)\.\ )
    | (?P<back>\[↩\]\([^)]*\))
    | (?P<head>^(?P<hashes>\#{1,6})\ (?P<title>.*?)(?=<a\ id="|$))
    """,
    regex.VERBOSE | regex.MULTILINE,
)

# Two headings carry their own note reference: Part Three's title in 24.md and
# ma-fang-preface.md's. The title pattern above stops short of the anchor so the
# reference is tokenized separately rather than swallowed -- but Part headings
# are dropped from fa/, which would leave 24.md's marker stranded on a line of
# its own and its back-link resolving to nothing. Reattach it to the heading
# that follows, which also keeps the file's declared `parity: offset -1` true.
# Matched against the *restored* body, so the marker is already in its Persian
# form -- `[^۱^](#n25-1)`, not `[<sup>¹</sup>](#n25-1)`.
ORPHAN_MARKER = regex.compile(
    r'^(?P<marker>(?:<a id="[^"]*"></a>\[[^\]]*\]\([^)]*\))+)\n+(?P<head>\#{1,6} .*)$',
    regex.MULTILINE,
)


def fa_heading(name: str, hashes: str, title: str) -> str | None:
    """The Persian form of a source heading, or None if fa/ drops it.

    Part headings are dropped: _quarto.yml carries them as `part:` entries so
    Quarto renders real part title pages, which is why the four part-opening
    chapters declare `<!-- parity: offset -1 -->`.
    """
    if title.startswith("Part "):
        return None
    if title == "Notes":
        return f"## {NOTES_HEADING}"
    if title.isdigit():
        return f"# {to_persian_digits(int(title))}"
    if name in TITLES:
        return f"# {TITLES[name]}"
    raise ValueError(f"{name}: no Persian form for heading {hashes} {title!r}")


def fa_token(name: str, match) -> str | None:
    """The Persian form of one source token, as it should land in fa/."""
    if match.group("ref"):
        digits = match.group("sup").translate(SUPERSCRIPT)
        marker = to_persian_digits(digits) if digits.isdigit() else match.group("sup")
        anchor = match.group("ref").split("[", 1)[0]
        return f"{anchor}[^{marker}^]({match.group('refdest')})"
    if match.group("note"):
        anchor = engine.ANCHOR_ID.match(match.group("note")).group()
        return f"{anchor}{to_persian_digits(int(match.group('num')))}. "
    if match.group("back"):
        return match.group("back")
    return fa_heading(name, match.group("hashes"), match.group("title"))


def render_for(name: str):
    """This book's token renderer, bound to a filename."""
    return partial(fa_token, name)


def strip(name: str, text: str) -> str:
    return engine.strip(text, TOKEN, render_for(name))


def restore(name: str, source_text: str, draft: str) -> str:
    """The engine's round-trip, plus the two things only this book needs."""
    body = engine.restore(name, source_text, draft, TOKEN, render_for(name))
    body = ORPHAN_MARKER.sub(lambda m: m.group("head") + m.group("marker"), body)
    return f"---\nstatus: {FINAL_STATUS}\n---\n\n{body.strip()}\n"


def main(argv: list[str] | None = None) -> int:
    return engine.main(
        argv,
        strip_text=strip,
        restore_text=restore,
        source_default=REPO / "source",
        target_default=REPO / "fa",
        exclude=EXCLUDE,
        description=__doc__,
    )


if __name__ == "__main__":
    raise SystemExit(main())
