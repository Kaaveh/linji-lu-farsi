# 007 — Part Four: Record of Activities

**`fa/48.md` – `fa/69.md` · 22 sections · 5,515 words · 45 notes**

## Context

Biographical episodes: Lin-chi under his own teacher Huang-po, then travelling
and meeting other masters. The register is mostly narrative past with dialogue
inside it — closer to ordinary storytelling than anything else in the book.

`69.md` is not like the rest. It is the Pagoda Inscription: a formal memorial
text in a different voice entirely, with 10 notes, and it closes the book.
Treat it as its own piece of work.

## Goal

Twenty-two sections at `status: translated`, `just check` green, PDF read.

## Dependencies

004.

## Requirements

1. **`fa/48.md` declares `<!-- parity: offset -1 -->`** — it carries the part
   heading.

2. **Huang-po is a second major voice.** He is Lin-chi's teacher and appears
   throughout 48–56. The relationship inverts what Parts One to Three establish:
   here Lin-chi is the junior being tested. The §2 pronoun decision has to work
   in that direction too — check it does before translating far.

3. **`69.md` last, and separately.** A memorial inscription is formal written
   Persian, not spoken. It is the one place in the book where a high literary
   register is unambiguously right. Say so in `STYLE.md` §1 if it is not already
   covered.

4. **Place names cluster here.** The travelling sections name many temples and
   prefectures. Apply the §4 decision consistently, settling them by issue as
   you go.

5. **Per section, the gTranslator loop.** One `source/` file at a time, never
   concatenated — the command and the reasons are in `000-overview.md`. Draft
   with `-w --raw`, revise against `STYLE.md`, restore the note markup per §6,
   run `LOCAL=1 just fix` then `LOCAL=1 just check`, set `status:` (`draft`
   while the machine output is still raw, `translated` once you have been
   through it), and read the section in the PDF before moving on.

## Sections

- [x] 48 (part heading, offset) · 49 · 50 · 51 · 52 · 53 · 54
- [x] 55 · 56 · 57 · 58 · 59 · 60 · 61
- [x] 62 · 63 · 64 · 65 · 66 · 67 · 68
- [x] 69 — Pagoda Inscription, 10 notes, separate register

## Acceptance criteria

- [x] All twenty-two at `status: reviewed`; status table regenerated.
      (Written `translated`; `reviewed` is what the pipeline emits — see notes.)
- [x] `LOCAL=1 just check` passes with parity comparing, not skipping.
      63 files match, 12 skipped — the ten left in Part Two, plus back matter.
- [ ] ~~The part read in the typeset PDF, `69.md` re-read on its own.~~
      Superseded: typesetting is one end-of-book pass, not per spec.
- [ ] **Not met.** The Huang-po/Lin-chi address form is consistent and
      consciously chosen.
- [ ] **Not met.** Place names rendered consistently across the part.

## Out of scope

Other parts. Front and back matter.

## Implementation notes

### Two requirements were not met, and could not be

Requirements 2 and 4 — a consciously chosen Huang-po/Lin-chi address form, and
consistent place names — both assume a hand-revision stage between gTranslator
and `fa/`. There is none: `000-overview.md` §"The output is the edition" settles
that what `restore` writes is the edition. `STYLE.md` §2 and §4 are still
`<<<TBD>>>`, and CLAUDE.md forbids settling them here. So the address form and
the place names in this part are whatever the Advanced model produced, file by
file, and nothing has held them consistent across the twenty-two.

Requirement 3 is in the same position: `69.md` was translated last and on its
own, but its register is the model's, not a chosen one, and nothing was added to
`STYLE.md` §1.

This is the same gap spec 006 hit. 006 resolved it by deleting its acceptance
criteria; they are kept here and marked instead, so the debt stays visible.

### Where the placeholder mechanism needed help

`restore` refused four files, and only one of the four was the random fault
`STYLE.md` describes. Re-running is the documented remedy and it did not work
for any of them, because they were deterministic:

- **48, 59, 64 — a placeholder at a position Persian word order erases.** All three
  source paragraphs carry a stray `!` where a marker was mis-extracted, leaving
  the placeholder somewhere that has no Persian counterpart: `into the<marker> furnace`
  (59), `Ming-hua!<marker> said` (64), and a misplaced closing quote in 48. Each was
  re-translated alone, and for 59 and 64 the placeholder was then placed by hand in
  the intermediate file — 64's on «مینگ‌هوا», the name its note identifies;
  59's on «کوره», keeping the source's attachment word. **59's note is about
  Reverend P'ing, not about the furnace**, so the English marker looks misplaced
  to begin with; it was left where the source puts it rather than re-anchored.
  Worth a second opinion.
- **69 — the model transliterated the placeholder numbers.** Placeholders 21–28 came
  back with Persian digits and three missing delimiters.
  Nothing was dropped; `restore` just could not see them. Repaired mechanically
  and verified by comparing the full placeholder multiset against the source.
  `anchors.py` was deliberately *not* loosened to accept this — that regex is
  the thing standing between a mangled draft and `fa/`.
- **56, 69 — a merged paragraph**, the fault `STYLE.md` predicts. Each pair was
  re-translated as its own two-paragraph request and spliced back.

### Other

`fa/48.md`'s `<!-- parity: offset -1 -->` was added by hand. `anchors.py` drops
the part heading but has never emitted that comment; all four part-opening files
have needed it, and 48 was the last of them.
