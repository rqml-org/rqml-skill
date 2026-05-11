from pathlib import Path
import unittest

from scripts import validate


class ValidateScriptTest(unittest.TestCase):
    def test_detect_schema_uses_document_version(self):
        fixture = Path("tests/fixtures/valid-2.0.1.rqml")
        schema = validate.detect_schema(fixture, None)
        self.assertEqual(schema.name, "rqml-2.0.1.xsd")

    def test_detect_schema_honors_override(self):
        fixture = Path("tests/fixtures/valid-2.0.1.rqml")
        schema = validate.detect_schema(fixture, "2.1.0")
        self.assertEqual(schema.name, "rqml-2.1.0.xsd")

    def test_install_guidance_mentions_all_backends(self):
        message = validate.install_guidance()
        self.assertIn("xmllint", message)
        self.assertIn("lxml", message)
        self.assertIn("xmlschema", message)

    def test_parse_xmllint_errors_extracts_location(self):
        stderr = "tests/fixtures/invalid-missing-version.rqml:2:3: element rqml: Schemas validity error : missing required attribute 'version'\n"
        errors = validate.parse_xmllint_errors(stderr)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].line, 2)
        self.assertEqual(errors[0].column, 3)
        self.assertIn("missing required attribute", errors[0].message)


if __name__ == "__main__":
    unittest.main()
