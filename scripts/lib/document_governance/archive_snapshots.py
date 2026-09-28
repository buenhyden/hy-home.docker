"""Compare post-cutover captures on worktree, index, and committed Git surfaces."""

from __future__ import annotations

import json
import pathlib

from scripts.lib.document_governance.archive import (
    _ARCHIVE_PREFIX,
    _CATALOG_RECORD,
    MAX_ARCHIVE_BYTES,
    MAX_ARCHIVE_ENTRIES,
    ArchiveFinding,
    _catalog_members,
    _catalog_rows,
    _code_span,
    _identity_findings,
    _names_are_valid,
    _safe_path,
)
from scripts.lib.document_governance.git_provenance import (
    _run_git,
    recovery_commit_is_valid,
)
from scripts.lib.document_governance.registry import (
    PRESERVED_DISPOSITIONS,
    DocumentRegistry,
    _unique_object,
    load_registry,
    preserved_origin_path,
)


def _blob(root: pathlib.Path, object_name: str) -> bytes:
    result = _run_git(root, ["cat-file", "blob", object_name])
    if result.returncode or len(result.stdout) > MAX_ARCHIVE_BYTES:
        raise ValueError("missing or oversized blob")
    return result.stdout


def _legacy_records(root: pathlib.Path, registry: DocumentRegistry) -> frozenset[str]:
    contract = registry.common.get("archive_retention", {})
    revision = str(contract.get("legacy_capture_revision", ""))
    if not recovery_commit_is_valid(revision):
        raise ValueError("invalid legacy capture revision")
    # A pre-catalog fixture has no legacy captures. A missing commit is not that case.
    kind = _run_git(root, ["cat-file", "-t", revision])
    if kind.returncode or kind.stdout.strip() != b"commit":
        raise ValueError("legacy capture commit unavailable")
    if _run_git(root, ["merge-base", "--is-ancestor", revision, "HEAD"]).returncode:
        raise ValueError("legacy capture commit is outside current history")
    text = _catalog(root, revision)
    if text is None:
        # Before SPEC-0184 extraction, the same capture table lived in README.
        members = _git_members(root, revision, "docs/98.archive/README.md", False)
        if not members:
            return frozenset()
        text = members[""][1].decode("utf-8")
    rows, findings = _catalog_rows(text)
    if findings:
        raise ValueError("invalid legacy catalog")
    return frozenset(record for row in rows if (record := _code_span(row.record)))


def is_legacy_capture(
    root: pathlib.Path, unit: str, registry: DocumentRegistry | None = None
) -> bool:
    """Generation is fixed by the approved cutover, never a catalog-row flag."""
    registry = load_registry() if registry is None else registry
    return unit in _legacy_records(root, registry) or unit in registry.common.get(
        "archive_retention", {}
    ).get("legacy_transition_units", ())


def _git_members(root: pathlib.Path, surface: str, path: str, package: bool):
    args = (
        ["ls-files", "--stage", "-z", "--", path]
        if surface == "index"
        else ["ls-tree", "-r", "-z", surface, "--", path]
    )
    result = _run_git(root, args)
    if result.returncode:
        raise ValueError("Git tree unavailable")
    members = {}
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        parts = metadata.decode("ascii").split()
        mode, oid = (parts[0], parts[1]) if surface == "index" else (parts[0], parts[2])
        if mode not in {"100644", "100755"} or (surface == "index" and parts[2] != "0"):
            raise ValueError("symlink, gitlink, or unmerged entry")
        name = name.decode("utf-8")
        if name != path and not name.startswith(path + "/"):
            raise ValueError("tree member escapes unit")
        key = name[len(path) :].lstrip("/") if package else ""
        if key in members or (not package and name != path):
            raise ValueError("invalid unit member")
        members[key] = (mode, _blob(root, oid))
        if len(members) > MAX_ARCHIVE_ENTRIES:
            raise ValueError("too many unit members")
        if sum(len(data) for _, data in members.values()) > MAX_ARCHIVE_BYTES:
            raise ValueError("unit byte limit exceeded")
    return members


def _catalog(root: pathlib.Path, surface: str) -> str | None:
    if surface == "worktree":
        members = _catalog_members(root / _CATALOG_RECORD, False)
        return members[""][1].decode("utf-8") if members else None
    members = _git_members(root, surface, _CATALOG_RECORD, False)
    return members[""][1].decode("utf-8") if members else None


