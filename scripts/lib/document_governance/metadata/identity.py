"""Tracked-source and monotonic document identity validation."""

from __future__ import annotations

import pathlib
import re
import subprocess
from collections.abc import Sequence

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
        return [
            pathlib.Path(item.decode("utf-8")) for item in output.split(b"\0") if item
        ]
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
        raise ProfileError(
            "cannot establish local Git snapshot: --root is not a Git worktree"
        )


def _tracked_markdown(
    root: pathlib.Path, *, require_git: bool = False
) -> list[pathlib.Path]:
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
        raise ProfileError(
            "cannot establish local Git snapshot: tracked Markdown discovery failed"
        )
    else:
        paths = [
            path.relative_to(root) for path in root.rglob("*.md") if path.is_file()
        ]
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
        raise ProfileError(
            "cannot establish local Git snapshot: repository contract Markdown discovery failed"
        )
    return sorted(
        {
            path
            for path in _decode_git_paths(
                result.stdout, "repository contract Markdown discovery"
            )
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
        raise ProfileError(
            "cannot establish local Git snapshot: machine template discovery failed"
        )
    return sorted(
        {
            path
            for path in _decode_git_paths(result.stdout, "machine template discovery")
            if _machine_template_path(path) and (root / path).is_file()
        },
        key=lambda path: path.as_posix(),
    )


def _registry_string_arrays(
    value: object, path: tuple[str, ...] = ()
) -> list[tuple[tuple[str, ...], list[str]]]:
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


def _reference_delegation_findings(
    root: pathlib.Path, profiles: dict[str, object]
) -> list[Finding]:
    registry = profiles.get("_registry")
    if (
        not isinstance(registry, DocumentRegistry)
        or not (root / "docs/90.references").exists()
    ):
        return []
    from scripts.lib.document_governance.references import (
        delegated_member_paths,
        generated_reference_owners,
        validate_current_references,
    )

    rule = {
        "kind": "delegate-reference-members",
        "owner": "scripts/lib/document_governance/references.py",
    }
    if rule not in registry.profiles["readme"].get("exceptions", ()):
        raise ProfileError("Reference member delegation is not registered")
    try:
        profiles["common"]["generated_outputs"] = generated_reference_owners(root)
        findings = validate_current_references(root)
        profiles["_delegated_reference_paths"] = delegated_member_paths(root)
    except ValueError as error:
        raise ProfileError(
            f"Reference delegation cannot be established: {error}"
        ) from error
    return [Finding(item.path.as_posix(), item.code, item.detail) for item in findings]


def _allocation_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    records: Sequence[Record],
    base_ref: str | None,
) -> list[Finding]:
    registry = profiles.get("_registry")
    if not isinstance(registry, DocumentRegistry):
        return []
    try:
        base = resolve_lifecycle_base(root, base_ref)
        findings = validate_allocation_transition(
            root,
            registry,
            {
                record.path.as_posix(): record.metadata["artifact_id"]
                for record in records
                if isinstance(record.metadata.get("artifact_id"), str)
                and record.path.as_posix()
                not in profiles.get("_delegated_reference_paths", ())
            },
            base,
            recovery_evidence={
                record.path.as_posix(): record.metadata["identity_recovery"]
                for record in records
                if "identity_recovery" in record.metadata
            },
            decision_evidence={
                record.path.as_posix(): record.metadata["identity_recovery_decisions"]
                for record in records
                if "identity_recovery_decisions" in record.metadata
            },
        )
    except (IdentityHistoryError, SpecPackageError) as error:
        raise ProfileError(str(error)) from error
    return [Finding(item.path, item.code, item.message) for item in findings]
