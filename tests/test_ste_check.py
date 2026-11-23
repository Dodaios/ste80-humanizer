"""Tests for scripts/ste_check.py --compare rewrite fidelity checks."""

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


class TestSteCheckCompareFidelity(unittest.TestCase):
    def test_faithful_ste_rewrite_passes(self) -> None:
        original = (
            "Great question! Kubernetes liveness probes might fail when `initialDelaySeconds` "
            "or `failureThreshold` is too low for 40+ services. See https://kubernetes.io/docs/tasks/.\n"
        )
        rewrite = (
            "A liveness probe can fail if `initialDelaySeconds` or `failureThreshold` "
            "is too low for 40+ services. Read the [docs](https://kubernetes.io/docs/tasks/).\n"
        )
        self.assertEqual(ste_check.compare_texts(original, rewrite), [])

    def test_catches_altered_quantifier_number(self) -> None:
        original = "We serve 40+ customers with 99.9% uptime.\n"
        rewrite = "We serve 40-odd customers with 99% uptime.\n"
        findings = ste_check.compare_texts(original, rewrite)
        self.assertEqual([f.rule for f in findings], ["fidelity-number", "fidelity-number"])
        self.assertIn("40+", findings[0].message)
        self.assertIn("99.9%", findings[1].message)

    def test_catches_missing_inline_and_fenced_code(self) -> None:
        original = (
            "Set `initialDelaySeconds` and `failureThreshold`.\n"
            "```bash\n"
            "kubectl apply -f probe.yaml\n"
            "```\n"
        )
        rewrite = (
            "Set `initialDelaySeconds`.\n"
            "```bash\n"
            "kubectl apply -f deploy.yaml\n"
            "```\n"
        )
        findings = ste_check.compare_texts(original, rewrite)
        self.assertEqual([f.rule for f in findings], ["fidelity-code", "fidelity-code"])
        self.assertIn("failureThreshold", findings[0].message)
        self.assertIn("fenced code block", findings[1].message)

    def test_catches_missing_url(self) -> None:
        original = "Read the [guide](https://example.com/guide) and https://example.com/api.\n"
        rewrite = "Read the [guide](https://example.com/guide).\n"
        findings = ste_check.compare_texts(original, rewrite)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "fidelity-url")
        self.assertIn("https://example.com/api", findings[0].message)

    def test_catches_dropped_quote(self) -> None:
        original = 'The note says "written in STE style" on the cover.\n'
        rewrite = "The note describes the style on the cover.\n"
        findings = ste_check.compare_texts(original, rewrite)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "fidelity-quote")

    def test_curly_to_straight_quote_normalization_passes(self) -> None:
        original = "The label reads “written in STE style”.\n"
        rewrite = 'The label reads "written in STE style".\n'
        self.assertEqual(ste_check.compare_texts(original, rewrite), [])

    def test_catches_dropped_uncertainty_hedge(self) -> None:
        original = "This change might fail on empty headers.\n"
        rewrite = "This change fails on empty headers.\n"
        findings = ste_check.compare_texts(original, rewrite)
        self.assertEqual([f.rule for f in findings], ["fidelity-certainty"])

    def test_allows_ste_certainty_swap_might_to_can(self) -> None:
        original = "This change might fail on empty headers.\n"
        rewrite = "This change can fail on empty headers.\n"
        self.assertEqual(ste_check.compare_texts(original, rewrite), [])

    def test_list_renumbering_does_not_false_positive(self) -> None:
        original = "1. Open the file.\n2. Save the file.\n"
        rewrite = "- Open the file.\n- Save the file.\n"
        self.assertEqual(ste_check.compare_texts(original, rewrite), [])

    def test_cli_compare_text_and_json_and_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            orig = Path(tmp) / "orig.md"
            good = Path(tmp) / "good.md"
            bad = Path(tmp) / "bad.md"
            orig.write_text("It might handle 40+ items via `run_job`.\n", encoding="utf-8")
            good.write_text("It can handle 40+ items with `run_job`.\n", encoding="utf-8")
            bad.write_text("It handles 40 items.\n", encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc_ok = ste_check.main(["--compare", str(orig), str(good)])
            self.assertEqual(rc_ok, 0)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc_bad = ste_check.main(["--compare", str(orig), str(bad), "--json"])
            self.assertEqual(rc_bad, 1)
            data = json.loads(buf.getvalue())
            rules = {f["rule"] for f in data["findings"]}
            self.assertEqual(rules, {"fidelity-number", "fidelity-code", "fidelity-certainty"})

            for bad_argv in (
                ["--compare", "-", "-"],
                ["--compare", str(orig), str(good), str(bad)],
                [],
            ):
                with self.assertRaises(SystemExit) as ctx:
                    with contextlib.redirect_stderr(io.StringIO()):
                        ste_check.main(bad_argv)
                self.assertEqual(ctx.exception.code, 2, bad_argv)


if __name__ == "__main__":
    unittest.main()
