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
- **Never invent a Persian rendering and present it as settled.** A rendering
  that has not been argued out is a suggestion, and must be labelled as one.
  Nothing enforces terminology mechanically any more — see `STYLE.md` §4.
- **`STYLE.md` is binding.** If it says `<<<TBD>>>` for something you need,
  that is a decision to ask for, not to make.
- **Never add the source text to this repository.** `source/` is gitignored
  because the English is licensed to the maintainer for translation only. It is
  not public domain.
- **Translate with `gTranslator`, one file at a time.** See
  `specs/000-overview.md` for the command and the reasoning. `-w` is mandatory —
  every other mode serves a much weaker model, and it fails silently. Never
  concatenate files: the book is 245,394 characters against a 5,000-character
  cap, and `fa/` must mirror `source/` file-for-file or parity cannot pair them.
- **Always through `tools/anchors.py`.** `strip` before, `restore -o` after.
  Sent raw, the translator silently deletes every note anchor. Never `>` into
  `fa/` — a redirect truncates the file before the tool can refuse a bad draft.
- **A translated file is `status: reviewed`.** There is no hand-revision stage
  after the pipeline, so there is no later step to promote a `draft` into place:
  what `restore` writes is the edition. Do not use `draft` or `translated`.
- One sentence per line in everything under `fa/`.

## Stack facts

- Quarto book project; `_quarto.yml` lists all 75 chapters in four parts.
- PDF is **LuaLaTeX**, not XeLaTeX — under XeLaTeX, babel's `bidi=default`
  reverses Latin-script runs inside Persian. Reasoning in `tex/preamble.tex`.
- `just check` runs everything CI runs; `LOCAL=1 just check` skips the container
  and is what you want for a fast loop. `just venv` sets the host env up.
- The four checkers are **not in this repository**. They are general, so they
  live in [`linji-tools`](https://pypi.org/project/linji-tools/), pinned in
  `tools/requirements.txt` and run as `python -m linji_tools.<name>`:
  orthography (`normalize`), semantic line breaks (`check_linebreaks`),
  source/translation block parity (`check_parity`), plus `status_table` and
  `make_stubs`. What makes them this book's is the `[tool.*]` sections of
  `pyproject.toml`; see spec 010.
- `tools/anchors.py` **does** stay here. It is the adapter: Watson's token
  pattern and the Persian form of every heading and marker. The round-trip it
  calls is `linji_tools.anchors`. 20 tests here, 154 there.
- `check_parity` only works locally — CI has no `source/`.

## Quality bar

- `just check` green before every commit.
- Read the typeset PDF, not the Markdown, before calling a section done. Bidi,
  ZWNJ and line-break faults are obvious typeset and invisible in a diff.
- Every commit signed off (`git commit -s`); the DCO check enforces it.
- Commit convention: `translate(chNN):`, `revise(chNN):`, `term:`, `fix(chNN):`,
  `build:`.
