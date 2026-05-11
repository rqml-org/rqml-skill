from pathlib import Path
import unittest

from scripts import lint
from scripts import _strictness


class StrictnessResolutionTest(unittest.TestCase):
    def test_override_wins(self):
        resolution = _strictness.resolve_strictness("strict", Path("."))
        self.assertEqual(resolution.level, "strict")
        self.assertEqual(resolution.source, "--strictness")

    def test_yaml_resolution(self):
        resolution = _strictness.resolve_strictness(None, Path("."))
        self.assertEqual(resolution.level, "standard")


class LintRulesTest(unittest.TestCase):
    def test_standard_requires_acceptance(self):
        fixture = Path("tests/fixtures/lint-no-acceptance.rqml")
        level, source, violations = lint.run_lint(fixture, "standard")
        self.assertEqual(level, "standard")
        self.assertTrue(any("missing acceptance criteria" in item for item in violations))

    def test_strict_requires_trace_edges(self):
        fixture = Path("tests/fixtures/lint-with-acceptance-no-trace.rqml")
        level, source, violations = lint.run_lint(fixture, "strict")
        self.assertEqual(level, "strict")
        self.assertTrue(any("No trace edges found" in item for item in violations))

    def test_certified_requires_trace_metadata(self):
        fixture = Path("tests/fixtures/lint-certified-missing-trace-metadata.rqml")
        level, source, violations = lint.run_lint(fixture, "certified")
        self.assertEqual(level, "certified")
        self.assertTrue(any("missing trace metadata attribute" in item for item in violations))


if __name__ == "__main__":
    unittest.main()
