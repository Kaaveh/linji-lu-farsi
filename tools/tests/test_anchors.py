import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from anchors import compare, fa_heading, hard_breaks, main, restore, strip

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
        self.assertNotIn("<sup>", out)
        self.assertIn('<a id="n39-1"></a>۱. ', out)

    def test_headings_take_their_persian_structural_form(self):
        out = restore("42.md", SECTION, self.draft())
        self.assertIn("# ۴۲", out)
        self.assertNotIn("### ۴۲", out)
        self.assertIn("## یادداشت‌ها", out)

    def test_status_is_final_not_provisional(self):
        out = restore("42.md", SECTION, self.draft())
        self.assertIn("status: reviewed", out)
        self.assertNotIn("status: draft", out)

    def test_a_dropped_sentinel_is_an_error(self):
        with self.assertRaises(ValueError) as caught:
            restore("42.md", SECTION, self.draft().replace("⟦2⟧", ""))
        self.assertIn("dropped", str(caught.exception))

    def test_a_duplicated_sentinel_is_an_error(self):
        with self.assertRaises(ValueError) as caught:
            restore("42.md", SECTION, self.draft().replace("⟦2⟧", "⟦2⟧⟦2⟧"))
        self.assertIn("duplicated", str(caught.exception))

    def test_an_invented_sentinel_is_an_error(self):
        with self.assertRaises(ValueError):
            restore("42.md", SECTION, self.draft() + "⟦99⟧")

    def test_a_reordered_sentinel_moves_its_marker(self):
        out = restore("42.md", SECTION, self.draft().replace("پرسید.⟦2⟧", "⟦2⟧پرسید."))
        self.assertIn('<a id="m39-1"></a>[^۱^](#n39-1)پرسید.', out)


class TestHeadings(unittest.TestCase):
    def test_part_headings_are_dropped(self):
        self.assertIsNone(fa_heading("01.md", "##", "Part One: Ascending the Hall"))

    def test_named_files_use_the_stub_titles(self):
        self.assertEqual(fa_heading("preface.md", "##", "Preface"), "# پیش‌گفتار")

    def test_an_unmapped_prose_heading_raises(self):
        with self.assertRaises(ValueError):
            fa_heading("42.md", "##", "Something Unexpected")


class TestCompare(unittest.TestCase):
    def tree(self, fa_body):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "source").mkdir()
        (tmp / "fa").mkdir()
        (tmp / "source" / "42.md").write_text(SECTION, encoding="utf-8")
        (tmp / "fa" / "42.md").write_text(fa_body, encoding="utf-8")
        return compare(tmp / "source", tmp / "fa")

    def test_a_faithful_round_trip_matches(self):
        fa = restore("42.md", SECTION, strip("42.md", SECTION))
        findings, compared, _ = self.tree(fa)
        self.assertEqual(findings, [])
        self.assertEqual(compared, 1)

    def test_a_lost_anchor_is_reported(self):
        fa = restore("42.md", SECTION, strip("42.md", SECTION))
        findings, _, _ = self.tree(fa.replace('<a id="m39-1"></a>', ""))
        self.assertEqual(len(findings), 1)
        self.assertIn("m39-1", str(findings[0]))

    def test_untranslated_files_are_skipped(self):
        findings, compared, skipped = self.tree("---\nstatus: untranslated\n---\n\n# ۴۲\n")
        self.assertEqual((findings, compared, skipped), ([], 0, 1))


class TestHardBreaks(unittest.TestCase):
    def test_counts_only_real_hard_breaks(self):
        self.assertEqual(hard_breaks("a  \nb  \nc\n"), 2)

    def test_a_blank_line_of_spaces_is_not_a_hard_break(self):
        self.assertEqual(hard_breaks("a\n   \nb\n"), 0)

    def test_losing_them_is_reported(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "source").mkdir()
        (tmp / "fa").mkdir()
        (tmp / "source" / "p.md").write_text("## Preface\n\n> one  \n> two\n", encoding="utf-8")
        (tmp / "fa" / "p.md").write_text(
            "---\nstatus: draft\n---\n\n# پیش‌گفتار\n\n> یک\n> دو\n", encoding="utf-8"
        )
        findings, _, _ = compare(tmp / "source", tmp / "fa")
        self.assertEqual(len(findings), 1)
        self.assertIn("reflow", str(findings[0]))


class TestOutFlag(unittest.TestCase):
    """-o must not write anything when validation fails.

    A shell redirect truncates the target before the tool runs, so a draft that
    restore correctly refuses would destroy the existing translation.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "42.md").write_text(SECTION, encoding="utf-8")
        self.target = self.tmp / "out.md"
        self.target.write_text("PREVIOUS TRANSLATION", encoding="utf-8")

    def test_a_refused_draft_leaves_the_target_untouched(self):
        bad = self.tmp / "bad.md"
        bad.write_text(strip("42.md", SECTION).replace("⟦2⟧", ""), encoding="utf-8")
        code = main(["restore", str(self.tmp / "42.md"), str(bad), "-o", str(self.target)])
        self.assertEqual(code, 1)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "PREVIOUS TRANSLATION")

    def test_a_good_draft_is_written(self):
        good = self.tmp / "good.md"
        good.write_text(strip("42.md", SECTION), encoding="utf-8")
        code = main(["restore", str(self.tmp / "42.md"), str(good), "-o", str(self.target)])
        self.assertEqual(code, 0)
        self.assertIn("# ۴۲", self.target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
