# 000 — Overview & Shared Context

> 📖 Reference document — not implementable on its own. Every spec assumes you
> have read this file. If a numbered spec contradicts it, the numbered spec wins
> for its own scope.

## What this is

A Persian translation of **_The Zen Teachings of Master Lin-chi_** — Burton
Watson's 1993 English rendering of the *Lín-chi lù* (臨濟錄), the recorded
sayings of the ninth-century Chan master Lin-chi Yi-hsüan, compiled by his
students and printed in 1120.

The infrastructure is complete and was built before any translation began. What
remains is the translation itself, plus the decisions it depends on.

## Structure

Seventy-five files under `fa/`, mirroring `source/` byte-for-byte:

| | |
|---|---|
| `preface.md`, `translators-introduction.md`, `ma-fang-preface.md`, `record-title-page.md` | front matter |
| `01.md`–`09.md` | Part One — Ascending the Hall |
| `10.md`–`23.md` | Part Two — Instructing the Group |
| `24.md`–`47.md` | Part Three — Testing and Rating |
| `48.md`–`69.md` | Part Four — Record of Activities |
| `appendix.md`, `glossary.md` | back matter |

Part titles are set in `_quarto.yml` as `part:` entries, not as headings in the
files, so Quarto renders real part title pages. The four part-opening files
therefore run one block short of their source counterpart and declare
`<!-- parity: offset -1 -->`.

`index.md` at the repo root is the website's home page for the book. It is
project chrome, not translated content, and has no `source/` counterpart.

## Hard constraints

**The source text is not public domain.** Watson died in 2017; the 1993 edition
is under copyright until 2087. It is licensed to the maintainer for producing
this translation, and nothing else. `source/` is gitignored and must stay that
way. This is why `check_parity.py` runs locally and reports "skipped" in CI.

**One sentence per line.** Git diffs by line, and a word-level diff of
right-to-left text is unreadable — changed words scatter in visual order, which
has nothing to do with storage order. `check_linebreaks.py` enforces it.

**Terminology goes through issues.** Open a terminology issue, argue it, record
the outcome in `glossary.yml` with a link back. Those issues are the decision
log; in two years the most valuable thing here may be a searchable record of why
a word was rendered the way it was. Never settle a term inside a translation
commit.

## Toolchain

```
LOCAL=1 just check     # fast loop: orthography, line breaks, parity, glossary, tests
LOCAL=1 just fix       # auto-correct orthography and run-on lines
just build             # HTML + PDF + EPUB (container)
just serve             # live preview
just status-write      # refresh the README progress table
```

`just venv` sets up the host Python environment. Everything else runs in the
pinned container; `LOCAL=1` opts out.

What the checkers catch, so you do not have to:

| Check | Catches |
|---|---|
| `normalize.py` | Arabic Yeh/Kaf, ZWNJ discipline, Arabic-Indic digits, Tatweel, quotes, **bidi overrides** (reported, never auto-fixed) |
| `check_linebreaks.py` | more than one sentence on a line |
| `check_parity.py` | a dropped paragraph, by block count against `source/` |
| `check_glossary.py` | a forbidden rendering; a missing approved one |

## Translating a file

First drafts are produced with **`gTranslator`**, at
`/Users/kaavehmohamedi/Project/Backend/gTranslator`. Its own README documents
the findings behind it; the parts that matter here:

```bash
GT=~/Project/Backend/gTranslator
tools/anchors.py strip source/42.md -o /tmp/42.en.md
"$GT/.venv/bin/python" "$GT/gtranslate.py" \
    -f /tmp/42.en.md -t fa -w --raw -o /tmp/42.fa.md
tools/anchors.py restore source/42.md /tmp/42.fa.md -o fa/42.md
```

Use `-o`, not `>`: a shell redirect truncates the target before the tool runs,
so a draft `restore` correctly refuses would destroy the existing translation.

The `strip` and `restore` steps are not optional — see **The markup hazard**
below. `strip` also shortens every file, since a sentinel is much shorter than
the token it replaces, so chunk counts come out at or below the estimates here.

