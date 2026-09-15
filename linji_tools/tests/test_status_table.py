import tempfile
import unittest

import regex
from pathlib import Path


from linji_tools import _md
from linji_tools.status_table import BEGIN, END, collect, heading_of, render, splice

URL = "https://example.invalid/repo"


def make_fa(tmp, files):
    fa = Path(tmp) / "fa"
    fa.mkdir()
    for name, status, heading in files:
        body = f"---\nstatus: {status}\n---\n\n# {heading}\n\nمتن\n"
        (fa / name).write_text(body, encoding="utf-8")
    return fa


class TestCollect(unittest.TestCase):
    def test_reads_status_and_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            fa = make_fa(tmp, [("01.md", "translated", "۱")])
            self.assertEqual(collect(fa), [("01.md", "۱", "translated")])

    def test_missing_status_defaults_to_untranslated(self):
        with tempfile.TemporaryDirectory() as tmp:
            fa = Path(tmp) / "fa"
            fa.mkdir()
            (fa / "01.md").write_text("# ۱\n", encoding="utf-8")
            self.assertEqual(collect(fa)[0][2], "untranslated")

    def test_numeric_order_not_lexical(self):
        with tempfile.TemporaryDirectory() as tmp:
            fa = make_fa(
                tmp,
                [("10.md", "untranslated", "۱۰"),
                 ("2.md", "untranslated", "۲"),
                 ("glossary.md", "untranslated", "واژه‌نامه")],
            )
            self.assertEqual([r[0] for r in collect(fa)], ["2.md", "10.md", "glossary.md"])


class TestRender(unittest.TestCase):
    def test_counts_only_translated_and_reviewed(self):
        rows = [("01.md", "۱", "translated"), ("02.md", "۲", "reviewed"),
                ("03.md", "۳", "draft"), ("04.md", "۴", "untranslated")]
        table = render(rows, URL)
        self.assertIn("۲ از ۴ بخش (۵۰٪)", table)

    def test_empty_tree_does_not_divide_by_zero(self):
        self.assertIn("۰ از ۰", render([], URL))

    def test_links_point_at_the_file(self):
        table = render([("01.md", "۱", "translated")], URL)
        self.assertIn(f"({URL}/blob/main/fa/01.md)", table)

    def test_rows_are_collapsed_but_summary_is_not(self):
        table = render([("01.md", "۱", "translated")], URL)
        head, _, rest = table.partition("<details>")
        self.assertIn("۱ از ۱", head)          # summary visible
        self.assertIn("01.md", rest)            # rows hidden
        self.assertTrue(table.rstrip().endswith("</details>"))

    def test_unknown_status_is_shown_not_swallowed(self):
        table = render([("01.md", "۱", "banana")], URL)
        self.assertIn("banana", table)


class TestSplice(unittest.TestCase):
    def test_replaces_between_markers(self):
        readme = f"before\n\n{BEGIN}\n\nold\n\n{END}\n\nafter\n"
        result = splice(readme, "new")
        self.assertIn("new", result)
        self.assertNotIn("old", result)
        self.assertTrue(result.startswith("before"))
        self.assertTrue(result.endswith("after\n"))

    def test_missing_markers_raise(self):
        with self.assertRaises(ValueError):
            splice("no markers here", "new")

    def test_splice_is_idempotent(self):
        readme = f"a\n\n{BEGIN}\n\nold\n\n{END}\n\nb\n"
        once = splice(readme, "new")
        self.assertEqual(splice(once, "new"), once)


class TestHeadingMarkup(unittest.TestCase):
    """A heading that carries a note reference must not leak it into README.

    The pattern is the project's, from [tool.status_table] heading_markup, so
    these pass it in explicitly rather than relying on a config section this
    repository does not have.
    """

    MARKUP = regex.compile(r'<a id="[^"]*"></a>(\[\^[^\]]*\]\([^)]*\))?')

    def test_note_markup_is_stripped_from_the_heading(self):
        doc = _md.parse(
            "ma-fang-preface.md",
            '---\nstatus: reviewed\n---\n\n# دیباچهٔ ما فانگ<a id="m1-1"></a>[^۱^](#n1-1)\n',
        )
        self.assertEqual(heading_of(doc, self.MARKUP), "دیباچهٔ ما فانگ")

    def test_a_plain_heading_is_unchanged(self):
        doc = _md.parse("42.md", "---\nstatus: reviewed\n---\n\n# ۴۲\n")
        self.assertEqual(heading_of(doc, self.MARKUP), "۴۲")


if __name__ == "__main__":
    unittest.main()
