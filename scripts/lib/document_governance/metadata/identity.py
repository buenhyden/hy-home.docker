"""Tracked-source and monotonic document identity validation."""

from __future__ import annotations

import collections
import pathlib
import re
import subprocess
from collections.abc import Mapping, Sequence

import yaml

from scripts.lib.document_governance.frontmatter import (
    safe_load_unique as _safe_load_unique,
)
from scripts.lib.document_governance.identity_history import (
    IdentityHistoryError,
    validate_allocation_transition,
)
from scripts.lib.document_governance.registry import DocumentRegistry
from scripts.lib.document_governance.spec_packages import (
    SpecPackageError,
    resolve_lifecycle_base,
)
from scripts.lib.document_governance.metadata.heading import _machine_template_path
from scripts.lib.document_governance.metadata.profile import (
    TARGET_MARKDOWN_PREFIXES,
    Finding,
    ProfileError,
    Record,
)

def _run_git(
    root: pathlib.Path,
    args: Sequence[str],
    *,
    operation: str,
    text: bool = False,
) -> subprocess.CompletedProcess[bytes] | subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=text,
            check=False,
        )
    except OSError:
        raise ProfileError(
            f"cannot establish local Git snapshot: Git executable unavailable during {operation}"
        ) from None


def _decode_git_paths(output: bytes, operation: str) -> list[pathlib.Path]:
    try:
        return [pathlib.Path(item.decode("utf-8")) for item in output.split(b"\0") if item]
    except UnicodeDecodeError:
        raise ProfileError(
            f"cannot establish local Git snapshot: {operation} returned a non-UTF-8 path"
        ) from None


def _require_git_worktree(root: pathlib.Path) -> None:
    result = _run_git(
        root,
        ["rev-parse", "--is-inside-work-tree"],
        operation="Git worktree validation",
        text=True,
    )
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise ProfileError("cannot establish local Git snapshot: --root is not a Git worktree")


def _tracked_markdown(root: pathlib.Path, *, require_git: bool = False) -> list[pathlib.Path]:
    try:
        result = _run_git(
            root,
            ["ls-files", "-z", "--", "*.md"],
            operation="tracked Markdown discovery",
        )
    except ProfileError:
        if require_git:
            raise
        result = None
    if result is not None and result.returncode == 0:
        paths = _decode_git_paths(result.stdout, "tracked Markdown discovery")
    elif require_git:
        raise ProfileError("cannot establish local Git snapshot: tracked Markdown discovery failed")
    else:
        paths = [path.relative_to(root) for path in root.rglob("*.md") if path.is_file()]
    return sorted(
        {
            path
            for path in paths
            if path.as_posix().startswith(TARGET_MARKDOWN_PREFIXES)
            and (root / path).is_file()
        },
        key=lambda path: path.as_posix(),
    )


def _tracked_repository_markdown(root: pathlib.Path) -> list[pathlib.Path]:
    result = _run_git(
        root,
        ["ls-files", "-z", "--", "*.md"],
        operation="repository contract Markdown discovery",
    )
    if result.returncode != 0:
        raise ProfileError("cannot establish local Git snapshot: repository contract Markdown discovery failed")
    return sorted(
        {
            path
            for path in _decode_git_paths(result.stdout, "repository contract Markdown discovery")
            if (root / path).is_file()
        },
        key=lambda path: path.as_posix(),
    )


def _tracked_machine_templates(root: pathlib.Path) -> list[pathlib.Path]:
    result = _run_git(
        root,
        ["ls-files", "-z", "--", "docs/99.templates/templates/"],
        operation="machine template discovery",
    )
    if result.returncode != 0:
        raise ProfileError("cannot establish local Git snapshot: machine template discovery failed")
    return sorted(
        {
            path
            for path in _decode_git_paths(result.stdout, "machine template discovery")
            if _machine_template_path(path)
            and (root / path).is_file()
        },
        key=lambda path: path.as_posix(),
    )


def _registry_string_arrays(value: object, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], list[str]]]:
    arrays: list[tuple[tuple[str, ...], list[str]]] = []
    if isinstance(value, dict):
        for key, member in value.items():
            if isinstance(key, str):
                arrays.extend(_registry_string_arrays(member, (*path, key)))
    elif isinstance(value, list) and all(isinstance(member, str) for member in value):
        arrays.append((path, value))
    return arrays


