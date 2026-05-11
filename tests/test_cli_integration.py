from pathlib import Path
import json
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_script(script_name, *args):
    script_path = ROOT / "scripts" / script_name
    return subprocess.run(
        [PYTHON, str(script_path), *[str(arg) for arg in args]],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


class CliIntegrationTest(unittest.TestCase):
    def test_validate_valid_fixture_json(self):
        result = run_script("validate.py", "--json", "tests/fixtures/valid-2.1.0.rqml")
        self.assertIn(result.returncode, {0, 2})
        if result.returncode == 0:
            payload = json.loads(result.stdout)
            self.assertIn("backend", payload)
            self.assertIn("schema", payload)
            self.assertIn("errors", payload)

    def test_validate_invalid_missing_version(self):
        result = run_script("validate.py", "tests/fixtures/invalid-missing-version.rqml")
        self.assertIn(result.returncode, {1, 2})

    def test_validate_old_schema_dispatch(self):
        result = run_script("validate.py", "--json", "tests/fixtures/valid-2.0.1.rqml")
        self.assertIn(result.returncode, {0, 2})
        if result.returncode == 0:
            payload = json.loads(result.stdout)
            self.assertTrue(payload["schema"].endswith("rqml-2.0.1.xsd"))

    def test_matrix_cli_outputs_markdown(self):
        result = run_script("matrix.py", "requirements.rqml")
        self.assertEqual(result.returncode, 0)
        self.assertIn("| Requirement | Title | Satisfies | Depends On | Mitigates | Verified By |", result.stdout)

    def test_extract_cli_outputs_json_array(self):
        result = run_script("extract.py", "tests/fixtures/valid-2.1.0.rqml")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIsInstance(payload, list)
        self.assertEqual(payload[0]["id"], "REQ-FIXTURE-001")

    def test_lint_cli_standard_fixture(self):
        result = run_script("lint.py", "--strictness", "standard", "tests/fixtures/lint-no-acceptance.rqml")
        self.assertEqual(result.returncode, 1)
        self.assertIn("STRICTNESS level=standard", result.stdout)

    def test_check_traces_cli_valid_doc(self):
        result = run_script("check_traces.py", "tests/fixtures/trace-valid-doc-target.rqml")
        self.assertEqual(result.returncode, 0)
        self.assertIn("OK edge=TR-TRACE-VALID", result.stdout)

    def test_id_audit_cli_valid_fixture(self):
        result = run_script("id_audit.py", "tests/fixtures/id-audit-valid.rqml")
        self.assertEqual(result.returncode, 0)
        self.assertIn("ID AUDIT OK", result.stdout)

    def test_performance_validate_on_small_fixture_is_fast(self):
        start = time.perf_counter()
        result = run_script("validate.py", "tests/fixtures/valid-2.1.0.rqml")
        elapsed = time.perf_counter() - start
        self.assertIn(result.returncode, {0, 2})
        self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
