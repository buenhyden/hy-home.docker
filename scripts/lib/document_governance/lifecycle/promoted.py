"""Validate the one preserved promoted-manifest evidence package."""

from __future__ import annotations

import pathlib

from scripts.lib.document_governance import archive as archive_authority
from scripts.lib.document_governance.git_provenance import HistoricalDocument
from scripts.lib.document_governance.lifecycle.contract import (
    Finding,
    ProfileError,
    _finding,
    _load_migration_manifest_text,
    _read_regular_repo_bytes,
)


def _historical_promoted_findings(root: pathlib.Path) -> list[Finding]:
    """Compare DATA-0067 with its exact approved recovery blob."""

    migration = archive_authority._migration_document(root)
    selected = [
        row for row in migration["rows"] if row.get("artifact_id") == "DATA-0067"
    ]
    if len(selected) != 1:
        raise ProfileError("promoted historical evidence mapping is incomplete")

    row = selected[0]
    recovery = row["recovery_commit"] or migration["baseline_commit"]
    expected = HistoricalDocument(
        root, recovery, row["source_path"]
    ).read_bytes()
    _load_migration_manifest_text(expected.decode("utf-8"))
    observed = _read_regular_repo_bytes(
        root, row["target_path"], require_tracked=True
    )
    if observed == expected:
        return []
    return [
        _finding(
            row["target_path"],
            "historical-manifest-drift",
            "historical evidence differs from its verified recovery blob",
        )
    ]
