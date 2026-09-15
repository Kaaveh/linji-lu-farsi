# 010 — Extract the General Tooling

## Context

This repository is going public. The translation *mechanism* should not: it
lives in [`gTranslator`](https://github.com/Kaaveh/gTranslator) (on this mashine: /Users/kaavehmohamedi/Project/Backend/gTranslator), which stays
private. What belongs here is the book, the build, and the adapter code that
knows this particular e-text's shape.

Measured, not estimated:

| Area | Lines |
|---|---:|
| `tools/` production Python | 1,536 |
| `tools/tests/` | 1,056 |
| CI workflows | 351 |
| `texlive-packages.txt` | 294 |
| Quarto config | 292 |
| Dockerfile + justfile + `tex/` + `assets/` + misc | 464 |
| **Total code and config** | **≈3,990** |

Six of the seven `tools/` modules know nothing about this book. Only
`anchors.py` does, and only partly.

| Module | Lines | Book-specific? |
|---|---:|---|
| `_md.py` | 236 | No |
| `normalize.py` | 304 | No — rules already toggled from `[tool.normalize]` |
| `check_linebreaks.py` | 213 | One constant: `ABBREVIATIONS` |
| `check_parity.py` | 155 | One constant: `EXCLUDE` |
| `status_table.py` | 145 | Config only: Persian labels, `--repo-url`, `HEADING_MARKUP` |
| `make_stubs.py` | 149 | One constant: `DEFAULT_TITLES` |
| `anchors.py` | 334 | **Roughly 160 general / 120 adapter / 52 docstring** |

### The seam already exists

`anchors.py` splits cleanly because `tokenize()` already walks a regex and calls
a per-token render function. Make those two parameters and the engine stops
knowing anything about Watson's markup.

**Engine (moves):** the sentinel round-trip — `⟦n⟧` substitution, restore by
sentinel position, refusal on dropped / duplicated / unknown sentinels — plus
`compare()`, `hard_breaks()`, `anchors_of()` and the `-o` write-only-if-valid
discipline.

**Adapter (stays):** `TOKEN` (the regex matching
`<a id="m2-2"></a>[<sup>²</sup>](#n2-2)`), `fa_heading()`, `fa_token()`,
`ORPHAN_MARKER`, `NOTES_HEADING`, `FINAL_STATUS`, `SUPERSCRIPT`.

### The thing that bites

`lint.yml` runs the checkers directly: `pip install -r tools/requirements.txt`,
then `python tools/normalize.py --check`. Move `tools/` out and that job cannot
run — nor can an outside contributor's PR, nor `just check` on a fresh clone.
The Dockerfile has the same dependency.

Requirement 2 settles this **before** anything moves.

## Goal

The general tooling lives in `gTranslator`. This repository keeps the book, the
build, and roughly 120 lines of adapter. `LOCAL=1 just check` still passes here,
on a clean clone, without private access — and the extracted code is not
recoverable from this repository's git history.

## Dependencies

None. This is orthogonal to the translation specs and can land at any time.

## Requirements

1. **Land the two prerequisite refactors here first, before anything moves.**
   Both are small, both are verifiable by the existing 151 tests, and both are
   worth having even if the extraction is abandoned.

   a. **Decouple `anchors.py` from `make_stubs.py`.** It currently imports
      `DEFAULT_TITLES` and `to_persian_digits`. Book data must not live inside a
      module that is about to become general. Move `DEFAULT_TITLES` to a project
      config file that both read.

   b. **Parameterise `tokenize()`.** Signature becomes
      `tokenize(text, token_re, render)`. `strip()` and `restore()` thread the
      two arguments through. No behaviour change — same sentinels, same
      validation, same output bytes.

   Verify: `LOCAL=1 just check` green, 151 tests still passing, and
   `git diff` on `fa/` empty after a `strip`/`restore` round-trip of any
   already-translated file.

2. **Decide how the public repo gets the private code, and write the decision
   down before moving a single file.**

   - **Recommended: publish to PyPI.** Private source, public wheel — a normal
     arrangement. CI becomes `pip install linji-tools==x.y.z`. Outside
     contributors and forks keep working. Costs packaging scaffolding in
     `gTranslator` (`pyproject.toml`, a release workflow, a version scheme).
   - *Submodule or `git+ssh`* needs a deploy key. Forks won't have it, so
     outside PRs lose lint entirely. Rejected unless outside contribution is
     explicitly not wanted.
   - *Vendoring a copy back* defeats the purpose.

   Record the choice and the reasoning in `## Implementation notes` on this
   spec.

3. **Extract the book-specific constants into config** so the modules that move
   carry no project knowledge:

   | Module | Constant | Becomes |
   |---|---|---|
   | `check_linebreaks.py` | `ABBREVIATIONS` (`Ch Skt Pali Tib Pkt` …) | config, defaulting to a general English set |
   | `check_parity.py` | `EXCLUDE = {"README.md"}` | CLI flag or config |
   | `status_table.py` | `STATUSES` Persian labels, `HEADING_MARKUP` | config |
   | `make_stubs.py` | `DEFAULT_TITLES` | project file (see 1a) |

   `normalize.py` needs nothing — `[tool.normalize]` in `pyproject.toml`
   already does this, and is the pattern to copy.

4. **Move the six general modules and the anchors engine** to `gTranslator`,
   with their tests. Tests map one-to-one to modules; `test_broken_fixture.py`
   covers `normalize`, `check_linebreaks` and `check_parity` and moves whole.
   `test_anchors.py` splits: engine tests go, the `fa_heading` tests stay.

5. **Write the adapter that stays.** One file — roughly 120 lines — holding the
   token regex, the heading rules, the orphan-marker reattachment, and the
   Persian constants. It imports the engine and supplies the book's knowledge to
   it. Keep the name `tools/anchors.py` so `CLAUDE.md`, `specs/000-overview.md`
   and `specs/002` do not all need rewriting; if it is renamed, update all three.

6. **Rewire CI and the container.** `lint.yml` installs the package instead of
   running local scripts. The `Dockerfile` does the same. The `hunspell` job and
   `tools/dict/project.dic` are untouched — the wordlist is book vocabulary and
   stays.

7. **Check what `LICENSE-CODE` still covers** once most of the Python has left.
   It currently covers `tools/`. It should end up covering the adapter, the
   build config, `tex/`, and `assets/` — and should not appear to claim code
   that now lives elsewhere under different terms.

8. **Update the docs that describe the tooling.** `CLAUDE.md` ("Four checkers in
   `tools/`… 150 tests"), `CONTRIBUTING.md`, `README.md`, and
   `specs/000-overview.md`. The pipeline command in `000-overview.md` must still
   be copy-pasteable by someone with private access, and must fail with a clear
   message for someone without it.

9. **Purge the extracted code from git history, then force-push. Last step, and
   only once every criterion above is met.** Deleting a file leaves it in
   history; a public repository with intact history still ships every line of
   the mechanism to anyone who runs `git log -p`.

   **Back up before touching anything.** This is irreversible.

   ```bash
   git clone --mirror . ../linji-lu-farsi-prerewrite.git   # keep offline
   ```

   Then:

   ```bash
   pip install git-filter-repo
   git filter-repo --invert-paths \
       --path tools/_md.py \
       --path tools/normalize.py \
       --path tools/check_linebreaks.py \
       --path tools/check_parity.py \
       --path tools/make_stubs.py \
       --path tools/status_table.py \
       --path tools/tests/test_normalize.py \
       --path tools/tests/test_check_linebreaks.py \
       --path tools/tests/test_check_parity.py \
       --path tools/tests/test_make_stubs.py \
       --path tools/tests/test_status_table.py \
       --path tools/tests/test_broken_fixture.py
   ```

   Use `git filter-repo`, not `git filter-branch` — the latter is deprecated,
   slow, and silently mishandles tags.

   `tools/anchors.py` is **not** on that list: it exists at that path both
   before and after, and the adapter that keeps the name must survive. If the
   engine's history has to go too, rewrite the file's content with
   `--replace-text` rather than dropping the path, or accept that the
   pre-extraction versions of `anchors.py` stay readable.

   Facts that matter when doing this:

   - The history is **16 commits and one tag (`v0.0.1`)**. Every SHA will
     change, because the first commit already touches `tools/`.
   - `filter-repo` rewrites tags, but the **GitHub Release** attached to
     `v0.0.1` pins a SHA that will no longer exist. Check the release after
     pushing and re-create it if it broke.
   - `filter-repo` removes the `origin` remote on purpose. Re-add it, then
     `git push --force --all && git push --force --tags`.
   - **Force-pushing does not immediately destroy the old objects on GitHub.**
     Unreachable commits stay addressable by SHA for some time, and stay visible
     through the API and cached views. If that residue is unacceptable, the only
     firm guarantees are to ask GitHub Support to run garbage collection, or to
     publish from a **freshly created repository** pushed from the rewritten
     tree. The repository has always been private and has no forks, so the
     practical exposure is small — but decide deliberately rather than assume
     the force-push was sufficient.

   **Verify afterwards**, and do not skip this:

   ```bash
   git log --all --oneline -- tools/normalize.py    # must be empty
   git rev-list --all | xargs -I{} git grep -l 'RE_ZWNJ_LOOSE' {} 2>/dev/null
   ```

   The second command searches every commit's tree for a string unique to the
   moved code. Empty output is the proof.

   **A judgement call to make, not to assume:** `specs/000-overview.md` and
   `specs/002-notes-and-apparatus.md` describe the sentinel technique in prose —
   why it exists, what fails without it, how `strip`/`restore` work. That is the
   design, in words, and purging the code does not purge it. Decide whether the
   prose stays. Keeping it is defensible (it documents the book's provenance and
   is not runnable); if it goes, it must go in the same rewrite, not a later one.

   **Checked already and clean:** `source/` has never been committed in any of
   the 16 commits, so the licensed English text is not in history. Re-confirm
   with `git log --all --oneline -- 'source/*'` before publishing anyway.

## Acceptance criteria

- [ ] Requirement 1 landed and committed separately, ahead of any extraction.
- [ ] The distribution decision is written in `## Implementation notes`.
- [ ] `tools/` contains the adapter, `dict/`, `hooks/`, `requirements.txt` and
      `texlive-packages.txt` — and no general checker.
- [ ] `LOCAL=1 just check` green **from a clean clone with no private access**,
      installing only what `tools/requirements.txt` names.
- [ ] `lint` and `build` green on a real pull request, including from a fork.
- [ ] `just build` still renders all three formats; the PDF is byte-comparable
      in structure to the pre-extraction render (same page count, notes resolve).
- [ ] No file in this repository imports from a path that only exists privately.
- [ ] `CLAUDE.md`, `CONTRIBUTING.md`, `README.md` and `specs/000-overview.md`
      describe the new arrangement.
- [ ] A mirror clone of the pre-rewrite history exists offline, verified
      readable, **before** the rewrite runs.
- [ ] History rewritten: `git log --all -- tools/normalize.py` is empty, and the
      `RE_ZWNJ_LOOSE` grep across all commits returns nothing.
- [ ] `git log --all --oneline -- 'source/*'` empty, re-confirmed post-rewrite.
- [ ] Force-pushed; `v0.0.1` still resolves and its GitHub Release is intact or
      re-created.
- [ ] The decision on the residual GitHub objects (Support GC, fresh repo, or
      accept) is recorded in `## Implementation notes`.
- [ ] The decision on the spec prose describing the sentinel technique is
      recorded, and acted on in the same rewrite if it is to go.
- [ ] `LOCAL=1 just check` green on a fresh clone of the **rewritten** remote.

## Out of scope

- **Trimming `texlive-packages.txt`.** It was captured wholesale from a working
  build and carries packages this book plainly does not use (`achemso`,
  `apacite`, `babel-french`, `algorithms`). Worth doing, unrelated to this spec.
- **Removing Docker.** Considered and rejected. The PDF is the deliverable,
  Persian LaTeX is version-fragile, `image.yml` has path filters so it is not in
  the PR loop, and `LOCAL=1` already exists for the fast loop.
- The `gTranslator` side beyond what requirement 2 needs: its own API design,
  docs and release cadence are its own concern.

## Implementation notes

### Requirement 1 — the two prerequisite refactors

Landed first, on its own commit, as the spec asks. Three deviations, all small:

**`to_persian_digits` moved too, and took a duplicate with it.** Requirement 1a
names only `DEFAULT_TITLES`, but `anchors.py` imported both symbols from
`make_stubs.py`, so moving one still left the coupling. `to_persian_digits` is
not book data — it is a digit mapping — so it went to `_md.py`, the module every
checker already imports, rather than into config. `status_table.py` had its own
second copy of `PERSIAN_DIGITS`; that is now gone. Net effect is three call sites
sharing one definition instead of three, and `anchors.py` importing nothing from
`make_stubs.py`.

**The titles live in `[tool.book.titles]`, read through a new `_md.config()`.**
This copies the `[tool.normalize]` pattern the spec points at. `_md.config()` is
six lines and generic over the section name, so a general checker can read a
project's table without knowing whose project it is. `make_stubs.DEFAULT_TITLES`
keeps its name and is now loaded from there, which left `load_titles()`, the
`--titles` override and every existing test untouched.

**The spec's verification for 1b is not runnable as written.** It asks for
`git diff` on `fa/` to be empty after a `strip`/`restore` round-trip of an
already-translated file. It cannot be: `restore` takes the *translated draft* as
its input, and the draft that produced each `fa/` file was not kept. Feeding the
stripped English back in writes English into `fa/`, which is a real diff and
proves nothing. Replaced with a stronger check that tests the same claim —
`scratchpad/roundtrip.py` loads the pre-refactor `anchors.py` from `HEAD`
alongside the new one and compares the output of both `strip` and `restore` over
all 75 real source files. Byte-identical on every one. `fa/` was never written
to, so its diff is empty by construction.

Test count went 151 → 153. The two new ones are `TestParameterisation`, which
round-trips an unrelated `{{word}}` markup through a plain stdlib `re` pattern.
Without them the seam is untested: every other test binds the book's own
`(TOKEN, render_for(name))` pair, so nothing would have caught `tokenize()`
quietly continuing to depend on the book's markup.
