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

`tools/normalize.py` converts ASCII and curly quotes to «» automatically. If
the decision goes the other way, turn `quotes` off in `pyproject.toml`.

## 4. Proper nouns

**Governs:** every Chinese name in the book, which is a lot of them.

Three defensible policies — transliterate into Persian script, keep the Latin
form, or give both on first occurrence and one thereafter. This interacts with
the glossary: whatever is chosen becomes a `glossary.yml` entry per name, so the
checker can enforce it.

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

The translation therefore has two distinct kinds of note, and they must be
visually distinguishable:

- **Author's notes** — carried over from the source, in the endnote list
- **Translator's notes** — yours, explaining a choice or a Persian-specific
  problem

- How a translator's note is marked as distinct: `<<<TBD>>>`
- When a translator's note is warranted at all: `<<<TBD>>>`
- Whether translator's notes go in the same list or a separate one: `<<<TBD>>>`
- Whether any author's note may be dropped as irrelevant to a Persian reader:
  `<<<TBD>>>`

Note markers in the source use Latin superscript digits (`²`, `³`). Persian
should use `۲`, `۳`. That is a mechanical change; decide it here and it can be
enforced.

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
| One sentence per line | `tools/check_linebreaks.py` |
| Farsi Yeh, Keheh, Persian digits, no Tatweel | `tools/normalize.py` |
| ZWNJ in `می‌`, `ها`, `تر`/`ترین` | `tools/normalize.py` |
| No bidi override characters | `tools/normalize.py` (never auto-fixed) |
| Settled terminology | `tools/check_glossary.py` |
| No dropped paragraphs | `tools/check_parity.py` (maintainer, locally) |

Harakat are **preserved** by default, because they carry meaning in verse and
quoted scripture. See section 7.
