from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_case.py"
SPEC = importlib.util.spec_from_file_location("patent_draft_init_case", SCRIPT)
assert SPEC and SPEC.loader
init_case = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(init_case)


class InitCaseTests(unittest.TestCase):
    def test_all_profiles_resolve_references_and_templates(self):
        expected_status = {
            "us-utility": "foundation_only",
            "ru-invention": "drafting_ready",
            "ru-utility-model": "drafting_ready",
        }
        for profile_id in init_case.PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile, profile_path = init_case.load_profile(profile_id)
                self.assertTrue(profile_path.is_file())
                self.assertEqual(profile_id, profile["profile_id"])
                self.assertEqual(
                    init_case.PROFILE_SCHEMA_VERSION, profile["schema_version"]
                )
                self.assertEqual(
                    expected_status[profile_id], profile["foundation_status"]
                )

    def test_initializes_each_profile(self):
        selections = {
            "us-utility": ("new_draft", "en"),
            "ru-invention": ("translate_adapt", "ru"),
            "ru-utility-model": ("new_draft", "ru"),
        }
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            evidence = temp_path / "disclosure.txt"
            evidence.write_text("authentic inventor disclosure\n", encoding="utf-8")

            for profile_id, (mode, language) in selections.items():
                with self.subTest(profile_id=profile_id):
                    output = temp_path / profile_id
                    init_case.initialize_case(
                        profile_id=profile_id,
                        mode=mode,
                        language=language,
                        filing_context="pre_filing",
                        output=output,
                        sources=[str(evidence)],
                    )
                    manifest = json.loads((output / "case.json").read_text(encoding="utf-8"))
                    self.assertEqual(profile_id, manifest["profile_id"])
                    self.assertEqual(
                        init_case.sha256_file(evidence),
                        manifest["source_files"][0]["sha256"],
                    )
                    self.assertTrue((output / "intake-common.yaml").is_file())
                    self.assertTrue((output / "evidence-inventory.yaml").is_file())
                    self.assertTrue((output / "working" / "invention-thesis.md").is_file())
                    self.assertTrue((output / "working" / "claim-plan.md").is_file())
                    self.assertTrue((output / "working" / "support-map.md").is_file())
                    self.assertEqual(
                        init_case.PROFILE_SCHEMA_VERSION,
                        manifest["profile_schema_version"],
                    )
                    self.assertTrue(manifest["reference_files"])
                    self.assertTrue(
                        all(entry["sha256"] for entry in manifest["reference_files"])
                    )
                    self.assertTrue((output / "evidence").is_dir())
                    self.assertTrue((output / "deliverables").is_dir())

                    if profile_id == "ru-invention":
                        self.assertTrue(
                            (output / "working" / "ru-invention-description.md").is_file()
                        )
                        self.assertTrue(
                            (output / "working" / "ru-invention-claims.md").is_file()
                        )
                        self.assertTrue(
                            (output / "working" / "ru-translation-review.md").is_file()
                        )
                        self.assertTrue(
                            (output / "working" / "ru-rule-check.md").is_file()
                        )
                    if profile_id == "ru-utility-model":
                        self.assertTrue(
                            (
                                output
                                / "working"
                                / "ru-utility-model-description.md"
                            ).is_file()
                        )
                        self.assertTrue(
                            (output / "working" / "ru-utility-model-claims.md").is_file()
                        )
                        self.assertFalse(
                            (output / "working" / "ru-translation-review.md").exists()
                        )
                        self.assertTrue(
                            (output / "working" / "ru-rule-check.md").is_file()
                        )

    def test_rejects_incompatible_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(init_case.CaseInitError, "not supported"):
                init_case.initialize_case(
                    profile_id="us-utility",
                    mode="translate_adapt",
                    language="en",
                    filing_context="pre_filing",
                    output=Path(temp) / "case",
                    sources=[],
                )

    def test_does_not_overwrite_existing_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "case"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep\n", encoding="utf-8")
            with self.assertRaisesRegex(init_case.CaseInitError, "already exists"):
                init_case.initialize_case(
                    profile_id="ru-invention",
                    mode="new_draft",
                    language="ru",
                    filing_context="pre_filing",
                    output=output,
                    sources=[],
                )
            self.assertEqual("keep\n", sentinel.read_text(encoding="utf-8"))

    def test_rejects_missing_source(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(init_case.CaseInitError, "not a file"):
                init_case.initialize_case(
                    profile_id="ru-utility-model",
                    mode="new_draft",
                    language="ru",
                    filing_context="pre_filing",
                    output=Path(temp) / "case",
                    sources=[str(Path(temp) / "missing.txt")],
                )

    def test_revision_and_translation_require_source_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            for index, (profile_id, mode, language) in enumerate(
                (
                    ("us-utility", "revise", "en"),
                    ("ru-invention", "translate_adapt", "ru"),
                )
            ):
                with self.subTest(profile_id=profile_id, mode=mode):
                    with self.assertRaisesRegex(
                        init_case.CaseInitError, "requires at least one --source"
                    ):
                        init_case.initialize_case(
                            profile_id=profile_id,
                            mode=mode,
                            language=language,
                            filing_context="pre_filing",
                            output=Path(temp) / f"case-{index}",
                            sources=[],
                        )

    def test_mode_specific_templates_are_isolated(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            source = temp_path / "source.txt"
            source.write_text("source disclosure\n", encoding="utf-8")

            translated = temp_path / "translated"
            init_case.initialize_case(
                profile_id="ru-utility-model",
                mode="translate_adapt",
                language="ru",
                filing_context="pre_filing",
                output=translated,
                sources=[str(source)],
            )
            self.assertTrue(
                (translated / "working" / "ru-translation-review.md").is_file()
            )

            new_draft = temp_path / "new-draft"
            init_case.initialize_case(
                profile_id="ru-utility-model",
                mode="new_draft",
                language="ru",
                filing_context="pre_filing",
                output=new_draft,
                sources=[str(source)],
            )
            self.assertFalse(
                (new_draft / "working" / "ru-translation-review.md").exists()
            )


if __name__ == "__main__":
    unittest.main()
