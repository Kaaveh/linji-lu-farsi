# 010 — Extract the General Tooling

## Context

This repository is going public. The translation *mechanism* should not: it
lives in [`gTranslator`](https://github.com/Kaaveh/gTranslator) — cloned at
`~/Project/Backend/gTranslator` on the maintainer's machine — which stays
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

The `anchors.py` estimate came out low on both sides. Actual after the split:
259 lines of engine and 165 of adapter, both counting their docstrings, which
are long here because they carry the measurements behind the design.

### The seam already exists

`anchors.py` splits cleanly because `tokenize()` already walks a regex and calls
a per-token render function. Make those two parameters and the engine stops
knowing anything about Watson's markup.

**Engine (moves):** the placeholder round-trip — substitution, restore by
placeholder position, refusal on dropped / duplicated / unknown ones — plus
`compare()`, `hard_breaks()`, `anchors_of()` and the `-o` write-only-if-valid
discipline.

**Adapter (stays):** `TOKEN` (the regex matching
`<a id="m2-2"></a>[<sup>²</sup>](#n2-2)`), `fa_heading()`, `fa_token()`,
`ORPHAN_MARKER`, `NOTES_HEADING`, `FINAL_STATUS`, `SUPERSCRIPT`, plus `TITLES`
and `EXCLUDE` once they come from config, and a `render_for(name)` helper to
bind the renderer to a filename.

One correction to the seam as drawn above: `restore()` has adapter work on
*both* sides of the engine, not just before it. The engine returns the restored
body; the orphan-marker reattachment and the `status: reviewed` front matter are
the adapter's, and run after. So it is two seams, not one.

### The thing that bites

`lint.yml` runs the checkers directly: `pip install -r tools/requirements.txt`,
then `python tools/normalize.py --check`. Move `tools/` out and that job cannot
run — nor can an outside contributor's PR, nor `just check` on a fresh clone.
The Dockerfile has the same dependency.

Requirement 2 settles this **before** anything moves.

## Goal

The general tooling lives in `gTranslator`. This repository keeps the book, the
build, and roughly 165 lines of adapter. `LOCAL=1 just check` still passes here,
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

      **Both symbols have to move, not just the first.** Relocating
      `DEFAULT_TITLES` alone leaves the import — and so the coupling — in place.
      `to_persian_digits` is not book data, so it belongs in the shared module
      rather than in config; `status_table.py` has a second copy of the same
      digit map, which goes at the same time.

   b. **Parameterise `tokenize()`.** Signature becomes
      `tokenize(text, token_re, render)`. `strip()` and `restore()` thread the
      two arguments through. No behaviour change — same placeholders, same
      validation, same output bytes.

   Verify: `LOCAL=1 just check` green and the tests still passing.

   **The round-trip check this spec originally asked for cannot be run.** It
   said `git diff` on `fa/` should be empty after a `strip`/`restore` round-trip
   of an already-translated file. It cannot be: `restore` takes the *translated
   draft* as input, and the draft behind each `fa/` file was never kept. Feeding
   the stripped English back in writes English into `fa/`, which is a real diff
   and proves nothing.

   Check the same claim a stronger way instead — load the pre-refactor
   `anchors.py` from `HEAD` alongside the new one and compare the output of both
   `strip` and `restore` over every file in `source/`. Byte-identical on all 75
   is the proof. `fa/` is then untouched and its diff is empty by construction.

2. **Decide how the public repo gets the private code, and write the decision
   down before moving a single file.**

   - **Recommended: publish to PyPI.** CI becomes
     `pip install linji-tools==x.y.z`. Outside contributors and forks keep
     working. Costs packaging scaffolding in `gTranslator` (`pyproject.toml`, a
     release workflow, a version scheme).

     **Do not read this as "private source, public wheel", as an earlier draft
     of this spec did.** A wheel is a zip of `.py` files, not a compiled
     artifact: publishing puts every line of the checkers in plain text on PyPI,
     including the identifier requirement 9 greps for as proof of purge. That is
     fine, but only because the checkers are not the sensitive part. The
     mechanism is `gtranslate.py`, CI never needs it, and it stays private under
     every option here. Choose this for the fork story, not for secrecy.
   - *Submodule or `git+ssh`* needs a deploy key. Forks won't have it, so
     outside PRs lose lint entirely. Rejected unless outside contribution is
     explicitly not wanted.
   - *Vendoring a copy back* defeats the purpose.

   Record the choice and the reasoning in `## Implementation notes` on this
   spec.

   **If it is PyPI: the private repository now builds a public artifact, and the
   default packaging behaviour is not on your side.** List the package
   explicitly — `[tool.setuptools] packages = ["linji_tools"]`, never a
   discovery glob — and give the package its own README, because setuptools
   pulls a top-level `README.md` into an sdist without being asked. That is not
   a theoretical risk: the first build of this package shipped `gTranslator`'s
   own README, findings and all, inside the tarball.

   `MANIFEST.in` fixes it, but do not let a manifest be the only thing standing
   between a private repository and PyPI. Write a guard that opens the built
   wheel and sdist and fails on anything outside the package, run it in the
   release workflow before the upload step, and test the guard itself by
   planting a file that must never ship and confirming it fails.

3. **Extract the book-specific constants into config** so the modules that move
   carry no project knowledge:

   | Module | Constant | Becomes |
   |---|---|---|
   | `check_linebreaks.py` | `ABBREVIATIONS` (`Ch Skt Pali Tib Pkt` …) | config, defaulting to a general English set |
   | `check_parity.py` | `EXCLUDE = {"README.md"}` | CLI flag or config |
   | `status_table.py` | `STATUSES` Persian labels, `HEADING_MARKUP` | config |
   | `make_stubs.py` | `DEFAULT_TITLES`, `DEFAULT_EXCLUDE` | project file (see 1a) |
   | `anchors.py` | `EXCLUDE` | same project file |

   `normalize.py` needs nothing — `[tool.normalize]` in `pyproject.toml`
   already does this, and is the pattern to copy.

   `EXCLUDE = {"README.md"}` is written out three times, in `check_parity.py`,
   `make_stubs.py` and `anchors.py`. It is one fact about the book and wants one
   home, so put project data shared across checkers in `[tool.book]` and keep
   `[tool.<checker>]` for what tunes a single checker.

   **Deliberately not in scope:** `source` and `fa` as the directory-name
   defaults, and the `/blob/main/fa/` path `status_table.render()` writes into a
   link. Those are target-language knowledge rather than book knowledge, every
   one is already CLI-overridable, and widening this requirement to cover them
   buys config nobody asked for.

4. **Move the six general modules and the anchors engine** to `gTranslator`,
   with their tests. Tests map one-to-one to modules; `test_broken_fixture.py`
   covers `normalize`, `check_linebreaks` and `check_parity` and moves whole.
   `test_anchors.py` splits: engine tests go, the `fa_heading` tests stay.
   Whatever tests requirement 1 or 3 add for the shared config move too.

   **Expect the move to break tests that pass here, and treat that as the
   point.** Three did: they were reading the *book's* abbreviations, titles and
   exclusions out of the installed config rather than supplying their own, so
   they passed in this repository and failed in one with no `[tool.book]`
   section. That is the leak the extraction exists to find, and it would have
   shipped silently otherwise. The fix is to give the function the value as a
   parameter and have the test pass a fixture — which is worth doing anyway,
   since a general checker should be drivable without a config file at all.

   The moved suite must pass in `gTranslator` with **no project config present**.
   That is the acceptance test for "these modules carry no project knowledge",
   and nothing weaker will do.

5. **Write the adapter that stays.** One file — about 165 lines — holding the
   token regex, the heading rules, the orphan-marker reattachment, and the
   Persian constants. It imports the engine and supplies the book's knowledge to
   it. Keep the name `tools/anchors.py` so `CLAUDE.md`, `specs/000-overview.md`
   and `specs/002` do not all need rewriting; if it is renamed, update all three.

6. **Rewire CI and the container.** `lint.yml` installs the package instead of
   running local scripts. The `Dockerfile` does the same. The `hunspell` job and
   `tools/dict/project.dic` are untouched — the wordlist is book vocabulary and
   stays.

   `lint.yml` is not the only workflow that shells out to a checker.
   `release.yml` calls `tools/status_table.py` to put the progress table in the
   release notes; that is a real break, not stale prose, and it is easy to miss
   because the workflow only runs on a tag. Grep every workflow for `tools/`
   before calling this done.

   Two things worth adding while here: a **Note anchors** step, since the adapter
   is the only checker code left in the repository and nothing in CI exercises
   it; and an `import linji_tools` assertion in the `Dockerfile`, so a broken pin
   fails the image build rather than every later `just check`.

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
       --path tools/check_glossary.py \
       --path glossary.yml \
       --path tools/tests/test_normalize.py \
       --path tools/tests/test_check_linebreaks.py \
       --path tools/tests/test_check_parity.py \
       --path tools/tests/test_make_stubs.py \
       --path tools/tests/test_status_table.py \
       --path tools/tests/test_broken_fixture.py \
       --path tools/tests/test_check_glossary.py \
       --path tools/tests/test_config.py
   ```

   **The last four were missing from this list and had to be added.** Derive the
   list from the repository, not from memory:

   ```bash
   git log --all --diff-filter=D --name-only --pretty=format: -- 'tools/*'
   ```

   That turns up `check_glossary.py` and its test, 197 lines of general checker
   removed after spec 005 but still fully readable in history. Strictly it is not
   "the extracted code" — it was deleted rather than moved — but it is the same
   class of thing, and leaving it means a public repository shipping a general
   checker in its history while six others are purged for being exactly that.
   `glossary.yml` goes with it, and `test_config.py` is whatever requirement 1
   or 3 added.

   Use `git filter-repo`, not `git filter-branch` — the latter is deprecated,
   slow, and silently mishandles tags.

   `tools/anchors.py` is **not** on that list: it exists at that path both
   before and after, and the adapter that keeps the name must survive. If the
   engine's history has to go too, rewrite the file's content with
   `--replace-text` rather than dropping the path, or accept that the
   pre-extraction versions of `anchors.py` stay readable.

   Facts that matter when doing this:

   - The history was **16 commits and one tag (`v0.0.1`)** when this was
     written, and 20 by the time the rewrite ran — the preceding requirements
     add their own. Every SHA changes, because the first commit already touches
     `tools/`.
   - `filter-repo` rewrites tags. A **GitHub Release** attached to `v0.0.1`
     would pin a SHA that no longer exists, so check it after pushing and
     re-create it if it broke. In the event there was no Release object at all,
     only the tag, so nothing needed repairing — confirm with
     `gh release view v0.0.1` rather than assuming either way.
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

   for c in $(git rev-list --all); do
       git grep -l 'RE_ZWNJ''_LOOSE' "$c" -- '*.py' 2>/dev/null
   done
   ```

   The second command searches every commit's tree for a string unique to the
   moved code. Empty output is the proof — but only if the command can actually
   fail, and two things here conspire against that:

   - **Scope it to `*.py`.** Unscoped, it matches this spec, which quotes the
     identifier as its own verification string. The proof command as originally
     written could not pass.
   - **Do not run the git call inside a `... | while read` pipeline.** A
     `git cat-file`/`git grep` that fails inside one can swallow its own error
     and print nothing, which is indistinguishable from a clean result. This is
     not hypothetical: a loop of that shape reported the engine as absent from
     `anchors.py` history when `SENTINEL` was plainly on line 92 of the
     requirement-1 commit. **Confirm the command against a known-positive case
     before trusting a negative one.**

   Check more than one identifier. `RE_ZWNJ_RUN`, `ARABIC_INDIC`,
   `apply_outside_protected`, `toggle_regions` and `COMMENT_ONLY` cover the
   other moved modules; a single string only proves something about one file.

   **A judgement call to make, not to assume:** `specs/000-overview.md` and
   `specs/002-notes-and-apparatus.md` describe the placeholder technique in prose —
   why it exists, what fails without it, how `strip`/`restore` work. That is the
   design, in words, and purging the code does not purge it. Decide whether the
   prose stays. Keeping it is defensible (it documents the book's provenance and
   is not runnable); if it goes, it must go in the same rewrite, not a later one.

   Two things this framing gets wrong, both found by doing it:

   - **It is ten files, not two.** `STYLE.md` and `CLAUDE.md` carry the working
     procedure, and five body specs record per-file failures in their work logs.
     Grep before estimating. Separate the *technique* from the *procedure* when
     cutting: removing the rule as well leaves `STYLE.md` §6 telling translators
     to run two commands for no stated reason, which is the fastest way to get
     the step skipped on a file that needed it.
   - **It cannot be combined with keeping `anchors.py`'s history.** Those are
     the same decision wearing two hats. The adapter keeps the path, so the path
     survives the rewrite, so the pre-split engine stays readable a few commits
     back. Redacting the prose that *describes* the technique while the code
     that *is* the technique sits in the same repository is theatre. Either
     `--replace-text` over `anchors.py` too, or accept both and scrub the prose
     in the working tree only, as tidying rather than as a purge. Decide the two
     together.

   **Checked already and clean:** `source/` has never been committed in any of
   the 16 commits, so the licensed English text is not in history. Re-confirm
   with `git log --all --oneline -- 'source/*'` before publishing anyway.

## Acceptance criteria

- [x] Requirement 1 landed and committed separately, ahead of any extraction.
- [x] The distribution decision is written in `## Implementation notes`.
- [x] `tools/` contains the adapter, `dict/`, `hooks/`, `requirements.txt` and
      `texlive-packages.txt` — and no general checker. (Also `tests/`, for the
      adapter; the criterion's list was not exhaustive.)
- [x] `LOCAL=1 just check` green **from a clean clone with no private access**,
      installing only what `tools/requirements.txt` names.
- [ ] `lint` and `build` green on a real pull request, including from a fork.
      **Blocked on publishing.** `checkers` fails on exactly one line —
      `No matching distribution found for linji-tools==0.1.0` — and nothing
      else. Publishing clears it. Note that `spelling` has failed on every run
      since at least 2026-09-13 on `Unable to locate package hunspell-fa`, which
      predates this spec and is not its to fix.
- [ ] `just build` still renders all three formats; the PDF is byte-comparable
      in structure to the pre-extraction render (same page count, notes resolve).
      Deferred with the rest of the typeset review — see the note below.
- [x] No file in this repository imports from a path that only exists privately.
- [x] `CLAUDE.md`, `CONTRIBUTING.md`, `README.md` and `specs/000-overview.md`
      describe the new arrangement.
- [x] A mirror clone of the pre-rewrite history exists offline, verified
      readable, **before** the rewrite runs. Taken twice — the first predated
      the prose commit — and proven by cloning from it and recovering
      `normalize.py`, `check_glossary.py` and all 75 `fa/` files.
- [x] History rewritten: `git log --all -- tools/normalize.py` is empty, and the
      identifier grep across all commits returns nothing for `*.py`.
- [x] `git log --all --oneline -- 'source/*'` empty, re-confirmed post-rewrite.
- [x] Force-pushed; `v0.0.1` still resolves. There was no GitHub Release object
      attached to it — only the tag — so nothing needed re-creating.
- [x] The decision on the residual GitHub objects is recorded below: **accept**.
- [x] The decision on the spec prose is recorded below, and acted on.
- [x] `LOCAL=1 just check` green on a fresh clone of the **rewritten** remote.

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

### Requirement 2 — the distribution decision

**PyPI, packaged from `gTranslator`.** The spec's recommendation, chosen for the
reason the spec gives: a fork has no access to a private remote, so any
deploy-key arrangement costs outside contributors their lint entirely, and
vendoring a copy back defeats the exercise. CI is
`pip install -r tools/requirements.txt`, which names `linji-tools==0.1.0`.

**One correction to the spec's framing, made before choosing.** Requirement 2
describes this as "private source, public wheel — a normal arrangement". A wheel
is a zip of `.py` files, not a compiled artifact: publishing puts
`normalize.py` in plain text on PyPI, including the very identifier
requirement 9 greps for as proof of purge. So publishing does not make the
checkers unreadable, and nothing here should be taken to claim it does.

That is fine, because the two things the spec bundles together are not the same
thing:

- The **checkers** are generic Markdown and Persian tooling. Nothing in them is
  sensitive, and they are exactly what CI needs.
- The **mechanism** is `gtranslate.py` — the browser automation and the
  Advanced-versus-Classic findings. CI never touches it, and it stays private
  under any of the three options.

The Goal scopes the purge to "this repository's git history", and that still
holds exactly as written. What changes is only the claim one may make about it.

`gTranslator` therefore now holds two halves, documented as such in its README.
`[tool.setuptools] packages = ["linji_tools"]` is an explicit list rather than a
discovery glob, and `MANIFEST.in` excludes the rest.

**Both were necessary.** The first build shipped `gTranslator`'s own README —
the findings document — inside the sdist, because setuptools includes a
top-level `README.md` without being asked. `scripts/check_dist.py` now opens the
built wheel and sdist and fails on anything outside `linji_tools/`; it runs in
`release.yml` before the upload step, and it was itself tested by planting
`gtranslate.py` in a wheel and confirming it fails. A secret defended only by a
manifest is not defended.

### Requirement 3 — book constants into config

Two config conventions, rather than one section per constant:

- **`[tool.book]`** is the project's own data, shared by whichever checkers need
  it. `exclude` and `titles` live here. `exclude` was the same `{"README.md"}`
  written out three times — in `check_parity.py`, `make_stubs.py` and
  `anchors.py` — and is now written once.
- **`[tool.<checker>]`** tunes one checker, which is what `[tool.normalize]`
  already did. Added `[tool.linebreaks]` and `[tool.status_table]`.

`ABBREVIATIONS` split rather than moved: a general constant keeps the
English set (`cf`, `ie`, `Mr`, `vol` …) in the module, and `[tool.linebreaks]
abbreviations` adds this book's language tags (`Ch`, `Skt`, `Pali` …) on top.
That is what the spec asked for — "config, defaulting to a general English set".

`check_parity.compare()` gained an `exclude` parameter and the CLI a matching
`--exclude`, so the general tool does not have to read a config section to be
driven.

`status_table.HEADING_MARKUP` is now optional and `None` when unconfigured; a
project whose headings are plain prose needs no such pattern. `STATUSES` falls
back to `{}`, which degrades to the existing `❓ {status}` label rather than
crashing. `--repo-url`'s default moved from a hardcoded URL to config.

Verified three ways: `LOCAL=1 just check` green; every migrated constant asserted
equal to its pre-config value; and the five modules copied into an empty
directory with no `pyproject.toml` at all, where each imports cleanly and falls
back to its general default — which is the property that makes them movable.

`tools/tests/test_config.py` is new, five tests on `_md.config()`. The fallback
it covers fails silently by design: a renamed section means every caller quietly
goes permissive, and nothing else in the suite would notice. 153 → 158 tests.

### Requirements 4 and 5 — the move and the adapter

`anchors.py` split where the spec said it would. The engine took `tokenize`,
`strip`, `restore`, `compare`, `hard_breaks`, `anchors_of` and the CLI shell;
the adapter kept `TOKEN`, `fa_heading`, `fa_token`, `ORPHAN_MARKER`,
`NOTES_HEADING`, `FINAL_STATUS`, `SUPERSCRIPT` and `TITLES`. Two seams rather
than one, because `restore` had adapter work on both sides of it: the engine's
`restore` returns the restored body, and the adapter wraps it with the
orphan-marker reattachment and the `status: reviewed` front matter. The engine's
`main()` takes `strip_text` and `restore_text` callables, so the write-only-
if-valid discipline moved without dragging the markup along.

The name `tools/anchors.py` is unchanged, so `CLAUDE.md`, `000-overview.md` and
`002` did not need rewriting for it — though all three needed other edits.

**Moving the tests found three real leaks.** `test_check_linebreaks`,
`test_make_stubs` and `test_check_parity` passed in this repository only because
they were reading the *book's* abbreviations, titles and exclusions out of the
installed config instead of supplying their own. In `gTranslator`, which has no
`[tool.book]` section, they failed. That is the leak the extraction was meant to
expose and it would have shipped silently otherwise. `find_violations()`,
`split_text()`, `process()`, `load_titles()`, `heading_of()` and
`check_parity.compare()` all take the relevant value as a parameter now, and the
tests pass fixtures.

**What deliberately did not change.** `source` and `fa` remain hardcoded
defaults for the directory names, and `render()` still writes `/blob/main/fa/`
into a status-table link. These are target-language knowledge, not book
knowledge; every one is CLI-overridable; and the spec's requirement 3 does not
list them. Left alone rather than widened into config nobody asked for.

### Requirement 6, 7, 8 — CI, licence, docs

`lint.yml` installs from PyPI and runs `python -m linji_tools.<name>`, which is
what keeps a fork's pull request able to lint. It gained a **Note anchors** step
that was not there before: the adapter is the one piece of checker code left in
the repository, and nothing in CI was exercising it. Like parity, it exits 0
with a notice when `source/` is absent.

`release.yml` had a real break, not just stale prose — it called
`python3 tools/status_table.py` to put the progress table in the release notes,
and that file no longer exists. It runs inside the container, which installs the
package, so it is now `python3 -m linji_tools.status_table`.

The `Dockerfile` installs the same pinned `tools/requirements.txt` and now
asserts `import linji_tools` at build time, so a broken pin fails the image
build rather than every later `just check`.

`LICENSE-CODE` gained a scope preamble. The MIT grant is untouched; what it
needed was to stop implying it covers the checkers, which are now distributed
separately with their own copy of the licence. It now names what it does cover
— the adapter, `tex/`, `assets/`, `.github/`, the build files — and points at
`LICENSE-TEXT` for the translation, at Shambhala for the source, and at
`fonts/OFL.txt` for Vazirmatn.

The pipeline command in `000-overview.md` now opens with a guard on
`$GT/gtranslate.py`. Without it, a reader with no private access gets only "no
such file or directory" against a path they have never heard of; with it they
get told that the mechanism is private, that nothing in `just check` depends on
it, and that only producing a *new* draft needs it. Written first with `-x`,
which was wrong — `gtranslate.py` is not executable, so the guard would have
blocked the maintainer too. Tested both ways.

### Verifying the extraction

- `LOCAL=1 just check` green **on a clean clone with no `source/`**, in a fresh
  venv built from `tools/requirements.txt` alone. `tools/` in that clone is the
  adapter, its tests, `dict/`, `hooks/`, `requirements.txt` and
  `texlive-packages.txt`, and nothing else.
- The adapter is **byte-identical** to the pre-extraction `anchors.py` for both
  `strip` and `restore` across all 75 source files.
- `status_table --check` passes, which it only can if the generated README table
  matches the committed one exactly.
- 154 tests in `gTranslator` pass there with no project config at all; 20 here.
- No file in this repository imports from a private path. The only mentions of
  `gTranslator` in code are two lines of prose in the adapter's docstring.

### Requirement 9 — the history rewrite

**Three judgement calls, decided by the maintainer and recorded here.**

**1. `tools/check_glossary.py` joined the purge list, which the spec omitted.**
197 lines of general checker, plus its tests and `glossary.yml`, removed after
spec 005 but still fully readable in history. Strictly it is not "the extracted
code" — it was deleted rather than moved, and exists nowhere now — but it is the
same class of thing, and leaving it would have meant a public repository
shipping a general checker in its history while six others were purged for being
exactly that. Three extra `--path` flags. Sixteen paths went in total.

**2. The prose describing the technique goes; the procedure stays.** Decided
against the spec's "keeping it is defensible". Out of the working tree: the
placeholder form and its codepoints, the measurements behind choosing it, how
validation works, and the moved modules' identifier names. Kept: the rule —
never send a file raw, `strip` before, `restore -o` after, re-run rather than
repair by hand — and the one-line hazard that makes the rule make sense. Cutting
the rule too would have left `STYLE.md` §6 telling translators to run two
commands for no stated reason, which is the fastest way to get the step skipped
on a file that needed it.

Wider than the spec anticipated: it named `000-overview.md` and `002`; it was
ten files, because the body specs' work logs record per-file failures in detail.
Those logs stay — which file failed, how, what fixed it — with the particulars
removed.

**3. That decision was then *not* applied to history, on purpose.** It would
have been theatre. `tools/anchors.py` keeps its path through the rewrite, because
the adapter carries the same name, and the maintainer's separate decision was to
accept its history rather than redact it — which leaves the pre-split engine,
`SENTINEL` and all, plainly readable four commits back. Scrubbing the prose that
*describes* the technique while the code that *is* the technique sits in the same
repository achieves nothing. The two decisions were in direct conflict; this is
how it was resolved. The working-tree scrub stands on its own as tidying.

**4. Residual GitHub objects: accepted.** Not Support GC, not a fresh repository.
The repository has always been private and has no forks, so nobody holds a SHA to
resolve; unreachable objects stay addressable for a while and are then collected.
And the checkers are going onto PyPI as readable source by decision 2 anyway, so
what the residue could expose is a copy of something already public.

**What the rewrite did.** 20 commits, every SHA changed, `v0.0.1` rewritten and
force-pushed. Verified from a fresh clone of the rewritten remote: all sixteen
paths at 0 commits; `RE_ZWNJ_LOOSE`, `RE_ZWNJ_RUN`, `ARABIC_INDIC`,
`apply_outside_protected`, `toggle_regions` and `COMMENT_ONLY` all empty across
every commit's `*.py`; `source/` still never committed; `LOCAL=1 just check`
green.

**One trap worth recording.** A `git rev-list --all | while read c; do git
cat-file -e "$c:path" ...; done` loop reported the engine as absent from
`anchors.py` history. It was not — `SENTINEL = ⟦…⟧` is on line 92 of the
requirement-1 commit. The pipeline was swallowing the failure and the loop
printed nothing, which reads exactly like a clean result. Any verification here
must be confirmed by checking a known-positive case, or it proves nothing.

### What remains

`linji-tools` is **not yet on PyPI**, by the maintainer's choice to force-push
first and publish after. Until it is, `checkers` is red. To finish:

1. Configure Trusted Publishing at <https://pypi.org/manage/account/publishing/>
   — repository `Kaaveh/gTranslator`, workflow `release.yml`, environment
   `pypi`. No API token. The name `linji-tools` was free as of this writing.
2. `git -C ~/Project/Backend/gTranslator tag linji-tools-v0.1.0 && git push --tags`.
   `release.yml` runs the tests, builds, runs `scripts/check_dist.py`, checks the
   tag against the packaged version, and uploads.
3. Confirm `lint` goes green here, and open one pull request from a fork to close
   the outstanding criterion.
