"""Current archive assessments, scoped approval evidence, and history continuity."""

from __future__ import annotations

import dataclasses
import datetime
import pathlib
import re
from collections.abc import Mapping

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text
from scripts.lib.document_governance.git_provenance import _run_git
from scripts.lib.document_governance.registry import (
    PRESERVED_DISPOSITIONS,
    classify_path,
    load_registry,
    preserved_origin_path,
)

MAX_HISTORY_REVISIONS = 4096
MAX_ASSESSMENTS = 512


@dataclasses.dataclass(frozen=True)
class ArchiveAssessment:
    record: str
    assessment: str = "unreviewed"
    availability: str = "retained"
    current_owner: str = "none"
    decision: str = "none"
    reason: str = "none"
    assessed_at: str = "none"
    hold: str = "none"


def _contract(registry=None) -> Mapping:
    active = registry if registry is not None else load_registry()
    contract = active.common.get("archive_retention")
    if not isinstance(contract, Mapping):
        raise ValueError("archive assessment contract is unavailable")
    return contract


def _literal(value: str) -> str:
    return value[1:-1] if value.startswith("`") and value.endswith("`") else value


def _unit(value: str) -> str:
    from scripts.lib.document_governance.archive import _safe_path, retention_unit

    value = _literal(value)
    path = _safe_path(value.rstrip("/"))
    if (
        path is None
        or path.as_posix() != value.rstrip("/")
        or value.partition("/")[0] not in PRESERVED_DISPOSITIONS
        or retention_unit(value) != value
        or preserved_origin_path(f"docs/98.archive/{value.rstrip('/')}") is None
    ):
        raise ValueError("archive assessment unit is invalid")
    return value


def _table(text: str, heading: str, columns) -> list[tuple[str, ...]]:
    sections = list(re.finditer(rf"(?m)^## {re.escape(heading)}[ \t]*$", text))
    if not sections:
        return []
    if len(sections) != 1:
        raise ValueError("duplicate archive table")
    body = re.split(r"(?m)^## ", text[sections[0].end() :], maxsplit=1)[0]
    lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if not lines:
        return []
    cells = [
        tuple(cell.strip() for cell in line.strip("|").split("|")) for line in lines
    ]
    if (
        len(cells) < 2
        or cells[0] != tuple(columns)
        or len(cells[1]) != len(columns)
        or any(re.fullmatch(r":?-{3,}:?", value) is None for value in cells[1])
        or any(len(row) != len(columns) for row in cells[2:])
        or len(cells) > MAX_ASSESSMENTS + 2
    ):
        raise ValueError("archive table shape is invalid")
    return cells[2:]


def _date(value: str) -> bool:
    try:
        return datetime.date.fromisoformat(value).isoformat() == value
    except (ValueError, TypeError):
        return False


def _source(value: str) -> tuple[str, str]:
    from scripts.lib.document_governance.archive import _safe_path

    revision, separator, path = _literal(value).partition(":")
    parsed = _safe_path(path)
    if (
        not separator
        or re.fullmatch(r"[0-9a-f]{40}", revision) is None
        or parsed is None
        or parsed.as_posix() != path
        or ":" in path
    ):
        raise ValueError(
            "archive source must name a full supported commit and safe path"
        )
    return revision, path


def _snapshot(text: str, contract: Mapping):
    captures = {}
    for cells in _table(text, contract["capture_section"], contract["capture_columns"]):
        unit = _unit(cells[0])
        if unit in captures or cells[1] != unit.partition("/")[0]:
            raise ValueError("archive capture identity is invalid")
        _source(cells[3])
        captures[unit] = cells
    assessments = {}
    for cells in _table(
        text, contract["assessment_section"], contract["assessment_columns"]
    ):
        unit = _unit(cells[0])
        row = ArchiveAssessment(unit, *(_literal(value) for value in cells[1:]))
        if (
            unit in assessments
            or unit not in captures
            or row.assessment not in contract["assessment_values"]
            or row.availability not in contract["availability_values"]
            or row.assessment == contract["default_assessment"]
            or not all(value.strip() for value in cells)
            or not _date(row.assessed_at)
            or row.reason == contract["absence_token"]
            or (
                row.assessment == "superseded"
                and row.current_owner == contract["absence_token"]
            )
        ):
            raise ValueError("archive assessment row is invalid")
        _source(row.decision)
        assessments[unit] = row
    return captures, assessments


