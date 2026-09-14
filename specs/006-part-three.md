# 006 — Part Three: Testing and Rating

**`fa/24.md` – `fa/47.md` · 24 sections · 4,099 words · 36 notes**

## Context

The most sections of any part and the fewest words each — average 170 words.
These are encounter stories: a monk arrives, something sharp happens, someone
leaves. Six of them have no notes at all (25, 28, 31, 37, 47, 52 — the first five
are in this part).

This is the hardest test of the dialogue register and the easiest part to make
sound flat. Each exchange turns on timing, and Persian that is one degree too
formal kills the joke. Do this second, after Part One, while the register
decision is still fresh enough to revise.

## Goal

Twenty-four sections at `status: translated`, `just check` green, PDF read.

## Dependencies

004.

## Requirements

1. **`fa/24.md` declares `<!-- parity: offset -1 -->`** — it carries the part
   heading, which lives in `_quarto.yml`. Note that its source part heading also
   contains a note reference; check where that note belongs after the heading
   moves out.

2. **Read each section aloud before committing it.** These are spoken exchanges.
   If it does not work aloud in Persian it does not work.

3. **Keep the shouts short.** English "the Master gave a shout" is four words;
   whatever Persian equivalent §3 settled must not sprawl. Consistency matters
   more than elegance here — it recurs dozens of times.

4. **P'u-hua appears repeatedly** (26, 28, 29, 47). His register is distinct from
   Lin-chi's — he is a holy fool. Decide once whether that comes through in the
   Persian, and be consistent.

5. **Per section, the gTranslator loop.** One `source/` file at a time, never
   concatenated — the command and the reasons are in `000-overview.md`. Draft
   with `-w --raw`, revise against `STYLE.md`, restore the note markup per §6,
   run `LOCAL=1 just fix` then `LOCAL=1 just check`, set `status:` (`draft`
   while the machine output is still raw, `translated` once you have been
   through it), and read the section in the PDF before moving on.

## Sections

- [ ] 24 (part heading, offset) · 25 · 26 · 27 · 28 · 29 · 30 · 31
- [ ] 32 · 33 · 34 · 35 · 36 · 37 · 38 · 39
- [ ] 40 · 41 · 42 · 43 · 44 · 45 · 46 · 47

## Out of scope

Other parts. Front and back matter.

## Implementation notes

_(filled in during implementation)_
