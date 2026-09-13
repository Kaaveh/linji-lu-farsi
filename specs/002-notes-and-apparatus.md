# 002 — Notes & Apparatus Convention

## Context

The book carries **253 notes**, unevenly: section 19 alone has 47, sections 11
and 23 have 16 and 17, and six sections (25, 28, 31, 37, 47, 52) have none.

The source uses endnotes per section, not page-bottom footnotes. Each section
ends with `#### Notes` and a list; a reference in the prose looks like

```
…to the lecture seat.<a id="m2-2"></a>[<sup>²</sup>](#n2-2)
```

and the note itself carries a back-link `[↩](#m2-2)`. Anchor ids are globally
unique across all 75 files and nothing links across files, so the whole book
concatenates into one PDF without collisions.

Two things need settling before any section is translated, because retrofitting
253 notes is miserable.

## Goal

`STYLE.md` §6 decided, and the convention demonstrated on one real section.

## Dependencies

001.

## Requirements

1. **Keep endnotes per section.** Do not convert to Pandoc `[^n]` footnotes.
   Section 19's 47 notes would be unreadable at the foot of a page, and the
   anchor scheme already works in all three formats. Record the reasoning in
   §6 so nobody relitigates it.

2. **Persian note markers.** The source uses Latin superscript digits (`²`, `³`).
   Decide the Persian form (`۲`, `۳`) and whether the `<sup>` wrapper stays.
   This is mechanical and affects all 253 references.

3. **Anchor ids stay untouched.** `m2-2` / `n2-2` are ASCII and must remain
   byte-identical to the source — they are what the back-links resolve against,
   and `tools/_md.py` deliberately protects them from the orthography pass.
   Confirm this in §6 so a future contributor does not "translate" them.

4. **Translator's notes.** The translation will need notes the source does not
   have. Decide how they are marked as distinct from the author's, and whether
   they share the list or get their own. Unlike the author's endnotes, these may
   be real Pandoc footnotes — `tex/preamble.tex` already mirrors the footnote
   rule to the right edge for exactly this case.

5. **The notes heading.** `#### Notes` becomes a level-2 `## یادداشت‌ها` in
   `fa/`, since section files open at level 1. Confirm the wording.

6. **Parity.** Each note is a block. Dropping or merging notes changes the block
   count and `check_parity.py` will say so. If a note is deliberately dropped,
   that is a `<!-- parity: offset -->`, not a `skip`.

7. **Settle how markup survives gTranslator.** The book has 1,012 inline markup
   tokens and machine translation will not leave them alone. Decide a repeatable
   procedure and write it into `STYLE.md` §6 so every later spec follows the
   same one. The options, roughly:

   - **Strip and restore.** Remove the anchors before translating, keep an
     ordered list, re-insert afterwards. Reliable, but manual per file.
   - **Translate around them.** Send only the prose between markers.
     Fiddlier to script, but the markers never reach Google.
   - **Translate as-is and repair.** Simplest to run, most to check.

   Whichever it is, the check afterwards is mechanical and should be scripted:
   the anchor ids in `fa/NN.md` must be the same multiset as in `source/NN.md`.
   If that ends up as a small addition to `tools/`, it belongs in this spec.

8. **Demonstrate it.** Apply the convention to one real section with notes —
   section 42 is a good size, two notes — and render the PDF to confirm the
   markers, the list and the back-links all behave. Do it through the real
   gTranslator path, not by hand, or the procedure in requirement 7 is untested.

## Acceptance criteria

- [x] `STYLE.md` §6 has no `<<<TBD>>>` left.
- [x] One section translated with notes end to end, and its PDF read.
      `fa/42.md`, page 105.
- [x] Back-links resolve in HTML; note markers render as decided in the PDF.
      HTML carries all four anchors and both back-links; PDF sets the markers as
      raised Persian digits. See note 3 below on the PDF back-link glyph.
- [x] `check_parity.py` reports that section as matching.
- [x] Anchor ids in `fa/` are byte-identical to `source/`, enforced from now on
      by `tools/anchors.py --check` in `just check`.
- [x] The markup-survival procedure is written into `STYLE.md` §6 and was
      exercised on the demonstration section through gTranslator, not by hand.

## Out of scope

Translating other sections. The glossary's own formatting, which is spec 008.

## Implementation notes

