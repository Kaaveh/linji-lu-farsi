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

2. **Every headword must already be in `glossary.yml`.** The glossary file is
   where terminology becomes visible to the reader; a headword rendered
   differently here than in the body is the worst possible inconsistency.
   `check_glossary.py` catches it — treat any warning on this file as an error.

3. **The parenthetical Sanskrit forms.** The source gives full diacritics
   (Ānanda, Aṅgulimāla) where they differ from the simplified form used in the
   text. Decide whether Persian keeps the Latin diacritical form, transliterates,
   or both — this follows from §4 but the glossary is where it is most visible.

4. **`appendix.md`** is ordinary prose and needs no special handling beyond the
   usual.

5. **Re-check the whole book afterwards.** Finishing the glossary is the first
   moment every term in the book is visible in one place. Expect to find
   inconsistencies in already-translated sections; fix them as `revise(chNN):`.

## Acceptance criteria

- [ ] Both files at `status: translated`; `just status-write` run.
- [ ] `LOCAL=1 just check` passes with parity comparing, not skipping.
- [ ] `check_glossary.py` reports zero warnings across the whole `fa/` tree.
- [ ] Every glossary headword appears in `glossary.yml` with a deciding issue.
- [ ] Ordering decision recorded in `STYLE.md`; any parity offset declared.

## Out of scope

Releasing. That is spec 009.

## Implementation notes

_(filled in during implementation)_
