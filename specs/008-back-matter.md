# 008 — Back Matter

**`fa/appendix.md`, `fa/glossary.md` · 2 files · 1,990 words · 2 notes**

## Context

Two files, one of which is unlike anything else in the book.

`glossary.md` is a reference list — roughly 100 entries, each a bolded headword
with a Sanskrit form in parentheses and a short definition. It is alphabetised by
the **English** headword. Persian sorts differently, and by a different alphabet
entirely, so ordering is a real decision rather than a copy.

This must come **after the body**, because the glossary's headwords have to be
the terms the translation actually settled on. Translating it early guarantees
rework.

## Goal

Both files at `status: translated`, `just check` green, PDF read.

## Dependencies

001–007. Genuinely all of them — the glossary depends on every term.

## Requirements

1. **Decide the ordering.** Persian alphabetical by the Persian headword,
   retained English order, or both forms shown. Each has a cost: re-sorting
   breaks parity block-for-block against the source; keeping English order makes
   a Persian reader hunt. Whatever is chosen, record it in `STYLE.md` and, if the
   order changes, declare the parity consequence rather than skipping the file.

2. **Every headword must match the body.** The glossary chapter is where
   terminology becomes visible to the reader; a headword rendered differently
   here than in the body is the worst possible inconsistency. Nothing catches
   this any more, so it has to be checked by reading.

3. **The parenthetical Sanskrit forms.** The source gives full diacritics
   (Ānanda, Aṅgulimāla) where they differ from the simplified form used in the
   text. Decide whether Persian keeps the Latin diacritical form, transliterates,
   or both — this follows from §4 but the glossary is where it is most visible.

4. **`appendix.md`** is ordinary prose and needs no special handling beyond the
   usual.

5. **Per section, the gTranslator loop.** One `source/` file at a time, never
   concatenated — the command and the reasons are in `000-overview.md`. Draft
   with `-w --raw`, revise against `STYLE.md`, restore the note markup per §6,
   run `LOCAL=1 just fix` then `LOCAL=1 just check`, set `status:` (`draft`
   while the machine output is still raw, `translated` once you have been
   through it), and read the section in the PDF before moving on.

   The glossary is a list of short independent entries, so chunk boundaries are
   harmless there — but the Advanced model has less context to work with per
   entry, and headwords are exactly where a wrong rendering is most visible.

6. **Re-check the whole book afterwards.** Finishing the glossary is the first
   moment every term in the book is visible in one place. Expect to find
   inconsistencies in already-translated sections; fix them as `revise(chNN):`.

## Acceptance criteria

- [x] Both files at `status: reviewed`; status table regenerated.
      (Written `translated`; `reviewed` is what the pipeline emits.)
- [x] `LOCAL=1 just check` passes with parity comparing, not skipping.
      65 files match, 10 skipped — the ten still owed by spec 005.
- [ ] **Not met.** Every glossary headword matches the rendering the body
      settled on. At least one does not, and a tenth of the body does not
      exist yet to be checked against — see notes.
- [x] Ordering decision recorded in `STYLE.md`; any parity offset declared.
      Source order kept, so no offset is needed.

## Out of scope

Releasing. That is spec 009.

## Implementation notes

### The dependency was not actually satisfied

This spec declares "001–007. Genuinely all of them — the glossary depends on
every term." Spec 005 is still unfinished: ten Part Two sections are
untranslated — 11, 12, 14–19, 21, 23 — including `19.md`, the longest section
in the book at 47 notes. So requirement 6, "the first moment every term in the
book is visible in one place", has not arrived. The glossary was translated
anyway because it is 33 self-contained entries and nothing about it changes
when those ten land; but it will need re-reading against them.

### The decisions

Both were put to the maintainer rather than settled here, per CLAUDE.md.

1. **Ordering: the source's.** Recorded in `STYLE.md` §4.
2. **Sanskrit parentheticals: the Latin diacritical form, as the source gives
   it.** Also recorded there.

Requirement 1 assumes re-sorting "breaks parity block-for-block". It does not:
`check_parity.py` compares block *counts*, so the re-sort option was free of
parity cost. The decision was made on reader-usability grounds instead, and the
correction is noted in `STYLE.md` so the option stays open.

### Requirement 2 is not met, and one violation is concrete

**«چَن» in the glossary, «ذن» in the body.** The glossary headword for Ch'an is
`**چَن**`. The body uses `ذن` 42 times across at least eight sections, and
`چَن` in only three files. This is precisely the mismatch requirement 2 calls
"the worst possible inconsistency". It needs a terminology decision, so it was
left alone rather than silently patched.

Two further defects in the machine output, recorded as suggestions, not fixes:

- **`**گود استار**` and `**گود تِرِژرز**`** — "Good Star" and "Good Treasures",
  English glosses of Buddhist names, transliterated phonetically into Persian
  instead of translated. `گود استار` also appears in the body, so the glossary
  is at least *consistent* with it; both are wrong together.
- **"Vehicle" is rendered two ways** — `حامل کوچک` for Lesser Vehicle but
  `سه وسیله` for Three Vehicles, inside the same 33-entry list.

What *was* verified as consistent: دارما, بودیساتوا, شاکیامونی, نیروانا,
کوان-یین, and بودیدارما (9 occurrences, one spelling).

### Where the sentinel mechanism needed help

`glossary.md` went through clean first try, chunked at 1,200. `appendix.md` did
not, and failed the same deterministic way Part Four's did: `K'o-fu?⟦3⟧` puts a
sentinel on a stray `?` that Persian word order erases. Re-translated alone, the
sentinel survived but came back as `[۳]` — square brackets and a Persian digit,
the same transliteration behaviour `69.md` showed. Repaired, and the marker
placed on «کو-فو», the name its note identifies. `appendix.md` had also merged
one paragraph, re-translated as its own pair and spliced back.