def _checkout_bytes(root: pathlib.Path, path: str, source: str, raw: bytes) -> bytes:
    # check-attr reads configuration only; neither it nor cat-file invokes filters.
    attrs = _run_git(
        root,
        [
            "check-attr",
            "-z",
            "filter",
            "working-tree-encoding",
            "eol",
            "text",
            "--",
            path,
            source,
        ],
    )
    if attrs.returncode:
        raise ValueError("attributes unavailable")
    values = attrs.stdout.decode("utf-8").split("\0")[:-1]
    attributes = {}
    for offset in range(0, len(values), 3):
        name, key, value = values[offset : offset + 3]
        attributes[(name, key)] = value
        if key in {"filter", "working-tree-encoding"} and value not in {
            "unspecified",
            "unset",
        }:
            raise ValueError("filter or working-tree-encoding is unsupported")
    eol = attributes.get((path, "eol"), "unspecified")
    text = attributes.get((path, "text"), "unspecified")
    autocrlf = _run_git(root, ["config", "--get", "core.autocrlf"]).stdout.strip()
    core_eol = _run_git(root, ["config", "--get", "core.eol"]).stdout.strip()
    crlf = eol == "crlf" or (
        eol == "unspecified"
        and (autocrlf == b"true" or (text in {"set", "auto"} and core_eol == b"crlf"))
    )
    if text != "unset" and crlf and b"\r\n" not in raw and b"\0" not in raw:
        return raw.replace(b"\n", b"\r\n")
    return raw


def _check_row(
    root,
    row,
    surface,
    legacy,
    transition,
    registry,
    assessment=None,
    names_registry=None,
):
    from scripts.lib.document_governance.archive_assessments import (
        preserved_payload_members,
    )

    record = _code_span(row.record)
    path = _ARCHIVE_PREFIX + (record or "")
    if (
        not record
        or _safe_path(record.rstrip("/")) is None
        or record.partition("/")[0] not in PRESERVED_DISPOSITIONS
    ):
        return [ArchiveFinding("catalog-record-invalid", path, surface)]
    owner_exists = (
        None
        if surface == "worktree"
        else lambda owner: bool(_git_members(root, surface, owner.as_posix(), False))
    )
    if not _names_are_valid(
        root, row.disposition, row.names, owner_exists, names_registry
    ):
        return [ArchiveFinding("catalog-names-invalid", path, surface)]
    if record in legacy:
        try:
            source = _git_members(
                root,
                registry.common["archive_retention"]["legacy_capture_revision"],
                path.rstrip("/"),
                record.endswith("/"),
            )
            preserved = (
                preserved_payload_members(root, record)
                if surface == "worktree"
                else _git_members(root, surface, path.rstrip("/"), record.endswith("/"))
            )
            return _compare_members(
                root,
                path,
                path.rstrip("/"),
                surface,
                source,
                preserved,
                assessment,
                registry,
            )
        except (OSError, ValueError, UnicodeError):
            return [ArchiveFinding("archive-exact-unsafe", path, surface)]
    commit, separator, origin = (_code_span(row.source) or "").partition(":")
    if (
        not separator
        or not recovery_commit_is_valid(commit)
        or _safe_path(origin) is None
        or origin != preserved_origin_path(path.rstrip("/"))
    ):
        return [ArchiveFinding("catalog-source-invalid", path, surface)]
    if record in transition:
        if commit != registry.common["archive_retention"]["legacy_capture_revision"]:
            return [ArchiveFinding("catalog-source-invalid", path, surface)]
        return _check_transition(
            root, path, record, commit, origin, surface, assessment, registry
        )
    if _run_git(root, ["merge-base", "--is-ancestor", commit, "HEAD"]).returncode:
        return [ArchiveFinding("catalog-source-commit-orphaned", path, surface)]
    kind = _run_git(root, ["cat-file", "-t", commit])
    if kind.returncode or kind.stdout.strip() != b"commit":
        return [ArchiveFinding("catalog-source-object-invalid", path, surface)]
    package = record.endswith("/")
    kind = _run_git(root, ["cat-file", "-t", f"{commit}:{origin}"])
    if kind.returncode or kind.stdout.strip() != (b"tree" if package else b"blob"):
        return [ArchiveFinding("catalog-source-object-invalid", path, surface)]
    try:
        source = _git_members(root, commit, origin, package)
        preserved = (
            preserved_payload_members(root, record)
            if surface == "worktree"
            else _git_members(root, surface, path.rstrip("/"), package)
        )
    except (OSError, ValueError, UnicodeError):
        return [ArchiveFinding("archive-exact-unsafe", path, surface)]
    return _compare_members(
        root, path, origin, surface, source, preserved, assessment, registry
    )


