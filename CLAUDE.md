# linji-lu-farsi — Persian translation of *The Zen Teachings of Master Lin-chi*

Persian translation of Burton Watson's English rendering of the *Lín-chi lù*
(臨濟錄). Pandoc Markdown, one file per section, built by Quarto into HTML, PDF
and EPUB. Published as a section of **kaavehdev.ir/translations/linji-lu/**.

The infrastructure is finished. What remains is the translation.

## Spec-driven workflow

Work is organised one spec at a time, in `specs/`. This mirrors the workflow in
the `kaavehdev` repository, with one adaptation: **a translation spec is not one
session.** A part takes weeks. Each body spec carries a per-section checklist,
and the status table tracks how far through it you are.

1. Read `specs/README.md` (roadmap + status) and `specs/000-overview.md` (shared
   context — read it every session).
2. Pick the spec the user asked for. If they did not name one, propose the first
   `⬜ Not started` spec whose dependencies are `✅ Done`, and confirm.
3. Set the status to `🟨 In progress` in `specs/README.md`.
4. Work **only** on that spec.
5. Verify the spec's **Acceptance criteria**.
6. Set `✅ Done`, commit.

### Rules

- **The spec is the contract.** If reality forces a deviation, do the sensible
  thing and record it in an `## Implementation notes` section on that spec.
- **Never invent a Persian rendering and present it as settled.** Terminology is
  decided in a GitHub issue, recorded in `glossary.yml` with a link back, and
  enforced by CI from then on. A rendering that has not been through that is a
  suggestion, and must be labelled as one.
- **`STYLE.md` is binding.** If it says `<<<TBD>>>` for something you need,
  that is a decision to ask for, not to make.
- **Never add the source text to this repository.** `source/` is gitignored
  because the English is licensed to the maintainer for translation only. It is
  not public domain.
- One sentence per line in everything under `fa/`.

## Stack facts

- Quarto book project; `_quarto.yml` lists all 75 chapters in four parts.
- PDF is **LuaLaTeX**, not XeLaTeX — under XeLaTeX, babel's `bidi=default`
  reverses Latin-script runs inside Persian. Reasoning in `tex/preamble.tex`.
- `just check` runs everything CI runs; `LOCAL=1 just check` skips the container
  and is what you want for a fast loop. `just venv` sets the host env up.
- Four checkers in `tools/`: orthography (`normalize.py`), semantic line breaks,
  source/translation block parity, glossary terms. 153 tests.
- `check_parity.py` only works locally — CI has no `source/`.

## Quality bar

- `just check` green before every commit.
- Read the typeset PDF, not the Markdown, before calling a section done. Bidi,
  ZWNJ and line-break faults are obvious typeset and invisible in a diff.
- Every commit signed off (`git commit -s`); the DCO check enforces it.
- Commit convention: `translate(chNN):`, `revise(chNN):`, `term:`, `fix(chNN):`,
  `build:`.
