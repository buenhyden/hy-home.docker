"""Content `version` change check against the merge-base blob of the same path."""

from __future__ import annotations

import json
import pathlib
import re
import tomllib
from collections.abc import Mapping

from scripts.lib.document_governance import semver
from scripts.lib.document_governance.metadata.lifecycle import (
    _metadata_at_ref,
    _text_at_ref,
)
from scripts.lib.document_governance.metadata.profile import Finding, Record, _finding

# Lifecycle state and review dates are independent of the content version
# (documentation protocol, Version objects): an edit confined to them is no
# content change.
_LIFECYCLE_KEY = re.compile(r"(?:status|updated|reviewed_at|next_review_at):")


def _without_lifecycle_keys(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return text
    kept, in_frontmatter = [lines[0]], True
    for line in lines[1:]:
        if in_frontmatter and line.rstrip() == "---":
            in_frontmatter = False
        elif in_frontmatter and _LIFECYCLE_KEY.match(line):
            continue
        kept.append(line)
    return "".join(kept)


def _content_changed(root: pathlib.Path, record: Record, base_ref: str) -> bool:
    base_text = _text_at_ref(root, record.path, base_ref)
    try:
        head_text = (root / record.path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False  # An unreadable body is reported by the body checks.
    return base_text is None or _without_lifecycle_keys(
        base_text
    ) != _without_lifecycle_keys(head_text)


def version_change_findings(
    root: pathlib.Path,
    records: Mapping[str, Record],
    base_ref: str | None,
    profiles: Mapping[str, object] | None = None,
) -> list[Finding]:
    """Flag a changed record whose `version` is unchanged or lower than its base.

    The rule is `semver.version_change_code`, the one every consumer shares.
    A new document, an absent or non-SemVer version on either side, and any path
    Git does not show at the base are not compared: a rename is never guessed.
    A path whose content, apart from lifecycle keys, is the base content is not
    a change, so only a lower version is reported for it.
    """

    findings: list[Finding] = []
    if not base_ref:
        return findings
    for record in records.values():
        head = record.metadata.get("version")
        base = (_metadata_at_ref(root, record.path, base_ref, profiles) or {}).get(
            "version"
        )
        if not (semver.is_semver(head) and semver.is_semver(base)):
            continue
        code = semver.version_change_code(base, head)
        if code == "version-unchanged":
            if not _content_changed(root, record, base_ref):
                continue
            message = (
                f"version {head} has the same SemVer precedence as {base} at "
                "the merge base although the document changed; raise it"
            )
        elif code == "version-downgrade":
            message = (
                f"version {head} has lower SemVer precedence than {base} at "
                "the merge base; raise it or restore the base version"
            )
        else:
            continue
        findings.append(_finding(record, code, message))
    return findings


# The inventoried product version files (documentation protocol, Version
# objects). A product releases on its own cadence, so only its `version` field
# is checked, never whether other edits to the file need a new version.
PRODUCT_VERSION_FILES = (
    "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/nodes/"
    "OpsflowSmtp/package.json",
    "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/pyproject.toml",
    "projects/storybook/nextjs/package.json",
    "projects/storybook/nextjs/packages/ui/package.json",
)


def _product_version(text: str | None, path: str) -> tuple[bool, object]:
    """Return (parsed, version); a missing text or an unparsable file is not parsed."""
    if text is None:
        return False, None
    try:
        if path.endswith(".toml"):
            return True, tomllib.loads(text).get("project", {}).get("version")
        values = json.loads(text)
    except (ValueError, AttributeError):
        return False, None
    return isinstance(values, dict), values.get("version") if isinstance(
        values, dict
    ) else None


def product_version_findings(root: pathlib.Path, base_ref: str | None) -> list[Finding]:
    """Flag a changed product `version` that is malformed or lower than its base.

    Only a version value that differs from the merge-base value is judged; an
    unchanged value with other edits is allowed. A new, deleted or unparsable
    file is not compared.
    """

    findings: list[Finding] = []
    if not base_ref:
        return findings
    for path in PRODUCT_VERSION_FILES:
        try:
            head_text = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        base_ok, base = _product_version(
            _text_at_ref(root, pathlib.Path(path), base_ref), path
        )
        head_ok, head = _product_version(head_text, path)
        if not (base_ok and head_ok) or not semver.is_semver(base) or head == base:
            continue
        if not semver.is_semver(head):
            findings.append(
                Finding(
                    path,
                    "version-malformed",
                    f"version {head!r} is not a complete SemVer 2.0 version "
                    "without v prefix",
                )
            )
        elif semver.version_change_code(base, head) == "version-downgrade":
            findings.append(
                Finding(
                    path,
                    "version-downgrade",
                    f"version {head} has lower SemVer precedence than {base} at "
                    "the merge base; raise it or restore the base version",
                )
            )
    return findings
