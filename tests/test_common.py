from pathlib import Path
import unittest

from scripts import _backends, _common, _xml


class CommonHelpersTest(unittest.TestCase):
    def test_repo_root_resolves_workspace(self):
        root = _common.repo_root(Path(__file__).resolve())
        self.assertTrue((root / "requirements.rqml").exists())

    def test_supported_schema_versions_include_bundled_files(self):
        versions = _common.list_supported_schema_versions()
        self.assertIn("2.0.1", versions)
        self.assertIn("2.1.0", versions)

    def test_schema_path_for_version_returns_existing_file(self):
        schema_path = _common.schema_path_for_version("2.1.0")
        self.assertTrue(schema_path.exists())
        self.assertEqual(schema_path.name, "rqml-2.1.0.xsd")

    def test_detect_version_from_fixture(self):
        fixture = Path("tests/fixtures/valid-2.1.0.rqml")
        version = _xml.detect_version(fixture)
        self.assertEqual(version, "2.1.0")

    def test_choose_backend_returns_info_or_none(self):
        backend = _backends.choose_backend()
        if backend is not None:
            self.assertTrue(backend.available)
            self.assertIn(backend.name, {"xmllint", "lxml", "xmlschema"})


if __name__ == "__main__":
    unittest.main()
