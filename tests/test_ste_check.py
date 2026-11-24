"""Tests for scripts/ste_check.py rule filtering, --max-findings, and inline directives."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ste_check  # noqa: E402


class TestSteCheckFilteringAndDirectives(unittest.TestCase):
    def test_backward_compatible_check_signature(self) -> None:
        bad = "It is important to note that the token is validated by the gateway.\n"
        findings = ste_check.check(bad, False)
        rules = {f.rule for f in findings}
        self.assertIn("word", rules)
        self.assertIn("passive", rules)

    def test_select_and_ignore_rules(self) -> None:
        text = "It is important to note that the token is validated by the gateway.\n"
        only_passive = ste_check.check(text, False, select={"passive"})
        self.assertTrue(only_passive)
        self.assertEqual({f.rule for f in only_passive}, {"passive"})

        no_passive = ste_check.check(text, False, ignore={"passive"})
        self.assertTrue(no_passive)
        self.assertNotIn("passive", {f.rule for f in no_passive})

        # --ignore applied after --select
        combined = ste_check.check(text, False, select={"passive", "word"}, ignore={"passive"})
        self.assertEqual({f.rule for f in combined}, {"word"})

    def test_disable_next_line_specific_and_all(self) -> None:
        text = (
            "<!-- ste-check-disable-next-line passive -->\n"
            "It is important to note that the token is validated by the gateway.\n"
            "The request is forwarded by the proxy.\n"
        )
        findings = ste_check.check(text, False)
        line2_rules = {f.rule for f in findings if f.line == 2}
        line3_rules = {f.rule for f in findings if f.line == 3}
        self.assertNotIn("passive", line2_rules)
        self.assertIn("word", line2_rules)
        self.assertIn("passive", line3_rules)

        all_suppressed = (
            "<!-- ste-check-disable-next-line -->\n"
            "It is important to note that the token is validated by the gateway.\n"
        )
        self.assertEqual(ste_check.check(all_suppressed, False), [])

    def test_disable_and_enable_block(self) -> None:
        text = (
            "<!-- ste-check-disable -->\n"
            "Great question! This seamless tool is validated by the gateway.\n"
            "<!-- ste-check-enable -->\n"
            "This seamless tool runs fast.\n"
        )
        findings = ste_check.check(text, False)
        self.assertEqual([(f.line, f.rule) for f in findings], [(4, "word")])

    def test_disable_block_specific_rule_and_partial_reenable(self) -> None:
        text = (
            "<!-- ste-check-disable passive, word -->\n"
            "The seamless token is validated by the gateway.\n"
            "<!-- ste-check-enable word -->\n"
            "The seamless token is validated by the gateway.\n"
            "<!-- ste-check-enable passive -->\n"
            "The token is validated by the gateway.\n"
        )
        findings = ste_check.check(text, False)
        self.assertEqual([(f.line, f.rule) for f in findings], [(4, "word"), (6, "passive")])

    def test_directives_ignored_in_code_fences_and_inline_code(self) -> None:
        text = (
            "```markdown\n"
            "<!-- ste-check-disable -->\n"
            "```\n"
            "The seamless token runs.\n"
            "Use `<!-- ste-check-disable -->` to skip a section.\n"
            "The robust token runs.\n"
        )
        findings = ste_check.check(text, False)
        self.assertEqual([(f.line, f.rule) for f in findings], [(4, "word"), (6, "word")])

    def test_unknown_rule_in_directive_is_reported(self) -> None:
        text = (
            "<!-- ste-check-disable -->\n"
            "The token is validated by the gateway.\n"
            "<!-- ste-check-enable passiv -->\n"
            "The token is validated by the gateway.\n"
        )
        findings = ste_check.check(text, False)
        self.assertEqual([(f.line, f.rule) for f in findings], [(3, "directive")])
        self.assertIn("passiv", findings[0].message)
        self.assertEqual(ste_check.check(text, False, ignore={"directive"}), [])

    def test_directive_comment_itself_does_not_trigger_dash_or_words(self) -> None:
        text = (
            "<!-- ste-check-disable-next-line passive -->\n"
            "The token is validated by the gateway.\n"
        )
        self.assertEqual(ste_check.check(text, False), [])
        stats = ste_check.summary(text)
        self.assertEqual(stats["sentences"], 1)

    def test_cli_list_rules_and_json(self) -> None:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ste_check.main(["--list-rules"])
        self.assertEqual(rc, 0)
        listed = buf.getvalue().strip().splitlines()
        self.assertEqual(set(listed), set(ste_check.ALL_RULES))

        buf_json = io.StringIO()
        with contextlib.redirect_stdout(buf_json):
            rc = ste_check.main(["--list-rules", "--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(set(json.loads(buf_json.getvalue())), set(ste_check.ALL_RULES))

    def test_cli_max_findings_and_select_ignore(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / "doc.md"
            sample.write_text("This seamless tool is validated by the gateway.\n", encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc_fail = ste_check.main([str(sample)])
            self.assertEqual(rc_fail, 1)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc_max = ste_check.main(["--max-findings", "2", str(sample)])
            self.assertEqual(rc_max, 0)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc_ignore = ste_check.main(["--ignore", "word", "--ignore", "passive", str(sample)])
            self.assertEqual(rc_ignore, 0)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc_select = ste_check.main(["--select", "semicolon", str(sample)])
            self.assertEqual(rc_select, 0)

    def test_cli_invalid_args_exit_2(self) -> None:
        for bad_argv in (
            ["--ignore", "not-a-real-rule", "-"],
            ["--select", "bogus", "-"],
            ["--max-findings", "-1", "-"],
            [],
        ):
            with self.assertRaises(SystemExit) as ctx:
                with contextlib.redirect_stderr(io.StringIO()):
                    ste_check.main(bad_argv)
            self.assertEqual(ctx.exception.code, 2, bad_argv)


if __name__ == "__main__":
    unittest.main()
