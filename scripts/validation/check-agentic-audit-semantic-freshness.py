#!/usr/bin/env python3
"""Validate deterministic semantic closures in the canonical agentic audit."""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
from dataclasses import dataclass
from typing import Any

from audit_criterion_contract import (
    EXPECTED_PACK_FILES,
    AuditCriterionContractError,
    validate_pack,
)


DEFAULT_CONTRACT = pathlib.Path(
    "scripts/validation/agentic-audit-semantic-contract.json"
)
EXPECTED_AUDIT_INDEX = "docs/90.references/audits/README.md"
EXPECTED_CANONICAL_PACK = (
    "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack"
)
EXPECTED_OVERVIEW = f"{EXPECTED_CANONICAL_PACK}/implementation-overview.md"
EXPECTED_TASK_EVIDENCE = (
    "docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md"
)
EXPECTED_TOP_LEVEL_PATHS = {
    "audit_index": EXPECTED_AUDIT_INDEX,
    "canonical_pack": EXPECTED_CANONICAL_PACK,
    "overview": EXPECTED_OVERVIEW,
    "task_evidence": EXPECTED_TASK_EVIDENCE,
}
SUPERSEDED_2026_07_07_README = pathlib.Path(
    "docs/90.references/audits/"
    "2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md"
)
EXPECTED_ASSERTION_IDS = {
    "DML-01",
    "DML-02",
    "DML-03",
    "DML-04",
    "DML-05",
    "DML-07",
    "DML-08",
    "DML-11",
    "DML-14",
    "QAF-12",
    "AUT-09",
}
EXPECTED_HEADINGS = [
    "## Canonical Current Audit",
    "## Dated Historical Snapshots",
    "## Supersession Ledgers",
]
CONTRACT_KEYS = {
    "schema_version",
    "audit_index",
    "canonical_pack",
    "overview",
    "task_evidence",
    "required_index_headings",
    "assertions",
}
ASSERTION_KEYS = {
    "criterion_id",
    "report",
    "required_state",
    "required_evidence_paths",
    "completed_task_ids",
    "forbidden_stale_phrases",
}


@dataclass(frozen=True)
class SemanticValidationResult:
    assertion_count: int


class AuditSemanticContractError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(errors))


