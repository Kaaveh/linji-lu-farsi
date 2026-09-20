# Style guide

The decisions here are what keep 69 sections sounding like one translator. Every
section below is scaffolded with what it governs and why it matters for *this*
book; the decisions themselves are marked `<<<TBD>>>` and are the maintainer's
to make.

Fill one in when you actually hit the problem, not before. A style guide written
in advance is a guess; one written the third time you hesitate over the same
sentence is a decision.

When a decision here conflicts with something already translated, the guide
wins and the text gets fixed — note it in the commit as `revise(chNN):`.

---

## 1. Register — کتابی or محاوره‌ای

**Governs:** the default voice of narration, and where it shifts.

This is the first decision and the one everything else leans on. The Lin-chi lu
is not uniform: it alternates between formal exposition to an assembled group
and extremely blunt spoken exchange — shouts, blows, one-line retorts. A single
register flattens the book. Formal Persian throughout makes the dialogue
lifeless; colloquial throughout makes the sermons sound careless.

So the real decision is not "which register" but "which register where, and how
is the boundary marked".

- Narration and frame ("The Master ascended the hall and said…"): `<<<TBD>>>`
- Sermons and formal instruction to the group: `<<<TBD>>>`
- Dialogue and exchanges between master and monk: `<<<TBD>>>`
- The verse and quoted scripture: `<<<TBD>>>`
- How the shift is signalled to the reader, if at all: `<<<TBD>>>`

## 2. Pronouns and honorifics

**Governs:** how the Master, monks, officials and the reader are addressed.

Persian carries social distance in ways English does not, and this book is
almost entirely people talking to each other across a status gap — and then
deliberately collapsing it. Lin-chi's whole method involves refusing the
deference his position invites. If the Persian is uniformly deferential, the
point of several exchanges disappears.

- Default address between master and monk: `<<<TBD>>>`
- شما versus تو, and whether it varies by speaker: `<<<TBD>>>`
- Rendering of «Master» / 師: `<<<TBD>>>`
- Titles for officials (Constant Attendant Wang, and so on): `<<<TBD>>>`
- Verb agreement for honorifics — ایشان + plural verb, or not: `<<<TBD>>>`
- Whether the translator ever addresses the reader directly: `<<<TBD>>>`

## 3. Dialogue punctuation

**Governs:** the visual grammar of speech, which is most of this book.

Persian typography has more than one live convention here and mixing them looks
like carelessness. Note that dialogue is frequently nested — someone quotes what
someone else said — so whatever is chosen has to survive two levels.

- Quotation marks: «» throughout, or dash-led dialogue: `<<<TBD>>>`
- Nested quotation: `<<<TBD>>>`
- Placement of the attribution («گفت») relative to the quote: `<<<TBD>>>`
- Punctuation inside or outside the closing guillemet: `<<<TBD>>>`
- How a shout (喝 / "the Master gave a shout") is set: `<<<TBD>>>`

`just fix` converts ASCII and curly quotes to «» automatically. If
the decision goes the other way, turn `quotes` off in `pyproject.toml`.

## 4. Proper nouns

**Governs:** every Chinese name in the book, which is a lot of them.

Three defensible policies — transliterate into Persian script, keep the Latin
form, or give both on first occurrence and one thereafter. Whatever is chosen
has to be held by hand: there is no terminology checker any more.

