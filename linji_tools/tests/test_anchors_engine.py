"""The sentinel round-trip, tested against markup it has never seen.

Deliberately not the markup of any real book. These tests use a toy `{{word}}`
token and a plain stdlib `re` pattern, because the whole claim of this module is
that it does not care: if anything here needed a particular text's anchors to
pass, that knowledge would have leaked out of the caller's adapter and into the
engine, which is the one thing this file exists to prevent.
"""

import contextlib
import io
import re
import tempfile
import unittest
from pathlib import Path

from linji_tools.anchors import (
    compare,
    hard_breaks,
    main,
    restore,
    strip,
    tokenize,
)

PATTERN = re.compile(r"\{\{(?P<word>\w+)\}\}")


def render(match):
    """Uppercase in brackets, or None for a token the translation drops."""
    word = match.group("word")
    return None if word == "drop" else f"[{word.upper()}]"


TEXT = "one {{alpha}} two {{beta}} three"


class TestTokenize(unittest.TestCase):
    def test_every_token_becomes_a_numbered_sentinel(self):
        out, forms = tokenize(TEXT, PATTERN, render)
        self.assertEqual(out, "one ⟦1⟧ two ⟦2⟧ three")
        self.assertEqual(forms, ["[ALPHA]", "[BETA]"])

    def test_prose_is_left_alone(self):
        self.assertEqual(strip("nothing to do here", PATTERN, render), "nothing to do here")

    def test_a_token_keeps_its_mid_sentence_position(self):
        self.assertEqual(strip("a{{x}}b", PATTERN, render), "a⟦1⟧b")


class TestRestore(unittest.TestCase):
    def test_round_trip(self):
        out = restore("f.md", TEXT, strip(TEXT, PATTERN, render), PATTERN, render)
        self.assertEqual(out, "one [ALPHA] two [BETA] three")

    def test_the_model_may_move_a_sentinel_and_the_token_follows(self):
        draft = "⟦2⟧ two ⟦1⟧ three"
        out = restore("f.md", TEXT, draft, PATTERN, render)
        self.assertEqual(out, "[BETA] two [ALPHA] three")

    def test_a_render_returning_none_drops_the_token(self):
        text = "keep {{drop}} this"
        out = restore("f.md", text, strip(text, PATTERN, render), PATTERN, render)
        self.assertEqual(out, "keep  this")

    def test_a_dropped_sentinel_is_refused(self):
        with self.assertRaises(ValueError) as caught:
            restore("f.md", TEXT, "one two ⟦2⟧ three", PATTERN, render)
        self.assertIn("dropped", str(caught.exception))
        self.assertIn("f.md", str(caught.exception))

    def test_a_duplicated_sentinel_is_refused(self):
        with self.assertRaises(ValueError) as caught:
            restore("f.md", TEXT, "⟦1⟧ ⟦1⟧ ⟦2⟧", PATTERN, render)
        self.assertIn("duplicated", str(caught.exception))

    def test_an_invented_sentinel_is_refused(self):
        with self.assertRaises(ValueError) as caught:
            restore("f.md", TEXT, strip(TEXT, PATTERN, render) + "⟦99⟧", PATTERN, render)
        self.assertIn("not in source", str(caught.exception))

    def test_a_text_with_no_tokens_round_trips(self):
        self.assertEqual(restore("f.md", "plain", "plain", PATTERN, render), "plain")


class TestHardBreaks(unittest.TestCase):
    def test_counts_only_real_hard_breaks(self):
        self.assertEqual(hard_breaks("a  \nb  \nc\n"), 2)

    def test_a_blank_line_of_spaces_is_not_a_hard_break(self):
        self.assertEqual(hard_breaks("a\n   \nb\n"), 0)


SRC = '### 1\n\nHe asked.<a id="m1-1"></a>[<sup>1</sup>](#n1-1) He sat.\n'
OUT = '---\nstatus: reviewed\n---\n\n# 1\n\nپرسید.<a id="m1-1"></a>[^1^](#n1-1) نشست.\n'