def _current(root: pathlib.Path, contract: Mapping):
    from scripts.lib.document_governance.archive import _read_regular

    try:
        text = _read_regular(root / contract["catalog_path"]).decode("utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError("archive catalog is unavailable") from error
    return _snapshot(text, contract)


def retention_contract_enabled(root: pathlib.Path) -> bool:
    """Once adopted, removing the current declaration cannot disable its gates."""
    import json

    from scripts.lib.document_governance.registry import (
        _unique_object,
        load_registry_document,
    )

    root = pathlib.Path(root)
    relative = "docs/99.templates/registry.json"
    path = root / relative
    try:
        path.lstat()
    except FileNotFoundError:
        common = {}
    else:
        common = load_registry_document(path).get("common", {})
    if not isinstance(common, Mapping):
        raise ValueError("archive registry common contract is invalid")
    if "archive_retention" in common:
        if not isinstance(common["archive_retention"], Mapping):
            raise ValueError("archive retention contract is invalid")
        return True
    if _run_git(root, ["rev-parse", "--verify", "HEAD"]).returncode:
        return False
    revisions = (
        _git(
            root,
            "rev-list",
            "--full-history",
            f"--max-count={MAX_HISTORY_REVISIONS + 1}",
            "HEAD",
            "--",
            relative,
        )
        .decode()
        .splitlines()
    )
    if len(revisions) > MAX_HISTORY_REVISIONS:
        raise ValueError("archive registry history limit exceeded")
    for revision in revisions:
        text = _historical_text(root, revision, relative)
        if text is None:
            continue
        historic = json.loads(text, object_pairs_hook=_unique_object)
        historic_common = (
            historic.get("common", {}) if isinstance(historic, Mapping) else None
        )
        if not isinstance(historic_common, Mapping):
            raise ValueError("archive registry history is invalid")
        if "archive_retention" in historic_common:
            raise ValueError("adopted archive retention contract was removed")
    return False


def preserved_payload_members(root: pathlib.Path, unit: str):
    """A missing unit's ancestors are absence; symlink ancestors remain unsafe."""
    from scripts.lib.document_governance.archive import _catalog_members

    unit = _unit(unit)
    disposition, _, relative = unit.partition("/")
    members = (
        _catalog_members(pathlib.Path(root) / "docs/98.archive" / disposition, True)
        or {}
    )
    if not unit.endswith("/"):
        return {"": members[relative]} if relative in members else {}
    return {
        name[len(relative) :]: value
        for name, value in members.items()
        if name.startswith(relative)
    }


def assessment_lookup(
    root: pathlib.Path, registry=None
) -> dict[str, ArchiveAssessment]:
    """Return effective assessments; malformed current management fails closed."""
    contract = _contract(registry)
    captures, explicit = _current(pathlib.Path(root), contract)
    return {unit: explicit.get(unit, ArchiveAssessment(unit)) for unit in captures}


def capture_sources(root: pathlib.Path, registry=None) -> dict[str, tuple[str, str]]:
    """Keep capture provenance separate from mutable assessment information."""
    from scripts.lib.document_governance.archive import _catalog_source_findings

    root = pathlib.Path(root)
    captures, _ = _current(root, _contract(registry))
    for unit, row in captures.items():
        if _catalog_source_findings(
            root, f"docs/98.archive/{unit}", row[3], unit.endswith("/")
        ):
            raise ValueError("archive capture provenance is invalid")
    return {unit: _source(row[3]) for unit, row in captures.items()}


def _git(root: pathlib.Path, *args: str) -> bytes:
    result = _run_git(root, list(args))
    if result.returncode:
        raise ValueError("archive history is unavailable")
    return result.stdout


def _historical_text(root: pathlib.Path, revision: str, path: str) -> str | None:
    listed = _git(root, "ls-tree", "-z", revision, "--", path)
    if not listed:
        return None
    metadata, _, listed_path = listed.rstrip(b"\0").partition(b"\t")
    mode, kind, oid = metadata.split()
    if (
        kind != b"blob"
        or mode not in (b"100644", b"100755")
        or listed_path.decode() != path
    ):
        raise ValueError("archive historical record is not a regular file")
    return _git(root, "cat-file", "blob", oid.decode()).decode("utf-8")


def _history(root: pathlib.Path, contract: Mapping, base: str | None):
    if _git(root, "rev-parse", "--is-shallow-repository").strip() != b"false":
        raise ValueError("archive history is incomplete")
    if _git(root, "rev-parse", "--show-object-format").strip() != b"sha1":
        raise ValueError("archive object format is unsupported")
    revisions = (
        _git(
            root,
            "rev-list",
            "--full-history",
            "--topo-order",
            "--reverse",
            f"--max-count={MAX_HISTORY_REVISIONS + 1}",
            "HEAD",
            "--",
            contract["catalog_path"],
            "docs/98.archive/README.md",
        )
        .decode()
        .splitlines()
    )
    if len(revisions) > MAX_HISTORY_REVISIONS:
        raise ValueError("archive history revision limit exceeded")
    if base is not None:
        if re.fullmatch(r"[0-9a-f]{40}", base) is None:
            raise ValueError("archive comparison base is invalid")
        _git(root, "merge-base", "--is-ancestor", base, "HEAD")
    cache = {}

    def snapshot(revision):
        if revision not in cache:
            if len(cache) >= MAX_HISTORY_REVISIONS:
                raise ValueError("archive history snapshot limit exceeded")
            text = _historical_text(root, revision, contract["catalog_path"])
            if text is None:
                text = _historical_text(root, revision, "docs/98.archive/README.md")
            cache[revision] = (
                _snapshot(text, contract) if text is not None else ({}, {})
            )
        return cache[revision]

    comparisons = []
    for revision in revisions:
        parents = _git(root, "show", "-s", "--format=%P", revision).decode().split()
        comparisons.append(
            (
                revision,
                snapshot(revision),
                tuple(snapshot(parent) for parent in parents),
            )
        )
    return comparisons, snapshot("HEAD")


def _visible(text: str) -> str:
    """Approval quotations in examples are not execution evidence."""
    text = re.sub(r"<!--.*?(?:-->|$)", "", text, flags=re.DOTALL)
    output = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif (
                token[0] == fence[0]
                and len(token) >= len(fence)
                and not line[marker.end() :].strip()
            ):
                fence = None
            continue
        if fence is None:
            output.append(line)
    return "\n".join(output)


def _historical_units(root: pathlib.Path) -> set[str]:
    from scripts.lib.document_governance.archive import retention_unit

    paths = (
        _git(
            root,
            "log",
            "--format=",
            "--name-only",
            "--no-renames",
            "HEAD",
            "--",
            *(f"docs/98.archive/{item}" for item in PRESERVED_DISPOSITIONS),
        )
        .decode()
        .splitlines()
    )
    return {
        retention_unit(path.removeprefix("docs/98.archive/"))
        for path in paths
        if path.startswith("docs/98.archive/")
    }


def _approval_record_matches(
    root: pathlib.Path,
    row: ArchiveAssessment,
    actions: set[str],
    context_revision: str = "HEAD",
) -> bool:
    """Match pinned record structure and ancestry without authenticating its actor.

    This read-only consistency check does not authorize archive removal.
    """
    from scripts.lib.document_governance.archive import _catalog_registry

    revision, path = _source(row.decision)
    _git(root, "merge-base", "--is-ancestor", revision, context_revision)
    text = _historical_text(root, revision, path)
    if text is None:
        return False
    origin = preserved_origin_path(path) or path
    if classify_path(origin, _catalog_registry()) != "task":
        return False
    metadata = parse_frontmatter_text(text)
    parts = pathlib.PurePosixPath(origin).parts
    identity = f"SPEC-{parts[2][:4]}-TSK-{parts[-1][4:8]}"
    if (
        not all(
            isinstance(metadata.get(key), str)
            for key in ("type", "artifact_id", "status", "owner")
        )
        or metadata.get("type") != "sdlc/task"
        or metadata.get("artifact_id") != identity
        or metadata.get("status") not in {"ready", "in-progress", "completed"}
        or not isinstance(metadata.get("archive_authorizations"), list)
    ):
        return False
    text = _visible(text)
    authorized = set()
    required = {"unit", "action", "approved_by", "approved_at", "evidence", "status"}
    for item in metadata["archive_authorizations"]:
        if (
            not isinstance(item, dict)
            or set(item) != required
            or not all(isinstance(value, str) for value in item.values())
        ):
            return False
        if (
            item["unit"] != row.record
            or item["status"] != "approved"
            or item["action"] not in actions
            or item["approved_at"] != row.assessed_at
            or not isinstance(item["approved_by"], str)
            or not item["approved_by"].strip()
            or item["approved_by"] != metadata.get("owner")
            or not isinstance(item["evidence"], str)
            or re.fullmatch(r"#[A-Za-z0-9][A-Za-z0-9._-]*", item["evidence"]) is None
        ):
            continue
        headings = list(re.finditer(r"(?m)^#{1,6} (.+)$", text))
        matches = []
        for index, heading in enumerate(headings):
            slug = re.sub(r"[^\w\- ]", "", heading.group(1).lower()).replace(" ", "-")
            if f"#{slug}" == item["evidence"]:
                end = (
                    headings[index + 1].start()
                    if index + 1 < len(headings)
                    else len(text)
                )
                matches.append(text[heading.end() : end])
        if len(matches) != 1:
            continue
        expected = (
            f"> {item['approved_by']} approved {item['action']} "
            f"for {row.record} on {row.assessed_at}."
        )
        if any(
            re.fullmatch(r" {0,3}" + re.escape(expected), line)
            for line in matches[0].splitlines()
        ):
            authorized.add(item["action"])
    return actions <= authorized


def registry_for_surface(root: pathlib.Path, surface: str = "worktree"):
    """Load the validated Registry from the same surface as its document inventory."""
    import tempfile

    from scripts.lib.document_governance.archive import _catalog_members

    root = pathlib.Path(root)
    path = "docs/99.templates/registry.json"
    try:
        current = _catalog_members(root / path, False)
    except ValueError as error:
        if not isinstance(error.__cause__, FileNotFoundError):
            raise
        current = None
    if surface == "worktree":
        raw = current[""][1] if current is not None else None
    elif surface == "index":
        entries = _git(root, "ls-files", "-s", "-z", "--", path).split(b"\0")
        entries = [entry for entry in entries if entry]
        if not entries:
            raw = None
        else:
            if len(entries) != 1:
                raise ValueError("unmerged Registry")
            header, name = entries[0].split(b"\t", 1)
            mode, oid, stage = header.split()
            if (
                name.decode() != path
                or mode not in (b"100644", b"100755")
                or stage != b"0"
            ):
                raise ValueError("Registry requires a regular blob")
            raw = _git(root, "cat-file", "blob", oid.decode())
    else:
        text = _historical_text(root, surface, path)
        raw = text.encode("utf-8") if text is not None else None
    if raw is None:
        if current is not None or _historical_text(root, "HEAD", path) is not None:
            raise ValueError("selected Registry is missing")
        return load_registry()
    with tempfile.TemporaryDirectory(prefix="archive-registry-") as directory:
        target = pathlib.Path(directory) / "registry.json"
        target.write_bytes(raw)
        return load_registry(target)


def _current_owner(root: pathlib.Path, value: str, surface: str = "worktree") -> bool:
    from scripts.lib.document_governance.archive import (
        _catalog_members,
    )

    registry = registry_for_surface(root, surface)
    candidates = []
    if surface == "worktree":
        names = _git(root, "ls-files", "-z", "--", "docs").decode().split("\0")
        objects = None
    else:
        args = (
            ("ls-files", "-s", "-z", "--", "docs")
            if surface == "index"
            else ("ls-tree", "-r", "-z", surface, "--", "docs")
        )
        objects = {}
        for entry in _git(root, *args).split(b"\0"):
            if not entry:
                continue
            header, name = entry.split(b"\t", 1)
            mode, second, third = header.split()
            if surface == "index" and third != b"0":
                raise ValueError("unmerged owner inventory")
            objects[name.decode()] = (mode, second if surface == "index" else third)
        names = objects.keys()
    for name in names:
        if not name.endswith(".md") or name.startswith("docs/98.archive/"):
            continue
        if classify_path(name, registry) is None:
            continue
        if objects is not None:
            mode, oid = objects[name]
            if mode not in (b"100644", b"100755"):
                raise ValueError("owner inventory requires regular blobs")
            content = _git(root, "cat-file", "blob", oid.decode())
        else:
            try:
                snapshot = _catalog_members(root / name, False)
            except ValueError as error:
                if isinstance(error.__cause__, FileNotFoundError):
                    continue
                raise
            if snapshot is None:
                continue
            content = snapshot[""][1]
        metadata = parse_frontmatter_text(content.decode("utf-8"))
        if value in (name, metadata.get("artifact_id")):
            candidates.append(metadata)
    return (
        len(candidates) == 1
        and isinstance(candidates[0].get("status"), str)
        and candidates[0]["status"]
        not in {
            "superseded",
            "retired",
            "cancelled",
            "completed",
            "rejected",
            "resolved",
        }
    )


def _assessment_change(
    root: pathlib.Path,
    prior,
    row: ArchiveAssessment,
    context_revision: str = "HEAD",
) -> list[str]:
    actions = {"assess"}
    codes = []
    if row.availability == "git-history-only":
        actions.add("remove")
    if prior is not None:
        if row != prior:
            if row.decision.split(":", 1)[0] == prior.decision.split(":", 1)[0]:
                codes.append("assessment-decision-unchanged")
            if row.reason == prior.reason:
                codes.append("assessment-reason-unchanged")
        if row.assessed_at < prior.assessed_at:
            codes.append("assessment-date-regressed")
        if prior.assessment == "invalidated" and row.assessment == "usable":
            actions.add("rehabilitate")
            if row.reason == prior.reason:
                codes.append("assessment-rehabilitation-reason-required")
        if prior.availability == "git-history-only" and row.availability == "retained":
            codes.append("assessment-payload-resurrection")
    try:
        record_matches = _approval_record_matches(root, row, actions, context_revision)
    except (OSError, ValueError, UnicodeError):
        record_matches = False
    if not record_matches:
        codes.append("assessment-approval-invalid")
    return codes


def validate_assessment_snapshot(
    root: pathlib.Path,
    text: str | None,
    prior_text: str | None,
    registry=None,
    surface: str = "worktree",
):
    """Check assessment changes on one caller-selected Git/working surface."""
    from scripts.lib.document_governance.archive import ArchiveFinding

    contract = _contract(registry)
    try:
        _, rows = _snapshot(text or "", contract)
        _, previous = _snapshot(prior_text or "", contract)
    except ValueError:
        return (
            ArchiveFinding(
                "assessment-table-invalid", contract["catalog_path"], surface
            ),
        )
    findings = [
        ArchiveFinding("assessment-row-removed", unit, surface)
        for unit in previous.keys() - rows.keys()
    ]
    for unit, row in rows.items():
        codes = _assessment_change(pathlib.Path(root), previous.get(unit), row)
        if row.availability == "git-history-only":
            try:
                archived = unit in _historical_units(pathlib.Path(root))
            except (OSError, ValueError, UnicodeError):
                archived = False
            if not archived:
                codes.append("assessment-removal-without-capture")
        if (
            row.availability == "git-history-only"
            and row.hold != contract["absence_token"]
        ):
            codes.append("assessment-removal-held")
        if row.current_owner != contract["absence_token"]:
            try:
                valid = _current_owner(pathlib.Path(root), row.current_owner, surface)
            except (OSError, ValueError, UnicodeError):
                valid = False
            if not valid:
                codes.append("assessment-owner-invalid")
        findings.extend(ArchiveFinding(code, unit, surface) for code in codes)
    return tuple(sorted(set(findings)))


def validate_archive_assessments(
    root: pathlib.Path, base: str | None = None, registry=None
):
    """Validate current assessments and detect loss hidden by current-tree deletion."""
    from scripts.lib.document_governance.archive import (
        ArchiveFinding,
        preserved_member_paths,
        retention_unit,
    )

    root = pathlib.Path(root)
    findings = []
    try:
        contract = _contract(registry)
    except ValueError:
        return (ArchiveFinding("assessment-contract-unavailable", "docs/98.archive"),)
    try:
        captures, assessments = _current(root, contract)
    except (OSError, ValueError, UnicodeError):
        captures, assessments = {}, {}
        findings.append(
            ArchiveFinding("assessment-table-invalid", contract["catalog_path"])
        )
    try:
        snapshots, (_, previous) = _history(root, contract, base)
        historical_units = _historical_units(root)
        current_units = {
            retention_unit(member)
            for disposition in PRESERVED_DISPOSITIONS
            for member in preserved_member_paths(root / "docs/98.archive", disposition)
        }
    except (OSError, ValueError, UnicodeError):
        return (
            *findings,
            ArchiveFinding("assessment-history-unavailable", contract["catalog_path"]),
        )
    original = {}
    assessed_units = set()
    for revision, (historical_captures, historical_assessments), parents in snapshots:
        for parent_captures, parent_assessments in parents or (({}, {}),):
            for unit in parent_captures.keys() - historical_captures.keys():
                findings.append(ArchiveFinding("capture-row-removed", unit))
            for unit in parent_assessments.keys() - historical_assessments.keys():
                findings.append(ArchiveFinding("assessment-row-removed", unit))
            for unit, row in historical_assessments.items():
                if parent_assessments.get(unit) != row:
                    findings.extend(
                        ArchiveFinding(code, unit)
                        for code in _assessment_change(
                            root, parent_assessments.get(unit), row, revision
                        )
                    )
        for unit, cells in historical_captures.items():
            if unit in original and original[unit] != cells:
                findings.append(ArchiveFinding("capture-row-changed", unit))
            original.setdefault(unit, cells)
        assessed_units.update(historical_assessments)
    for unit in historical_units - current_units - captures.keys():
        findings.append(ArchiveFinding("capture-history-unit-unrecorded", unit))
    for unit, cells in original.items():
        if unit not in captures:
            findings.append(ArchiveFinding("capture-row-removed", unit))
        elif captures[unit] != cells:
            findings.append(ArchiveFinding("capture-row-changed", unit))
    for unit in assessed_units - assessments.keys():
        findings.append(ArchiveFinding("assessment-row-removed", unit))
    for unit, cells in captures.items():
        row = assessments.get(unit, ArchiveAssessment(unit))
        try:
            revision, origin = _source(cells[3])
            _git(root, "merge-base", "--is-ancestor", revision, "HEAD")
            expected_kind = b"tree" if unit.endswith("/") else b"blob"
            if (
                _git(root, "cat-file", "-t", f"{revision}:{origin}").strip()
                != expected_kind
            ):
                raise ValueError("wrong source kind")
            members = preserved_payload_members(root, unit)
            present = bool(members)
            listed = _git(root, "ls-tree", "-r", "-z", revision, "--", origin)
            expected = {
                entry.partition(b"\t")[2].decode()[len(origin) :].lstrip("/")
                for entry in listed.split(b"\0")
                if entry
            }
            if present and set(members) != expected:
                findings.append(ArchiveFinding("assessment-unit-partial", unit))
        except (OSError, ValueError):
            findings.append(ArchiveFinding("assessment-recovery-unavailable", unit))
            continue
        if row.availability == "retained" and not present:
            findings.append(ArchiveFinding("assessment-retained-payload-missing", unit))
        if row.availability == "git-history-only":
            if unit not in historical_units:
                findings.append(
                    ArchiveFinding("assessment-removal-without-capture", unit)
                )
            if present:
                findings.append(
                    ArchiveFinding("assessment-history-only-payload-present", unit)
                )
            if row.hold != contract["absence_token"]:
                findings.append(ArchiveFinding("assessment-removal-held", unit))
        if unit not in assessments:
            continue
        findings.extend(
            ArchiveFinding(code, unit)
            for code in _assessment_change(root, previous.get(unit), row)
        )
        if row.current_owner != contract["absence_token"]:
            try:
                valid_owner = _current_owner(root, row.current_owner)
            except (OSError, ValueError, UnicodeError):
                valid_owner = False
            if not valid_owner:
                findings.append(ArchiveFinding("assessment-owner-invalid", unit))
    return tuple(sorted(set(findings)))
