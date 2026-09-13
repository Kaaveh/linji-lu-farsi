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

5. **Per section, the gTranslator loop.** One `source/` file at a time, never
   concatenated — the command and the reasons are in `000-overview.md`. Draft
   with `-w --raw`, revise against `STYLE.md`, restore the note markup per §6,
   run `LOCAL=1 just fix` then `LOCAL=1 just check`, set `status:` (`draft`
   while the machine output is still raw, `translated` once you have been
   through it), and read the section in the PDF before moving on.

## Sections

- [x] `01.md` — 8 notes · has the part heading, needs the parity offset
- [x] `02.md` — 1 note
- [x] `03.md` — 3 notes · the "true man of no rank" passage
- [x] `04.md` — 3 notes
- [x] `05.md` — 1 note
- [x] `06.md` — 3 notes
- [x] `07.md` — 2 notes
- [x] `08.md` — 1 note
- [x] `09.md` — 3 notes

## Acceptance criteria

- [x] All nine at `status: reviewed` (not `translated` — see notes);
      `just status-write` run.
- [x] `LOCAL=1 just check` passes, parity included — nine files compared, not
      skipped.
- [ ] The whole part read in the typeset PDF. **Not done — waived by the
      maintainer.** The PDF builds (`LOCAL=1 just pdf`), but the pages were
      never read.
- [ ] Every terminology decision made here traces to an issue and a
      `glossary.yml` entry. **Not done — waived by the maintainer.**
      `glossary.yml` is still empty; see notes.
- [x] Any `STYLE.md` change made during this spec is applied consistently across
      all nine sections. Vacuous: no `STYLE.md` change was needed.

## Out of scope

Other parts. Front and back matter.

## Implementation notes

**Closed with two acceptance criteria unmet, by the maintainer's decision.**
Both are recorded above rather than quietly ticked.

### Deviations from the requirements as written

- **Requirement 3 no longer applies.** It made `STYLE.md` provisional for this
  part so the text could correct the register decisions. Spec 001 was dropped
  after this spec was written: `fa/` carries pipeline output with no hand
  revision, so there is no register decision for the text to argue with. No
  `STYLE.md` change was needed and none was made.
- **Requirement 5's `status:` instruction is superseded.** It says `draft` while
  raw and `translated` once revised. `000-overview.md` settled that neither
  value is used — what `restore` writes is the edition, so all nine are
  `reviewed`.

### What was actually run

The `000-overview.md` loop, unchanged, one file at a time:

```bash
tools/anchors.py strip source/NN.md -o $S/NN.en.md
gtranslate.py -f $S/NN.en.md -t fa -w --raw -o $S/NN.fa.md
tools/anchors.py restore source/NN.md $S/NN.fa.md -o fa/NN.md
LOCAL=1 just fix
```

Sentinels in equalled sentinels out on all nine, first attempt, so no file
needed re-running. None of the nine is on `STYLE.md` §6's list of long files, and
none needed the verified-group procedure — `01.md` is the largest at 4,580
characters stripped, which gTranslator chunks in two with no seam damage.

`fa/01.md` carries `<!-- parity: offset -1 -->` as required; it is the first
such directive in `fa/`. Parity then reports 14 files matching, 61 skipped.

### Terminology is unsettled, and the text shows it

This is the real debt. `glossary.yml` is still `terms: []`, so
`check_glossary.py` reports zero warnings only because it is enforcing nothing.
The drift is visible across the nine sections:

| source | renderings produced |
|---|---|
| ascend the hall / step up to the lecture seat | جایگاه سخنرانی · جایگاه سخن · منبر · تالار |
| Constant Attendant | مقام عالی‌رتبه (01) · خدمتگزار دائم (01 notes) |
| basic meaning of Buddhism | معنای بنیادین بودیسم — consistent |
| the great concern | دغدغه‌ی بزرگ — consistent |
| true man of no rank | انسان حقیقیِ بی‌مقام — consistent |
| host and guest | مهمان و میزبان — consistent |

"Constant Attendant" diverging inside a single file is the worst of it: the same
official is two different people to a reader. The remote and `gh` are configured
now, so the issue process is available to whoever picks this up — it was not
run here. Part Three and Four will multiply this, since they are mostly the same
formulas repeated.

### Build

There is no Docker on the maintainer's machine, so `just pdf` fails at the
container. `LOCAL=1 just pdf` renders on the host — quarto 1.x and TeX Live 2026
LuaHBTeX are both installed — and produced
`_book/آموزه‌های-ذن-استاد-لین‌چی.pdf` without error. The pages were not read.
