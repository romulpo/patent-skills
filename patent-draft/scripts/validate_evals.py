#!/usr/bin/env python3
"""Validate and smoke-initialize the patent-draft evaluation corpus."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = ROOT / "evals"
DEFAULT_MANIFEST = EVAL_ROOT / "cases.json"
INIT_CASE_SCRIPT = ROOT / "scripts" / "init_case.py"

SPEC = importlib.util.spec_from_file_location("patent_draft_init_case_for_evals", INIT_CASE_SCRIPT)
assert SPEC and SPEC.loader
init_case = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(init_case)

CASE_KEYS = {
    "id",
    "profile_id",
    "mode",
    "language",
    "filing_context",
    "request_path",
    "source_paths",
    "scenario_tags",
    "expected_disposition",
    "required_observations",
    "forbidden_outcomes",
}
OBSERVATION_KEYS = {"id", "criterion"}
DISPOSITIONS = {"draft_packet", "review_packet", "blocked_for_input"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class EvalValidationError(ValueError):
    """A deterministic evaluation-corpus validation error."""


def eval_path(value: str) -> Path:
    path = (EVAL_ROOT / value).resolve()
    try:
        path.relative_to(EVAL_ROOT.resolve())
    except ValueError as exc:
        raise EvalValidationError(f"evaluation path escapes evals/: {value}") from exc
    if not path.is_file():
        raise EvalValidationError(f"evaluation file does not exist: {value}")
    return path


def unique_nonempty_strings(values: object, *, label: str) -> list[str]:
    if (
        not isinstance(values, list)
        or not values
        or not all(isinstance(value, str) and value.strip() for value in values)
        or len(values) != len(set(values))
    ):
        raise EvalValidationError(f"{label} must be unique non-empty strings")
    return values


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvalValidationError(f"cannot read evaluation manifest {path}: {exc}") from exc

    if set(manifest) != {"schema_version", "cases"}:
        raise EvalValidationError("evaluation manifest has unexpected keys")
    if manifest["schema_version"] != 1:
        raise EvalValidationError(
            f"unsupported evaluation schema: {manifest['schema_version']}"
        )
    if not isinstance(manifest["cases"], list) or not manifest["cases"]:
        raise EvalValidationError("evaluation manifest must contain cases")
    return manifest


def validate_case(case: object, seen_ids: set[str]) -> dict:
    if not isinstance(case, dict) or set(case) != CASE_KEYS:
        raise EvalValidationError("evaluation case has unexpected or missing keys")

    case_id = case["id"]
    if not isinstance(case_id, str) or not ID_PATTERN.fullmatch(case_id):
        raise EvalValidationError(f"invalid case id: {case_id!r}")
    if case_id in seen_ids:
        raise EvalValidationError(f"duplicate case id: {case_id}")
    seen_ids.add(case_id)

    for key in (
        "profile_id",
        "mode",
        "language",
        "filing_context",
        "request_path",
        "expected_disposition",
    ):
        if not isinstance(case[key], str) or not case[key].strip():
            raise EvalValidationError(f"{case_id}: {key} must be a non-empty string")

    if case["profile_id"] not in {"ru-invention", "ru-utility-model"}:
        raise EvalValidationError(f"{case_id}: eval corpus accepts only RU profiles")
    if case["expected_disposition"] not in DISPOSITIONS:
        raise EvalValidationError(f"{case_id}: invalid expected_disposition")

    profile, _ = init_case.load_profile(case["profile_id"])
    try:
        init_case.validate_selection(
            profile,
            case["mode"],
            case["language"],
            case["filing_context"],
        )
    except init_case.CaseInitError as exc:
        raise EvalValidationError(f"{case_id}: {exc}") from exc

    request = eval_path(case["request_path"])
    source_values = unique_nonempty_strings(
        case["source_paths"], label=f"{case_id}.source_paths"
    )
    sources = [eval_path(value) for value in source_values]
    if request in sources:
        raise EvalValidationError(f"{case_id}: request must be separate from evidence")
    if case["mode"] == "translate_adapt" and len(sources) < 2:
        raise EvalValidationError(f"{case_id}: translation case needs source and target")

    unique_nonempty_strings(
        case["scenario_tags"], label=f"{case_id}.scenario_tags"
    )
    observations = case["required_observations"]
    if not isinstance(observations, list) or not observations:
        raise EvalValidationError(f"{case_id}: required_observations must not be empty")
    observation_ids: set[str] = set()
    for observation in observations:
        if not isinstance(observation, dict) or set(observation) != OBSERVATION_KEYS:
            raise EvalValidationError(f"{case_id}: invalid observation")
        observation_id = observation["id"]
        criterion = observation["criterion"]
        if (
            not isinstance(observation_id, str)
            or not ID_PATTERN.fullmatch(observation_id)
            or observation_id in observation_ids
            or not isinstance(criterion, str)
            or not criterion.strip()
        ):
            raise EvalValidationError(f"{case_id}: invalid observation values")
        observation_ids.add(observation_id)

    unique_nonempty_strings(
        case["forbidden_outcomes"], label=f"{case_id}.forbidden_outcomes"
    )
    return {"case": case, "request": request, "sources": sources}


def validate_eval_corpus(path: Path = DEFAULT_MANIFEST) -> list[dict]:
    manifest = load_manifest(path)
    seen_ids: set[str] = set()
    validated = [validate_case(case, seen_ids) for case in manifest["cases"]]

    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        for item in validated:
            case = item["case"]
            output = temp_root / case["id"]
            init_case.initialize_case(
                profile_id=case["profile_id"],
                mode=case["mode"],
                language=case["language"],
                filing_context=case["filing_context"],
                output=output,
                sources=[str(path) for path in item["sources"]],
            )
            case_manifest = json.loads(
                (output / "case.json").read_text(encoding="utf-8")
            )
            if len(case_manifest["source_files"]) != len(item["sources"]):
                raise EvalValidationError(
                    f"{case['id']}: initializer did not record every source"
                )
            if not (output / "working" / "ru-rule-check.md").is_file():
                raise EvalValidationError(
                    f"{case['id']}: RU rule-check template was not initialized"
                )
            translation_review = output / "working" / "ru-translation-review.md"
            if translation_review.is_file() != (case["mode"] == "translate_adapt"):
                raise EvalValidationError(
                    f"{case['id']}: translation template routing is incorrect"
                )
    return validated


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        validated = validate_eval_corpus(args.manifest)
    except EvalValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    for item in validated:
        case = item["case"]
        print(
            f"ok  {case['id']}: {case['profile_id']} / {case['mode']} / "
            f"{case['expected_disposition']}"
        )
    print(f"validated {len(validated)} RU drafting evaluation cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
