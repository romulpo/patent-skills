#!/usr/bin/env python3
"""Initialize a support-mapped patent drafting workspace.

The script validates a shipped profile, records hashes for supplied source files,
and copies blank working templates. It never modifies or copies source evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT / "references" / "profiles"
PROFILE_IDENTITIES = {
    "us-utility": {"jurisdiction": "us", "application_kind": "utility"},
    "ru-invention": {"jurisdiction": "ru", "application_kind": "invention"},
    "ru-utility-model": {"jurisdiction": "ru", "application_kind": "utility_model"},
}
PROFILE_IDS = tuple(PROFILE_IDENTITIES)
MODES = ("new_draft", "revise", "translate_adapt")
FILING_CONTEXTS = ("pre_filing", "filed_pending")
LANGUAGES = ("en", "ru")
FOUNDATION_STATUSES = ("foundation_only", "drafting_ready")

REQUIRED_PROFILE_KEYS = {
    "schema_version",
    "profile_id",
    "jurisdiction",
    "application_kind",
    "default_language",
    "allowed_languages",
    "drafting_modes",
    "filing_contexts",
    "profile_reference",
    "common_references",
    "templates",
    "foundation_status",
}


class CaseInitError(ValueError):
    """A safe, user-correctable initialization error."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_skill_path(value: str) -> Path:
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise CaseInitError(f"profile path escapes the skill directory: {value}") from exc
    return candidate


def load_profile(profile_id: str) -> tuple[dict, Path]:
    if profile_id not in PROFILE_IDS:
        raise CaseInitError(
            f"unknown profile {profile_id!r}; choose one of: {', '.join(PROFILE_IDS)}"
        )
    path = PROFILES_DIR / f"{profile_id}.json"
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CaseInitError(f"cannot read profile {path}: {exc}") from exc

    missing = sorted(REQUIRED_PROFILE_KEYS - set(profile))
    extra = sorted(set(profile) - REQUIRED_PROFILE_KEYS)
    if missing or extra:
        raise CaseInitError(
            f"invalid profile keys for {profile_id}: missing={missing}, extra={extra}"
        )
    if profile["schema_version"] != 1:
        raise CaseInitError(f"unsupported profile schema: {profile['schema_version']}")
    if profile["profile_id"] != profile_id:
        raise CaseInitError(
            f"profile ID mismatch: requested {profile_id}, file declares {profile['profile_id']}"
        )

    expected_identity = PROFILE_IDENTITIES[profile_id]
    for key, expected in expected_identity.items():
        if profile[key] != expected:
            raise CaseInitError(
                f"profile {profile_id} has invalid {key}: expected {expected!r}, "
                f"got {profile[key]!r}"
            )

    list_constraints = {
        "allowed_languages": set(LANGUAGES),
        "drafting_modes": set(MODES),
        "filing_contexts": set(FILING_CONTEXTS),
    }
    for key, allowed in list_constraints.items():
        values = profile[key]
        if (
            not isinstance(values, list)
            or not values
            or len(values) != len(set(values))
            or not set(values).issubset(allowed)
        ):
            raise CaseInitError(f"profile {profile_id} has invalid {key}: {values!r}")

    if profile["default_language"] not in profile["allowed_languages"]:
        raise CaseInitError(
            f"profile {profile_id} default language is not in allowed_languages"
        )
    if profile["foundation_status"] not in FOUNDATION_STATUSES:
        raise CaseInitError(
            f"profile {profile_id} has invalid foundation_status: "
            f"{profile['foundation_status']!r}"
        )

    for key in ("common_references", "templates"):
        values = profile[key]
        if (
            not isinstance(values, list)
            or not values
            or len(values) != len(set(values))
            or not all(isinstance(value, str) and value for value in values)
        ):
            raise CaseInitError(f"profile {profile_id} has invalid {key}: {values!r}")
    if (
        not isinstance(profile["profile_reference"], str)
        or not profile["profile_reference"]
    ):
        raise CaseInitError(f"profile {profile_id} has invalid profile_reference")

    referenced = [
        profile["profile_reference"],
        *profile["common_references"],
        *profile["templates"],
    ]
    missing_paths = [
        value for value in referenced if not relative_skill_path(value).is_file()
    ]
    if missing_paths:
        raise CaseInitError(
            f"profile {profile_id} references missing files: {', '.join(missing_paths)}"
        )
    return profile, path


def validate_selection(profile: dict, mode: str, language: str, filing_context: str) -> None:
    if mode not in MODES or mode not in profile["drafting_modes"]:
        raise CaseInitError(
            f"mode {mode!r} is not supported by profile {profile['profile_id']}"
        )
    if language not in LANGUAGES or language not in profile["allowed_languages"]:
        raise CaseInitError(
            f"language {language!r} is not supported by profile {profile['profile_id']}"
        )
    if (
        filing_context not in FILING_CONTEXTS
        or filing_context not in profile["filing_contexts"]
    ):
        raise CaseInitError(
            f"filing context {filing_context!r} is not supported by profile "
            f"{profile['profile_id']}"
        )


def source_entries(values: list[str]) -> list[dict[str, str]]:
    entries = []
    seen: set[Path] = set()
    for value in values:
        path = Path(value).expanduser().resolve()
        if path in seen:
            raise CaseInitError(f"duplicate source file: {path}")
        seen.add(path)
        if not path.is_file():
            raise CaseInitError(f"source is not a file: {path}")
        entries.append({"path": str(path), "sha256": sha256_file(path)})
    return entries


def initialize_case(
    *,
    profile_id: str,
    mode: str,
    language: str,
    filing_context: str,
    output: Path,
    sources: list[str],
) -> Path:
    profile, profile_path = load_profile(profile_id)
    validate_selection(profile, mode, language, filing_context)
    if mode in {"revise", "translate_adapt"} and not sources:
        raise CaseInitError(f"mode {mode!r} requires at least one --source file")
    source_manifest = source_entries(sources)

    output = output.expanduser().resolve()
    if output.exists():
        raise CaseInitError(
            f"output already exists; choose a new case directory: {output}"
        )

    output.mkdir(parents=True)
    try:
        (output / "evidence").mkdir()
        (output / "working").mkdir()
        (output / "deliverables").mkdir()

        for template_value in profile["templates"]:
            source = relative_skill_path(template_value)
            if source.parent.name == "templates":
                target = output / "working" / source.name
            else:
                target = output / source.name
            shutil.copyfile(source, target)

        manifest = {
            "schema_version": 1,
            "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "profile_id": profile_id,
            "jurisdiction": profile["jurisdiction"],
            "application_kind": profile["application_kind"],
            "drafting_mode": mode,
            "document_language": language,
            "filing_context": filing_context,
            "profile_sha256": sha256_file(profile_path),
            "foundation_status": profile["foundation_status"],
            "source_files": source_manifest,
            "source_handling": "hashed in place; not copied or modified",
        }
        (output / "case.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=PROFILE_IDS)
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--language", required=True, choices=LANGUAGES)
    parser.add_argument("--filing-context", required=True, choices=FILING_CONTEXTS)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="source evidence file; repeatable",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        output = initialize_case(
            profile_id=args.profile,
            mode=args.mode,
            language=args.language,
            filing_context=args.filing_context,
            output=args.output,
            sources=args.source,
        )
    except CaseInitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"initialized patent drafting case: {output}")
    manifest = json.loads((output / "case.json").read_text(encoding="utf-8"))
    if manifest["foundation_status"] == "foundation_only":
        print(
            "profile status: foundation_only; jurisdiction-specific drafting "
            "rules are not installed"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