class _DuplicateJsonKey(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJsonKey(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _is_safe_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = pathlib.PurePosixPath(value)
    return not path.is_absolute() and all(
        part not in {"", ".", ".."} for part in path.parts
    )


def _validate_string_array(
    owner: str,
    key: str,
    value: object,
    errors: list[str],
) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty array")
        return
    if any(not isinstance(item, str) or not item for item in value):
        errors.append(f"{owner}: {key} must contain only non-empty strings")
        return
    if len(value) != len(set(value)):
        errors.append(f"{owner}: {key} contains duplicate values")


def _validate_contract_schema(contract: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["semantic contract root must be a JSON object"]

    actual_keys = set(contract)
    missing_keys = sorted(CONTRACT_KEYS - actual_keys)
    unknown_keys = sorted(actual_keys - CONTRACT_KEYS)
    if missing_keys:
        errors.append(f"missing contract keys: {', '.join(missing_keys)}")
    if unknown_keys:
        errors.append(f"unknown contract keys: {', '.join(unknown_keys)}")
    if missing_keys:
        return errors

    if type(contract["schema_version"]) is not int or contract["schema_version"] != 1:
        errors.append("schema_version must be integer 1")

    for key in ("audit_index", "canonical_pack", "overview", "task_evidence"):
        if not _is_safe_repo_path(contract[key]):
            errors.append(f"{key}: unsafe repository-relative path: {contract[key]!r}")
        if contract[key] != EXPECTED_TOP_LEVEL_PATHS[key]:
            errors.append(
                f"{key} must use fixed canonical path: {EXPECTED_TOP_LEVEL_PATHS[key]}"
            )

    headings = contract["required_index_headings"]
    if headings != EXPECTED_HEADINGS:
        errors.append(
            "required_index_headings must exactly match the three canonical lifecycle headings"
        )

    assertions = contract["assertions"]
    if not isinstance(assertions, list):
        errors.append("assertions must be an array")
        return errors

    assertion_ids: list[str] = []
    for index, assertion in enumerate(assertions):
        owner = f"assertions[{index}]"
        if not isinstance(assertion, dict):
            errors.append(f"{owner} must be an object")
            continue
        actual_assertion_keys = set(assertion)
        missing_assertion_keys = sorted(ASSERTION_KEYS - actual_assertion_keys)
        unknown_assertion_keys = sorted(actual_assertion_keys - ASSERTION_KEYS)
        if missing_assertion_keys:
            errors.append(
                f"{owner}: missing assertion keys: {', '.join(missing_assertion_keys)}"
            )
        if unknown_assertion_keys:
            errors.append(
                f"{owner}: unknown assertion keys: {', '.join(unknown_assertion_keys)}"
            )
        if missing_assertion_keys:
            continue

        criterion_id = assertion["criterion_id"]
        if not isinstance(criterion_id, str) or not criterion_id:
            errors.append(f"{owner}: criterion_id must be a non-empty string")
        else:
            assertion_ids.append(criterion_id)
            owner = criterion_id

        if not _is_safe_repo_path(assertion["report"]):
            errors.append(
                f"{owner}: report has unsafe repository-relative path: {assertion['report']!r}"
            )
        if assertion["required_state"] != "Implemented":
            errors.append(f"{owner}: required_state must be Implemented")

        for key in (
            "required_evidence_paths",
            "completed_task_ids",
            "forbidden_stale_phrases",
        ):
            _validate_string_array(owner, key, assertion[key], errors)

        evidence_paths = assertion["required_evidence_paths"]
        if isinstance(evidence_paths, list):
            for path in evidence_paths:
                if not _is_safe_repo_path(path):
                    errors.append(
                        f"{owner}: unsafe repository-relative path in required_evidence_paths: {path!r}"
                    )

    duplicates = sorted(
        criterion_id
        for criterion_id in set(assertion_ids)
        if assertion_ids.count(criterion_id) > 1
    )
    if duplicates:
        errors.append(f"duplicate assertion IDs: {', '.join(duplicates)}")
    if len(assertions) != 11 or set(assertion_ids) != EXPECTED_ASSERTION_IDS:
        errors.append(
            "assertion IDs must be exactly: "
            + ", ".join(sorted(EXPECTED_ASSERTION_IDS))
        )

    return errors


def _load_contract(path: pathlib.Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
        contract = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except _DuplicateJsonKey as exc:
        raise AuditSemanticContractError([str(exc)]) from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AuditSemanticContractError(
            [f"unable to load semantic contract {path}: {exc}"]
        ) from exc

    errors = _validate_contract_schema(contract)
    if errors:
        raise AuditSemanticContractError(errors)
    return contract


def _tracked_paths(repo_root: pathlib.Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise AuditSemanticContractError([f"git ls-files failed: {exc}"]) from exc
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise AuditSemanticContractError(
            [
                f"git ls-files failed with exit {result.returncode}: {message or 'no diagnostic'}"
            ]
        )
    try:
        decoded = result.stdout.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise AuditSemanticContractError(["git ls-files returned a non-UTF-8 path"])
    return {path for path in decoded.split("\0") if path}


def _read_required(path: pathlib.Path, label: str, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: unable to read {path}: {exc}")
        return None


def _validate_repository_input(
    repo_root: pathlib.Path,
    relative: str,
    tracked: set[str],
    label: str,
    tracked_description: str,
) -> list[str]:
    if not _is_safe_repo_path(relative):
        return [f"{label}: unsafe repository-relative path: {relative!r}"]

    try:
        resolved_root = repo_root.resolve(strict=True)
    except OSError as exc:
        return [f"{label}: unable to resolve repository root {repo_root}: {exc}"]

    candidate = repo_root
    for part in pathlib.PurePosixPath(relative).parts:
        candidate /= part
        if candidate.is_symlink():
            return [f"{label}: symlink input is forbidden: {relative}"]

    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        resolved = None

    errors: list[str] = []
    if resolved is not None and not resolved.is_relative_to(resolved_root):
        errors.append(f"{label}: resolved path escapes repository root: {relative}")
    if relative not in tracked or resolved is None or not candidate.is_file():
        errors.append(f"{label}: {tracked_description} is missing: {relative}")
    return errors


def _frontmatter_status(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    for line in lines[1:end]:
        match = re.fullmatch(r"status:\s*(\S+)\s*", line)
        if match:
            return match.group(1)
    return None


def _validate_tracked_contract_paths(
    repo_root: pathlib.Path,
    contract: dict[str, Any],
    tracked: set[str],
) -> list[str]:
    errors: list[str] = []
    declared = [
        ("audit index", contract["audit_index"]),
        ("canonical pack README", f"{contract['canonical_pack']}/README.md"),
        ("overview", contract["overview"]),
        ("task evidence", contract["task_evidence"]),
        ("2026-07-07 README", SUPERSEDED_2026_07_07_README.as_posix()),
    ]
    for label, relative in declared:
        errors.extend(
            _validate_repository_input(
                repo_root,
                relative,
                tracked,
                label,
                "required tracked path",
            )
        )

    for filename in sorted(EXPECTED_PACK_FILES):
        relative = f"{contract['canonical_pack']}/{filename}"
        errors.extend(
            _validate_repository_input(
                repo_root,
                relative,
                tracked,
                "canonical audit input",
                "required tracked canonical audit input",
            )
        )
    return errors


def _validate_lifecycle(repo_root: pathlib.Path, contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    index_text = _read_required(
        repo_root / contract["audit_index"], "audit index", errors
    )
    if index_text is not None:
        index_lines = set(index_text.splitlines())
        for heading in contract["required_index_headings"]:
            if heading not in index_lines:
                errors.append(f"audit index: required heading is missing: {heading}")

    canonical_readme = repo_root / contract["canonical_pack"] / "README.md"
    canonical_text = _read_required(canonical_readme, "canonical README", errors)
    if canonical_text is not None and _frontmatter_status(canonical_text) != "active":
        errors.append("canonical README: required frontmatter status: active")

    superseded_readme = repo_root / SUPERSEDED_2026_07_07_README
    superseded_text = _read_required(superseded_readme, "2026-07-07 README", errors)
    if (
        superseded_text is not None
        and _frontmatter_status(superseded_text) != "superseded"
    ):
        errors.append("2026-07-07 README: required frontmatter status: superseded")
    return errors


def _task_is_done(task_text: str, task_id: str) -> bool:
    pattern = re.compile(
        rf"^\|\s*{re.escape(task_id)}\s*\|.*\|\s*Done\s*\|\s*$",
        re.MULTILINE,
    )
    return bool(pattern.search(task_text))


def _validate_assertions(
    repo_root: pathlib.Path,
    contract: dict[str, Any],
    rows: dict[str, Any],
    tracked: set[str],
) -> list[str]:
    errors: list[str] = []
    task_text = _read_required(
        repo_root / contract["task_evidence"], "task evidence", errors
    )
    report_cache: dict[str, str | None] = {}

    for assertion in contract["assertions"]:
        criterion_id = assertion["criterion_id"]
        row = rows.get(criterion_id)
        if row is None:
            errors.append(f"{criterion_id}: criterion row is missing")
            continue

        expected_report = assertion["report"]
        report_errors = _validate_repository_input(
            repo_root,
            expected_report,
            tracked,
            criterion_id,
            "required tracked report",
        )
        errors.extend(report_errors)
        try:
            actual_report = row.report.relative_to(repo_root).as_posix()
        except ValueError:
            actual_report = row.report.as_posix()
        if actual_report != expected_report:
            errors.append(
                f"{criterion_id}: report mismatch; expected {expected_report}, found {actual_report}"
            )
        if row.raw_status != assertion["required_state"]:
            errors.append(
                f"{criterion_id}: required state {assertion['required_state']}; found {row.raw_status}"
            )

        for evidence_path in assertion["required_evidence_paths"]:
            errors.extend(
                _validate_repository_input(
                    repo_root,
                    evidence_path,
                    tracked,
                    criterion_id,
                    "required tracked evidence",
                )
            )

        if task_text is not None:
            for task_id in assertion["completed_task_ids"]:
                if not _task_is_done(task_text, task_id):
                    errors.append(
                        f"{criterion_id}: completed task {task_id} is missing or not Done"
                    )

        if not report_errors and expected_report not in report_cache:
            report_cache[expected_report] = _read_required(
                repo_root / expected_report, f"{criterion_id} report", errors
            )
        report_text = report_cache.get(expected_report)
        if report_text is not None:
            for phrase in assertion["forbidden_stale_phrases"]:
                if phrase in report_text:
                    errors.append(
                        f"{criterion_id}: forbidden stale phrase is present: {phrase!r}"
                    )

    return errors


def validate_semantics(
    repo_root: pathlib.Path = pathlib.Path("."),
    contract_path: pathlib.Path = DEFAULT_CONTRACT,
) -> SemanticValidationResult:
    repo_root = pathlib.Path(repo_root)
    contract_path = pathlib.Path(contract_path)
    if not _is_safe_repo_path(contract_path.as_posix()):
        raise AuditSemanticContractError(
            [f"semantic contract: unsafe repository-relative path: {contract_path}"]
        )

    tracked = _tracked_paths(repo_root)
    contract_errors = _validate_repository_input(
        repo_root,
        contract_path.as_posix(),
        tracked,
        "semantic contract",
        "required tracked contract",
    )
    if contract_errors:
        raise AuditSemanticContractError(contract_errors)

    contract = _load_contract(repo_root / contract_path)
    input_errors = _validate_tracked_contract_paths(repo_root, contract, tracked)
    for assertion in contract["assertions"]:
        input_errors.extend(
            _validate_repository_input(
                repo_root,
                assertion["report"],
                tracked,
                assertion["criterion_id"],
                "required tracked report",
            )
        )
        for evidence_path in assertion["required_evidence_paths"]:
            input_errors.extend(
                _validate_repository_input(
                    repo_root,
                    evidence_path,
                    tracked,
                    assertion["criterion_id"],
                    "required tracked evidence",
                )
            )
    if input_errors:
        raise AuditSemanticContractError(input_errors)

    try:
        criterion_contract = validate_pack(repo_root / contract["canonical_pack"])
    except AuditCriterionContractError as exc:
        raise AuditSemanticContractError(
            [f"audit criterion contract: {error}" for error in exc.errors]
        ) from exc
    except UnicodeError as exc:
        raise AuditSemanticContractError(
            [f"audit criterion contract: invalid UTF-8 input: {exc}"]
        ) from exc
    except OSError as exc:
        raise AuditSemanticContractError(
            [f"audit criterion contract: unable to read input: {exc}"]
        ) from exc
    rows = {row.criterion_id: row for row in criterion_contract.rows}
    errors = _validate_lifecycle(repo_root, contract)
    errors.extend(_validate_assertions(repo_root, contract, rows, tracked))
    if errors:
        raise AuditSemanticContractError(errors)
    return SemanticValidationResult(assertion_count=len(contract["assertions"]))


def main() -> int:
    try:
        result = validate_semantics()
    except AuditSemanticContractError as exc:
        for error in exc.errors:
            print(f"FAIL: {error}")
        return 1
    print(
        f"audit_semantic_freshness: PASS assertions={result.assertion_count} failures=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