Note that the source uses Wade-Giles (Lin-chi, Huang-po, Ch'an), not Pinyin
(Linji, Huangbo, Chan). Transliterating from Wade-Giles into Persian and
transliterating from Pinyin give different results.

- Chinese personal names: `<<<TBD>>>`
- Chinese place names: `<<<TBD>>>`
- Sanskrit terms already naturalised in Persian (بودا، نیروانا): `<<<TBD>>>`
- Sanskrit terms not naturalised: `<<<TBD>>>`
- Whether the Latin form appears on first occurrence: `<<<TBD>>>`
- Whether Wade-Giles or Pinyin is the basis for transliteration: `<<<TBD>>>`
- Handling of the apostrophe in Wade-Giles (Ch'an, P'u-hua, T'ang): `<<<TBD>>>`

### Settled in spec 008 — the glossary

- **The glossary keeps the source's ordering.** It stays alphabetised by the
  English headword rather than re-sorted into Persian alphabetical order. A
  Persian reader looking up «آناندا» therefore has to know it files under A.
  This is reversible: `check_parity.py` compares block *counts*, not order, so
  re-sorting later costs no parity offset — contrary to what spec 008
  requirement 1 assumes.
- **Parenthetical Sanskrit forms keep the Latin diacritical form**, exactly as
  the source gives them (Ānanda, Aṅgulimāla). They are not transliterated and
  not doubled.

Both apply to `glossary.md`. Neither settles the wider §4 questions above.

## 5. Digits

**Governs:** section numbers, note markers, dates, and numbers in prose.

Currently: section headings and note markers use Persian digits, and
`latin_digits` is **off** in `pyproject.toml`, so digits typed in prose stay as
typed. The typeset PDF renders all LaTeX counters — page numbers, chapter
numbers — in Persian digits via babel's `maparabic`.

- Numbers in running prose: `<<<TBD>>>`
- Dates: Gregorian, Hijri, or both: `<<<TBD>>>`
- Century and dynasty references (the T'ang, the ninth century): `<<<TBD>>>`
- Citations of Taishō or other catalogue numbers: `<<<TBD>>>`

If prose digits should be Persian too, set `latin_digits = true` in
`[tool.normalize]` and run `just fix`.

## 6. Notes

**Governs:** the apparatus, which is substantial — 253 notes across 69 sections.

The source uses **endnotes per section**, not page-bottom footnotes: each
section ends with a `## یادداشت‌ها` list and the references are anchored links
that jump both ways. Keep that. Section 19 alone has 47 notes; as footnotes that
page would be unreadable.

Settled in spec 002. All of it is mechanical, and `tools/anchors.py` does it —
none of these are per-chapter judgement calls.

### The decisions

- **Endnotes per section stay.** Not converted to Pandoc `[^n]` footnotes.
  Section 19 has 47 notes; at the foot of a page it would be unreadable, and the
  anchor scheme already works in HTML, PDF and EPUB. Do not relitigate.
- **Note markers are Persian digits in Pandoc's native superscript**:
  `[<sup>²</sup>](#n2-2)` becomes `[^۲^](#n2-2)`. The raw `<sup>` wrapper is
  **dropped**, and this is not cosmetic — Pandoc passes raw `<sup>` through to
  HTML but silently discards it for LaTeX, so with the wrapper all 253 markers
  set at full body size in the PDF. `^۲^` compiles to `\textsuperscript{۲}` for
  LaTeX and back to `<sup>۲</sup>` for HTML, so one form is right everywhere.
- **Note list numbers are Persian digits**: `<a id="n39-1"></a>۱. `. The anchor
  precedes the digit, so the block classifies as a paragraph rather than a
  Markdown list — which is what the source does too, so parity is unaffected.
- **Anchor ids are never translated.** `m2-2` / `n2-2` stay byte-identical ASCII;
  they are what the 506 cross-references resolve against. The checkers protect
  them from the orthography pass, and `anchors.py` re-emits them from `source/`
  rather than from the translation, so they cannot drift. If you are ever
  hand-editing an anchor id, something has gone wrong upstream.
- **The notes heading is `## یادداشت‌ها`** — level 2, because section files open
  at level 1 (`# ۴۲`) where the source opens at level 3 (`### 42`).
- **Translator's notes: none.** `fa/` carries machine output normalised by
  `just fix`, with no hand revision (see spec 001), so there is no translator
  voice to footnote. If that policy ever changes, these become real Pandoc
  footnotes — `tex/preamble.tex` already mirrors the footnote rule to the right
  edge for exactly this case — which keeps them visually distinct from the
  author's endnotes without any further convention.
- **No author's note is dropped.** Each note is a block, so dropping one changes
  the block count and `check_parity.py` will say so. If one ever is dropped
  deliberately, that is a `<!-- parity: offset -->`, never a `skip`.

### How the markup survives gTranslator

The book carries 1,012 inline markup tokens sitting mid-sentence. Google
Translate's Advanced model does not mangle them — it **deletes** them, all of
them, silently. Measured on `source/42.md`: ten tokens in, zero out. So
"translate as-is and repair" has nothing to repair, and restoring by position
afterwards is impossible, because markers sit mid-sentence rather than at
paragraph ends.

There is a class of placeholder the model does leave alone, in place and
mid-sentence. `tools/anchors.py` swaps the markup for those on the way out and
puts it back on the way in, so every file goes through it:

```bash
GT=~/Project/Backend/gTranslator
tools/anchors.py strip source/42.md -o /tmp/42.en.md
"$GT/.venv/bin/python" "$GT/gtranslate.py" -f /tmp/42.en.md -t fa -w --raw -o /tmp/42.fa.md
tools/anchors.py restore source/42.md /tmp/42.fa.md -o fa/42.md
LOCAL=1 just fix && LOCAL=1 just check
```

**Use `-o`, never a shell redirect.** `> fa/42.md` truncates the file before the
tool runs, so a draft that `restore` correctly refuses destroys the translation
that was already there. With `-o` nothing is written until validation passes.

`restore` puts each token back where the model left its placeholder — so if
the model moved a sentence, the marker moves with it, which is what you want —
and it re-emits the ids from `source/`, so they cannot drift. It **fails
loudly** rather than writing a damaged file. Never repair a mangled file by
hand; re-run it.

Headings go through the same mechanism, because every heading in the book is
structural rather than prose — 69 `### <number>`, 66 `#### Notes`, 4
`## Part ...`, and 6 named front/back-matter titles. Not one needs translating,
so all are re-emitted deterministically and the model never sees them.

`tools/anchors.py --check` runs in `just check` and compares the anchor-id and
note-link multisets in `fa/` against `source/`, plus the count of Markdown hard
line breaks — lose those and the Ikkyū poem in `preface.md` reflows into prose.
Like `check_parity.py` it is maintainer-local, and reports "skipped" in CI where
`source/` is absent.

### Long files: keep each submission small

On a submission of a few thousand characters Google intermittently merges a
paragraph or swallows a token — roughly one fault per long request, varying from
run to run, so re-running the whole file is a lottery. Nine files are long
enough to be split: `11`, `18`, `19`, `21`, `23`, `48`, `69`, `glossary`,
`translators-introduction`.

For those, translate in **verified groups of about 1,200 characters**, checking
each group's markup and paragraph count before moving on and retrying only the
group that failed. `translators-introduction.md` went through as 46 groups,
every one clean first time; the same file submitted whole lost a paragraph and a
note marker on all three attempts. The other 66 files fit in one request and need
none of this.

Never hand-repair a file that comes back short. `restore` refuses it for a
reason — re-run the piece.

## 7. Verse and quoted scripture

**Governs:** the poems, the gathas, and quotations from sutras.

These need to look different from prose on the page and to survive all three
output formats. Markdown hard line breaks (two trailing spaces) are preserved
by the pre-commit hooks specifically so verse is not reflowed into prose.

- Verse form: metrical Persian, free verse, or literal prose rendering:
  `<<<TBD>>>`
- Whether rhyme is attempted: `<<<TBD>>>`
- Typographic treatment — blockquote, indentation, centring: `<<<TBD>>>`
- Quoted sutra passages: distinguished from verse, or treated the same:
  `<<<TBD>>>`
- Whether harakat are used in verse (they are preserved by default): `<<<TBD>>>`

## 8. Units and measures

**Governs:** the occasional concrete detail — distances, weights, times of day.

- Chinese units (li, chi, catty): converted, transliterated, or glossed:
  `<<<TBD>>>`
- Times of day and watches of the night: `<<<TBD>>>`
- Monastic time markers (the summer session, and so on): `<<<TBD>>>`

---

## Mechanical rules, already enforced

These are not up for discussion per-chapter; they are checked in CI.

| Rule | Enforced by |
|---|---|
| One sentence per line | `bargardan_tools.check_linebreaks` |
| Farsi Yeh, Keheh, Persian digits, no Tatweel | `bargardan_tools.normalize` |
| ZWNJ in `می‌`, `ها`, `تر`/`ترین` | `bargardan_tools.normalize` |
| No bidi override characters | `bargardan_tools.normalize` (never auto-fixed) |
| No dropped paragraphs | `bargardan_tools.check_parity` (maintainer, locally) |
| Note anchors match the source | `tools/anchors.py --check` (maintainer, locally) |

Harakat are **preserved** by default, because they carry meaning in verse and
quoted scripture. See section 7.
