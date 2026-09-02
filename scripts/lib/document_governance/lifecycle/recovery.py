"""Minimal Stage 98 recovery-reference validation."""

from __future__ import annotations

import pathlib

from scripts.lib.document_governance import archive as archive_authority


def run(root: pathlib.Path) -> int:
    """Validate only the archive recovery rows owned by the recovery mode."""

    inventory = archive_authority.load_archive(root / "docs/98.archive")
    decisions = archive_authority.load_task10_preservation_decisions(root)
    recovery_rows = archive_authority.load_task10_recovery_references(root)
    findings = archive_authority.validate_recovery_rows(recovery_rows, root)
    for finding in findings:
        print(
            f"{finding.code}: {finding.path}: "
            "validation rule is not satisfied"
        )
    violations = len(findings)
    print(
        "archive recovery: "
        f"migrations={len(inventory.migrations)} "
        f"tombstones={len(inventory.tombstones)} "
        f"decisions={len(decisions)} "
        f"recovery_rows={len(recovery_rows)} violations={violations}"
    )
    return 1 if violations else 0
