# linji-lu-farsi — Persian translation of *The Zen Teachings of Master Lin-chi*

Persian translation of Burton Watson's English rendering of the *Lín-chi lù*
(臨濟錄). Pandoc Markdown, one file per section, built by Quarto into HTML, PDF
and EPUB. Published as a section of **kaavehdev.ir/translations/linji-lu/**.

The infrastructure is finished. What remains is the translation.

## Rules

There is no `specs/` directory. The book is translated — all 75 sections — so
the roadmap that carried it there was deleted rather than left to rot. Work is
whatever the user asks for.

- **Never invent a Persian rendering and present it as settled.** A rendering
  that has not been argued out is a suggestion, and must be labelled as one.
  Nothing enforces terminology mechanically any more — see `STYLE.md` §4.
- **`STYLE.md` is binding.** If it says `<<<TBD>>>` for something you need,
  that is a decision to ask for, not to make.
- **Never add the source text to this repository.** `source/` is gitignored
  because the English is licensed to the maintainer for translation only. It is
  not public domain.
- **Translate with `gTranslator`, one file at a time.** It lives at
  `~/Project/Backend/gTranslator`, is private, and nothing in `just check`
  depends on it — only producing a *new* draft does:

  ```bash
  GT=~/Project/Backend/gTranslator
  tools/anchors.py strip source/42.md -o /tmp/42.en.md
  "$GT/.venv/bin/python" "$GT/gtranslate.py" \
      -f /tmp/42.en.md -t fa -w --raw -o /tmp/42.fa.md
  tools/anchors.py restore source/42.md /tmp/42.fa.md -o fa/42.md
  ```

  `-w` is mandatory — every other mode serves the Classic model, which
  translates clause by clause and is markedly worse here. The failure is
  silent: the model picker claims "Advanced" while Classic is served, so judge
  the output text, never the picker. Never concatenate files: the book is
  245,394 characters against a 5,000-character cap, and `fa/` must mirror
  `source/` file-for-file or parity cannot pair them.
- **Always through `tools/anchors.py`.** `strip` before, `restore -o` after.
  Sent raw, the translator silently deletes every note anchor. Never `>` into
  `fa/` — a redirect truncates the file before the tool can refuse a bad draft.
- **When `restore` refuses, place the marker yourself — do not hand it back.**
  The model drops or duplicates a sentinel on some sections. The refusal quotes
  the English line each lost sentinel sat in, so the position is recoverable
  without reading `source/` and the draft back in full:

  ```
  error: 42.md: the model dropped sentinel(s) [2]
    ⟦2⟧  …asked; “In the case of the twelve-faced Kuan-yin, which face is the
         real one?”⟦2⟧
  ```

  Insert a bare `⟦2⟧` into `/tmp/42.fa.md` at the matching point in the Persian
  — the same clause, the same side of it — and run `restore` again. Three rules
  hold this together:

  - **Edit the draft in `/tmp`, never `fa/`.** `restore` is the only thing that
    writes `fa/`, and it validates first.
  - **Only ever insert or delete a bare `⟦n⟧`.** Never write anchor markup by
    hand; `restore` re-emits the token from `source/`, so what you are choosing
    is a position and nothing else. A bad guess is a marker in the wrong clause,
    never a lost note.
  - **If most of the file's sentinels are missing, re-translate instead.** That
    is the silent `-w` failure above — Classic was served — and placing a dozen
    markers into a bad draft only makes it look finished.

  A hard-line-break refusal works the same way: end the named draft lines with
  two spaces. Say in the commit body which markers were placed by hand —
  `Markers ⟦2⟧ and ⟦7⟧ placed by hand — Google dropped them.` Nothing goes in
  the frontmatter.
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
- The checkers live in `linji_tools/` and run as `python -m linji_tools.<name>`
  from the repo root: orthography (`normalize`), semantic line breaks
  (`check_linebreaks`), source/translation block parity (`check_parity`), plus
  `make_stubs`. Imported from the tree, not installed —
  `tools/requirements.txt` is just PyYAML and regex.
- **They carry no knowledge of this book**, and that is enforced: their tests in
  `linji_tools/tests/` must pass with no `[tool.*]` config present at all. What
  makes them this book's is `pyproject.toml`. Keep it that way — a book fact
  belongs in the config, not in a checker.
- `tools/anchors.py` is the adapter, and is the one piece that *is* this book's:
  Watson's token pattern and the Persian form of every heading and marker. The
  round-trip it calls is `linji_tools.anchors`. 154 tests there, 20 here.
- `check_parity` only works locally — CI has no `source/`.

## Quality bar

- `just check` green before every commit.
- Read the typeset PDF, not the Markdown, before calling a section done. Bidi,
  ZWNJ and line-break faults are obvious typeset and invisible in a diff.
- Every commit signed off (`git commit -s`); the DCO check enforces it.
- Commit convention: `translate(chNN):`, `revise(chNN):`, `term:`, `fix(chNN):`,
  `build:`.
