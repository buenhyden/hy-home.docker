"""Minimal Stage 98 recovery-reference validation."""

from __future__ import annotations

import pathlib

from scripts.lib.document_governance import archive as archive_authority
from scripts.lib.document_governance.registry import PRESERVED_DISPOSITIONS


def run(root: pathlib.Path, base: str | None = None) -> int:
    """Validate only the archive recovery rows owned by the recovery mode.

    ``base`` is the lifecycle comparison commit. The Retention Catalog rules
    use it to find the preserved records a change adds.
    """

    try:
        inventory = archive_authority.load_archive(root / "docs/98.archive")
    except ValueError as error:
        # A contract violation is a finding, not an internal error. The caller's
        # bare `except Exception` reported it as "lifecycle operation failed
        # safely", which is true and useless: the operator learned nothing about
        # which archive document broke its contract.
        path = getattr(error, "path", "docs/98.archive")
        print(f"archive-contract-invalid: {path}: validation rule is not satisfied")
        print(
            "archive recovery: migrations=0 tombstones=0 decisions=0 "
            "recovery_rows=0 violations=1"
        )
        return 1
    decisions = archive_authority.load_task10_preservation_decisions(root)
    recovery_rows = archive_authority.load_task10_recovery_references(root)
    findings = archive_authority.validate_recovery_rows(recovery_rows, root)
    for finding in findings:
        print(f"{finding.code}: {finding.path}: validation rule is not satisfied")
    # A record of a decision and a preserved body are different things, and the
    # index says so in prose. This is what keeps them from being conflated.
    boundary = archive_authority.validate_preservation_boundary(
        root / "docs/98.archive"
    )
    for detail in boundary:
        print(f"archive-preservation-boundary: {detail}")
    # An active stage holds current work; a terminal document has left that
    # state and belongs under the subtree for its disposition.
    occupancy = archive_authority.validate_active_stage_occupancy(root)
    for detail in occupancy:
        print(f"active-stage-occupancy: {detail}")
    retention = archive_authority.validate_retention(root, base)
    for finding in retention:
        print(f"{finding.code}: {finding.path}: validation rule is not satisfied")
    violations = len(findings) + len(boundary) + len(occupancy) + len(retention)
    preserved = sum(
        1
        for disposition in PRESERVED_DISPOSITIONS
        for _ in (root / "docs/98.archive" / disposition).rglob("*.md")
        if (root / "docs/98.archive" / disposition).is_dir()
    )
    print(
        "archive recovery: "
        f"migrations={len(inventory.migrations)} "
        f"tombstones={len(inventory.tombstones)} "
        f"preserved={preserved} "
        f"decisions={len(decisions)} "
        f"recovery_rows={len(recovery_rows)} violations={violations}"
    )
    return 1 if violations else 0
