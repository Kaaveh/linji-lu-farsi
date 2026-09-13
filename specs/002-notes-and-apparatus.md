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

- [ ] `STYLE.md` §6 has no `<<<TBD>>>` left.
- [ ] One section translated with notes end to end, and its PDF read.
- [ ] Back-links resolve in HTML; note markers render as decided in the PDF.
- [ ] `check_parity.py` reports that section as matching.
- [ ] Anchor ids in `fa/` are byte-identical to `source/`.
- [ ] The markup-survival procedure is written into `STYLE.md` §6 and was
      exercised on the demonstration section through gTranslator, not by hand.

## Out of scope

Translating other sections. The glossary's own formatting, which is spec 008.

## Implementation notes

_(filled in during implementation)_
