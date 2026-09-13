# 005 — Part Two: Instructing the Group

**`fa/10.md` – `fa/23.md` · 14 sections · 17,962 words · 134 notes**

## Context

**This part is 45% of the book by word count and 53% of its notes.** Fourteen
files, but four times the prose of any other part. It is the doctrinal core —
sustained sermons rather than exchanges — and it is where the translation will
either read as thought or as paraphrase.

Section 19 alone carries 47 notes, more than Parts One, Three and Four combined
per section. Section 11 has 16, section 23 has 17, section 18 has 10.

Do this **last of the body**, after 004, 006 and 007. By then the voice is
settled across 55 sections and you are translating rather than deciding.

## Goal

Fourteen sections at `status: translated`, `just check` green, PDF read.

## Dependencies

004. In practice also 006 and 007 — see the recommended order in
`specs/README.md`.

## Requirements

1. **`fa/10.md` declares `<!-- parity: offset -1 -->`** — it carries the part
   heading.

2. **Budget by section, not by part.** At roughly 1,280 words each these are not
   one sitting. Sections 11, 19 and 23 are substantially larger than the rest and
   should be planned as multiple sessions on their own.

3. **This is the sermon register.** §1 decided it; this part is where it is
   actually exercised at length. If it does not hold up over 1,000 continuous
   words, that is a real finding — raise it before translating the rest of the
   part, not after.

4. **The technical vocabulary concentrates here.** The four-fold formulations,
   the true man of no rank, the fourfold relation of guest and host, the three
   mysterious gates. Each is a terminology issue. Expect this part to add more
   `glossary.yml` entries than the other three combined.

5. **Section 19's notes need their own pass.** Forty-seven notes in one section
   is a document in itself. Translate the body first, then the notes, then check
   every back-link resolves.

6. **Per section**: `status: translated`, `LOCAL=1 just check`, read in the PDF.

## Sections

- [ ] `10.md` — 5 notes · part heading, offset
- [ ] `11.md` — 16 notes · large
- [ ] `12.md` — 3 notes
- [ ] `13.md` — 5 notes
- [ ] `14.md` — 3 notes
- [ ] `15.md` — 6 notes
- [ ] `16.md` — 3 notes
- [ ] `17.md` — 4 notes
- [ ] `18.md` — 10 notes
- [ ] `19.md` — **47 notes · the largest single unit in the book**
- [ ] `20.md` — 2 notes
- [ ] `21.md` — 7 notes
- [ ] `22.md` — 6 notes
- [ ] `23.md` — 17 notes · large

## Acceptance criteria

- [ ] All fourteen at `status: translated`; `just status-write` run.
- [ ] `LOCAL=1 just check` passes with parity comparing, not skipping.
- [ ] The part read in the typeset PDF; section 19 re-read for note behaviour.
- [ ] Every note in 19 has a resolving back-link in the HTML output.
- [ ] Every technical term traces to an issue and a `glossary.yml` entry.

## Out of scope

Other parts. Front and back matter.

## Implementation notes

_(filled in during implementation)_
