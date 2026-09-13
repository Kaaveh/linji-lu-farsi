# Specs Roadmap — linji-lu-farsi

How to work on this project: see `CLAUDE.md` at the repo root. Shared context for
every spec: [`000-overview.md`](./000-overview.md).

Unlike a code project, **one spec here is not one session.** The body specs cover
weeks of work and carry a per-section checklist. Update the **Status** column
when you start (`🟨 In progress`) and when you finish (`✅ Done`).

## Status table

| #   | Spec                                                        | Depends on | Status         |
|-----|-------------------------------------------------------------|------------|----------------|
| 000 | [Overview & shared context](./000-overview.md)              | —          | 📖 Reference   |
| 001 | [Style decisions](./001-style-decisions.md)                 | —          | ⬜ Not started |
| 002 | [Notes & apparatus convention](./002-notes-and-apparatus.md)| 001        | ⬜ Not started |
| 003 | [Front matter](./003-front-matter.md)                       | 001, 002   | ⬜ Not started |
| 004 | [Part One — Ascending the Hall](./004-part-one.md)          | 001, 002   | ⬜ Not started |
| 005 | [Part Two — Instructing the Group](./005-part-two.md)       | 004        | ⬜ Not started |
| 006 | [Part Three — Testing and Rating](./006-part-three.md)      | 004        | ⬜ Not started |
| 007 | [Part Four — Record of Activities](./007-part-four.md)      | 004        | ⬜ Not started |
| 008 | [Back matter](./008-back-matter.md)                         | 001–007    | ⬜ Not started |
| 009 | [First release & publication](./009-release-and-publish.md) | 003–008    | ⬜ Not started |

## Recommended order

Not top to bottom. The numbering follows the book; the work should not.

```
001 → 002 → 004 → 006 → 007 → 005 → 003 → 008 → 009
      style    pilot   short   short   core  intro  back  ship
```

- **004 (Part One) is the pilot.** Nine sections, 2,506 words — the smallest body
  part. Translate it first to test the 001 and 002 decisions against real text
  while revising is still cheap.
- **006 and 007 next.** Short exchanges, mostly dialogue. They exercise the
  register decision hardest and build momentum: 46 of the 69 sections.
- **005 (Part Two) last of the body.** It is 45% of the whole book by word count
  and the most doctrinally dense. Attempt it once the voice is settled.
- **003 (front matter) late.** Watson's translator's introduction is 7,700 words
  of modern scholarly English — a different register from the book itself, and a
  poor place to discover your style decisions do not hold.
- **008 (back matter) after the body**, because the glossary's Persian headwords
  must match the terminology the body actually settled on.

## Scale

| Group             | Files | Words  | Notes |
|-------------------|------:|-------:|------:|
| Front matter      |     4 |  7,734 |    11 |
| Part One (01–09)  |     9 |  2,506 |    25 |
| Part Two (10–23)  |    14 | 17,962 |   134 |
| Part Three (24–47)|    24 |  4,099 |    36 |
| Part Four (48–69) |    22 |  5,515 |    45 |
| Back matter       |     2 |  1,990 |     2 |
| **Total**         | **75** | **39,806** | **253** |

Word counts are of the English source prose, notes included. Note counts are note
*definitions*; each has a reference anchor and a definition anchor, so the repo
contains 506 anchors in total.

## Definition of done (every spec)

- [ ] Every item in the spec's **Acceptance criteria** is checked and true.
- [ ] `LOCAL=1 just check` passes.
- [ ] The typeset PDF was read for the sections touched — not just the Markdown.
- [ ] `status:` front matter updated, and `just status-write` run.
- [ ] No terminology invented outside the issue → `glossary.yml` process.
- [ ] Status table above updated; work committed, signed off.
