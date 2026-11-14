"""Content `version` downgrade check against the merge-base blob of the same path."""

from __future__ import annotations

import pathlib
import re
from collections.abc import Mapping

from scripts.lib.document_governance.metadata.lifecycle import _metadata_at_ref
from scripts.lib.document_governance.metadata.profile import Finding, Record, _finding

# Private copy of the pure SemVer 2.0 comparator in scripts/operations/release.py,
# the reference implementation: lib modules are import-only and never import an
# operations entrypoint. A lib test keeps the two in agreement.
_SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


def _parse(version: object) -> tuple[tuple[int, ...], tuple[object, ...] | None] | None:
    match = _SEMVER.fullmatch(version) if isinstance(version, str) else None
    if match is None:
        return None
    pre = match.group(4)
    return tuple(int(part) for part in match.groups()[:3]), (
        None
        if pre is None
        else tuple(
            (0, int(part)) if part.isdigit() else (1, part) for part in pre.split(".")
        )
    )


def compare_semver(left: str, right: str) -> int:
    """Return -1, 0 or 1 by SemVer precedence; raise ValueError when malformed."""
    a, b = _parse(left), _parse(right)
    if a is None or b is None:
        raise ValueError("not a complete SemVer 2.0 version without v prefix")
    (a_core, a_pre), (b_core, b_pre) = a, b
    if a_core != b_core:
        return -1 if a_core < b_core else 1
    if a_pre == b_pre:
        return 0
    if a_pre is None or b_pre is None:  # a prerelease precedes its release
        return 1 if a_pre is None else -1
    return -1 if a_pre < b_pre else 1


def version_downgrade_findings(
    root: pathlib.Path,
    records: Mapping[str, Record],
    base_ref: str | None,
    profiles: Mapping[str, object] | None = None,
) -> list[Finding]:
    """Flag a changed record whose `version` precedes its same-path base version.

    A new document, an absent or non-SemVer version on either side, and any path
    Git does not show at the base are not compared: a rename is never guessed.
    """

    findings: list[Finding] = []
    if not base_ref:
        return findings
    for record in records.values():
        head = record.metadata.get("version")
        base = (_metadata_at_ref(root, record.path, base_ref, profiles) or {}).get(
            "version"
        )
        if _parse(head) is None or _parse(base) is None:
            continue
        if compare_semver(head, base) < 0:
            findings.append(
                _finding(
                    record,
                    "version-downgrade",
                    f"version {head} has lower SemVer precedence than {base} at "
                    "the merge base; raise it or restore the base version",
                )
            )
    return findings