def _check_transition(
    root, path, record, commit, origin, surface, assessment, registry
):
    from scripts.lib.document_governance.archive_assessments import (
        preserved_payload_members,
    )

    package = record.endswith("/")
    unit = path.rstrip("/")
    # The one approved bootstrap transformation ends at its first preserved commit.
    history = _run_git(root, ["log", "--reverse", "--format=%H", "HEAD", "--", unit])
    if history.returncode:
        raise ValueError("bootstrap history unavailable")
    revisions = history.stdout.decode("ascii").splitlines()
    if len(revisions) > 4096:
        raise ValueError("bootstrap history exceeds bound")
    source = None
    for revision in revisions:
        captured = _git_members(root, revision, unit, package)
        if captured:
            source = captured
            break
    preserved = (
        preserved_payload_members(root, record)
        if surface == "worktree"
        else _git_members(root, surface, unit, package)
    )
    original = _git_members(root, commit, origin, package)
    if source is not None:
        return _bootstrap_identity(original, source, path, surface) + _compare_members(
            root, path, unit, surface, source, preserved, assessment, registry
        )
    if surface == "worktree":
        try:
            original = {
                member: (
                    mode,
                    _checkout_bytes(
                        root,
                        unit + ("/" + member if member else ""),
                        origin + ("/" + member if member else ""),
                        raw,
                    ),
                )
                for member, (mode, raw) in original.items()
            }
        except ValueError:
            return [ArchiveFinding("archive-checkout-unsupported", path, surface)]
    return _bootstrap_identity(original, preserved, path, surface)


def _bootstrap_identity(source, preserved, path, surface):
    if set(source) != set(preserved):
        return [ArchiveFinding("archive-exact-members-differ", path, surface)]
    findings = []
    for member, (mode, raw) in source.items():
        actual_mode, actual = preserved[member]
        if mode != actual_mode:
            findings.append(ArchiveFinding("archive-exact-mode-differs", path, surface))
        if (
            b"\r\n" in raw
            and b"\n" not in raw.replace(b"\r\n", b"")
            and b"\n" not in actual.replace(b"\r\n", b"")
        ):
            raw, actual = raw.replace(b"\r\n", b"\n"), actual.replace(b"\r\n", b"\n")
        findings.extend(
            ArchiveFinding(code, path, surface)
            for code in _identity_findings(raw, actual)
        )
    return findings


def _compare_members(
    root, path, source_path, surface, source, preserved, assessment, registry
):
    if assessment is not None and assessment.availability == "git-history-only":
        from scripts.lib.document_governance.archive_assessments import _approval

        if assessment.hold != registry.common["archive_retention"][
            "absence_token"
        ] or not _approval(root, assessment, {"assess", "remove"}):
            return [ArchiveFinding("assessment-approval-invalid", path, surface)]
        return (
            [ArchiveFinding("assessment-history-only-payload-present", path, surface)]
            if preserved
            else []
        )
    if set(source) != set(preserved):
        return [ArchiveFinding("archive-exact-members-differ", path, surface)]
    findings = []
    for member, (mode, raw) in source.items():
        preserved_mode, actual = preserved[member]
        if mode != preserved_mode:
            findings.append(ArchiveFinding("archive-exact-mode-differs", path, surface))
        if surface == "worktree":
            try:
                raw = _checkout_bytes(
                    root,
                    path.rstrip("/") + ("/" + member if member else ""),
                    source_path + ("/" + member if member else ""),
                    raw,
                )
            except ValueError:
                findings.append(
                    ArchiveFinding("archive-checkout-unsupported", path, surface)
                )
                continue
        if actual != raw:
            findings.append(ArchiveFinding("archive-exact-bytes-differ", path, surface))
    return findings


def _generation_contract(raw):
    document = json.loads(raw, object_pairs_hook=_unique_object)
    if not isinstance(document, dict) or not isinstance(
        document.get("common", {}), dict
    ):
        raise ValueError("invalid historical Registry")
    contract = document.get("common", {}).get("archive_retention")
    if contract is not None and not isinstance(contract, dict):
        raise ValueError("invalid historical generation")
    return (document.get("common", {}).get("archive_disposition_model"), contract)


def _partial_adoption(root, registry_path):
    try:
        worktree = _catalog_members(root / registry_path, False)
    except ValueError as error:
        if isinstance(error.__cause__, FileNotFoundError):
            return False
        raise
    if not worktree or _generation_contract(worktree[""][1])[1] is None:
        return False
    staged = _run_git(
        root,
        [
            "diff",
            "--cached",
            "--name-only",
            "HEAD",
            "--",
            "docs/98.archive",
            "docs/99.templates",
            "scripts/lib/document_governance",
            ".agents/governance",
            "docs/02.architecture",
        ],
    )
    if staged.returncode:
        raise ValueError("staged adoption changes unavailable")
    return bool(staged.stdout)


