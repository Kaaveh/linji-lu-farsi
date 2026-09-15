# Contributing

Thank you for reading this before opening something. It will save us both time.

## What this project accepts

**Chapter translation is done by the maintainer and a small trusted core.**
Public contributions are welcome for:

- **Typos and orthography** — send a pull request
- **Terminology proposals** — open an issue; please do not open a pull request
- **Factual and footnote corrections** — issue or pull request, either is fine
- **Tooling** — the scripts in `tools/`, the build, the workflows

**Please do not send a pull request that translates a chapter you have not
claimed.** It will be declined, and that is a waste of your afternoon.

This is not gatekeeping for its own sake. A literary translation with many
uncoordinated contributors reads like many people, because it is many people.
Voice, register, and the rhythm of a sentence are not things Git can merge.
Ten translators produce ten books stapled together, and no amount of review
afterwards turns that back into one. Being clear about this up front is kinder
than accepting your work and then rewriting it.

If you want to translate chapters, that is genuinely welcome — see
[Claiming a chapter](#claiming-a-chapter). The point is coordination, not
exclusion.

## Licensing and sign-off

The translation is [CC BY-SA 4.0](LICENSE-TEXT). The tooling is [MIT](LICENSE-CODE).
**Inbound equals outbound:** what you contribute is licensed to the project on
the same terms the project uses.

There is no CLA. Instead we use the [Developer Certificate of Origin](https://developercertificate.org/),
which you accept by signing off each commit:

```
git commit -s
```

That appends a `Signed-off-by:` line using your Git name and email. It certifies
that you wrote the change, or that you have the right to submit it under these
licences. CI checks every commit in a pull request; if you forget:

```
git rebase --signoff main
```

### About the source text

The English source is **not in this repository** and must not be added to it.
It is licensed to the maintainer for translation, not for redistribution. The
`source/` directory is in `.gitignore` for that reason. If you find source text
committed anywhere, please report it privately rather than opening a public
issue.

This is why the parity check reports "skipped" in CI — it has nothing to
compare against there. It runs locally for the maintainer.

## Getting set up

Everything runs in a pinned container, so you do not need TeX on your machine:

```
just check      # the full lint
just build      # HTML, PDF and EPUB
just serve      # live preview on http://localhost:4200
```

For the Python checks alone — which is all you need for a typo fix — skip the
container:

```
just venv
LOCAL=1 just check
```

`just --list` shows everything.

### The one-click path for a typo

You do not need any of the above. Every page of the
[live site](https://kaavehdev.ir/translations/linji-lu) has an **«ویرایش این صفحه در گیت‌هاب»**
link that opens the file in GitHub's web editor. Fix, describe, commit. Tick
"sign off" if GitHub offers it, or add the trailer by hand:

```
Signed-off-by: Your Name <you@example.com>
```

## Semantic line breaks

**One sentence per line.** This is the rule that everything else depends on.

Git diffs by line. A word-level diff of right-to-left text is genuinely
unreadable — the changed words scatter across the line in visual order, which
has nothing to do with the order they are stored in. One sentence per line makes
the sentence the unit of review, which is also the unit a translator works in.

Wrong:

```markdown
او گفت که راه دور است. ما فردا می‌رویم. هوا هم سرد خواهد بود.
```

Right:

```markdown
او گفت که راه دور است.
ما فردا می‌رویم.
هوا هم سرد خواهد بود.
```

Rendered output is identical — Markdown joins the lines. Only the diff changes,
and it changes from unreadable to obvious.

`just fix` splits run-on lines for you. `just check` fails on them.

## Orthography

The orthography check enforces Persian spelling rules invisible in review:
Arabic Yeh where Farsi Yeh belongs, missing ZWNJ in `می‌رود` and `کتاب‌ها`,
Arabic-Indic digits, stray Tatweel. These are the errors that accumulate for
years and then break search and sorting all at once.

```
just fix        # corrects what can be corrected
just check      # fails if anything is left
```

One thing is reported but **never** fixed automatically: **bidi override
characters** (U+202A–U+202E, U+2066–U+2069). They can make a diff display in a
different order than it is stored, which makes reviewing a pull request
meaningless. If the checker reports one, remove it by hand and say in the PR
where it came from — usually a copy-paste from a word processor.

Rules are individually toggleable in `[tool.normalize]` in `pyproject.toml`, and
a region can be exempted:

```markdown
<!-- normalize: off -->
متنی که نباید دست بخورد
<!-- normalize: on -->
```

## Terminology

**Open an issue, not a pull request.**

The issue thread is the whole record. Nothing enforces a rendering
mechanically, so consistency across chapters is a matter of reading — and a
pull request that silently changes a term leaves no trace of why.

## Claiming a chapter

1. Comment on the pinned tracking issue saying which section you want and
   roughly when you expect to finish, or use the
   [chapter claim template](../../issues/new?template=chapter-claim.yml).
2. A maintainer applies the `chapter:claimed` label and updates the tracking
   issue.
3. Set `status: claimed` in the file's front matter in your first commit, so the
   [README status table](README.md) reflects reality.

A claim lapses after a month of silence. That is not a judgement — life happens.
Say so and re-claim whenever you like.

Front matter statuses, in order: `untranslated` → `claimed` → `draft` →
`translated` → `reviewed`.

## Commit messages

```
translate(ch03): first pass
revise(ch03): tighten dialogue rhythm
term: settle on X for Y (closes #42)
fix(ch02): ZWNJ in plural forms
build: pin texlive to 2025
```

Prefixes: `translate`, `revise`, `term`, `fix`, `build`. The scope is the
chapter where there is one. Sign off every commit.

## What happens to your pull request

1. **lint** runs the orthography, line-break and spelling checks, and
   verifies every commit is signed off.
2. **build** renders all three formats and posts a comment linking the PDF and
   EPUB.
3. A maintainer reads the PDF, not the diff. Please do the same before asking
   for review — bidi, ZWNJ and line-break problems are obvious when typeset and
   nearly invisible in Markdown.

If the spell check flags a word that is genuinely correct — a transliterated
name, a Buddhist technical term — add it to `tools/dict/project.dic`, sorted.
Do not add a word to silence a real typo.
