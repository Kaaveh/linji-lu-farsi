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

- [ ] 48 (part heading, offset) · 49 · 50 · 51 · 52 · 53 · 54
- [ ] 55 · 56 · 57 · 58 · 59 · 60 · 61
- [ ] 62 · 63 · 64 · 65 · 66 · 67 · 68
- [ ] 69 — Pagoda Inscription, 10 notes, separate register

## Acceptance criteria

- [ ] All twenty-two at `status: translated`; `just status-write` run.
- [ ] `LOCAL=1 just check` passes with parity comparing, not skipping.
- [ ] The part read in the typeset PDF, `69.md` re-read on its own.
- [ ] The Huang-po/Lin-chi address form is consistent and consciously chosen.
- [ ] Place names rendered consistently across the part.

## Out of scope

Other parts. Front and back matter.

## Implementation notes

_(filled in during implementation)_