def _generation_unchanged(root, base, registry):
    current = registry.common["archive_retention"]
    path = "docs/99.templates/registry.json"
    contracts = []
    for revision in dict.fromkeys(("HEAD", base)):
        listed = _run_git(root, ["ls-tree", "-z", revision, "--", path])
        if listed.returncode:
            raise ValueError("generation baseline unavailable")
        if listed.stdout:
            contracts.append(_generation_contract(_blob(root, f"{revision}:{path}")))
    adopted = any(contract is not None for _, contract in contracts)
    staged = _git_members(root, "index", path, False)
    index_contract = _generation_contract(staged[""][1]) if staged else (None, None)
    if index_contract[1] is None and (adopted or _partial_adoption(root, path)):
        return False
    contracts.append(index_contract)
    return all(
        old is None
        or (
            model == registry.common.get("archive_disposition_model")
            and old.get("legacy_capture_revision")
            == current.get("legacy_capture_revision")
            and tuple(old.get("legacy_transition_units", ()))
            == tuple(current.get("legacy_transition_units", ()))
        )
        for model, old in contracts
    )


def validate_archive_snapshots(
    root: pathlib.Path, base: str, registry: DocumentRegistry | None = None
) -> tuple[ArchiveFinding, ...]:
    """Validate new-generation captures even when already present at base."""
    root = pathlib.Path(root)
    registry = load_registry() if registry is None else registry
    if "archive_retention" not in registry.common:
        return ()
    try:
        if not _generation_unchanged(root, base, registry):
            return (
                ArchiveFinding(
                    "archive-generation-changed", "docs/99.templates/registry.json"
                ),
            )
        legacy = _legacy_records(root, registry)
    except (ValueError, UnicodeError):
        return (ArchiveFinding("archive-generation-unavailable", _CATALOG_RECORD),)
    from scripts.lib.document_governance.archive_assessments import _unit

    try:
        configured = registry.common["archive_retention"].get(
            "legacy_transition_units", ()
        )
        transition = frozenset(_unit(unit) for unit in configured)
        if any(_unit(unit) != unit for unit in configured):
            raise ValueError("bootstrap unit is not canonical")
        if len(transition) != len(configured) or transition & legacy:
            raise ValueError("bootstrap units duplicate another generation")
    except (ValueError, TypeError, AttributeError):
        return (ArchiveFinding("archive-generation-unavailable", _CATALOG_RECORD),)
    from scripts.lib.document_governance.archive_assessments import (
        _snapshot,
        registry_for_surface,
        validate_assessment_snapshot,
    )

    findings = []
    records_by_surface = {}
    texts_by_surface = {}
    for surface in ("HEAD", "index", "worktree"):
        try:
            text = _catalog(root, surface)
            if surface == "HEAD":
                priors = (_catalog(root, base),)
            elif surface == "index":
                priors = (texts_by_surface.get("HEAD"),)
            else:
                priors = (texts_by_surface.get("HEAD"), texts_by_surface.get("index"))
            captures, assessments = _snapshot(
                text or "", registry.common["archive_retention"]
            )
            for prior in priors:
                findings.extend(
                    validate_assessment_snapshot(root, text, prior, registry, surface)
                )
                prior_captures, _ = _snapshot(
                    prior or "", registry.common["archive_retention"]
                )
                findings.extend(
                    ArchiveFinding("capture-row-changed", unit, surface)
                    for unit in captures.keys() & prior_captures.keys()
                    if captures[unit] != prior_captures[unit]
                )
            texts_by_surface[surface] = text
            rows, errors = _catalog_rows(text) if text is not None else ((), [])
            records = frozenset(_code_span(row.record) for row in rows)
            records_by_surface[surface] = records
            findings.extend(
                ArchiveFinding(item.code, item.path, surface) for item in errors
            )
            if surface != "HEAD":
                required = records_by_surface.get("HEAD", frozenset())
                if surface == "worktree":
                    required |= records_by_surface.get("index", frozenset())
                for missing in required - records:
                    findings.append(
                        ArchiveFinding(
                            "archive-capture-row-missing", str(missing), surface
                        )
                    )
            names_registry = registry_for_surface(root, surface) if rows else registry
            for row in rows:
                findings.extend(
                    _check_row(
                        root,
                        row,
                        surface,
                        legacy,
                        transition,
                        registry,
                        assessments.get(_code_span(row.record)),
                        names_registry,
                    )
                )
        except (OSError, ValueError, UnicodeError):
            findings.append(
                ArchiveFinding("archive-snapshot-unavailable", _CATALOG_RECORD, surface)
            )
    return tuple(sorted(set(findings)))
