"""Content `version` change check against the merge-base blob of the same path."""

from __future__ import annotations

import json
import pathlib
import tomllib
from collections.abc import Mapping

from scripts.lib.document_governance import semver
from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.metadata.lifecycle import (
    _metadata_at_ref,
    _text_at_ref,
)
from scripts.lib.document_governance.metadata.profile import Finding, Record, _finding

# Lifecycle state and review dates are independent of the content version
# (documentation protocol, Version objects): an edit confined to them is no
# content change.
_LIFECYCLE_KEYS = frozenset(
    {
        "status",
        "lifecycle",
        "document_lifecycle",
        "updated",
        "reviewed_at",
        "next_review_at",
    }
)


def _typed_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _typed_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return tuple(map(_typed_value, value))
    if isinstance(value, frozenset):
        return frozenset(map(_typed_value, value))
    # YAML scalars such as 1 and 1.0 can compare equal in Python.
    return type(value), value


def _versioned_content(path: pathlib.Path, text: str) -> tuple[dict[str, object], str]:
    document = frontmatter_record_from_text(path, text)
    return {
        key: _typed_value(value)
        for key, value in document.metadata.items()
        if key not in _LIFECYCLE_KEYS
    }, document.body


def _content_changed(
    root: pathlib.Path, record: Record, base_ref: str, base_text: str | None
) -> bool:
    if base_text is None:
        base_text = _text_at_ref(root, record.path, base_ref)
    try:
        head_text = (root / record.path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False  # An unreadable body is reported by the body checks.
    if base_text is None or base_text == head_text:
        return base_text is None
    try:
        return _versioned_content(record.path, base_text) != _versioned_content(
            record.path, head_text
        )
    except FrontmatterError:
        return True  # The raw text changed and the parser reports its own finding.


def version_change_findings(
    root: pathlib.Path,
    records: Mapping[str, Record],
    base_ref: str | None,
    profiles: Mapping[str, object] | None = None,
    *,
    base_texts: Mapping[str, str] | None = None,
) -> list[Finding]:
    """Flag a changed record whose `version` is unchanged or lower than its base.

    The rule is `semver.version_change_code`, the one every consumer shares.
    The current document must use a numeric version. The merge base may use
    the full SemVer admitted by earlier schemas. New paths are not compared.
    A path whose content, apart from lifecycle keys, is the base content is not
    a change, so only a lower version is reported for it.
    """

    findings: list[Finding] = []
    if not base_ref:
        return findings
    for record in records.values():
        head = record.metadata.get("version")
        base_text = (base_texts or {}).get(record.path.as_posix())
        base = (
            _metadata_at_ref(
                root, record.path, base_ref, profiles, known_text=base_text
            )
            or {}
        ).get("version")
        if not (semver.is_numeric_version(head) and semver.is_semver(base)):
            continue
        code = semver.version_change_code(base, head)
        if code == "version-unchanged":
            # A template source stays at the registered initial version
            # (`invalid-template-version`), so its edits never need a raise.
            # Template drift is caught by that pin, the Registry and template
            # tests and the protected-surface review of `docs/99.templates/**`.
            if record.artifact_type == "template-source" or not _content_changed(
                root, record, base_ref, base_text
            ):
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
            old_core, _ = semver.parse_semver(base)
            new_core, _ = semver.parse_semver(head)
            if new_core[0] > old_core[0] and any(new_core[1:]):
                code = "version-major-reset"
                message = "a document MAJOR increase resets MINOR and PATCH to zero"
            elif (
                new_core[:1] == old_core[:1]
                and new_core[1] > old_core[1]
                and new_core[2]
            ):
                code = "version-minor-reset"
                message = "a document MINOR increase resets PATCH to zero"
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
