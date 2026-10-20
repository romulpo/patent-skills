from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_evals.py"
SPEC = importlib.util.spec_from_file_location("patent_draft_validate_evals", SCRIPT)
assert SPEC and SPEC.loader
validate_evals = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_evals)


class RussianEvaluationCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validated = validate_evals.validate_eval_corpus()
        cls.cases = [item["case"] for item in cls.validated]

    def test_corpus_has_unique_cases_and_files(self):
        self.assertEqual(6, len(self.cases))
        self.assertEqual(len(self.cases), len({case["id"] for case in self.cases}))
        for item in self.validated:
            self.assertTrue(item["request"].is_file())
            self.assertTrue(all(path.is_file() for path in item["sources"]))

    def test_corpus_covers_profiles_modes_and_filing_contexts(self):
        self.assertEqual(
            {"ru-invention", "ru-utility-model"},
            {case["profile_id"] for case in self.cases},
        )
        self.assertEqual(
            {"new_draft", "revise", "translate_adapt"},
            {case["mode"] for case in self.cases},
        )
        self.assertEqual(
            {"pre_filing", "filed_pending"},
            {case["filing_context"] for case in self.cases},
        )

    def test_corpus_covers_expected_risk_classes(self):
        tags = {tag for case in self.cases for tag in case["scenario_tags"]}
        self.assertTrue(
            {
                "claim_architecture",
                "device_only",
                "no_fabrication",
                "translation_integrity",
                "new_matter",
                "support_mapping",
            }.issubset(tags)
        )
        self.assertEqual(
            {"draft_packet", "review_packet", "blocked_for_input"},
            {case["expected_disposition"] for case in self.cases},
        )

    def test_evidence_is_explicitly_synthetic(self):
        for item in self.validated:
            for source in item["sources"]:
                with self.subTest(case=item["case"]["id"], source=source.name):
                    text = source.read_text(encoding="utf-8").lower()
                    self.assertTrue("synthetic" in text or "синтет" in text)

    def test_eval_paths_cannot_escape_the_corpus(self):
        with self.assertRaisesRegex(
            validate_evals.EvalValidationError, "escapes evals"
        ):
            validate_evals.eval_path("../SKILL.md")


if __name__ == "__main__":
    unittest.main()
