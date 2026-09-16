"""The adapter: what this book's markup becomes on the way into fa/.

The sentinel round-trip itself is `linji_tools.anchors` and is tested there,
against a toy markup, precisely so that nothing about Watson's anchors can leak
into it. What is left here is the book's own knowledge -- the token pattern, the
Persian form of every token, and the two irregularities the text turns out to
have -- plus one end-to-end pass to prove the two halves still fit together.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from anchors import TOKEN, fa_heading, fa_token, main, restore, strip

SECTION = """\
### 42

He asked.<a id="m39-1"></a>[<sup>¹</sup>](#n39-1) Then he sat down.

#### Notes

<a id="n39-1"></a>1. Ma-yü appeared in section 2. [↩](#m39-1)
"""


class TestStrip(unittest.TestCase):
    def test_every_token_becomes_a_sentinel(self):
        out = strip("42.md", SECTION)
        self.assertNotIn("<a id=", out)
        self.assertNotIn("<sup>", out)
        self.assertNotIn("↩", out)
        self.assertNotIn("#", out)
        for n in range(1, 6):
            self.assertIn(f"⟦{n}⟧", out)

    def test_prose_is_left_alone(self):
        self.assertIn("Ma-yü appeared in section 2.", strip("42.md", SECTION))

    def test_marker_keeps_its_mid_sentence_position(self):
        source = 'the great concern<a id="m2-3"></a>[<sup>³</sup>](#n2-3) of Buddhism'
        self.assertEqual(strip("01.md", source), "the great concern⟦1⟧ of Buddhism")


class TestRestore(unittest.TestCase):
    def draft(self):
        return strip("42.md", SECTION).replace("He asked.", "پرسید.")

    def test_round_trip_restores_every_anchor_id(self):
        out = restore("42.md", SECTION, self.draft())
        self.assertIn('<a id="m39-1"></a>', out)
        self.assertIn('<a id="n39-1"></a>', out)
        self.assertIn("(#n39-1)", out)
        self.assertIn("[↩](#m39-1)", out)

    def test_note_markers_become_persian_digits(self):
        out = restore("42.md", SECTION, self.draft())
        self.assertIn("[^۱^](#n39-1)", out)
        self.assertIn('<a id="n39-1"></a>۱. ', out)

    def test_the_sup_wrapper_is_replaced_by_pandoc_superscript(self):
        # Pandoc passes raw <sup> to HTML but drops it for LaTeX, which sets
        # all 253 markers at full size in the PDF. Invisible in the Markdown.
        out = restore("42.md", SECTION, self.draft())
        self.assertNotIn("<sup>", out)
        self.assertIn("[^۱^]", out)

    def test_headings_take_their_persian_structural_form(self):
        out = restore("42.md", SECTION, self.draft())
        self.assertIn("# ۴۲", out)
        self.assertNotIn("### ۴۲", out)
        self.assertIn("## یادداشت‌ها", out)

    def test_status_is_final_not_provisional(self):
        out = restore("42.md", SECTION, self.draft())
        self.assertTrue(out.startswith("---\nstatus: reviewed\n---\n\n"))
        self.assertNotIn("status: draft", out)

    def test_a_reordered_sentinel_moves_its_marker(self):
        out = restore("42.md", SECTION, self.draft().replace("پرسید.⟦2⟧", "⟦2⟧پرسید."))
        self.assertIn('<a id="m39-1"></a>[^۱^](#n39-1)پرسید.', out)

    def test_a_marker_on_a_heading_is_refused(self):
        # Quarto reuses a heading verbatim for the sidebar and <title>, with no
        # inline processing, so a marker there ships as raw Markdown in the nav.
        # 24.md and ma-fang-preface.md both used to do this; the fix is to move
        # the marker a paragraph down, in source/, which is the author's call
        # and not something restore can make for them.
        source = (
            '## Part Three: Testing and Rating<a id="m25-1"></a>[<sup>¹</sup>](#n25-1)'
            "\n\n### 24\n\nHe asked.\n"
        )
        with self.assertRaises(ValueError) as caught:
            restore("24.md", source, strip("24.md", source))
        self.assertIn("inline markup", str(caught.exception))

    def test_a_marker_below_the_heading_survives(self):
        source = '## Part Three\n\n### 24\n\nHe asked.<a id="m25-1"></a>[<sup>¹</sup>](#n25-1)\n'
        out = restore("24.md", source, strip("24.md", source))
        self.assertIn('He asked.<a id="m25-1"></a>[^۱^](#n25-1)', out)
        self.assertIn("# ۲۴\n", out)

    def test_a_dropped_sentinel_is_still_refused_through_the_adapter(self):
        with self.assertRaises(ValueError) as caught:
            restore("42.md", SECTION, self.draft().replace("⟦2⟧", ""))
        self.assertIn("dropped", str(caught.exception))

    def test_a_refusal_quotes_the_english_the_marker_belongs_in(self):
        # Google Translate deletes a marker outright on some sections. The whole
        # point of the quote is that the position can be worked out from the
        # English without reading source/ and the draft back in full.
        with self.assertRaises(ValueError) as caught:
            restore("42.md", SECTION, self.draft().replace("⟦2⟧", ""))
        self.assertIn("He asked.⟦2⟧ Then he sat down.", str(caught.exception))

    def test_a_marker_placed_back_by_hand_restores_at_that_position(self):
        repaired = self.draft().replace("پرسید.⟦2⟧", "⟦2⟧پرسید.")
        out = restore("42.md", SECTION, repaired)
        self.assertIn('<a id="m39-1"></a>[^۱^](#n39-1)پرسید.', out)


class TestHeadings(unittest.TestCase):
    def test_part_headings_are_dropped(self):
        self.assertIsNone(fa_heading("01.md", "##", "Part One: Ascending the Hall"))

    def test_notes_heading_is_persian_and_level_two(self):
        self.assertEqual(fa_heading("42.md", "####", "Notes"), "## یادداشت‌ها")

    def test_numbered_sections_open_at_level_one(self):
        self.assertEqual(fa_heading("42.md", "###", "42"), "# ۴۲")

    def test_named_files_use_the_configured_titles(self):
        self.assertEqual(fa_heading("preface.md", "##", "Preface"), "# پیش‌گفتار")

    def test_an_unmapped_prose_heading_raises(self):
        # Better to stop than to invent a Persian heading for something the
        # book was not expected to contain.
        with self.assertRaises(ValueError):
            fa_heading("42.md", "##", "Something Unexpected")


class TestTokenForms(unittest.TestCase):
    def render(self, name, text):
        return fa_token(name, next(TOKEN.finditer(text)))

    def test_a_back_link_is_passed_through_unchanged(self):
        self.assertEqual(self.render("42.md", "[↩](#m39-1)"), "[↩](#m39-1)")

    def test_a_non_numeric_marker_is_left_alone(self):
        marker = '<a id="m1-1"></a>[<sup>*</sup>](#n1-1)'
        self.assertEqual(self.render("42.md", marker), '<a id="m1-1"></a>[^*^](#n1-1)')


class TestEndToEnd(unittest.TestCase):
    """The adapter and the installed engine, through the CLI, on a real file."""

    def test_strip_then_restore_produces_a_publishable_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "42.md"
        source.write_text(SECTION, encoding="utf-8")
        stripped, final = tmp / "42.en.md", tmp / "42.fa.md"

        self.assertEqual(main(["strip", str(source), "-o", str(stripped)]), 0)
        self.assertIn("⟦1⟧", stripped.read_text(encoding="utf-8"))

        self.assertEqual(
            main(["restore", str(source), str(stripped), "-o", str(final)]), 0
        )
        out = final.read_text(encoding="utf-8")
        self.assertIn("status: reviewed", out)
        self.assertIn("# ۴۲", out)
        self.assertIn('<a id="m39-1"></a>[^۱^](#n39-1)', out)

    def test_a_refused_draft_leaves_the_previous_translation_intact(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "42.md"
        source.write_text(SECTION, encoding="utf-8")
        bad = tmp / "bad.md"
        bad.write_text(strip("42.md", SECTION).replace("⟦2⟧", ""), encoding="utf-8")
        target = tmp / "fa.md"
        target.write_text("PREVIOUS TRANSLATION", encoding="utf-8")

        self.assertEqual(
            main(["restore", str(source), str(bad), "-o", str(target)]), 1
        )
        self.assertEqual(target.read_text(encoding="utf-8"), "PREVIOUS TRANSLATION")


if __name__ == "__main__":
    unittest.main()
