"""Stable document taxonomy checks with no filesystem side effects."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
import re


_YEAR_PART_PATTERN = re.compile(r"[0-9]{4}")
_DATE_PREFIX_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-")
_INCIDENT_YEAR_PATTERN = re.compile(r"[0-9]{4}")
_INCIDENT_PACKET_PATTERN = re.compile(r"inc-[0-9]{4}-[a-z0-9][a-z0-9-]*")
_INTERNAL_REQUIREMENT_ID_PATTERN = re.compile(
    r"(?:PRD-[0-9]{4}-(?:R|AC)[0-9]{4}|(?:SRS|IFR)-[0-9]{4}-R[0-9]{4})"
)


@dataclass(frozen=True)
class TaxonomyFinding:
    """A deterministic stable-identity validation result."""

    code: str
    path: str
    message: str


def is_valid_internal_requirement_id(value: str) -> bool:
    """Return whether ``value`` uses the canonical typed internal ID shape."""

    return _INTERNAL_REQUIREMENT_ID_PATTERN.fullmatch(value) is not None


def is_valid_incident_path(path: PurePosixPath) -> bool:
    """Return whether ``path`` is one fixed-role file in a canonical packet."""

    parts = path.parts
    return (
        len(parts) == 6
        and parts[:3] == ("docs", "05.operations", "incidents")
        and _INCIDENT_YEAR_PATTERN.fullmatch(parts[3]) is not None
        and _INCIDENT_PACKET_PATTERN.fullmatch(parts[4]) is not None
        and parts[5] in {"incident.md", "postmortem.md"}
    )


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
        parent_id_pattern = profile.get("parent_id_pattern")
        artifact_id_identity_pattern = profile.get("artifact_id_identity_pattern")
        identity_capture = profile.get("identity_capture")
        if (
            not isinstance(parent_id_pattern, str)
            or not isinstance(artifact_id_identity_pattern, str)
            or not isinstance(identity_capture, str)
        ):
            return False
        parent_match = re.compile(parent_id_pattern).fullmatch(path.parent.name)
        artifact_match = re.compile(artifact_id_identity_pattern).fullmatch(
            artifact_id
        )
        if parent_match is None or artifact_match is None:
            return False
        try:
            return (
                parent_match.group(identity_capture)
                == artifact_match.group(identity_capture)
            )
        except IndexError:
            return False
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
    incident_role = artifact_type in {"incident", "postmortem"}
    role_filename_valid = (
        artifact_type == "incident" and path.name == "incident.md"
    ) or (
        artifact_type == "postmortem" and path.name == "postmortem.md"
    )
    valid_incident_route = (
        incident_role and role_filename_valid and is_valid_incident_path(path)
    )
    if incident_role and not valid_incident_route:
        findings.append(
            TaxonomyFinding(
                "incident-path-invalid",
                str(path),
                "incident and postmortem files require docs/05.operations/incidents/"
                "<year>/inc-####-<slug>/<role>.md",
            )
        )
    dated_parts = () if valid_incident_route else find_dated_identity_parts(path)
    for part in dated_parts:
        findings.append(TaxonomyFinding("dated-path-identity", str(path), part))
    return findings
