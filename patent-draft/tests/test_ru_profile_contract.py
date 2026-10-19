from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_case.py"
SPEC = importlib.util.spec_from_file_location("patent_draft_init_case_contract", SCRIPT)
assert SPEC and SPEC.loader
init_case = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(init_case)


class RussianProfileContractTests(unittest.TestCase):
    def test_ru_profiles_are_drafting_ready_and_source_mapped(self):
        for profile_id in ("ru-invention", "ru-utility-model"):
            with self.subTest(profile_id=profile_id):
                profile, _ = init_case.load_profile(profile_id)
                self.assertEqual("drafting_ready", profile["foundation_status"])
                self.assertGreaterEqual(len(profile["jurisdiction_references"]), 5)
                self.assertIn(
                    "references/ru/source-manifest.md",
                    profile["jurisdiction_references"],
                )
                self.assertIn(
                    "assets/templates/ru-translation-review.md",
                    profile["mode_templates"]["translate_adapt"],
                )

    def test_profile_specific_claim_templates_do_not_cross_route(self):
        invention, _ = init_case.load_profile("ru-invention")
        utility_model, _ = init_case.load_profile("ru-utility-model")

        self.assertIn(
            "assets/templates/ru-invention-claims.md", invention["templates"]
        )
        self.assertNotIn(
            "assets/templates/ru-utility-model-claims.md", invention["templates"]
        )
        self.assertIn(
            "assets/templates/ru-utility-model-claims.md",
            utility_model["templates"],
        )
        self.assertNotIn(
            "assets/templates/ru-invention-claims.md", utility_model["templates"]
        )

    def test_us_profile_does_not_load_ru_sources(self):
        profile, _ = init_case.load_profile("us-utility")
        self.assertEqual([], profile["jurisdiction_references"])
        self.assertEqual({}, profile["mode_templates"])


if __name__ == "__main__":
    unittest.main()
