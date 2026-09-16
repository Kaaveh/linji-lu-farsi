# آموزه‌های ذن استاد لین‌چی

A Persian translation of **_The Zen Teachings of Master Lin-chi_**, Burton
Watson's English rendering of the *Lín-chi lù* (臨濟錄) — the recorded sayings
of the ninth-century Chinese Chan master Lin-chi Yi-hsüan, compiled by his
students and printed in 1120.

Sixty-nine numbered sections in four parts, plus front matter, an appendix and
a glossary. The apparatus runs to 253 notes.

📖 **[Read it online](https://kaavehdev.ir/translations/linji-lu)** ·
📄 **[Latest PDF and EPUB](../../releases/latest)**

Every page of the site has an **«ویرایش این صفحه در گیت‌هاب»** link. If you spot
a typo, that is the whole workflow — no clone, no toolchain.

---

## Rights

Read this before contributing or forking.

| | |
|---|---|
| **The Persian translation** | [CC BY-SA 4.0](LICENSE-TEXT) — share and adapt, keep it open |
| **The code and build** — `linji_tools/`, `tools/`, `.github/`, `Dockerfile`, `justfile`, `tex/`, `assets/` | [MIT](LICENSE-CODE) |
| **The English source text** | © Burton Watson / Shambhala Publications, 1993. **Not redistributed here.** |
| **The underlying Chinese text** | Public domain (Taishō T1985, compiled c. 1120) |

The English source is licensed to the maintainer for the purpose of producing
this translation. It is **not** public domain — Watson died in 2017 and the
1993 edition is under copyright until 2087 — and it is **not** in this
repository. `source/` is in `.gitignore` and must stay there.

One consequence worth knowing: the parity check, which catches dropped
paragraphs by comparing block counts between the two trees, cannot run in CI.
It reports "skipped" there and runs locally for the maintainer.

## Contributing

**Chapter translation is coordinated**; typos, orthography, terminology
proposals, footnote corrections and tooling are open to everyone. See
[CONTRIBUTING.md](CONTRIBUTING.md) — it explains why, and how to claim a chapter
if you do want to translate.

Translation conventions live in [STYLE.md](STYLE.md).

## Building from source

Everything runs in a pinned container, so you need only Docker and
[`just`](https://github.com/casey/just):

```bash
git clone https://github.com/Kaaveh/linji-lu-farsi
cd linji-lu-farsi
just build          # HTML, PDF and EPUB into _book/
```

| | |
|---|---|
| `just check` | orthography, line breaks, parity, note anchors, tests |
| `just fix` | correct what can be corrected automatically |
| `just build` | all three formats |
| `just pdf` / `just epub` | one format |
| `just pdf-mobile` | the phone-sized PDF, into `_book-mobile/` |
| `just serve` | live preview on <http://localhost:4200> |
| `just --list` | everything |

Without Docker, for the Python checks only:

```bash
just venv
LOCAL=1 just check
```

The image is published to GHCR by `.github/workflows/image.yml`. **On a fresh
fork, run that workflow once via *Actions → image → Run workflow* before the
build and release workflows will work** — they pull the image and cannot run
until it exists.

### How it gets published

The book is read at
[kaavehdev.ir/translations/linji-lu](https://kaavehdev.ir/translations/linji-lu),
a section of [kaavehdev.ir](https://kaavehdev.ir). That site is an Astro project
deployed by Cloudflare Workers Builds, whose build image has Node, Python, PHP,
Ruby and Go — but no TeX and no Quarto. It cannot render this book.

So it does not try to. Tagging a release here builds all three formats and
attaches `linji-lu-farsi-VERSION-html.tar.gz` — the entire rendered site,
including the PDF and EPUB the download buttons point at. The website fetches
that tarball at its own build time and unpacks it into
`public/translations/linji-lu/`, pinned to a version it names explicitly.

Two consequences worth knowing:

- **Nothing reaches the website until you tag a release.** Pushing to `main`
  here updates the repository, not the published book.
- **Bumping the book on the site is a separate, deliberate change** in the
  website repository. That is the point — the site stays reproducible, and a
  book update is a reviewable one-line version bump rather than a silent drift.

`release.yml` asserts the bundle is relocatable before publishing it. Quarto
emits only relative asset paths and a relative `<meta name="quarto:offset">`, so
serving from a subdirectory works — but a future Quarto version that emitted
root-absolute paths would break the site silently and only in production, so the
check is explicit.

### How the book is built

Pandoc-flavoured Markdown, one file per section, rendered by
[Quarto](https://quarto.org) into HTML, EPUB and PDF from a single source tree.

The PDF uses **LuaLaTeX, not XeLaTeX**. Under XeLaTeX, Pandoc's template
selects babel with `bidi=default`, whose bidirectional handling is heuristic
rather than a real implementation of the Unicode Bidirectional Algorithm — it
reverses the word order of Latin-script runs embedded in Persian text, so
"semantic line breaks" typesets as "breaks line semantic". For a book carrying
transliterated Chinese in most paragraphs that is disqualifying. LuaLaTeX gets
`bidi=basic`, which is a real UBA implementation. The reasoning and the other
approaches tried are recorded in [`tex/preamble.tex`](tex/preamble.tex).

Fonts are vendored: [Vazirmatn](https://github.com/rastikerdar/vazirmatn) 33.003
under the SIL Open Font License, in `fonts/`. Vendoring rather than resolving
from the system font path is what makes the typeset output reproducible.

## Versioning

Releases are tagged `vMAJOR.MINOR.PATCH`.

| | |
|---|---|
| **MAJOR** | A new edition, or a retranslation |
| **MINOR** | A new chapter, or a substantive revision to an existing one |
| **PATCH** | Typos, orthography, formatting, tooling |

Tagging builds the book from a clean tree and attaches it to the GitHub
release. Two PDFs go up: the print one, and `-mobile.pdf` — the same book on a
90×160mm page, so a phone fitting it to the screen shows type about twice the
size.

## Repository layout

```
fa/            the translation — one file per section, mirroring source/
source/        the English source (gitignored, never committed)
tex/           the LaTeX preamble for the PDF
fonts/         vendored Vazirmatn + OFL
assets/        RTL and EPUB stylesheets
linji_tools/   the checkers -- general, know nothing about this book
tools/         the note-apparatus adapter, dictionary, DCO hook, pins
_quarto.yml    the book: three formats, 75 chapters in four parts
_quarto-mobile.yml  the phone PDF: same book, small page (--profile mobile)
_language.yml  Persian UI strings — Quarto ships no fa locale
```