def _fenced_yaml_string_arrays(text: str) -> list[tuple[tuple[str, ...], list[str]]]:
    arrays: list[tuple[tuple[str, ...], list[str]]] = []
    for match in re.finditer(r"(?ms)^```(?:yaml|yml)\s*\n(.*?)^```\s*$", text):
        try:
            loaded = _safe_load_unique(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(loaded, dict):
            arrays.extend(_registry_string_arrays(loaded))
    return arrays


_PRD_PATH = re.compile(r"docs/01\.requirements/prd-(?P<number>[0-9]{4})-[a-z0-9-]+\.md")
_SRS_PATH = re.compile(r"docs/01\.requirements/srs-(?P<number>[0-9]{4})-[a-z0-9-]+\.md")
_IFR_PATH = re.compile(r"docs/01\.requirements/interface-(?P<number>[0-9]{4})-[a-z0-9-]+\.md")
_LEVEL_TWO_SECTION = re.compile(
    r"(?ms)^## (?P<name>[^\n]+)\n(?P<body>.*?)(?=^## |\Z)"
)
_REQUIREMENT_LIST_PREFIX = r"[ \t]*(?:(?:[-*+]\s+)|(?:[0-9]+[.)]\s+))"
_REQUIREMENT_BOLD_ITEM = re.compile(
    rf"^{_REQUIREMENT_LIST_PREFIX}\*\*(?P<label>[^*]+)\*\*:"
)
_REQUIREMENT_LIST_ITEM = re.compile(rf"^{_REQUIREMENT_LIST_PREFIX}\S")
_REQUIREMENT_TABLE_ITEM = re.compile(r"^\s*\|\s*(?P<label>[^|]+?)\s*\|")
_REQUIREMENT_INTERNAL_TOKEN = re.compile(
    r"(?<![A-Z0-9-])(?P<identity>"
    r"(?:PRD|SRS|IFR)-[A-Z0-9]+-[A-Z]+[A-Z0-9]+"
    r"|(?:REQ|VAL|FR|NFR)-[A-Z0-9]+(?:-[A-Z0-9]+)+"
    r")(?![A-Z0-9-])",
    re.IGNORECASE,
)
_REQUIREMENT_CANONICAL_INTERNAL = re.compile(
    r"(?P<owner>(?P<prefix>PRD|SRS|IFR)-[0-9]{4})-"
    r"(?P<kind>R|AC)[0-9]{4}"
)
_REQUIREMENT_INTERNAL_CONTRACTS = (
    (
        _PRD_PATH,
        "PRD",
        {
            "Requirements": "R",
            "Non-functional Requirements": "R",
            "Acceptance and Verification": "AC",
        },
        ("R", "AC"),
    ),
    (
        _SRS_PATH,
        "SRS",
        {"System Behavior": "R", "Quality Requirements": "R"},
        ("R",),
    ),
    (
        _IFR_PATH,
        "IFR",
        {
            "Information Semantics": "R",
            "Constraints and Compatibility": "R",
            "Failure Expectations": "R",
        },
        ("R",),
    ),
)


def validate_prd_internal_id_contract(
    path: pathlib.Path,
    text: str,
) -> list[Finding]:
    """Validate current PRD requirement/acceptance IDs against their owner."""

    if _PRD_PATH.fullmatch(path.as_posix()) is None:
        return []
    return validate_requirement_internal_id_contract(path, text)


def validate_requirement_internal_id_contract(
    path: pathlib.Path,
    text: str,
) -> list[Finding]:
    """Validate typed requirement IDs and references across Stage 01 roles."""

    path_text = path.as_posix()
    selected: tuple[
        re.Pattern[str], str, Mapping[str, str], Sequence[str]
    ] | None = None
    match: re.Match[str] | None = None
    for candidate in _REQUIREMENT_INTERNAL_CONTRACTS:
        candidate_match = candidate[0].fullmatch(path_text)
        if candidate_match is not None:
            selected = candidate
            match = candidate_match
            break
    if selected is None or match is None:
        return []
    _, prefix, section_kinds, required_kinds = selected
    owner = f"{prefix}-{match.group('number')}"
    counters = {kind: 0 for kind in required_kinds}
    declared_counts: collections.Counter[str] = collections.Counter()
    findings: list[Finding] = []
    for section in _LEVEL_TWO_SECTION.finditer(text):
        section_name = section.group("name")
        kind = section_kinds.get(section_name)
        if kind is None:
            continue
        for line_number, line in enumerate(section.group("body").splitlines(), start=1):
            identity: str | None = None
            bold = _REQUIREMENT_BOLD_ITEM.match(line)
            if bold is not None:
                identity = bold.group("label").split(" —", 1)[0].strip()
            else:
                table = _REQUIREMENT_TABLE_ITEM.match(line)
                if table is not None:
                    candidate = table.group("label").strip()
                    if candidate != "ID" and re.fullmatch(r"-+", candidate) is None:
                        identity = candidate
                elif _REQUIREMENT_LIST_ITEM.match(line):
                    findings.append(
                        Finding(
                            path_text,
                            "internal-id-missing",
                            f"{section_name} item {line_number} requires a typed ID",
                        )
                    )
                    continue
            if identity is None:
                continue
            declared_counts[identity] += 1
            if declared_counts[identity] > 1:
                findings.append(
                    Finding(
                        path_text,
                        "internal-id-duplicate",
                        f"{section_name} item {line_number} repeats a typed ID",
                    )
                )
            counters[kind] += 1
            expected = f"{owner}-{kind}{counters[kind]:04d}"
            if identity != expected:
                findings.append(
                    Finding(
                        path_text,
                        "internal-id-invalid",
                        f"{section_name} item {line_number} must use {expected}",
                    )
                )
    token_counts = collections.Counter(
        token.group("identity")
        for token in _REQUIREMENT_INTERNAL_TOKEN.finditer(text)
    )
    for identity in sorted(token_counts):
        canonical = _REQUIREMENT_CANONICAL_INTERNAL.fullmatch(identity)
        if identity.upper().startswith(("REQ-", "VAL-", "FR-", "NFR-")):
            findings.append(
                Finding(
                    path_text,
                    "internal-id-legacy",
                    "current requirement document contains a retired internal-ID namespace",
                )
            )
            continue
        allowed_kind = canonical is not None and (
            prefix == "PRD" or canonical.group("kind") == "R"
        )
        if (
            canonical is None
            or canonical.group("owner") != owner
            or not allowed_kind
        ):
            findings.append(
                Finding(
                    path_text,
                    "internal-id-invalid",
                    "current requirement document contains a malformed or foreign internal ID",
                )
            )
            continue
        if declared_counts[identity] != 1:
            findings.append(
                Finding(
                    path_text,
                    "internal-id-extra",
                    "typed requirement IDs require exactly one canonical declaration",
                )
            )
    for kind in required_kinds:
        label = "acceptance" if kind == "AC" else "requirement"
        if counters[kind] == 0:
            findings.append(
                Finding(
                    path_text,
                    "internal-id-missing",
                    f"current requirement document must declare at least one typed {label} ID",
                )
            )
    return sorted(set(findings))


def _reference_delegation_findings(root: pathlib.Path, profiles: dict[str, object]) -> list[Finding]:
    registry = profiles.get("_registry")
    if not isinstance(registry, DocumentRegistry) or not (root / "docs/90.references").exists():
        return []
    from scripts.lib.document_governance.references import delegated_member_paths, generated_reference_owners, validate_current_references

    rule = {"kind": "delegate-reference-members", "owner": "scripts/lib/document_governance/references.py"}
    if rule not in registry.profiles["readme"].get("exceptions", ()):
        raise ProfileError("Reference member delegation is not registered")
    try:
        profiles["common"]["generated_outputs"] = generated_reference_owners(root)
        findings = validate_current_references(root)
        profiles["_delegated_reference_paths"] = delegated_member_paths(root)
    except ValueError as error:
        raise ProfileError(f"Reference delegation cannot be established: {error}") from error
    return [Finding(item.path.as_posix(), item.code, item.detail) for item in findings]


def _allocation_findings(root: pathlib.Path, profiles: dict[str, object], records: Sequence[Record], base_ref: str | None) -> list[Finding]:
    registry = profiles.get("_registry")
    if not isinstance(registry, DocumentRegistry):
        return []
    try:
        base = resolve_lifecycle_base(root, base_ref)
        findings = validate_allocation_transition(root, registry, {
            record.path.as_posix(): record.metadata["artifact_id"]
            for record in records
            if isinstance(record.metadata.get("artifact_id"), str)
            and record.path.as_posix() not in profiles.get("_delegated_reference_paths", ())
        }, base)
    except (IdentityHistoryError, SpecPackageError) as error:
        raise ProfileError(str(error)) from error
    return [Finding(item.path, item.code, item.message) for item in findings]