class TestCompare(unittest.TestCase):
    """compare() reads finished files, so it works on real anchor markup."""

    def tree(self, body, source=SRC):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "source").mkdir()
        (tmp / "fa").mkdir()
        (tmp / "source" / "1.md").write_text(source, encoding="utf-8")
        (tmp / "fa" / "1.md").write_text(body, encoding="utf-8")
        return compare(tmp / "source", tmp / "fa")

    def test_a_faithful_translation_matches(self):
        findings, compared, skipped = self.tree(OUT)
        self.assertEqual((findings, compared, skipped), ([], 1, 0))

    def test_a_lost_anchor_is_reported(self):
        findings, _, _ = self.tree(OUT.replace('<a id="m1-1"></a>', ""))
        self.assertEqual(len(findings), 1)
        self.assertIn("m1-1", str(findings[0]))

    def test_untranslated_files_are_skipped(self):
        findings, compared, skipped = self.tree("---\nstatus: untranslated\n---\n\n# 1\n")
        self.assertEqual((findings, compared, skipped), ([], 0, 1))

    def test_lost_hard_breaks_are_reported(self):
        findings, _, _ = self.tree(
            "---\nstatus: reviewed\n---\n\n> یک\n> دو\n", source="> one  \n> two\n"
        )
        self.assertEqual(len(findings), 1)
        self.assertIn("reflow", str(findings[0]))

    def test_the_finding_is_labelled_with_the_target_directory(self):
        findings, _, _ = self.tree(OUT.replace('<a id="m1-1"></a>', ""))
        self.assertTrue(str(findings[0]).startswith("fa/1.md:"))


def book_strip(name, text):
    return strip(text, PATTERN, render)


def book_restore(name, source_text, draft):
    return restore(name, source_text, draft, PATTERN, render)


def run(argv):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(io.StringIO()):
        code = main(
            argv,
            strip_text=book_strip,
            restore_text=book_restore,
            source_default=Path("source"),
            target_default=Path("fa"),
        )
    return code, buffer.getvalue()


class TestOutFlag(unittest.TestCase):
    """-o must not write anything when validation fails.

    A shell redirect truncates the target before the tool runs, so a draft that
    restore correctly refuses would destroy the existing translation.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.source = self.tmp / "1.md"
        self.source.write_text(TEXT, encoding="utf-8")
        self.target = self.tmp / "out.md"
        self.target.write_text("PREVIOUS TRANSLATION", encoding="utf-8")

    def test_a_refused_draft_leaves_the_target_untouched(self):
        bad = self.tmp / "bad.md"
        bad.write_text("one two ⟦2⟧ three", encoding="utf-8")
        code, _ = run(["restore", str(self.source), str(bad), "-o", str(self.target)])
        self.assertEqual(code, 1)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "PREVIOUS TRANSLATION")

    def test_a_good_draft_is_written(self):
        good = self.tmp / "good.md"
        good.write_text(strip(TEXT, PATTERN, render), encoding="utf-8")
        code, _ = run(["restore", str(self.source), str(good), "-o", str(self.target)])
        self.assertEqual(code, 0)
        self.assertIn("[ALPHA]", self.target.read_text(encoding="utf-8"))

    def test_strip_writes_sentinels(self):
        code, _ = run(["strip", str(self.source), "-o", str(self.target)])
        self.assertEqual(code, 0)
        self.assertEqual(self.target.read_text(encoding="utf-8"), "one ⟦1⟧ two ⟦2⟧ three")


class TestCheckMode(unittest.TestCase):
    def test_an_absent_source_tree_is_a_notice_not_a_failure(self):
        # The normal state in CI for a text that is licensed, not public.
        code, out = run(["--check", "--source", "/nonexistent/source"])
        self.assertEqual(code, 0)
        self.assertIn("skipped", out)


if __name__ == "__main__":
    unittest.main()
