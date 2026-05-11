from pathlib import Path
import tempfile
import subprocess
import unittest

from scripts import id_audit


class IdAuditTest(unittest.TestCase):
    def test_reports_malformed_ids(self):
        fixture = Path("tests/fixtures/id-audit-malformed.rqml")
        result = id_audit.run_audit(fixture)
        self.assertIn("1BAD-ID", result["malformed"])

    def test_valid_fixture_has_no_malformed_or_duplicates(self):
        fixture = Path("tests/fixtures/id-audit-valid.rqml")
        result = id_audit.run_audit(fixture)
        self.assertEqual(result["duplicates"], [])
        self.assertEqual(result["malformed"], [])

    def test_compare_with_previous_handles_missing_git_history(self):
        fixture = Path("tests/fixtures/id-audit-valid.rqml")
        previous = id_audit.compare_with_previous(fixture)
        self.assertIn(previous, (None, previous))

    def test_compare_with_previous_detects_changes_in_temp_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True, capture_output=True)

            (repo / ".rqml").mkdir()
            target = repo / "requirements.rqml"
            target.write_text(
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<rqml xmlns=\"https://rqml.org/schema/2.1.0\" version=\"2.1.0\" docId=\"TMP\" status=\"draft\">\n"
                "  <meta><title>Tmp</title><system>tmp</system></meta>\n"
                "  <requirements><req id=\"REQ-OLD-001\" type=\"FR\" title=\"Old\"><statement>Old</statement></req></requirements>\n"
                "</rqml>\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "requirements.rqml", ".rqml"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True)

            target.write_text(
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<rqml xmlns=\"https://rqml.org/schema/2.1.0\" version=\"2.1.0\" docId=\"TMP\" status=\"draft\">\n"
                "  <meta><title>Tmp</title><system>tmp</system></meta>\n"
                "  <requirements><req id=\"REQ-NEW-001\" type=\"FR\" title=\"New\"><statement>New</statement></req></requirements>\n"
                "</rqml>\n",
                encoding="utf-8",
            )

            previous = id_audit.compare_with_previous(target)
            self.assertIsNotNone(previous)
            removed, added = previous
            self.assertIn("REQ-OLD-001", removed)
            self.assertIn("REQ-NEW-001", added)


if __name__ == "__main__":
    unittest.main()
