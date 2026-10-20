from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_case.py"
SPEC = importlib.util.spec_from_file_location("patent_draft_init_case_us", SCRIPT)
assert SPEC and SPEC.loader
init_case = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(init_case)


class USProfileContractTests(unittest.TestCase):
    def test_us_profile_is_drafting_ready_and_source_mapped(self):
        profile, _ = init_case.load_profile("us-utility")

        self.assertEqual("drafting_ready", profile["foundation_status"])
        self.assertGreaterEqual(len(profile["jurisdiction_references"]), 5)
        self.assertIn(
            "references/us/source-manifest.md",
            profile["jurisdiction_references"],
        )
        self.assertIn(
            "references/us/claim-drafting.md",
            profile["jurisdiction_references"],
        )

    def test_us_profile_routes_us_templates_only(self):
        profile, _ = init_case.load_profile("us-utility")

        self.assertIn("assets/templates/us-utility-description.md", profile["templates"])
        self.assertIn("assets/templates/us-utility-claims.md", profile["templates"])
        self.assertIn("assets/templates/us-abstract.md", profile["templates"])
        self.assertIn("assets/templates/us-rule-check.md", profile["templates"])
        self.assertFalse(any("/ru-" in value for value in profile["templates"]))

    def test_us_initializer_copies_profile_specific_artifacts(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "case"
            init_case.initialize_case(
                profile_id="us-utility",
                mode="new_draft",
                language="en",
                filing_context="pre_filing",
                output=output,
                sources=[],
            )

            for name in (
                "us-utility-description.md",
                "us-utility-claims.md",
                "us-abstract.md",
                "us-rule-check.md",
            ):
                self.assertTrue((output / "working" / name).is_file())


if __name__ == "__main__":
    unittest.main()
