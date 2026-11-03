"""Active-stage occupancy: terminal documents and Stage 03 package membership."""

from __future__ import annotations

import functools
import pathlib
import subprocess
from collections.abc import Mapping
from typing import Any

from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    classify_path,
    load_registry,
    path_matches_pattern,
)

ACTIVE_STAGE_PREFIXES = (
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
    "docs/90.references/",
)
_STAGE_03_PREFIX = "docs/03.specs/"
_STAGE_98_PREFIX = "docs/98.archive/"
# Stage 98 holds no records (SPEC-0249); only its README describes the scheme.
_STAGE_98_ALLOWED = frozenset({"docs/98.archive/README.md"})
_STAGE_03_MEMBER_PROFILES = ("spec", "plan", "task")


@functools.lru_cache(maxsize=1)
def _code_registry() -> DocumentRegistry:
    # Package membership is the repository Registry's code-time contract, so a
    # fixture root that carries no Registry still reads it.
    return load_registry()


def _stage_03_package(relative: str) -> str | None:
    """Return the Stage 03 package a tracked path belongs to, read from Stage 99.

    Membership is the Registry's contract. Deriving it from a second path shape
    written here would split silently the day a pattern changes.
    """

    profiles = _code_registry().profiles
    for profile_id in _STAGE_03_MEMBER_PROFILES:
        if path_matches_pattern(relative, profiles[profile_id].get("path_pattern")):
            return "/".join(relative.split("/")[:3])
    return None


def validate_active_stage_occupancy(
    root: pathlib.Path, registry: DocumentRegistry | None = None
) -> tuple[str, ...]:
    """Judge Stage 03 packages and reject any Stage 98 file but its README."""
    from scripts.lib.document_governance.frontmatter import read_frontmatter_values
    from scripts.lib.document_governance.spec_packages import (
        SpecPackageError,
        _document_anchor_references,
        acceptance_criterion_numbers,
        disposition_entry_statuses,
        task_cancellation_findings,
    )

    root = pathlib.Path(root)
    tracked = subprocess.run(
        ["git", "ls-files", "docs"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.split()
    findings: list[str] = []
    members: dict[str, dict[str, Mapping[str, Any]]] = {}
    for relative in tracked:
        if relative.startswith(_STAGE_98_PREFIX) and relative not in _STAGE_98_ALLOWED:
            findings.append(f"{relative}: Stage 98 holds no records")
            continue
        if not relative.endswith(".md") or not relative.startswith(
            ACTIVE_STAGE_PREFIXES
        ):
            continue
        try:
            metadata = read_frontmatter_values(root / relative)
        except Exception:
            continue
        status = metadata.get("status")
        if not isinstance(status, str):
            continue
        package = (
            _stage_03_package(relative)
            if relative.startswith(_STAGE_03_PREFIX)
            else None
        )
        if package is None:
            standalone_registry = registry if registry is not None else _code_registry()
            profile = classify_path(relative, standalone_registry)
            if profile and status in disposition_entry_statuses(
                profile, standalone_registry
            ):
                findings.append(
                    f"{relative}: {status} document remains in an active stage"
                )
        else:
            members.setdefault(package, {})[relative] = metadata
    if not members:
        return tuple(findings)
    if registry is None:
        registry_path = root / "docs/99.templates/registry.json"
        registry = (
            load_registry(registry_path) if registry_path.is_file() else load_registry()
        )
    terminal = registry.lifecycle_terminal_statuses
    for package, package_members in sorted(members.items()):
        spec = package_members.get(f"{package}/spec.md", {})
        spec_status = spec.get("status")
        if spec_status in terminal["spec"] and spec_status != "completed":
            findings.extend(
                f"{relative}: package with a terminal Spec keeps no member in an active stage"
                for relative in sorted(package_members)
            )
            continue
        task_statuses = {
            metadata.get("artifact_id", ""): metadata["status"]
            for relative, metadata in package_members.items()
            if relative.startswith(f"{package}/tasks/")
        }
        for relative, metadata in sorted(package_members.items()):
            status = metadata["status"]
            kind = (
                "spec"
                if relative == f"{package}/spec.md"
                else ("plan" if relative == f"{package}/plan.md" else "task")
            )
            if kind == "spec":
                continue
            if kind == "plan":
                invalid = (
                    status != "completed"
                    if spec_status == "completed"
                    else status in terminal["plan"]
                )
            elif spec_status == "completed":
                invalid = status not in terminal["task"]
            else:
                invalid = status in terminal["task"] and status not in {
                    "completed",
                    "cancelled",
                }
            if invalid:
                findings.append(
                    f"{relative}: {status} member violates package occupancy"
                )
                continue
            if kind == "task" and status == "cancelled":
                try:
                    generation = int(registry.common.get("lifecycle_generation", 4))
                    heading = (
                        str(registry.common["spec_section"])
                        if generation >= 5
                        else str(
                            registry.common["spec_completion_evidence"]["spec_section"]
                        )
                    )
                    criteria = acceptance_criterion_numbers(
                        (root / package / "spec.md").read_text(encoding="utf-8"),
                        heading,
                    )
                    findings.extend(
                        f"{relative}: {finding}"
                        for finding in task_cancellation_findings(
                            metadata.get("artifact_id", ""),
                            metadata.get("cancellation"),
                            frozenset(criteria),
                            task_statuses,
                            generation=generation,
                            references=_document_anchor_references(
                                (root / relative).read_text(encoding="utf-8")
                            ),
                        )
                    )
                except (OSError, SpecPackageError) as error:
                    findings.append(
                        f"{relative}: cancellation criteria unavailable: {error}"
                    )
    return tuple(findings)


def run(root: pathlib.Path) -> int:
    """Print active-stage occupancy findings and return the exit code."""

    findings = validate_active_stage_occupancy(root)
    for detail in findings:
        print(f"active-stage-occupancy: {detail}")
    print(f"active stage occupancy: violations={len(findings)}")
    return 1 if findings else 0
