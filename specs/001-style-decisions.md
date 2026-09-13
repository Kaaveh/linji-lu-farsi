# 001 — Style Decisions

## Context

`STYLE.md` exists with eight scaffolded sections, every decision marked
`<<<TBD>>>`. Nothing else can start until the register question in §1 is
answered, because every sentence of the book is written in one register or
another and changing your mind at section 40 means revising 39 sections.

This is a decision session, not a translation session. It produces prose in
`STYLE.md` and nothing under `fa/`.

## Goal

`STYLE.md` §1–§8 with no `<<<TBD>>>` left in §1, §2, §3 and §4. §5–§8 may stay
open if the book has not yet forced them.

## Dependencies

None.

## Requirements

1. **§1 Register.** The load-bearing one. Decide narration, sermon, dialogue and
   verse separately, and decide whether the shift between them is signalled to
   the reader or left implicit.

2. **§2 Pronouns and honorifics.** How master and monk address each other, شما
   versus تو, how «Master» is rendered, how officials are titled. Test the
   decision against a section where Lin-chi is deliberately rude — if the
   Persian cannot be rude, the decision is wrong.

3. **§3 Dialogue punctuation.** Guillemets or dashes; nested quotation, which
   this book needs constantly; where attribution sits; how a shout is set. Note
   that `normalize.py` converts ASCII and curly quotes to «» — if the decision
   goes the other way, turn `quotes` off in `pyproject.toml` in the same commit.

4. **§4 Proper nouns.** Transliterate, keep Latin, or both on first occurrence.
   The source is Wade-Giles (Lin-chi, Huang-po, Ch'an), not Pinyin, and the two
   transliterate into Persian differently — decide which is the basis. Decide
   what happens to the Wade-Giles apostrophe.

5. **Seed the glossary.** §4 implies a `glossary.yml` entry per recurring name.
   Do not write them in this spec — open the terminology issues, so the decision
   log starts as it means to continue. Record the issue numbers in `STYLE.md`.

6. **Do not decide in advance what the book has not asked.** §5–§8 exist so that
   when the question arrives there is a place to put the answer. A guess written
   now is worse than a `<<<TBD>>>`, because it looks settled.

## Acceptance criteria

- [ ] `STYLE.md` §1–§4 contain decisions, each with a sentence of reasoning.
- [ ] The §2 decision was tested against at least one deliberately blunt
      exchange and survives it.
- [ ] `pyproject.toml` matches the §3 decision on quotes.
- [ ] Terminology issues opened for the recurring proper nouns; numbers recorded.
- [ ] No `<<<TBD>>>` remains in §1–§4; any left in §5–§8 is deliberate.
- [ ] `LOCAL=1 just check` passes.

## Out of scope

Translating anything. Populating `glossary.yml` — that follows from the issues,
not from this spec.

## Implementation notes

_(filled in during implementation)_
