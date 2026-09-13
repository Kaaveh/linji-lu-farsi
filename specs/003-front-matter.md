# 003 — Front Matter

**`fa/preface.md`, `fa/translators-introduction.md`, `fa/ma-fang-preface.md`,
`fa/record-title-page.md` · 4 files · 7,734 words · 11 notes**

## Context

Four files, but three different registers and none of them the book's own:

- `preface.md` — Watson's short preface, opening with a poem by Ikkyū in
  blockquote. Modern, personal. No notes.
- `translators-introduction.md` — the bulk of it. Modern scholarly English:
  historical context, textual history, Chan lineage. This is the hardest prose in
  the repository and nothing like the sayings.
- `ma-fang-preface.md` — Ma Fang's 1120 preface. Classical Chinese formality,
  contemporary with the text itself.
- `record-title-page.md` — a title page. Almost no words. No notes.

**Do this late**, after the body. Discovering at 7,000 words that the scholarly
register does not work is expensive, and the introduction discusses terminology
the body will have already settled — translating it first means guessing at
choices you have not made yet.

## Goal

Four files at `status: translated`, `just check` green, PDF read.

## Dependencies

001, 002. In practice the body parts as well — see `specs/README.md`.

## Requirements

1. **A fourth register.** `STYLE.md` §1 covers narration, sermon, dialogue and
   verse. Watson's introduction is none of those. Add a decision for
   modern scholarly prose, and note that Ma Fang's preface is different again.

2. **The introduction must agree with the body.** It names and discusses terms
   the body already renders. Every one must match `glossary.yml`;
   `check_glossary.py` will say so if not.

3. **Ikkyū's poem.** Four lines of verse in a blockquote, using Markdown hard
   line breaks — two trailing spaces, which the pre-commit hooks preserve
   deliberately. Do not let it reflow into prose. §7 governs the verse form.

4. **Watson speaks as translator here.** The Persian edition has two translators
   in play: Watson into English, and you into Persian. Decide how the reader
   knows which is speaking — this is the one place where a translator's note
   about the translator's introduction may be warranted.

5. **`record-title-page.md` is nearly empty.** Check what parity expects before
   assuming it is trivial.

## Acceptance criteria

- [ ] All four at `status: translated`; `just status-write` run.
- [ ] `LOCAL=1 just check` passes with parity comparing, not skipping.
- [ ] `check_glossary.py` reports no warnings for these files — every term the
      introduction discusses matches the body's rendering.
- [ ] The Ikkyū poem renders as four lines in HTML, PDF and EPUB.
- [ ] `STYLE.md` §1 covers the scholarly register explicitly.

## Out of scope

The body. The appendix and glossary, which are spec 008.

## Implementation notes

_(filled in during implementation)_
