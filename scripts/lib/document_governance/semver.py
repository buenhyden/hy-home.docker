"""The one SemVer 2.0.0 parser, comparator and version-change rule.

Every consumer (release publication, the document `version` check) imports this
module; none keeps its own copy. A value is `MAJOR.MINOR.PATCH` with an
optional `-prerelease` and `+build`, no `v` prefix and no leading zeros.
Precedence ignores build metadata and puts a prerelease below its release.
"""

from __future__ import annotations

import re

SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


class SemVerError(ValueError):
    """A value is not a complete SemVer 2.0 version without v prefix."""


class VersionChangeError(SemVerError):
    """A version change that is missing, unchanged or lower; `code` names which."""

    def __init__(self, code: str) -> None:
        super().__init__(
            {
                "version-missing": "version is missing",
                "version-unchanged": "version is unchanged in precedence",
                "version-downgrade": "version is a downgrade",
            }[code]
        )
        self.code = code


def is_semver(version: object) -> bool:
    return isinstance(version, str) and SEMVER.fullmatch(version) is not None


def parse_semver(version: object) -> tuple[tuple[int, ...], tuple[object, ...] | None]:
    """Return (core, prerelease) for SemVer precedence; build is dropped."""
    match = SEMVER.fullmatch(version) if isinstance(version, str) else None
    if match is None:
        raise SemVerError("not a complete SemVer 2.0 version without v prefix")
    core = tuple(int(part) for part in match.groups()[:3])
    pre = match.group(4)
    if pre is None:
        return core, None
    return core, tuple(
        (0, int(part)) if part.isdigit() else (1, part) for part in pre.split(".")
    )


def compare_semver(left: object, right: object) -> int:
    """Return -1, 0 or 1 by SemVer precedence; build metadata is ignored."""
    (a_core, a_pre), (b_core, b_pre) = parse_semver(left), parse_semver(right)
    if a_core != b_core:
        return -1 if a_core < b_core else 1
    if a_pre == b_pre:
        return 0
    if a_pre is None or b_pre is None:  # a prerelease precedes its release
        return 1 if a_pre is None else -1
    # Numeric identifiers precede alphanumeric; a longer equal prefix is higher.
    return -1 if a_pre < b_pre else 1


def version_change_code(old: object, new: object) -> str | None:
    """Classify a change of one object's version; None means it was raised.

    An empty side is `version-missing`; a non-empty value that is not SemVer
    raises `SemVerError`, because it is a malformed value, not a verdict.
    """
    if not old or not new:
        return "version-missing"
    order = compare_semver(old, new)
    if order == 0:
        return "version-unchanged"
    return "version-downgrade" if order > 0 else None


def check_version_change(old: object, new: object) -> None:
    """Refuse a missing, unchanged or lower version for the same object."""
    code = version_change_code(old, new)
    if code is not None:
        raise VersionChangeError(code)
