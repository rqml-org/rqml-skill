from pathlib import Path
import unittest

from scripts import _trace


class TraceResolverTest(unittest.TestCase):
    def test_resolves_valid_doc_locator(self):
        fixture = Path("tests/fixtures/trace-valid-doc-target.rqml")
        results = _trace.resolve_trace_locators(fixture)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].ok)

    def test_reports_unresolved_doc_locator(self):
        fixture = Path("tests/fixtures/trace-invalid-doc-target.rqml")
        results = _trace.resolve_trace_locators(fixture)
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].ok)
        self.assertIn("unresolved doc target", results[0].message)

    def test_accepts_http_external_locator(self):
        fixture = Path("tests/fixtures/trace-valid-external-target.rqml")
        results = _trace.resolve_trace_locators(fixture)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].ok)
        self.assertIn("external HTTP target parsed", results[0].message)


if __name__ == "__main__":
    unittest.main()
