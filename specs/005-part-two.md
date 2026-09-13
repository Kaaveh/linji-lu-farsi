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
   mysterious gates. Each is a terminology issue. Expect this part to settle
   more of them than the other three combined.

5. **Section 19's notes need their own pass.** Forty-seven notes in one section
   is a document in itself. Translate the body first, then the notes, then check
   every back-link resolves.

6. **Per section, the gTranslator loop.** One `source/` file at a time, never
   concatenated — the command and the reasons are in `000-overview.md`. Draft
   with `-w --raw`, revise against `STYLE.md`, restore the note markup per §6,
   run `LOCAL=1 just fix` then `LOCAL=1 just check`, set `status:` (`draft`
   while the machine output is still raw, `translated` once you have been
   through it), and read the section in the PDF before moving on.

## Sections

- [x] `10.md` — 5 notes · part heading, offset
- [ ] `11.md` — 16 notes · large — **hand-finish:** dropped 4–9, 12–16, 47; duplicated 46
- [ ] `12.md` — 3 notes — **hand-finish:** a paragraph merged (10 blocks, source has 11)
- [x] `13.md` — 5 notes
- [ ] `14.md` — 3 notes — **hand-finish:** dropped 3, 4
- [ ] `15.md` — 6 notes — **hand-finish:** a paragraph merged (13 blocks, source has 14)
- [ ] `16.md` — 3 notes — **hand-finish:** a paragraph merged (9 blocks, source has 10)
- [ ] `17.md` — 4 notes — **hand-finish:** dropped 2, 3, 4
- [ ] `18.md` — 10 notes — **hand-finish:** dropped 7, 8
- [ ] `19.md` — **47 notes · the largest single unit in the book** — **hand-finish:** dropped 12, 24, 25, 40–43
- [x] `20.md` — 2 notes
- [ ] `21.md` — 7 notes — **hand-finish:** a paragraph merged (21 blocks, source has 22)
- [x] `22.md` — 6 notes
- [ ] `23.md` — 17 notes · large — **hand-finish:** duplicated 23, 25, 27

## Acceptance criteria

- [ ] All fourteen at `status: translated`; `just status-write` run.
- [ ] `LOCAL=1 just check` passes with parity comparing, not skipping.
- [ ] The part read in the typeset PDF; section 19 re-read for note behaviour.
- [ ] Every note in 19 has a resolving back-link in the HTML output.
- [ ] Every technical term traces to a terminology issue.

## Out of scope

Other parts. Front and back matter.

## Implementation notes

**Partial. Four of fourteen sections are in; ten are left for the maintainer to
finish by hand.** The spec stays `🟨 In progress`. Which markers are missing from
which file is recorded against each section above, so nobody has to re-run a
translation to find out what is wrong with it.

Landed: `10.md`, `13.md`, `20.md`, `22.md`. `fa/10.md` carries the
`<!-- parity: offset -1 -->` required by requirement 1. Parity now compares 18
files and skips 57.

### Why the other ten were skipped

The maintainer's call, once the failure turned out not to be a retry problem.
Two distinct faults, both in the model rather than in this repository:

| Fault | Caught by | Sections |
|---|---|---|
| A note marker deleted, or emitted twice | `anchors.py restore` | 11, 14, 17, 18, 19, 23 |
| Two paragraphs merged into one | `check_parity.py` | 12, 15, 16, 21 |

Both refuse the file rather than publishing it damaged, which is the behaviour
spec 002 built them for. Nothing incomplete was written: `restore -o` leaves the
stub alone, and the four merged files were reverted to their stubs with
`git checkout` once parity reported them.

The merge fault is the more dangerous of the two, because `restore` accepts a
merged draft — every sentinel is present and correctly placed. Only the block
count shows it. `check_parity.py` is the sole thing standing between a merged
paragraph and the published edition, which is worth knowing before anyone
proposes relaxing it.

### Submission size is not the lever, and §6 needs amending

`STYLE.md` §6 says the answer to a damaged long file is smaller submissions in
verified groups. That did not reproduce here.

- `14.md` (3,557 chars stripped) lost sentinels 3 and 4 at `--chunk 4500`, lost
  them again at `--chunk 1200`, and lost them again with the single affected
  block submitted alone — eight submissions, same casualties every time. This is
  not the stochastic per-request failure spec 003 measured; for this file it is
  deterministic.
- Both losses sit inside paragraphs of about a thousand characters, and
  `split_chunks` prefers paragraph boundaries. A paragraph is therefore the
  smallest thing that is ever submitted, so no `--chunk` below its length
  changes what the model sees. §6's "groups of about 1,200 characters" cannot go
  finer than one paragraph, which is the granularity that would be needed here.
- Four of the ten failures are in files §6 does not list as long at all — 12,
  14, 16, 17 are all under 4,800 characters. Length is not the predictor §6
  takes it to be.

§6 should be corrected on both points. Left undone here rather than rewritten on
one part's evidence.

### A repair driver was tried and removed

`tools/translate.py`: translate the file whole, compare each translated block's
sentinel set against its source block, and re-submit only the damaged blocks.
The idea was to make retries granular without a browser session per group.

It was deleted. Two reasons, both from running it:

- **It did not help.** Block-level resubmission recovered nothing on `14.md` or
  `17.md`, because those losses are deterministic rather than stochastic.
- **It was worse than the documented loop.** It gated on whole-file block-count
  equality before attempting any repair, so a single merged paragraph made it
  reject a file it had not yet tried to fix — and it reported the failure as
  *every* marker missing, because the draft variable was still empty on that
  path. The plain `000-overview.md` loop got 8 files through where the driver
  got none.

So spec 003's open question — whether the grouping driver belongs in `tools/`
or in gTranslator — is answered "neither, on this evidence". Per-block retry
does not address the fault that actually dominates here. Anyone revisiting it
should start from why a marker is deleted deterministically at one position and
never at another, which is still unexplained.

### Not attempted

Requirements 3, 4 and 5 — the sermon register at length, the technical
vocabulary as terminology issues, and section 19's note pass — are all
downstream of having the sections translated. No terminology was settled; the
`glossary.yml` mechanism was removed outright after this spec, having never
held an entry across the first eighteen translated files. The four landed
sections were not read in the typeset PDF.
