# 004 — Part One: Ascending the Hall

**`fa/01.md` – `fa/09.md` · 9 sections · 2,506 words · 25 notes**

## Context

The smallest body part, and therefore the pilot. Nine short sections in which
Lin-chi formally takes the seat and is questioned. The register is mixed from the
first page: ceremonial framing, then a monk asks something and gets shouted at.

This is where the 001 and 002 decisions meet real text. Expect to revise
`STYLE.md` during this spec — that is the point of doing the smallest part first,
while revising costs nine sections rather than sixty-nine.

## Goal

Nine sections at `status: translated`, `just check` green, PDF read.

## Dependencies

001, 002.

## Requirements

1. **`fa/01.md` declares `<!-- parity: offset -1 -->`.** Its source opens with
   `## Part One: Ascending the Hall`, which lives in `_quarto.yml` as a `part:`
   entry instead. Without the offset, parity reports a false mismatch.

2. **Translate in order**, 01 through 09. They build on each other and the
   opening frame recurs.

3. **Treat `STYLE.md` as provisional here and only here.** When the text
   contradicts a decision, change the decision, then revise what you already
   translated to match. Record the change in `STYLE.md` with a line of
   reasoning. After this spec, the guide is binding.

4. **Terminology as you meet it.** Recurring vocabulary starts in this part —
   the formulas around ascending the hall, the address to the assembly, «the
   great concern». Open an issue, settle it, record it in `glossary.yml`. Do not
   accumulate a private list to formalise later.

5. **Per section**: set `status: translated`, run `LOCAL=1 just check`, and read
   that section in the PDF before moving on.

## Sections

- [ ] `01.md` — 8 notes · has the part heading, needs the parity offset
- [ ] `02.md` — 1 note
- [ ] `03.md` — 3 notes · the "true man of no rank" passage
- [ ] `04.md` — 3 notes
- [ ] `05.md` — 1 note
- [ ] `06.md` — 3 notes
- [ ] `07.md` — 2 notes
- [ ] `08.md` — 1 note
- [ ] `09.md` — 3 notes

## Acceptance criteria

- [ ] All nine at `status: translated`; `just status-write` run.
- [ ] `LOCAL=1 just check` passes, parity included — nine files compared, not
      skipped.
- [ ] The whole part read in the typeset PDF.
- [ ] Every terminology decision made here traces to an issue and a
      `glossary.yml` entry.
- [ ] Any `STYLE.md` change made during this spec is applied consistently across
      all nine sections.

## Out of scope

Other parts. Front and back matter.

## Implementation notes

_(filled in during implementation)_
