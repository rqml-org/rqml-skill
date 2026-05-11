from pathlib import Path
import unittest

from scripts import matrix


class MatrixTest(unittest.TestCase):
    def test_extract_rows_from_requirements_doc(self):
        rows = matrix.extract_requirements_and_traces(Path("requirements.rqml"))
        self.assertTrue(len(rows) > 0)
        self.assertIn("id", rows[0])
        self.assertIn("title", rows[0])
        self.assertIn("satisfies", rows[0])
        self.assertIn("dependsOn", rows[0])
        self.assertIn("mitigates", rows[0])
        self.assertIn("verifiedBy", rows[0])

    def test_render_matrix_has_header_and_rows(self):
        rows = matrix.extract_requirements_and_traces(Path("requirements.rqml"))
        output = matrix.render_matrix(rows)
        self.assertIn("| Requirement | Title | Satisfies | Depends On | Mitigates | Verified By |", output)
        self.assertIn("REQ-SKILL-MD", output)

    def test_fixture_matrix_has_one_requirement_row(self):
        rows = matrix.extract_requirements_and_traces(Path("tests/fixtures/valid-2.1.0.rqml"))
        self.assertEqual(len(rows), 1)
        output = matrix.render_matrix(rows)
        self.assertIn("REQ-FIXTURE-001", output)


if __name__ == "__main__":
    unittest.main()
