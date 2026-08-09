"""Stable document taxonomy checks with no filesystem side effects."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
import re


_YEAR_PART_PATTERN = re.compile(r"[0-9]{4}")
_DATE_PREFIX_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-")


@dataclass(frozen=True)
class TaxonomyFinding:
    """A deterministic stable-identity validation result."""

    code: str
    path: str
    message: str


def classify_path(
    path: PurePosixPath,
    profiles: Mapping[str, Mapping[str, object]],
) -> str | None:
    """Return the unique profile whose path glob matches ``path``.

    The caller owns the profile mapping and its ``path_globs`` entries. No
    match or an ambiguous match returns ``None``.
    """

    candidates: list[str] = []
    for artifact_type, profile in profiles.items():
        globs = profile.get("path_globs", ())
        if isinstance(globs, str):
            globs = (globs,)
        if not isinstance(globs, (tuple, list)):
            continue
        if any(path.match(str(pattern)) for pattern in globs):
            candidates.append(artifact_type)
    return candidates[0] if len(candidates) == 1 else None


def find_dated_identity_parts(path: PurePosixPath) -> tuple[str, ...]:
    """Return year partitions and date-prefixed path components in order."""

    return tuple(
        part
        for part in path.parts
        if _YEAR_PART_PATTERN.fullmatch(part)
        or _DATE_PREFIX_PATTERN.match(part)
    )


def _matches_path_identity(
    path: PurePosixPath,
    artifact_id: str,
    profile: Mapping[str, object],
) -> bool:
    """Return whether ``path`` carries direct or inherited profile identity."""

    path_identity = str(profile.get("path_identity", "direct"))
    if path_identity == "direct":
        return any(
            part == artifact_id or part.startswith(artifact_id + "-")
            for part in path.parts
        )
    if path_identity == "inherited":
        parent_id_pattern = str(profile.get("parent_id_pattern", ""))
        return bool(parent_id_pattern) and (
            re.compile(parent_id_pattern).fullmatch(path.parent.name) is not None
        )
    return False


def validate_stable_identity(
    path: PurePosixPath,
    metadata: Mapping[str, object],
    profiles: Mapping[str, Mapping[str, object]],
) -> list[TaxonomyFinding]:
    """Validate the metadata ID and stable identity represented by ``path``."""

    findings: list[TaxonomyFinding] = []
    artifact_type = str(metadata.get("artifact_type", ""))
    artifact_id = str(metadata.get("artifact_id", ""))
    profile = profiles.get(artifact_type)
    if profile is None:
        return [TaxonomyFinding("profile-missing", str(path), artifact_type)]

    id_pattern = str(profile["id_pattern"])
    if re.compile(id_pattern).fullmatch(artifact_id) is None:
        findings.append(
            TaxonomyFinding("artifact-id-invalid", str(path), artifact_id)
        )
    if not _matches_path_identity(path, artifact_id, profile):
        findings.append(
            TaxonomyFinding("path-id-mismatch", str(path), artifact_id)
        )
    for part in find_dated_identity_parts(path):
        findings.append(TaxonomyFinding("dated-path-identity", str(path), part))
    return findings
