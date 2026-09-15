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

6. **Per section, the gTranslator loop.** One `source/` file at a time, never
   concatenated — the command and the reasons are in `000-overview.md`. Draft
   with `-w --raw`, revise against `STYLE.md`, restore the note markup per §6,
   run `LOCAL=1 just fix` then `LOCAL=1 just check`, set `status:` (`draft`
   while the machine output is still raw, `translated` once you have been
   through it), and read the section in the PDF before moving on.

   `translators-introduction.md` is the largest single file in the repository at
   39,543 characters — nine chunks at gTranslator's 4,500 default. Expect chunk
   boundaries to fall mid-argument and check the seams.

## Acceptance criteria

- [x] All four at `status: reviewed`; `just status-write` run. See
      implementation note 4 — `reviewed` is this project's finished state.
- [x] `LOCAL=1 just check` passes with parity comparing, not skipping —
      5 files match (the four here plus `42.md` from spec 002).
- [x] `check_glossary.py` reports no warnings for these files. Trivially true:
      `glossary.yml` is still empty, because terminology needs the issue process
      and the repo has no remote. Not a real test of agreement with the body yet.
- [x] The Ikkyū poem renders as four lines in HTML, PDF and EPUB — verified as
      3 `<br>` in the HTML and EPUB blockquote, and read on PDF page 9.
- [~] `STYLE.md` §1 covers the scholarly register explicitly. **Not done, and
      deliberately so** — §1 was dropped with spec 001, since register binds a
      human editor and there is none. Requirements 1 and 4 fall with it.

## Out of scope

The body. The appendix and glossary, which are spec 008.

## Implementation notes

**1. Requirements 1 and 4 are void.** Both are register decisions — a fourth
register for scholarly prose, and how the reader tells Watson-as-translator from
the Persian translator. Spec 001 was dropped, so there is no register layer to
add one to. Requirements 2, 3, 5 and 6 were done as written.

**2. A gTranslator bug, found here and fixed upstream.** The `-w` path merged a
paragraph at every chunk boundary. `split_chunks` is lossless — each chunk
carries its own trailing separator — but the page returns text with `.strip()`
applied, so that separator never comes back, and `translate_web` then rejoined
the results with `"\n".join(...)`. A paragraph break became a line break, and any
placeholder sitting just before the seam was swallowed with it. Breaks *inside* a
chunk were never affected, which is why only long files showed it.

Fixed in `~/Project/Backend/gTranslator` as `_rejoin()`: re-append each chunk's
own whitespace and join with nothing. Whitespace is restored from both ends,
because when a single paragraph exceeds the limit `split_chunks` falls through to
finer separators and a chunk can carry its separator in front. Three tests added
there; its existing two still pass. On this file the fix recovered 11 of the 15
lost paragraph breaks.

**3. The remaining 4 were Google, not gTranslator.** Reproduced with chunk 9
submitted alone: 3,958 characters, 7 paragraphs in, 6 out, trailing placeholder
gone. It is not positional — a 140-character submission ending in the same
placeholder round-tripped perfectly, and across three whole-file runs the casualty
moved (placeholder 4, then 4 again, then 2). It is a per-request failure rate that
rises with submission size.

The answer is to keep each submission small and verify it: 46 groups of ~1,200
characters, checking each group's placeholder set and paragraph count and retrying
only what failed. All 46 passed first time. Written into `STYLE.md` §6 with the
list of nine files that need it. The other 66 fit in one request.

The grouping driver lives in the session scratchpad, not in `tools/` — it is 40
lines, it was needed for one file here and eight later, and it is not obvious yet
whether it belongs in this repo or in gTranslator as a `--verify` mode. Worth
deciding before spec 005, which has `19.md` in it.

**4. Status: `reviewed`.** Settled by the maintainer while this spec was open:
the pipeline output is the final text, so neither `draft` nor `translated`
applies. All five translated files are `status: reviewed`, `restore` writes it,
and the project now uses only `untranslated` and `reviewed`.

**5. `anchors.py` gained two things** this spec forced:

- `-o`, which writes only after validation passes. A shell redirect truncates
  the target *before* the tool runs, so when `restore` correctly refused the bad
  introduction draft, it had already destroyed `fa/translators-introduction.md`.
  Recovered with `git checkout`; the flag means it cannot recur. Two tests.
- A hard-line-break count in `--check`. The Ikkyū poem's three trailing
  double-spaces do not survive translation, and without them four lines of verse
  reflow into a paragraph — correct-looking Markdown, wrong book. `restore`
  cannot reinstate them reliably (it would need the translated block to align
  line for line), so the check reports the loss and the fix is manual. This is
  the only verse in the book; `grep -n '  $' source/*.md` finds nothing else.

**6. `glossary.yml` is still empty**, so requirement 2 — the introduction must
agree with the body's terminology — passed without testing anything. It cannot
be tested until the terminology process runs, and that needs a git remote. The
introduction discusses a lot of terms the body will later render; expect to
revisit these four files once `glossary.yml` has entries.

**7. A note marker in a running head.** `ma-fang-preface.md` carries a note
reference on its title, so the PDF running head reads `دیباچهٔ ما فانگ¹`
(page 24). Harmless but slightly odd. `24.md` will do the same when spec 006
reaches it — see spec 002 note 4.

**8. Bidi confirmed good.** The introduction is dense with Latin-script
romanizations inside Persian prose — `Lin-chi lu`, `Ho-nan`, `Hsing`, `Ts'ao`,
`(780-865)`, `saindhava` — and all of them read left-to-right in the typeset
page. That is the LuaLaTeX choice in `tex/preamble.tex` doing its job; this file
is the best evidence in the book that it was the right call.