**1. The model deletes the markup; it does not mangle it.** `000-overview.md`
warned that machine translation would drop, duplicate, reorder or "translate"
the anchors. Measured on `source/42.md` through the real `-w --raw` path: all ten
tokens were deleted, cleanly, leaving well-formed Persian prose with no trace
that a note had ever been there. That rules out requirement 7's third option —
"translate as-is and repair" has nothing to repair — and it rules out positional
restore too, since markers sit mid-sentence rather than at paragraph ends.

Bracketed numeric sentinels *do* survive, in place, mid-sentence. Tested six
bracket styles in one pass; twelve sentinels in, twelve out, all correctly
positioned. `⟦n⟧` (U+27E6/U+27E7) was chosen and verified absent from all 75
source files. So requirement 7 is settled as **strip and restore**, scripted.

**2. `tools/anchors.py`** (+ `tools/tests/test_anchors.py`, 17 tests) does
`strip` / `restore` / `--check`, and `--check` is wired into `just check`
alongside `check_parity.py`, skipping in CI for the same reason. Tokens are
re-derived from `source/` at restore time rather than stashed in a sidecar, so
there is one source of truth and nothing to keep in sync.

Headings went into the same mechanism after a survey found that **all 145
headings in the book are structural** — 69 `### <number>`, 66 `#### Notes`, 4
`## Part ...`, 6 named titles already in `make_stubs.DEFAULT_TITLES` — so none
needs translating and all can be re-emitted deterministically.

Verified by dry round-trip over all 74 book files before any translation: anchor
ids, note-link destinations and parity block counts all match, including the
declared `-1` offsets on the four part openers.

**3. The `<sup>` wrapper had to go, and only the PDF showed it.** Pandoc passes
raw `<sup>` through to HTML but silently discards it for LaTeX, so the first
render set the markers at full body size, inline with the text — correct in the
Markdown, correct in HTML, wrong in print. Switched to Pandoc's native `^۲^`,
which compiles to `\textsuperscript{}` for LaTeX and `<sup>` for HTML. This is
exactly the class of fault the quality bar's "read the typeset PDF, not the
Markdown" rule exists to catch; it is invisible in a diff.

Also found while reading it: **the `↩` back-link is invisible in the PDF.**
Vazirmatn has no glyph for U+21A9 (confirmed against the font's cmap), and the
source's `<a id>` anchors produce no LaTeX label, so PDF back-links neither draw
nor resolve. HTML is unaffected and back-links work there, which is what this
spec's acceptance criterion asks for. Left as is deliberately: a back-link is
meaningless in print, and vendoring a second font for one arrow is
disproportionate. If it ever matters, the fix is a `\newfontfamily` fallback in
`tex/preamble.tex` for that codepoint, not a change to the note convention.

**4. Two headings carry their own note reference** — Part Three's title in
`24.md` and `ma-fang-preface.md`'s. `ma-fang-preface.md` keeps its heading, so
the marker reattaches to it. `24.md`'s Part heading is dropped from `fa/`
(it lives in `_quarto.yml` as a `part:` entry, which is that file's declared
`parity: offset -1`), which would have stranded the marker on a line of its own,
broken its back-link, and falsified the offset. `restore` reattaches an orphaned
marker to the heading that follows, so `fa/24.md` will open `# ۲۴[^۱^](#n25-1)`.
Worth a look in the PDF when spec 006 reaches section 24 — a hyperlink inside a
LaTeX section title also lands in the table of contents.

**5. Corrections to `000-overview.md`**, both now made there:

- It states that nothing links across files. Two links do:
  `record-title-page.md` → `01.md#n2-1`, and back. Anything that assumes
  per-file self-containment has to allow for it.
- It gives 4,500 characters as gTranslator's chunk size against a 5,000 cap,
  which stands — but note that `strip` *shortens* every file, since a sentinel
  is far shorter than the token it replaces. Chunk counts for the big files will
  come out at or below the estimates in `specs/README.md`.

**6. Status: `reviewed`, settled.** This spec originally left `fa/42.md` at
`draft` and flagged the conflict with the definition of done. The maintainer
settled it: the pipeline output is the final text, so neither `draft` nor
`translated` applies — a finished file is `status: reviewed`. `restore` writes
it, `specs/README.md`, `000-overview.md` and `CLAUDE.md` say so, and the project
now uses only `untranslated` and `reviewed`.

**7. Section-with-no-notes count.** The spec says six sections have no notes
(25, 28, 31, 37, 47, 52). The corpus has 69 `### <number>` headings and 66
`#### Notes`, so three sections lack them, not six. Not chased down — it affects
nothing mechanical — but do not trust the six when planning specs 005–007.
