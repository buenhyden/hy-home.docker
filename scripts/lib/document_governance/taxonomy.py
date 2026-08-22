"""Stable document taxonomy checks with no filesystem side effects."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath
import re


_YEAR_PART_PATTERN = re.compile(r"[0-9]{4}")
_DATE_PREFIX_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-")
_INCIDENT_YEAR_PATTERN = re.compile(r"[0-9]{4}")
_INCIDENT_PACKET_PATTERN = re.compile(r"inc-[0-9]{4}-[a-z0-9][a-z0-9-]*")
_INTERNAL_REQUIREMENT_ID_PATTERN = re.compile(
    r"REQ-[0-9]{4}-(?:FR|NFR|IF)-[0-9]{4}"
)
_REQUIREMENT_PACKAGE_PATH_PATTERN = re.compile(
    r"docs/01\.requirements/(?P<number>[0-9]{4})-[a-z0-9][a-z0-9-]*\.md"
)
_REGISTERED_TOKEN_PATTERN = re.compile(
    r"\{(?:number|package_number|task_number|subject_number|year):4\}"
    r"|\{(?:slug|domain|stage)\}"
)
_REGISTERED_STAGES = (
    "00.agent-governance",
    "01.requirements",
    "02.architecture",
    "03.specs",
    "05.operations",
    "90.references",
    "98.archive",
    "99.templates",
)


def _segment_nfa(
    pattern: str,
) -> tuple[dict[int, list[tuple[frozenset[str] | None, int]]], int]:
    transitions: dict[int, list[tuple[frozenset[str] | None, int]]] = {}
    state = 0
    next_state = 1

    def edge(source: int, characters: frozenset[str] | None, target: int) -> None:
        transitions.setdefault(source, []).append((characters, target))

    def literal(source: int, value: str) -> int:
        nonlocal next_state
        for character in value:
            target = next_state
            next_state += 1
            edge(source, frozenset({character}), target)
            source = target
        return source

    cursor = 0
    digits = frozenset("0123456789")
    alphanumeric = frozenset("abcdefghijklmnopqrstuvwxyz0123456789")
    slug_characters = alphanumeric | frozenset("-")
    for match in _REGISTERED_TOKEN_PATTERN.finditer(pattern):
        state = literal(state, pattern[cursor : match.start()])
        token = match.group(0)
        if token.endswith(":4}"):
            for _ in range(4):
                target = next_state
                next_state += 1
                edge(state, digits, target)
                state = target
        elif token == "{stage}":
            target = next_state
            next_state += 1
            for stage in _REGISTERED_STAGES:
                branch = literal(state, stage)
                edge(branch, None, target)
            state = target
        else:
            target = next_state
            next_state += 1
            edge(state, alphanumeric, target)
            edge(target, slug_characters, target)
            state = target
        cursor = match.end()
    return transitions, literal(state, pattern[cursor:])


def _epsilon_closure(
    transitions: Mapping[int, Sequence[tuple[frozenset[str] | None, int]]],
    states: frozenset[int],
) -> frozenset[int]:
    closure = set(states)
    pending = list(states)
    while pending:
        state = pending.pop()
        for characters, target in transitions.get(state, ()):
            if characters is None and target not in closure:
                closure.add(target)
                pending.append(target)
    return frozenset(closure)


def _segment_patterns_overlap(left: str, right: str) -> bool:
    left_nfa, left_final = _segment_nfa(left)
    right_nfa, right_final = _segment_nfa(right)
    alphabet = sorted(
        {
            character
            for nfa in (left_nfa, right_nfa)
            for edges in nfa.values()
            for characters, _ in edges
            if characters is not None
            for character in characters
        }
    )
    start = (
        _epsilon_closure(left_nfa, frozenset({0})),
        _epsilon_closure(right_nfa, frozenset({0})),
    )
    pending = [start]
    visited = {start}
    while pending:
        left_states, right_states = pending.pop()
        if left_final in left_states and right_final in right_states:
            return True
        for character in alphabet:
            left_next = frozenset(
                target
                for state in left_states
                for characters, target in left_nfa.get(state, ())
                if characters is not None and character in characters
            )
            right_next = frozenset(
                target
                for state in right_states
                for characters, target in right_nfa.get(state, ())
                if characters is not None and character in characters
            )
            if not left_next or not right_next:
                continue
            pair = (
                _epsilon_closure(left_nfa, left_next),
                _epsilon_closure(right_nfa, right_next),
            )
            if pair not in visited:
                visited.add(pair)
                pending.append(pair)
    return False


def registered_path_patterns_overlap(left: str, right: str) -> bool:
    """Decide intersection for the complete registered path-pattern grammar."""

    left_segments = left.split("/")
    right_segments = right.split("/")
    return len(left_segments) == len(right_segments) and all(
        _segment_patterns_overlap(left_segment, right_segment)
        for left_segment, right_segment in zip(left_segments, right_segments)
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


def requirement_package_identity(path: PurePosixPath) -> str | None:
    """Return the package identity owned by a canonical Stage 01 path."""

    match = _REQUIREMENT_PACKAGE_PATH_PATTERN.fullmatch(path.as_posix())
    return None if match is None else f"REQ-{match.group('number')}"


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
    profiles: Mapping[str, Mapping[str, object]] | None = None,
) -> str | None:
    """Return the unique profile whose path glob matches ``path``.

    The caller owns the profile mapping and its ``path_globs`` entries. No
    match or an ambiguous match returns ``None``.
    """

    if profiles is None:
        from scripts.lib.document_governance.registry import classify_path as classify_registered_path

        return classify_registered_path(path)
    candidates: list[str] = []
    for artifact_type, profile in profiles.items():
        path_pattern = profile.get("path_pattern")
        if isinstance(path_pattern, str):
            from scripts.lib.document_governance.registry import _path_regex

            if _path_regex(path_pattern).fullmatch(path.as_posix()):
                candidates.append(artifact_type)
            continue
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

    id_pattern = profile.get("id_pattern")
    artifact_pattern = profile.get("artifact_id_pattern")
    valid_id = False
    if isinstance(id_pattern, str):
        valid_id = re.compile(id_pattern).fullmatch(artifact_id) is not None
    elif isinstance(artifact_pattern, str):
        from scripts.lib.document_governance.registry import _path_regex

        valid_id = _path_regex(artifact_pattern).fullmatch(artifact_id) is not None
    elif artifact_pattern is None:
        valid_id = not artifact_id
    if not valid_id:
        findings.append(
            TaxonomyFinding("artifact-id-invalid", str(path), artifact_id)
        )
    identity_relation = profile.get("identity_relation")
    path_matches = (
        identity_relation == "none"
        or (
            isinstance(profile.get("path_pattern"), str)
            and isinstance(artifact_pattern, str)
            and _numeric_identity_matches(
                path,
                artifact_id,
                str(profile["path_pattern"]),
                artifact_pattern,
                str(identity_relation),
            )
        )
        or _matches_path_identity(path, artifact_id, profile)
    )
    if not path_matches:
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


def _numeric_identity_matches(
    path: PurePosixPath,
    artifact_id: str,
    path_pattern: str,
    artifact_pattern: str,
    identity_relation: str,
) -> bool:
    path_match = _named_identity_pattern(path_pattern).fullmatch(path.as_posix())
    artifact_match = _named_identity_pattern(artifact_pattern).fullmatch(artifact_id)
    if path_match is None or artifact_match is None:
        return False
    if identity_relation == "subject-member":
        # The Operations migration manifest owns exact role-to-subject
        # membership. Registry validation establishes each identity shape
        # independently and must never equate their four-digit numbers.
        return "subject_number" in path_match.groupdict()
    required = "number" if identity_relation == "direct" else next(
        (
            token
            for token in ("package_number", "number")
            if token in path_match.groupdict()
            and token in artifact_match.groupdict()
        ),
        "",
    )
    return (
        required in path_match.groupdict()
        and required in artifact_match.groupdict()
        and path_match.group(required) == artifact_match.group(required)
        and all(
            path_match.group(name) == value
            for name, value in artifact_match.groupdict().items()
            if name in path_match.groupdict() and value is not None
        )
    )


_IDENTITY_TOKEN_PATTERN = re.compile(
    r"\{(number|package_number|task_number|subject_number|year):4\}"
    r"|\{(slug|domain|stage)\}"
)


def _named_identity_pattern(pattern: str) -> re.Pattern[str]:
    """Compile a registered path/ID pattern with exact numeric captures."""

    rendered: list[str] = ["^"]
    cursor = 0
    for match in _IDENTITY_TOKEN_PATTERN.finditer(pattern):
        rendered.append(re.escape(pattern[cursor : match.start()]))
        numeric_name, text_name = match.groups()
        if numeric_name is not None:
            rendered.append(fr"(?P<{numeric_name}>[0-9]{{4}})")
        elif text_name == "stage":
            rendered.append(
                r"(?:00\.agent-governance|01\.requirements|02\.architecture|"
                r"03\.specs|05\.operations|90\.references|98\.archive|99\.templates)"
            )
        else:
            rendered.append(r"[a-z0-9][a-z0-9-]*")
        cursor = match.end()
    rendered.append(re.escape(pattern[cursor:]))
    rendered.append("$")
    return re.compile("".join(rendered))