**`-w` / `--web` is not optional.** Only the browser-driven mode reaches
Google's Advanced (Gemini) model, which reads a whole passage and produces
literary register with ezafe. Every HTTP path — the default endpoint, the Cloud
Translation API — serves the old Classic model, which translates clause by
clause and is markedly worse for this book. `--raw` is the right companion to
`--web`: the Advanced model handles wrapped input by itself.

The failure is silent. gTranslator's own README is emphatic: the model picker on
the page reports "Advanced" even while Classic is being served. **Never trust
the picker — judge the output text.** If a passage suddenly reads mechanically,
suspect the model before suspecting the source.

### One file at a time. Never the whole book.

This is a hard requirement, not a preference:

- **The site caps input at 5,000 characters.** The book concatenated is 245,394
  — fifty-five times over. The tool chunks at 4,500 by default, and 8 of the 75
  files exceed the cap on their own. `translators-introduction.md` (39,543
  chars) and `19.md` (38,739) are nine chunks each.
- **`fa/` must mirror `source/` file-for-file** or `check_parity.py` cannot pair
  them. A single concatenated translation would have to be split back up by
  hand, which is exactly the operation that drops a paragraph.
- **Failures stay isolated.** One file that comes back mangled is one file to
  re-run.

Budget roughly 11 seconds per 800 characters.

### The output is the edition

`restore` writes `status: reviewed`, and that is the end state. The pipeline
produces the published text in one pass — strip, translate, restore, normalise —
with no hand-revision stage after it, so there is no later step for a `draft` or
a `translated` to be promoted from. Those two values are not used.

What that buys in speed it costs in fidelity, and the cost is real. gTranslator
knows nothing about this project:

- **It has never read `STYLE.md`.** Register, pronouns, dialogue punctuation and
  proper-noun policy are all yours to impose afterwards.
- **It has never read `glossary.yml`.** It will render a settled term three
  different ways across three files. `check_glossary.py` is the corrective.
- **It will not produce semantic line breaks or correct Persian orthography.**
  Run `LOCAL=1 just fix` on the file immediately after.

### The markup hazard

The source carries **1,012 inline markup tokens** — note anchors, superscript
references and back-links — sitting mid-sentence:

```
…to the lecture seat.<a id="m2-2"></a>[<sup>²</sup>](#n2-2)
```

Machine translation does not mangle these — measured, it **deletes** them, every
one, silently, leaving prose that reads perfectly well with no trace that a note
was ever there. They are load-bearing: 253 notes resolve through them, and the
ids must stay byte-identical to `source/`.

**Spec 002 settled this.** Never send a file to gTranslator raw. Run it through
`tools/anchors.py strip` first and `tools/anchors.py restore` after; the
procedure is in `STYLE.md` §6 and `anchors.py --check` enforces the result in
`just check`.

Note that two links cross files — `record-title-page.md` → `01.md#n2-1`, and the
back-link returning — so anchor ids are globally unique but a file is not
necessarily self-contained.

## Conventions in `fa/`

Front matter is `status:` only. `tools/status_table.py` knows five values —
`untranslated`, `claimed`, `draft`, `translated`, `reviewed` — but this project
uses two: **`untranslated`** for a stub, **`reviewed`** for a finished file.
There is no revision stage in between for the other three to describe. The
status table in `README.md` is generated from it.

Each file opens with a level-1 heading — the section number in Persian digits
(`# ۴۲`), or the part name for front and back matter. Notes go in a level-2
`## یادداشت‌ها` section at the end. Spec 002 settles the details.

## Register, in one paragraph

The book is not uniform, and this is the thing most likely to go wrong. It
alternates between formal exposition to an assembled group and extremely blunt
spoken exchange — shouts, blows, one-line retorts. A single register flattens it:
formal Persian throughout makes the dialogue lifeless, colloquial throughout
makes the sermons sound careless. Lin-chi's method also involves actively
refusing the deference his position invites, so uniformly deferential Persian
destroys the point of several exchanges. `STYLE.md` §1 and §2 are where this gets
decided; spec 001 is where it gets done.

## Publication

The book is read at **kaavehdev.ir/translations/linji-lu/**, a section of the
`kaavehdev` site (spec 016 there). Cloudflare's build image has no Quarto, so
tagging a release here attaches the rendered site as a tarball and the website
unpacks it at its own build time, pinned to a version it names. **Nothing reaches
the site until a release is tagged.** Spec 009 covers the first one.
