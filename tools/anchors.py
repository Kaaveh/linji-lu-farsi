#!/usr/bin/env python3
"""Carry the note apparatus across gTranslator, and verify it survived.

The book's 253 notes resolve through 1,012 inline markup tokens that sit
mid-sentence:

    ...to the lecture seat.<a id="m2-2"></a>[<sup>²</sup>](#n2-2)

Google Translate's Advanced model does not mangle these -- it *deletes* them,
every one, silently. Measured on source/42.md: ten tokens in, zero out. So
"translate as-is and repair" has nothing to repair, and restoring by position
afterwards is impossible because markers sit mid-sentence, not at paragraph
ends.

What the model does preserve is bracketed numeric sentinels, in place, including
mid-sentence. Measured across six bracket styles: twelve sentinels in, twelve
out, all positioned correctly. So:

    tools/anchors.py strip   source/42.md            > /tmp/42.en.md
    <gTranslator on /tmp/42.en.md>                   > /tmp/42.fa.md
    tools/anchors.py restore source/42.md /tmp/42.fa.md > fa/42.md
    tools/anchors.py --check

`strip` replaces every token with U+27E6..U+27E7 sentinels, which occur nowhere
in the source text. `restore` puts the tokens back where the model left the
sentinels -- if the model moved a sentence, its marker moves with it, which is
what you want. Anchor ids are re-emitted from source/, never from the
translation, so they cannot drift.

Headings are handled by the same mechanism, because every heading in the book is
structural rather than prose -- 69 `### <number>`, 66 `#### Notes`, 4
`## Part ...` and 6 named front/back-matter titles, and not one of them needs
translating. Their Persian forms are derived here:

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
`\textsuperscript{۲}` for LaTeX and back to `<sup>۲</sup>` for HTML, so one form
is correct in all three outputs. Caught by reading the typeset page, invisible
in the Markdown.

Usage:
    tools/anchors.py strip SOURCE
    tools/anchors.py restore SOURCE DRAFT
    tools/anchors.py --check
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import regex

import _md
from _md import to_persian_digits

REPO = _md.REPO

# source/ files with no translation to pair against, from [tool.book] exclude.
EXCLUDE = set(_md.config("book").get("exclude", []))

NOTES_HEADING = "یادداشت‌ها"

# The Persian headings for the six non-numbered files, from [tool.book.titles]
# in pyproject.toml. Read from config rather than imported from make_stubs.py:
# the round-trip below is general machinery, and the book's own vocabulary has
# no business living inside it.
TITLES = _md.config("book").get("titles", {})

# What `restore` writes. The pipeline produces the published text in one pass --
# strip, translate, restore, normalise -- with no hand-revision stage after it,
# so there is no later step to promote a `draft` or a `translated` into place.
# The output is the edition, and its status says so.
FINAL_STATUS = "reviewed"

# U+27E6 / U+27E7. Verified absent from all 75 source files, and preserved in
# place by the Advanced model. Any bracketed numeric form survives; this one is
# exotic enough that a collision with the text is not a live worry.
SENTINEL = "⟦{}⟧"
SENTINEL_RE = regex.compile(r"⟦(\d+)⟧")

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

ANCHOR_ID = regex.compile(r'<a id="([^"]*)"></a>')
LINK_DEST = regex.compile(r"\]\(([^)]*)\)")


@dataclass(frozen=True)
class Finding:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


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
        anchor = ANCHOR_ID.match(match.group("note")).group()
        return f"{anchor}{to_persian_digits(int(match.group('num')))}. "
    if match.group("back"):
        return match.group("back")
    return fa_heading(name, match.group("hashes"), match.group("title"))


def render_for(name: str):
    """This book's token renderer, bound to a filename."""
    return partial(fa_token, name)


def tokenize(text: str, token_re, render) -> tuple[str, list[str | None]]:
    """Returns (text with sentinels, replacement form of each token by index).

    `token_re` and `render` are the only things here that know what a token
    looks like or what it should become, which is what keeps the round-trip
    itself free of any knowledge of this book's markup.
    """
    out: list[str] = []
    forms: list[str | None] = []
    cursor = 0
    for match in token_re.finditer(text):
        out.append(text[cursor : match.start()])
        out.append(SENTINEL.format(len(forms) + 1))
        forms.append(render(match))
        cursor = match.end()
    out.append(text[cursor:])
    return "".join(out), forms


def strip(text: str, token_re, render) -> str:
    return tokenize(text, token_re, render)[0]


