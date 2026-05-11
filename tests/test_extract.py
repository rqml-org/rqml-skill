from pathlib import Path
import unittest

from scripts import extract


class ExtractRequirementsTest(unittest.TestCase):
    def test_extract_from_main_requirements_doc(self):
        items = extract.extract_requirements(Path("requirements.rqml"))
        self.assertTrue(len(items) > 0)
        self.assertIn("id", items[0])
        self.assertIn("type", items[0])
        self.assertIn("title", items[0])
        self.assertIn("priority", items[0])
        self.assertIn("status", items[0])
        self.assertIn("statement", items[0])

    def test_extract_from_fixture(self):
        items = extract.extract_requirements(Path("tests/fixtures/valid-2.1.0.rqml"))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "REQ-FIXTURE-001")
        self.assertEqual(items[0]["type"], "FR")
        self.assertEqual(items[0]["title"], "Fixture requirement")
        self.assertEqual(items[0]["priority"], "must")
        self.assertEqual(items[0]["status"], "approved")
        self.assertIn("2.1.0 schema", items[0]["statement"])

    def test_output_order_is_stable_by_id(self):
        items = extract.extract_requirements(Path("requirements.rqml"))
        ids = [item["id"] for item in items]
        self.assertEqual(ids, sorted(ids))


if __name__ == "__main__":
    unittest.main()