def restore(name: str, source_text: str, draft: str, token_re, render) -> str:
    """Put the tokens back where the model left the sentinels."""
    _, forms = tokenize(source_text, token_re, render)

    seen = [int(m.group(1)) for m in SENTINEL_RE.finditer(draft)]
    expected = set(range(1, len(forms) + 1))
    missing = sorted(expected - set(seen))
    unknown = sorted(set(seen) - expected)
    duplicated = sorted({n for n in seen if seen.count(n) > 1})

    problems = []
    if missing:
        problems.append(f"the model dropped sentinel(s) {missing}")
    if unknown:
        problems.append(f"sentinel(s) {unknown} are not in source/{name}")
    if duplicated:
        problems.append(f"the model duplicated sentinel(s) {duplicated}")
    if problems:
        raise ValueError(f"{name}: " + "; ".join(problems))

    body = SENTINEL_RE.sub(lambda m: forms[int(m.group(1)) - 1] or "", draft)
    body = ORPHAN_MARKER.sub(lambda m: m.group("head") + m.group("marker"), body)
    return f"---\nstatus: {FINAL_STATUS}\n---\n\n{body.strip()}\n"


def anchors_of(text: str) -> tuple[list[str], list[str]]:
    """The anchor ids and note-link destinations a file carries."""
    dests = [d for d in LINK_DEST.findall(text) if "#" in d]
    return sorted(ANCHOR_ID.findall(text)), sorted(dests)


def hard_breaks(text: str) -> int:
    """Lines ending in a Markdown hard line break (two trailing spaces).

    The model strips these -- measured on the Ikkyu poem in preface.md, which is
    the only place in the book that uses them. Lose them and four lines of verse
    reflow into one paragraph, which reads as prose and is easy to miss in a
    diff. `restore` cannot put them back reliably, because that needs the
    translated block to line up with the source line for line, so this counts
    them instead and says so when they go missing.
    """
    return sum(1 for line in text.split("\n") if line.endswith("  ") and line.strip())


def compare(source_dir: Path, fa_dir: Path) -> tuple[list[Finding], int, int]:
    findings: list[Finding] = []
    compared = skipped = 0

    names = {p.name for p in source_dir.glob("*.md")} - EXCLUDE
    for name in sorted(names):
        fa_path = fa_dir / name
        if not fa_path.exists():
            continue
        fa_doc = _md.read(fa_path)
        if fa_doc.status == "untranslated":
            skipped += 1
            continue

        compared += 1
        src_text = (source_dir / name).read_text(encoding="utf-8")
        fa_text = fa_path.read_text(encoding="utf-8")
        src_ids, src_dests = anchors_of(src_text)
        fa_ids, fa_dests = anchors_of(fa_text)

        src_breaks, fa_breaks = hard_breaks(src_text), hard_breaks(fa_text)
        if fa_breaks != src_breaks:
            findings.append(
                Finding(
                    f"fa/{name}",
                    f"{fa_breaks} hard line break(s), source has {src_breaks} — "
                    "verse will reflow into prose",
                )
            )

        if fa_ids != src_ids:
            lost = sorted(set(src_ids) - set(fa_ids))
            extra = sorted(set(fa_ids) - set(src_ids))
            detail = f"{len(fa_ids)} anchor id(s), source has {len(src_ids)}"
            if lost:
                detail += f"; missing {lost}"
            if extra:
                detail += f"; unexpected {extra}"
            findings.append(Finding(f"fa/{name}", detail))
        if fa_dests != src_dests:
            findings.append(
                Finding(
                    f"fa/{name}",
                    f"{len(fa_dests)} note link(s), source has {len(src_dests)}",
                )
            )

    return findings, compared, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", nargs="?", choices=["strip", "restore"])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        help="write here, and only if validation passed. Prefer this to a shell "
        "redirect: `> fa/42.md` truncates the file before the tool runs, so a "
        "draft this correctly refuses destroys the previous translation.",
    )
    parser.add_argument("--source", type=Path, default=REPO / "source")
    parser.add_argument("--fa", type=Path, default=REPO / "fa")
    args = parser.parse_args(argv)

    if args.check:
        if not args.source.is_dir():
            print(
                f"anchors: skipped — {args.source}/ is not present.\n"
                "This is expected in CI: the source text is licensed to the maintainer "
                "for translation, not for redistribution. Run this locally."
            )
            return 0
        findings, compared, skipped = compare(args.source, args.fa)
        for finding in findings:
            print(finding)
        if findings:
            print(f"\n{len(findings)} anchor problem(s)", file=sys.stderr)
            return 1
        print(f"anchors: {compared} file(s) match, {skipped} skipped (untranslated)")
        return 0

    if not args.mode:
        parser.error("give a mode (strip/restore) or --check")

    try:
        source = args.files[0]
        text = source.read_text(encoding="utf-8")
        if args.mode == "strip":
            result = strip(text, TOKEN, render_for(source.name))
        else:
            draft = args.files[1].read_text(encoding="utf-8")
            result = restore(source.name, text, draft, TOKEN, render_for(source.name))
        # Only now, with validation behind us, is anything written.
        if args.out:
            args.out.write_text(result, encoding="utf-8")
        else:
            sys.stdout.write(result)
    except IndexError:
        parser.error(f"{args.mode} needs {'SOURCE' if args.mode == 'strip' else 'SOURCE DRAFT'}")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
