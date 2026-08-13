"""Typed, fail-closed Operations catalog migration manifest validation."""

from __future__ import annotations

import dataclasses
import functools
import hashlib
import io
import pathlib
import re
import stat
import subprocess
import tarfile
import types
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from typing import Literal

from scripts.lib.document_governance.frontmatter import safe_load_unique
from scripts.lib.document_governance.links import parse_local_markdown_links


SubjectAction = Literal["retain", "rename", "merge", "delete"]
FileAction = Literal["retain", "rewrite", "merge", "delete"]
FileRole = Literal["guide", "policy", "runbook", "domain-readme"]
ValidationMode = Literal["manifest", "structure", "executed", "complete"]

_OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
_DOMAIN = re.compile(r"[0-9]{2}-[a-z0-9][a-z0-9-]*")
_OPS_ID = re.compile(r"ops-[0-9]{4}")
_SUBJECT_NAME = re.compile(r"ops-(?P<identity>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)")
_SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
_YEAR = re.compile(r"[0-9]{4}")
_INCIDENT_PACKET = re.compile(r"inc-[0-9]{4}-[a-z0-9][a-z0-9-]*")
_RELEASE_PACKET = re.compile(r"rel-[0-9]{4}-[a-z0-9][a-z0-9-]*")
_YAML_BLOCK = re.compile(r"(?ms)^```yaml\n(?P<body>.*?)\n```$")
_TABLE_ROW = re.compile(
    r"^\| `(?P<id>ops-[0-9]{4})` \| `(?P<path>[^`]+)` \| "
    r"`(?P<action>[^`]+)` \| `(?P<owner>[^`]+)` \| "
    r"(?P<roles>[^|]+?) \| (?P<reason>[^|]+?) \|$"
)
_FORBIDDEN_SLUG_TOKENS = frozenset({"guide", "policy", "runbook", "document", "manual"})
_SUBJECT_FIELDS = frozenset(
    {
        "legacy_subject_path",
        "source_commit",
        "source_tree",
        "current_ops_id",
        "catalog_domain",
        "catalog_path",
        "canonical_ops_id",
        "canonical_slug",
        "final_path",
        "semantic_action",
        "merge_into",
        "owner_match",
        "control_boundary_match",
        "trigger_and_recovery_match",
        "independent_evidence_boundary",
        "reason",
    }
)
_FILE_FIELDS = frozenset(
    {
        "legacy_path",
        "source_commit",
        "source_blob",
        "role",
        "catalog_path",
        "final_path",
        "semantic_action",
        "canonical_role_owner",
        "preserved_semantics",
        "removed_semantics",
        "active_consumers",
        "final_consumers",
    }
)
_TOP_FIELDS = frozenset(
    {"schema_version", "migration_id", "baseline_commit", "subjects", "files", "approval"}
)
_APPROVAL_FIELDS = frozenset({"status", "approved_at", "approved_by"})
_SUBJECT_ACTIONS = frozenset({"retain", "rename", "merge", "delete"})
_FILE_ACTIONS = frozenset({"retain", "rewrite", "merge", "delete"})
_FILE_ROLES = frozenset({"guide", "policy", "runbook", "domain-readme"})
_MODES = frozenset({"manifest", "structure", "executed", "complete"})
_STRUCTURAL_DOMAINS = frozenset(
    {
        "00-workspace",
        "01-gateway",
        "02-auth",
        "03-security",
        "04-data",
        "05-messaging",
        "06-observability",
        "07-workflow",
        "08-ai",
        "09-tooling",
        "10-communication",
        "11-laboratory",
        "12-infra-net",
    }
)


class ManifestError(ValueError):
    """Raised when a manifest cannot be parsed into the exact typed schema."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


@dataclasses.dataclass(frozen=True, order=True)
class CatalogFinding:
    """One deterministic Operations catalog contract violation."""

    code: str
    path: str
    message: str


@dataclasses.dataclass(frozen=True)
class OperationSubjectRecord:
    legacy_subject_path: pathlib.PurePosixPath
    source_commit: str
    source_tree: str
    current_ops_id: str
    catalog_domain: str
    catalog_path: pathlib.PurePosixPath
    canonical_ops_id: str
    canonical_slug: str
    final_path: pathlib.PurePosixPath
    semantic_action: SubjectAction
    merge_into: str | None
    owner_match: bool
    control_boundary_match: bool
    trigger_and_recovery_match: bool
    independent_evidence_boundary: bool
    reason: str


@dataclasses.dataclass(frozen=True)
class OperationFileRecord:
    legacy_path: pathlib.PurePosixPath
    source_commit: str
    source_blob: str
    role: FileRole
    catalog_path: pathlib.PurePosixPath
    final_path: pathlib.PurePosixPath | None
    semantic_action: FileAction
    canonical_role_owner: pathlib.PurePosixPath | None
    preserved_semantics: tuple[str, ...]
    removed_semantics: tuple[str, ...]
    active_consumers: tuple[pathlib.PurePosixPath, ...]
    final_consumers: tuple[pathlib.PurePosixPath, ...]


@dataclasses.dataclass(frozen=True)
class OperationsCatalogApproval:
    status: Literal["pending", "approved"]
    approved_at: str | None
    approved_by: str | None


@dataclasses.dataclass(frozen=True)
class OperationsCatalogManifest:
    schema_version: int
    migration_id: str
    baseline_commit: str
    subjects: tuple[OperationSubjectRecord, ...]
    files: tuple[OperationFileRecord, ...]
    approval: OperationsCatalogApproval
    approval_rows: tuple[tuple[str, str, str, str, str, str], ...] = ()


def _mapping(value: object, label: str, fields: frozenset[str]) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise ManifestError("mapping-invalid", f"{label} must be a string-keyed mapping")
    actual = frozenset(value)
    if actual != fields:
        missing = sorted(fields - actual)
        unknown = sorted(actual - fields)
        raise ManifestError(
            "fields-invalid",
            f"{label} fields mismatch; missing={missing} unknown={unknown}",
        )
    return value


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError("string-invalid", f"{label} must be a non-empty string")
    return value


def _path(value: object, label: str, *, nullable: bool = False) -> pathlib.PurePosixPath | None:
    if value is None and nullable:
        return None
    return pathlib.PurePosixPath(_string(value, label))


def _boolean(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise ManifestError("boolean-invalid", f"{label} must be boolean")
    return value


def _string_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ManifestError("list-invalid", f"{label} must be a string list")
    return tuple(value)


def _path_tuple(value: object, label: str) -> tuple[pathlib.PurePosixPath, ...]:
    return tuple(pathlib.PurePosixPath(item) for item in _string_tuple(value, label))


def _subject_record(value: object, index: int) -> OperationSubjectRecord:
    row = _mapping(value, f"subjects[{index}]", _SUBJECT_FIELDS)
    action = _string(row["semantic_action"], f"subjects[{index}].semantic_action")
    if action not in _SUBJECT_ACTIONS:
        raise ManifestError("subject-action-invalid", f"subjects[{index}] invalid semantic_action")
    merge_into = row["merge_into"]
    if merge_into is not None and not isinstance(merge_into, str):
        raise ManifestError("merge-target-invalid", f"subjects[{index}].merge_into")
    return OperationSubjectRecord(
        legacy_subject_path=_path(row["legacy_subject_path"], "legacy_subject_path"),  # type: ignore[arg-type]
        source_commit=_string(row["source_commit"], "source_commit"),
        source_tree=_string(row["source_tree"], "source_tree"),
        current_ops_id=_string(row["current_ops_id"], "current_ops_id"),
        catalog_domain=_string(row["catalog_domain"], "catalog_domain"),
        catalog_path=_path(row["catalog_path"], "catalog_path"),  # type: ignore[arg-type]
        canonical_ops_id=_string(row["canonical_ops_id"], "canonical_ops_id"),
        canonical_slug=_string(row["canonical_slug"], "canonical_slug"),
        final_path=_path(row["final_path"], "final_path"),  # type: ignore[arg-type]
        semantic_action=action,  # type: ignore[arg-type]
        merge_into=merge_into,
        owner_match=_boolean(row["owner_match"], "owner_match"),
        control_boundary_match=_boolean(row["control_boundary_match"], "control_boundary_match"),
        trigger_and_recovery_match=_boolean(row["trigger_and_recovery_match"], "trigger_and_recovery_match"),
        independent_evidence_boundary=_boolean(row["independent_evidence_boundary"], "independent_evidence_boundary"),
        reason=_string(row["reason"], "reason"),
    )


def _file_record(value: object, index: int) -> OperationFileRecord:
    row = _mapping(value, f"files[{index}]", _FILE_FIELDS)
    action = _string(row["semantic_action"], f"files[{index}].semantic_action")
    role = _string(row["role"], f"files[{index}].role")
    if action not in _FILE_ACTIONS:
        raise ManifestError("file-action-invalid", f"files[{index}] invalid semantic_action")
    if role not in _FILE_ROLES:
        raise ManifestError("file-role-invalid", f"files[{index}] invalid role")
    return OperationFileRecord(
        legacy_path=_path(row["legacy_path"], "legacy_path"),  # type: ignore[arg-type]
        source_commit=_string(row["source_commit"], "source_commit"),
        source_blob=_string(row["source_blob"], "source_blob"),
        role=role,  # type: ignore[arg-type]
        catalog_path=_path(row["catalog_path"], "catalog_path"),  # type: ignore[arg-type]
        final_path=_path(row["final_path"], "final_path", nullable=True),
        semantic_action=action,  # type: ignore[arg-type]
        canonical_role_owner=_path(
            row["canonical_role_owner"], "canonical_role_owner", nullable=True
        ),
        preserved_semantics=_string_tuple(row["preserved_semantics"], "preserved_semantics"),
        removed_semantics=_string_tuple(row["removed_semantics"], "removed_semantics"),
        active_consumers=_path_tuple(row["active_consumers"], "active_consumers"),
        final_consumers=_path_tuple(row["final_consumers"], "final_consumers"),
    )


def load_operations_catalog_manifest(path: pathlib.Path) -> OperationsCatalogManifest:
    """Load the sole YAML block in a migration record using an exact schema."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ManifestError("manifest-unreadable", str(error)) from error
    blocks = list(_YAML_BLOCK.finditer(text))
    if len(blocks) != 1:
        raise ManifestError("yaml-block-invalid", "manifest requires exactly one YAML block")
    try:
        document = safe_load_unique(blocks[0].group("body"))
    except Exception as error:
        raise ManifestError("yaml-invalid", str(error)) from error
    root = _mapping(document, "manifest", _TOP_FIELDS)
    if root["schema_version"] != 1:
        raise ManifestError("schema-version-invalid", "schema_version must equal 1")
    if root["migration_id"] != "mig-0002":
        raise ManifestError("migration-id-invalid", "migration_id must equal mig-0002")
    raw_subjects = root["subjects"]
    raw_files = root["files"]
    if not isinstance(raw_subjects, list) or not isinstance(raw_files, list):
        raise ManifestError("records-invalid", "subjects and files must be lists")
    approval = _mapping(root["approval"], "approval", _APPROVAL_FIELDS)
    status = approval["status"]
    if status not in {"pending", "approved"}:
        raise ManifestError("approval-status-invalid", "approval.status is invalid")
    for key in ("approved_at", "approved_by"):
        if approval[key] is not None and not isinstance(approval[key], str):
            raise ManifestError("approval-field-invalid", f"approval.{key} must be string or null")
    approval_rows = tuple(
        (
            match.group("id"),
            match.group("path"),
            match.group("action"),
            match.group("owner"),
            match.group("roles").strip(),
            match.group("reason").strip(),
        )
        for line in text.splitlines()
        if (match := _TABLE_ROW.fullmatch(line)) is not None
    )
    return OperationsCatalogManifest(
        schema_version=1,
        migration_id="mig-0002",
        baseline_commit=_string(root["baseline_commit"], "baseline_commit"),
        subjects=tuple(_subject_record(row, index) for index, row in enumerate(raw_subjects)),
        files=tuple(_file_record(row, index) for index, row in enumerate(raw_files)),
        approval=OperationsCatalogApproval(
            status=status,  # type: ignore[arg-type]
            approved_at=approval["approved_at"],  # type: ignore[arg-type]
            approved_by=approval["approved_by"],  # type: ignore[arg-type]
        ),
        approval_rows=approval_rows,
    )


def _safe_path(path: pathlib.PurePosixPath) -> bool:
    return (
        bool(path.parts)
        and not path.is_absolute()
        and "\\" not in path.as_posix()
        and "\x00" not in path.as_posix()
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _finding(code: str, path: object, message: str) -> CatalogFinding:
    return CatalogFinding(code, str(path), message)


def _git(repo_root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo_root, check=False, capture_output=True, text=True
    )


@functools.lru_cache(maxsize=None)
def _baseline_objects(
    repo_root: str, commit: str
) -> Mapping[str, tuple[str, str]]:
    result = _git(
        pathlib.Path(repo_root),
        "ls-tree",
        "-r",
        "-t",
        commit,
        "--",
        "docs/05.operations",
    )
    if result.returncode != 0:
        return types.MappingProxyType({})
    objects: dict[str, tuple[str, str]] = {}
    for line in result.stdout.splitlines():
        metadata, separator, path = line.partition("\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            continue
        _mode, kind, object_id = fields
        objects[path] = (object_id, kind)
    return types.MappingProxyType(objects)


@functools.lru_cache(maxsize=None)
def _git_object(
    repo_root: str, commit: str, path: str
) -> tuple[str | None, str | None]:
    baseline = _baseline_objects(repo_root, commit).get(path)
    if baseline is not None:
        return baseline
    root = pathlib.Path(repo_root)
    result = _git(root, "rev-parse", f"{commit}:{path}")
    if result.returncode != 0 or _OBJECT_ID.fullmatch(result.stdout.strip()) is None:
        return None, None
    object_id = result.stdout.strip()
    kind = _git(root, "cat-file", "-t", object_id)
    return object_id, kind.stdout.strip() if kind.returncode == 0 else None


@functools.lru_cache(maxsize=None)
def _baseline_inventory(repo_root: pathlib.Path, commit: str) -> tuple[set[str], set[str]]:
    subjects: set[str] = set()
    files: set[str] = set()
    for path, (_object_id, kind) in _baseline_objects(
        str(repo_root.resolve()), commit
    ).items():
        if kind != "blob":
            continue
        parts = pathlib.PurePosixPath(path).parts
        if (
            len(parts) == 5
            and parts[:2] == ("docs", "05.operations")
            and _DOMAIN.fullmatch(parts[2])
            and _SUBJECT_NAME.fullmatch(parts[3])
            and parts[4] in {"guide.md", "policy.md", "runbook.md"}
        ):
            subjects.add("/".join(parts[:4]))
            files.add(path)
        elif (
            len(parts) == 4
            and parts[:2] == ("docs", "05.operations")
            and _DOMAIN.fullmatch(parts[2])
            and parts[3] == "README.md"
        ):
            files.add(path)
    return subjects, files


@functools.lru_cache(maxsize=None)
def _baseline_tracked_paths(repo_root: str, commit: str) -> frozenset[str]:
    result = _git(pathlib.Path(repo_root), "ls-tree", "-r", "--name-only", commit)
    if result.returncode != 0:
        return frozenset()
    return frozenset(result.stdout.splitlines())


@functools.lru_cache(maxsize=None)
def _baseline_texts(
    repo_root: str, commit: str
) -> Mapping[str, str]:
    result = subprocess.run(
        ["git", "archive", "--format=tar", commit, "--", "docs/05.operations"],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return types.MappingProxyType({})
    texts: dict[str, str] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                source = archive.extractfile(member)
                if source is None:
                    continue
                try:
                    texts[member.name] = source.read().decode("utf-8")
                except UnicodeDecodeError:
                    continue
    except tarfile.TarError:
        return types.MappingProxyType({})
    return types.MappingProxyType(texts)


def _source_text(repo_root: str, commit: str, path: str) -> str | None:
    return _baseline_texts(repo_root, commit).get(path)


def _body_text(text: str) -> str:
    if text.startswith("---\n"):
        marker = text.find("\n---\n", 4)
        if marker >= 0:
            return text[marker + 5 :]
    return text


@functools.lru_cache(maxsize=None)
def _baseline_consumer_lines(
    repo_root: str, commit: str
) -> Mapping[pathlib.PurePosixPath, tuple[str, ...]]:
    common = (
        "grep",
        "-I",
        "-z",
        "-n",
        "-e",
        "docs/05.operations/",
        "-e",
        "ops-",
        "-e",
        "README.md",
        commit,
        "--",
    )
    current = _git(
        pathlib.Path(repo_root),
        *common,
        ".",
        ":(exclude)graphify-out/**",
        ":(exclude)docs/98.archive/**",
        ":(exclude)docs/90.references/**",
        ":(exclude)docs/00.agent-governance/memory/progress.md",
    )
    generated = _git(
        pathlib.Path(repo_root),
        *common,
        "docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md",
        "docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md",
    )
    if current.returncode not in {0, 1} or generated.returncode not in {0, 1}:
        return types.MappingProxyType({})
    lines: defaultdict[pathlib.PurePosixPath, list[str]] = defaultdict(list)
    record = re.compile(
        rf"(?:^|\n){re.escape(commit)}:(?P<path>[^\0\n]+)"
        r"\0(?P<line>[0-9]+)\0(?P<text>[^\n]*)"
    )
    for match in record.finditer(current.stdout + generated.stdout):
        path = pathlib.PurePosixPath(match.group("path"))
        if _current_consumer(path):
            lines[path].append(match.group("text"))
    return types.MappingProxyType(
        {path: tuple(values) for path, values in lines.items()}
    )


def _grep_consumers(
    repo_root: str, commit: str, patterns: tuple[str, ...]
) -> tuple[pathlib.PurePosixPath, ...]:
    return tuple(
        path
        for path, lines in _baseline_consumer_lines(repo_root, commit).items()
        if any(pattern in line for pattern in patterns for line in lines)
    )


def _current_consumer(path: pathlib.PurePosixPath) -> bool:
    value = path.as_posix()
    if value.startswith("graphify-out/") or value == "docs/00.agent-governance/memory/progress.md":
        return False
    if value.startswith("docs/98.archive/"):
        return False
    if value.startswith("docs/90.references/"):
        return value in {
            "docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md",
            "docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md",
        }
    return True


def _derived_consumers(
    repo_root: pathlib.Path,
    manifest: OperationsCatalogManifest,
    row: OperationFileRecord,
) -> tuple[pathlib.PurePosixPath, ...]:
    patterns = [row.legacy_path.as_posix()]
    if row.role == "domain-readme":
        patterns.append("/".join(row.legacy_path.parts[2:]))
    else:
        patterns.append("/".join(row.legacy_path.parts[-2:]))
        role_count = sum(
            other.legacy_path.parent == row.legacy_path.parent
            for other in manifest.files
            if other.role != "domain-readme"
        )
        if role_count == 1:
            patterns.append(row.legacy_path.parent.name.split("-", 2)[0] + "-" + row.legacy_path.parent.name.split("-", 2)[1])
    discovered = _grep_consumers(
        str(repo_root.resolve()), manifest.baseline_commit, tuple(patterns)
    )
    sibling_consumers: set[pathlib.PurePosixPath] = set()
    if row.role != "domain-readme":
        for other in manifest.files:
            if other.legacy_path.parent != row.legacy_path.parent or other == row:
                continue
            source = _source_text(
                str(repo_root.resolve()), manifest.baseline_commit, other.legacy_path.as_posix()
            )
            if source is not None and row.legacy_path.name in source:
                sibling_consumers.add(other.legacy_path)
    return tuple(
        sorted(
            {
                path
                for path in (*discovered, *sibling_consumers)
                if path != row.legacy_path and _current_consumer(path)
            },
            key=lambda item: item.as_posix(),
        )
    )


def _final_consumer_path(
    manifest: OperationsCatalogManifest,
    consumer: pathlib.PurePosixPath,
) -> pathlib.PurePosixPath:
    for row in manifest.files:
        if row.legacy_path == consumer and row.final_path is not None:
            return row.final_path
    for subject in manifest.subjects:
        try:
            suffix = consumer.relative_to(subject.legacy_subject_path)
        except ValueError:
            continue
        return subject.final_path / suffix
    return consumer


def _expected_approval_rows(
    manifest: OperationsCatalogManifest,
) -> tuple[tuple[str, str, str, str, str, str], ...]:
    files_by_subject: defaultdict[pathlib.PurePosixPath, list[OperationFileRecord]] = defaultdict(list)
    for row in manifest.files:
        if row.role != "domain-readme":
            files_by_subject[row.legacy_path.parent].append(row)
    role_order = {"guide": 0, "policy": 1, "runbook": 2}
    expected = []
    for subject in manifest.subjects:
        files = sorted(files_by_subject[subject.legacy_subject_path], key=lambda row: role_order[row.role])
        verb = "merge" if subject.semantic_action == "merge" else "retain"
        roles = f"{verb} " + ", ".join(row.role for row in files)
        if subject.semantic_action == "merge":
            roles += "; remove predecessor after approved semantic execution"
        expected.append(
            (
                subject.current_ops_id,
                subject.final_path.as_posix(),
                subject.semantic_action,
                subject.canonical_ops_id,
                roles,
                subject.reason,
            )
        )
    return tuple(expected)


def validate_subject_disposition(
    row: OperationSubjectRecord,
) -> tuple[CatalogFinding, ...]:
    """Validate a semantic subject proposal, including all four merge proofs."""

    findings: list[CatalogFinding] = []
    if row.semantic_action == "merge":
        if not row.owner_match:
            findings.append(_finding("merge-owner-boundary-unproven", row.current_ops_id, "operational owner does not match"))
        if not row.control_boundary_match:
            findings.append(_finding("merge-control-boundary-unproven", row.current_ops_id, "control boundary does not match"))
        if not row.trigger_and_recovery_match:
            findings.append(_finding("merge-trigger-recovery-unproven", row.current_ops_id, "trigger, verification, and recovery boundary do not match"))
        if row.independent_evidence_boundary:
            findings.append(_finding("merge-independent-evidence-boundary", row.current_ops_id, "subject owns independent review or evidence"))
        if row.merge_into is None:
            findings.append(_finding("merge-target-missing", row.current_ops_id, "merge requires merge_into"))
        elif row.merge_into == row.current_ops_id:
            findings.append(_finding("merge-self", row.current_ops_id, "subject cannot merge into itself"))
        elif row.canonical_ops_id != row.merge_into:
            findings.append(_finding("merge-target-mismatch", row.current_ops_id, "canonical ID must equal merge target"))
    elif row.merge_into is not None:
        findings.append(_finding("merge-target-unexpected", row.current_ops_id, "non-merge action forbids merge_into"))
    return tuple(sorted(findings))


def find_operations_merge_candidates(
    subjects: Iterable[OperationSubjectRecord],
) -> tuple[OperationSubjectRecord, ...]:
    """Return only manifest rows whose four merge criteria are fully proven."""

    return tuple(
        row
        for row in subjects
        if row.semantic_action == "merge" and not validate_subject_disposition(row)
    )


def _duplicates(values: Iterable[object]) -> set[object]:
    counts = Counter(values)
    return {value for value, count in counts.items() if count > 1}


def _section_tokens(text: str) -> set[str]:
    matches = list(re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", text))
    tokens: set[str] = set()
    for index, match in enumerate(matches):
        slug = re.sub(r"[^a-z0-9]+", "-", match.group(1).lower()).strip("-")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.start():end].strip()
        tokens.add(f"section:{slug}:{hashlib.sha256(section.encode()).hexdigest()[:12]}")
    return tokens


def _semantic_section_tokens(
    text: str,
    row: OperationFileRecord,
    manifest: OperationsCatalogManifest,
    source_path: pathlib.PurePosixPath,
    removed_fragments: tuple[str, ...] = (),
) -> tuple[set[str], bool]:
    normalized = text
    unsafe = False
    for fragment in removed_fragments:
        normalized = normalized.replace(fragment, "")
    canonical_targets: dict[pathlib.PurePosixPath, pathlib.PurePosixPath] = {}
    for file_row in manifest.files:
        target = file_row.final_path or file_row.catalog_path
        canonical_targets[file_row.legacy_path] = target
        canonical_targets[file_row.catalog_path] = target
        if file_row.final_path is not None:
            canonical_targets[file_row.final_path] = target
    for subject in manifest.subjects:
        canonical_targets[subject.legacy_subject_path] = subject.final_path
        canonical_targets[subject.catalog_path] = subject.final_path
        canonical_targets[subject.final_path] = subject.final_path
    for link in parse_local_markdown_links(source_path, normalized):
        if link.has_unsafe_target:
            unsafe = True
            continue
        target = canonical_targets.get(link.target, link.target)
        identity = f"{target.as_posix()}#{link.fragment or ''}"
        marker = f"<link:{hashlib.sha256(identity.encode()).hexdigest()[:16]}>"
        normalized = normalized.replace(
            f"]({link.raw_target}",
            f"]({marker}",
        ).replace(
            f"](<{link.raw_target}>",
            f"](<{marker}>",
        )
    replacements: dict[str, str] = {
        row.legacy_path.as_posix(): "<role-path>",
        row.catalog_path.as_posix(): "<role-path>",
        row.legacy_path.parent.as_posix(): "<subject-path>",
        row.catalog_path.parent.as_posix(): "<subject-path>",
        row.legacy_path.parent.name: "<subject-name>",
        row.catalog_path.parent.name: "<subject-name>",
    }
    if row.final_path is not None:
        replacements[row.final_path.as_posix()] = "<role-path>"
        replacements[row.final_path.parent.as_posix()] = "<subject-path>"
        replacements[row.final_path.parent.name] = "<subject-name>"
    for index, file_row in enumerate(manifest.files):
        if file_row.final_path is None:
            continue
        # Keep replacement markers opaque.  Embedding a path in the marker lets
        # later subject-path substitutions rewrite the marker itself, making an
        # equivalent legacy-to-final link rewrite hash differently.
        marker = f"<file-row:{index:04d}>"
        replacements[file_row.legacy_path.as_posix()] = marker
        replacements[file_row.catalog_path.as_posix()] = marker
        replacements[file_row.final_path.as_posix()] = marker
    for subject in manifest.subjects:
        marker = f"<subject:{subject.canonical_ops_id}>"
        replacements[subject.legacy_subject_path.as_posix()] = marker
        replacements[subject.catalog_path.as_posix()] = marker
        replacements[subject.final_path.as_posix()] = marker
        if subject.legacy_subject_path.name != subject.final_path.name:
            replacements[subject.legacy_subject_path.name] = marker
            replacements[subject.final_path.name] = marker
    for domain in sorted({subject.catalog_domain for subject in manifest.subjects}):
        marker = f"<catalog-domain:{domain}>"
        replacements[f"docs/05.operations/{domain}"] = marker
        replacements[f"docs/05.operations/catalog/{domain}"] = marker
        replacements[f"05.operations/{domain}"] = marker
        replacements[f"05.operations/catalog/{domain}"] = marker
    for value, marker in sorted(
        replacements.items(), key=lambda item: len(item[0]), reverse=True
    ):
        normalized = normalized.replace(value, marker)
    return _section_tokens(normalized), unsafe


def _structural_body_normalization(
    text: str,
    source_path: pathlib.PurePosixPath,
    domains: frozenset[str],
) -> tuple[str, bool]:
    """Normalize only approved domain-prefix and safe Markdown link rebases."""

    normalized = text
    unsafe = False
    for link in parse_local_markdown_links(source_path, text):
        if link.has_unsafe_target:
            unsafe = True
            continue
        target = link.target
        parts = target.parts
        if (
            len(parts) >= 4
            and parts[:3] == ("docs", "05.operations", "catalog")
            and parts[3] in domains
        ):
            target = pathlib.PurePosixPath("docs/05.operations", *parts[3:])
        identity = f"{target.as_posix()}#{link.fragment or ''}"
        marker = f"<structural-link:{hashlib.sha256(identity.encode()).hexdigest()[:16]}>"
        normalized = normalized.replace(
            f"]({link.raw_target}",
            f"]({marker}",
        ).replace(
            f"](<{link.raw_target}>",
            f"](<{marker}>",
        )
    for domain in sorted(domains):
        marker = f"<structural-domain:{domain}>"
        for prefix in (
            f"docs/05.operations/catalog/{domain}",
            f"docs/05.operations/{domain}",
            f"05.operations/catalog/{domain}",
            f"05.operations/{domain}",
        ):
            normalized = normalized.replace(prefix, marker)
    return normalized, unsafe


def _removed_text_fragments(row: OperationFileRecord) -> tuple[str, ...]:
    return tuple(
        item.split(":", 2)[2]
        for item in row.removed_semantics
        if item.startswith("remove-text:") and item.count(":") >= 2
    )


def _has_symlink_component(
    root: pathlib.Path, path: pathlib.PurePosixPath
) -> bool:
    return any(
        root.joinpath(*path.parts[:index]).is_symlink()
        for index in range(1, len(path.parts) + 1)
    )


def _validate_subjects(
    repo_root: pathlib.Path,
    manifest: OperationsCatalogManifest,
    expected_subjects: set[str],
) -> list[CatalogFinding]:
    findings: list[CatalogFinding] = []
    actual_sources = {row.legacy_subject_path.as_posix() for row in manifest.subjects}
    if actual_sources != expected_subjects:
        findings.append(_finding("subject-inventory-mismatch", "subjects", f"missing={sorted(expected_subjects - actual_sources)} extra={sorted(actual_sources - expected_subjects)}"))
    if list(actual_sources) and tuple(row.legacy_subject_path.as_posix() for row in manifest.subjects) != tuple(sorted(actual_sources)):
        findings.append(_finding("subject-order-invalid", "subjects", "subjects must be ordered by legacy_subject_path"))
    for value in _duplicates(row.legacy_subject_path for row in manifest.subjects):
        findings.append(_finding("duplicate-subject-source", value, "legacy subject source is duplicated"))
    for value in _duplicates(row.catalog_path for row in manifest.subjects):
        findings.append(_finding("duplicate-subject-target", value, "structural catalog target is duplicated"))
    for value in _duplicates(row.current_ops_id for row in manifest.subjects):
        findings.append(_finding("duplicate-subject-id", value, "current ops identity is duplicated"))

    by_id = {row.current_ops_id: row for row in manifest.subjects}
    merge_edges: dict[str, str] = {}
    final_owners: defaultdict[pathlib.PurePosixPath, list[OperationSubjectRecord]] = defaultdict(list)
    for row in manifest.subjects:
        label = row.legacy_subject_path
        if not _safe_path(row.legacy_subject_path) or not _safe_path(row.catalog_path) or not _safe_path(row.final_path):
            findings.append(_finding("unsafe-path", label, "subject path is not safe repository-relative POSIX"))
            continue
        parts = row.legacy_subject_path.parts
        match = _SUBJECT_NAME.fullmatch(row.legacy_subject_path.name)
        if len(parts) != 4 or parts[:2] != ("docs", "05.operations") or _DOMAIN.fullmatch(parts[2]) is None or match is None:
            findings.append(_finding("legacy-subject-path-invalid", label, "legacy subject path shape is invalid"))
            continue
        identity = f"ops-{match.group('identity')}"
        if row.current_ops_id != identity or _OPS_ID.fullmatch(row.current_ops_id) is None:
            findings.append(_finding("current-ops-id-invalid", label, "current_ops_id does not match source path"))
        if row.catalog_domain != parts[2] or _DOMAIN.fullmatch(row.catalog_domain) is None:
            findings.append(_finding("catalog-domain-invalid", label, "catalog domain does not match source"))
        expected_catalog = pathlib.PurePosixPath("docs/05.operations/catalog") / row.catalog_domain / row.legacy_subject_path.name
        if row.catalog_path != expected_catalog:
            findings.append(_finding("catalog-path-invalid", label, f"expected {expected_catalog}"))
        if _OPS_ID.fullmatch(row.canonical_ops_id) is None or _SLUG.fullmatch(row.canonical_slug) is None:
            findings.append(_finding("canonical-identity-invalid", label, "canonical ID or slug is invalid"))
        tokens = row.canonical_slug.split("-")
        domain_slug = row.catalog_domain.split("-", 1)[1]
        if (
            _FORBIDDEN_SLUG_TOKENS.intersection(tokens)
            or any(tokens[index] == tokens[index - 1] for index in range(1, len(tokens)))
            or row.canonical_slug == domain_slug
            or row.canonical_slug.endswith(("-basics", "-setup"))
            or row.canonical_slug in {"basics", "setup"}
        ):
            findings.append(_finding("canonical-slug-invalid", label, row.canonical_slug))
        expected_final = pathlib.PurePosixPath("docs/05.operations/catalog") / row.catalog_domain / f"{row.canonical_ops_id}-{row.canonical_slug}"
        if row.final_path != expected_final:
            findings.append(_finding("final-path-invalid", label, f"expected {expected_final}"))
        if row.semantic_action == "retain" and (row.canonical_ops_id != row.current_ops_id or row.final_path != row.catalog_path):
            findings.append(_finding("retain-target-invalid", label, "retain must preserve identity and catalog path"))
        if row.semantic_action == "rename" and (row.canonical_ops_id != row.current_ops_id or row.final_path == row.catalog_path):
            findings.append(_finding("rename-target-invalid", label, "rename preserves ID and changes slug"))
        if not row.reason.strip():
            findings.append(_finding("reason-missing", label, "reason must be non-empty"))
        findings.extend(validate_subject_disposition(row))
        if row.semantic_action == "merge" and row.merge_into is not None:
            merge_edges[row.current_ops_id] = row.merge_into
            if row.merge_into not in by_id:
                findings.append(_finding("merge-target-unknown", label, row.merge_into))
        final_owners[row.final_path].append(row)

        if row.source_commit != manifest.baseline_commit:
            findings.append(_finding("source-commit-mismatch", label, "subject source commit differs from baseline"))
        object_id, kind = _git_object(
            str(repo_root.resolve()),
            row.source_commit,
            row.legacy_subject_path.as_posix(),
        )
        if (
            object_id is None
            or _OBJECT_ID.fullmatch(row.source_tree) is None
            or row.source_tree != object_id
            or kind != "tree"
        ):
            findings.append(_finding("source-tree-mismatch", label, "source tree does not resolve exactly"))

    for target, owners in final_owners.items():
        if len(owners) <= 1:
            continue
        canonical = [row for row in owners if row.semantic_action != "merge"]
        merged = [row for row in owners if row.semantic_action == "merge"]
        if len(canonical) != 1 or any(row.merge_into != canonical[0].current_ops_id for row in merged):
            findings.append(_finding("duplicate-final-subject-owner", target, "final subject ownership is ambiguous"))

    for origin in sorted(merge_edges):
        visited: set[str] = set()
        current = origin
        while current in merge_edges:
            if current in visited:
                findings.append(_finding("merge-cycle", origin, "subject merge graph contains a cycle"))
                break
            visited.add(current)
            current = merge_edges[current]
    return findings


def _validate_files(
    repo_root: pathlib.Path,
    manifest: OperationsCatalogManifest,
    expected_files: set[str],
) -> list[CatalogFinding]:
    findings: list[CatalogFinding] = []
    actual_sources = {row.legacy_path.as_posix() for row in manifest.files}
    if actual_sources != expected_files:
        findings.append(_finding("file-inventory-mismatch", "files", f"missing={sorted(expected_files - actual_sources)} extra={sorted(actual_sources - expected_files)}"))
    if tuple(row.legacy_path.as_posix() for row in manifest.files) != tuple(sorted(actual_sources)):
        findings.append(_finding("file-order-invalid", "files", "files must be ordered by legacy_path"))
    for value in _duplicates(row.legacy_path for row in manifest.files):
        findings.append(_finding("duplicate-file-source", value, "legacy file source is duplicated"))
    for value in _duplicates(row.catalog_path for row in manifest.files):
        findings.append(_finding("duplicate-file-target", value, "structural file target is duplicated"))

    subjects = {row.legacy_subject_path: row for row in manifest.subjects}
    for row in manifest.files:
        label = row.legacy_path
        paths = [
            row.legacy_path,
            row.catalog_path,
            *row.active_consumers,
            *row.final_consumers,
        ]
        if row.final_path is not None:
            paths.append(row.final_path)
        if row.canonical_role_owner is not None:
            paths.append(row.canonical_role_owner)
        if any(not _safe_path(path) for path in paths):
            findings.append(_finding("unsafe-path", label, "file path is not safe repository-relative POSIX"))
            continue
        is_readme = row.legacy_path.name == "README.md"
        expected_role = "domain-readme" if is_readme else row.legacy_path.stem
        if row.role != expected_role:
            findings.append(_finding("file-role-path-mismatch", label, f"expected role {expected_role}"))
        parts = row.legacy_path.parts
        if is_readme:
            if len(parts) != 4 or _DOMAIN.fullmatch(parts[2]) is None:
                findings.append(_finding("domain-readme-path-invalid", label, "domain README path is invalid"))
            expected_catalog = pathlib.PurePosixPath("docs/05.operations/catalog") / parts[2] / "README.md"
            if row.canonical_role_owner is not None:
                findings.append(_finding("domain-readme-owner-invalid", label, "domain README has no role owner"))
        else:
            subject = subjects.get(row.legacy_path.parent)
            if subject is None:
                findings.append(_finding("file-subject-missing", label, "file has no subject row"))
                continue
            expected_catalog = subject.catalog_path / row.legacy_path.name
            expected_final = subject.final_path / row.legacy_path.name
            if row.final_path != expected_final or row.canonical_role_owner != expected_final:
                findings.append(_finding("file-final-owner-mismatch", label, f"expected {expected_final}"))
            expected_action = "merge" if subject.semantic_action == "merge" else ("rewrite" if subject.semantic_action == "rename" else "retain")
            allowed_actions = (
                {"retain", "rewrite", "delete"}
                if subject.semantic_action == "retain"
                else {expected_action}
            )
            if row.semantic_action not in allowed_actions:
                findings.append(_finding("file-action-subject-mismatch", label, f"expected {expected_action}"))
        if row.catalog_path != expected_catalog:
            findings.append(_finding("file-catalog-path-invalid", label, f"expected {expected_catalog}"))
        if row.semantic_action == "delete":
            if row.final_path is not None or row.canonical_role_owner is not None:
                findings.append(_finding("delete-target-invalid", label, "delete forbids final owners"))
        elif row.final_path is None:
            findings.append(_finding("file-final-path-missing", label, "non-delete file requires final_path"))
        if not row.preserved_semantics or tuple(sorted(set(row.preserved_semantics))) != row.preserved_semantics:
            findings.append(_finding("preserved-semantics-invalid", label, "preserved_semantics must be non-empty, unique, and sorted"))
        if tuple(sorted(set(row.removed_semantics))) != row.removed_semantics:
            findings.append(_finding("removed-semantics-invalid", label, "removed_semantics must be unique and sorted"))
        source = _source_text(
            str(repo_root.resolve()), row.source_commit, row.legacy_path.as_posix()
        )
        declared_sections = {
            item for item in row.preserved_semantics if item.startswith("section:")
        }
        if source is None or declared_sections != _section_tokens(source):
            findings.append(
                _finding(
                    "section-preservation-inventory-mismatch",
                    label,
                    "every pinned source section must be frozen exactly once",
                )
            )
        if tuple(sorted(set(row.active_consumers), key=lambda item: item.as_posix())) != row.active_consumers:
            findings.append(_finding("active-consumers-invalid", label, "active_consumers must be safe, unique, and sorted"))
        expected_final_consumers = tuple(
            _final_consumer_path(manifest, consumer)
            for consumer in row.active_consumers
        )
        if row.final_consumers != expected_final_consumers:
            findings.append(
                _finding(
                    "active-consumer-routes-mismatch",
                    label,
                    "every baseline consumer must map in order to its exact final path",
                )
            )
        if row.semantic_action == "merge":
            if not any(
                item.startswith("text:") for item in row.preserved_semantics
            ) or any(
                not item.startswith(("section:", "text:"))
                for item in row.preserved_semantics
            ):
                findings.append(_finding("merge-preserved-semantics-unproven", label, "merge requires complete section inventory and concrete text witness semantics"))
            if not row.removed_semantics or any(
                not item.startswith(("duplicate:", "template-residue:"))
                for item in row.removed_semantics
            ):
                findings.append(_finding("merge-removed-semantics-unproven", label, "merge requires concrete duplicate or template residue semantics"))
        if row.semantic_action == "rewrite" and not row.removed_semantics:
            findings.append(_finding("rewrite-reason-missing", label, "rewrite requires exact removed stale or contradictory semantics"))
        if row.semantic_action == "rewrite" and not any(
            item.startswith("text:") for item in row.preserved_semantics
        ):
            findings.append(_finding("rewrite-preserved-semantics-unproven", label, "rewrite requires a concrete text witness"))
        for item in row.preserved_semantics:
            if not item.startswith("text:"):
                continue
            witness = item.split(":", 2)[2] if item.count(":") >= 2 else ""
            if (
                len(witness) < 24
                or witness.startswith(("artifact_id:", "status:", "parent_ids:", "created:", "updated:", "#", "<!--"))
                or "docs/05.operations/" in witness
                or any(root in witness for root in ("guides/", "policies/", "runbooks/"))
            ):
                findings.append(_finding("text-witness-invalid", label, "text witness must preserve meaningful role body, not metadata or a stale path"))
            if source is None or witness not in _body_text(source):
                findings.append(
                    _finding(
                        "text-witness-source-mismatch",
                        label,
                        "text witness is not derived from the pinned source role body",
                    )
                )
        for fragment in _removed_text_fragments(row):
            if (
                source is None
                or fragment not in _body_text(source)
                or len(fragment) < 24
            ):
                findings.append(
                    _finding(
                        "removed-text-source-mismatch",
                        label,
                        "removed text must be a meaningful exact fragment of the pinned role body",
                    )
                )
        if row.semantic_action == "delete" and not row.preserved_semantics:
            findings.append(_finding("delete-preservation-unproven", label, "delete requires preserved semantics and canonical owner"))
        for consumer in row.active_consumers:
            if consumer.parts[:2] == ("docs", "98.archive") or (
                consumer.parts[:2] == ("docs", "90.references")
                and consumer.as_posix()
                not in {
                    "docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md",
                    "docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md",
                }
            ):
                findings.append(
                    _finding(
                        "active-consumer-historical",
                        label,
                        f"historical or immutable evidence is not an active consumer: {consumer}",
                    )
                )
            if consumer.as_posix() not in _baseline_tracked_paths(
                str(repo_root.resolve()), manifest.baseline_commit
            ):
                findings.append(_finding("active-consumer-untracked", label, consumer.as_posix()))
        expected_consumers = _derived_consumers(repo_root, manifest, row)
        if row.active_consumers != expected_consumers:
            findings.append(
                _finding(
                    "active-consumers-mismatch",
                    label,
                    f"expected exact baseline consumers: {[item.as_posix() for item in expected_consumers]}",
                )
            )
        if row.source_commit != manifest.baseline_commit:
            findings.append(_finding("source-commit-mismatch", label, "file source commit differs from baseline"))
        object_id, kind = _git_object(
            str(repo_root.resolve()), row.source_commit, row.legacy_path.as_posix()
        )
        if kind != "blob" or object_id != row.source_blob:
            findings.append(_finding("source-blob-mismatch", label, "source blob does not resolve exactly"))
    return findings


def _is_real_directory(path: pathlib.Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def _is_real_file(path: pathlib.Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and stat.S_ISREG(path.lstat().st_mode)
    )


def _validate_complete_index(
    path: pathlib.Path,
    relative_path: pathlib.PurePosixPath,
) -> list[CatalogFinding]:
    if _is_real_file(path):
        return []
    return [
        _finding(
            "complete-index-invalid",
            relative_path,
            "final Operations index must be a real regular file",
        )
    ]


def _validate_complete_index_routes(
    path: pathlib.Path,
    relative_path: pathlib.PurePosixPath,
    route_parent: pathlib.PurePosixPath,
    expected_routes: set[pathlib.PurePosixPath],
) -> list[CatalogFinding]:
    if not _is_real_file(path):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return [
            _finding(
                "complete-index-unreadable",
                relative_path,
                "final Operations index must be readable UTF-8",
            )
        ]
    links = parse_local_markdown_links(relative_path, text)
    invalid_routes = tuple(
        link
        for link in links
        if link.has_unsafe_target
    )
    actual_routes = {
        link.target
        for link in links
        if link.is_directory_route
        and not link.has_unsafe_target
        and link.target.parent == route_parent
    }
    findings = [
        _finding(
            "complete-index-route-invalid",
            relative_path,
            "absolute, outside-repository, decoded C0/DEL, and backslash index routes are forbidden: "
            f"{sorted(link.raw_target for link in invalid_routes)}",
        )
    ] if invalid_routes else []
    if actual_routes != expected_routes:
        findings.append(
            _finding(
                "complete-index-routes-mismatch",
                relative_path,
                "expected exact direct directory routes "
                f"{sorted(route.as_posix() for route in expected_routes)}",
            )
        )
    return findings


def _validate_complete_catalog(
    final_root: pathlib.Path,
    manifest: OperationsCatalogManifest,
    domain_names: set[str],
) -> list[CatalogFinding]:
    findings: list[CatalogFinding] = []
    catalog_relative = pathlib.PurePosixPath("docs/05.operations/catalog")
    catalog_root = final_root / catalog_relative
    expected_entries = {"README.md", *domain_names}
    actual_entries = (
        {path.name for path in catalog_root.iterdir()}
        if _is_real_directory(catalog_root)
        else set()
    )
    if actual_entries != expected_entries:
        findings.append(
            _finding(
                "complete-catalog-contents-mismatch",
                catalog_relative,
                f"expected exact contents {sorted(expected_entries)}",
            )
        )
    findings.extend(
        _validate_complete_index(
            catalog_root / "README.md",
            catalog_relative / "README.md",
        )
    )
    findings.extend(
        _validate_complete_index_routes(
            catalog_root / "README.md",
            catalog_relative / "README.md",
            catalog_relative,
            {catalog_relative / domain for domain in domain_names},
        )
    )

    final_subjects = {subject.final_path for subject in manifest.subjects}
    for domain in sorted(domain_names):
        domain_relative = catalog_relative / domain
        domain_root = final_root / domain_relative
        expected_subjects = {
            subject_path.name
            for subject_path in final_subjects
            if subject_path.parent == domain_relative
        }
        expected_children = {"README.md", *expected_subjects}
        actual_children = (
            {path.name for path in domain_root.iterdir()}
            if _is_real_directory(domain_root)
            else set()
        )
        if actual_children != expected_children:
            findings.append(
                _finding(
                    "complete-domain-contents-mismatch",
                    domain_relative,
                    f"expected exact contents {sorted(expected_children)}",
                )
            )

    expected_role_files: dict[pathlib.PurePosixPath, set[str]] = defaultdict(set)
    for row in manifest.files:
        if row.role != "domain-readme" and row.final_path is not None:
            expected_role_files[row.final_path.parent].add(row.final_path.name)
    for subject_relative in sorted(final_subjects):
        subject_root = final_root / subject_relative
        actual_roles = (
            {path.name for path in subject_root.iterdir()}
            if _is_real_directory(subject_root)
            else set()
        )
        expected_roles = expected_role_files[subject_relative]
        if actual_roles != expected_roles:
            findings.append(
                _finding(
                    "complete-subject-contents-mismatch",
                    subject_relative,
                    f"expected exact role files {sorted(expected_roles)}",
                )
            )
        if _is_real_directory(subject_root):
            for subject_readme in subject_root.rglob("README.md"):
                findings.append(
                    _finding(
                        "complete-subject-readme-invalid",
                        subject_readme.relative_to(final_root),
                        "subject directories cannot publish README.md recursively",
                    )
                )
    return findings


def _validate_complete_incidents(final_root: pathlib.Path) -> list[CatalogFinding]:
    findings: list[CatalogFinding] = []
    incidents_relative = pathlib.PurePosixPath("docs/05.operations/incidents")
    incidents_root = final_root / incidents_relative
    findings.extend(
        _validate_complete_index(
            incidents_root / "README.md",
            incidents_relative / "README.md",
        )
    )
    if not _is_real_directory(incidents_root):
        return findings
    for entry in incidents_root.iterdir():
        if entry.name == "README.md":
            continue
        if not _is_real_directory(entry) or _YEAR.fullmatch(entry.name) is None:
            findings.append(
                _finding(
                    "complete-incident-contents-invalid",
                    entry.relative_to(final_root),
                    "incident root allows only README.md and four-digit containment years",
                )
            )
            continue
        for packet in entry.iterdir():
            packet_relative = pathlib.PurePosixPath(packet.relative_to(final_root))
            if (
                not _is_real_directory(packet)
                or _INCIDENT_PACKET.fullmatch(packet.name) is None
            ):
                findings.append(
                    _finding(
                        "complete-incident-contents-invalid",
                        packet_relative,
                        "incident year allows only inc-####-<slug> packet directories",
                    )
                )
                continue
            packet_entries = {child.name for child in packet.iterdir()}
            allowed_entries = {"incident.md", "postmortem.md"}
            roles_are_regular = all(
                _is_real_file(packet / role) for role in packet_entries
            )
            if (
                "incident.md" not in packet_entries
                or not packet_entries <= allowed_entries
                or not roles_are_regular
            ):
                findings.append(
                    _finding(
                        "complete-incident-contents-invalid",
                        packet_relative,
                        "incident packet requires incident.md and permits only optional postmortem.md",
                    )
                )
    return findings


def _validate_complete_releases(final_root: pathlib.Path) -> list[CatalogFinding]:
    findings: list[CatalogFinding] = []
    releases_relative = pathlib.PurePosixPath("docs/05.operations/releases")
    releases_root = final_root / releases_relative
    findings.extend(
        _validate_complete_index(
            releases_root / "README.md",
            releases_relative / "README.md",
        )
    )
    if not _is_real_directory(releases_root):
        return findings
    for packet in releases_root.iterdir():
        if packet.name == "README.md":
            continue
        packet_relative = pathlib.PurePosixPath(packet.relative_to(final_root))
        if (
            not _is_real_directory(packet)
            or _RELEASE_PACKET.fullmatch(packet.name) is None
        ):
            findings.append(
                _finding(
                    "complete-release-contents-invalid",
                    packet_relative,
                    "release root allows only rel-####-<slug> packet directories",
                )
            )
            continue
        packet_entries = {child.name for child in packet.iterdir()}
        if packet_entries != {"release.md"} or not _is_real_file(
            packet / "release.md"
        ):
            findings.append(
                _finding(
                    "complete-release-contents-invalid",
                    packet_relative,
                    "release packet must contain exactly one regular release.md",
                )
            )
    return findings


def _validate_complete_topology(
    final_root: pathlib.Path,
    manifest: OperationsCatalogManifest,
    domain_names: set[str],
) -> list[CatalogFinding]:
    findings: list[CatalogFinding] = []
    operations_relative = pathlib.PurePosixPath("docs/05.operations")
    operations_root = final_root / operations_relative
    expected_entries = {"README.md", "catalog", "incidents", "releases"}
    actual_entries = (
        {path.name for path in operations_root.iterdir()}
        if _is_real_directory(operations_root)
        else set()
    )
    if actual_entries != expected_entries:
        findings.append(
            _finding(
                "complete-root-contents-mismatch",
                operations_relative,
                f"expected exact root entries {sorted(expected_entries)}",
            )
        )
    for required_directory in ("catalog", "incidents", "releases"):
        required_path = operations_root / required_directory
        if not _is_real_directory(required_path):
            findings.append(
                _finding(
                    "complete-required-root-missing",
                    operations_relative / required_directory,
                    "required Operations root must be a real directory",
                )
            )
    root_index = operations_root / "README.md"
    findings.extend(_validate_complete_index(root_index, operations_relative / "README.md"))
    findings.extend(
        _validate_complete_index_routes(
            root_index,
            operations_relative / "README.md",
            operations_relative,
            {
                operations_relative / "catalog",
                operations_relative / "incidents",
                operations_relative / "releases",
            },
        )
    )
    findings.extend(_validate_complete_catalog(final_root, manifest, domain_names))
    findings.extend(_validate_complete_incidents(final_root))
    findings.extend(_validate_complete_releases(final_root))
    return findings


def validate_operations_catalog_manifest(
    root: pathlib.Path,
    manifest: OperationsCatalogManifest,
    *,
    mode: ValidationMode = "manifest",
    domains: tuple[str, ...] = (),
    execution_root: pathlib.Path | None = None,
) -> tuple[CatalogFinding, ...]:
    """Validate the frozen inventory and optionally later execution phases."""

    findings: list[CatalogFinding] = []
    if mode not in _MODES:
        return (_finding("mode-invalid", mode, "unknown validation mode"),)
    if mode == "executed":
        if not domains:
            findings.append(_finding("domains-required", mode, "executed mode requires domains"))
    elif domains:
        findings.append(_finding("domains-unexpected", mode, "only executed mode accepts domains"))

    verified = _git(root, "rev-parse", "--verify", f"{manifest.baseline_commit}^{{commit}}")
    baseline = verified.stdout.strip()
    if verified.returncode != 0 or _OBJECT_ID.fullmatch(manifest.baseline_commit) is None or baseline != manifest.baseline_commit:
        findings.append(_finding("baseline-commit-invalid", "manifest", "baseline commit does not resolve exactly"))
        return tuple(sorted(findings))
    expected_subjects, expected_files = _baseline_inventory(root, manifest.baseline_commit)
    if manifest.approval_rows != _expected_approval_rows(manifest):
        findings.append(
            _finding(
                "approval-table-mismatch",
                "Proposed Subject Dispositions",
                "displayed approval rows must exactly equal the machine subject and role dispositions",
            )
        )
    findings.extend(_validate_subjects(root, manifest, expected_subjects))
    findings.extend(_validate_files(root, manifest, expected_files))

    domain_names = {row.catalog_domain for row in manifest.subjects}
    for domain in domains:
        if domain not in domain_names:
            findings.append(_finding("domain-unknown", domain, "domain is not in manifest"))

    if manifest.approval.status == "pending":
        if manifest.approval.approved_at is not None or manifest.approval.approved_by is not None:
            findings.append(_finding("approval-pending-fields", "approval", "pending requires null approval metadata"))
        if mode != "manifest":
            findings.append(_finding("approval-pending", mode, "semantic and structural execution require explicit approval"))
    else:
        if not manifest.approval.approved_at or manifest.approval.approved_by != "user":
            findings.append(_finding("approval-invalid", "approval", "approved requires date and approved_by: user"))

    if mode in {"structure", "executed", "complete"} and manifest.approval.status == "approved":
        final_root = root if execution_root is None else execution_root
        selected = domain_names if mode != "executed" else set(domains)
        for subject in manifest.subjects:
            if subject.catalog_domain not in selected:
                continue
            expected = subject.catalog_path if mode == "structure" else subject.final_path
            target = final_root / expected
            if not target.is_dir():
                findings.append(_finding("executed-subject-missing", expected, "expected subject directory is absent"))
            elif _has_symlink_component(final_root, expected):
                findings.append(
                    _finding(
                        "executed-symlink-invalid",
                        expected,
                        "final subject and its ancestors must be real directories",
                    )
                )
            if mode in {"executed", "complete"}:
                predecessor = final_root / subject.legacy_subject_path
                if predecessor.exists() or predecessor.is_symlink():
                    findings.append(
                        _finding(
                            "executed-predecessor-present",
                            subject.legacy_subject_path,
                            "legacy predecessor must be absent after semantic execution",
                        )
                    )
        selected_files = (
            row
            for row in manifest.files
            if row.legacy_path.parts[2] in selected
            and row.semantic_action != "delete"
            and row.final_path is not None
        )
        for row in selected_files:
            expected_path = row.catalog_path if mode == "structure" else row.final_path
            target = final_root / expected_path
            if not target.is_file():
                findings.append(_finding("executed-file-missing", expected_path, "expected final file is absent"))
                continue
            if target.is_symlink() or not stat.S_ISREG(target.lstat().st_mode):
                findings.append(
                    _finding(
                        "executed-symlink-invalid",
                        expected_path,
                        "final role file must be a real regular file",
                    )
                )
                continue
            try:
                target_text = target.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                findings.append(_finding("executed-file-unreadable", expected_path, "final file is not readable UTF-8"))
                continue
            source_text = _source_text(
                str(root.resolve()),
                row.source_commit,
                row.legacy_path.as_posix(),
            )
            if mode == "structure":
                source_normalized, source_unsafe = _structural_body_normalization(
                    source_text or "",
                    row.legacy_path,
                    _STRUCTURAL_DOMAINS,
                )
                target_normalized, target_unsafe = _structural_body_normalization(
                    target_text,
                    row.catalog_path,
                    _STRUCTURAL_DOMAINS,
                )
                if source_unsafe or target_unsafe:
                    findings.append(
                        _finding(
                            "structural-link-target-unsafe",
                            row.catalog_path,
                            "structural semantic normalization requires safe repository-local Markdown targets",
                        )
                    )
                if source_text is None or source_normalized != target_normalized:
                    findings.append(
                        _finding(
                            "structural-body-mismatch",
                            row.catalog_path,
                            "structural target must equal its pinned source after only approved domain-prefix and link rebases",
                        )
                    )
                continue
            required_text = {
                item.split(":", 2)[2]
                for item in row.preserved_semantics
                if item.startswith("text:") and item.count(":") >= 2
            }
            source_sections, source_link_invalid = _semantic_section_tokens(
                source_text or "",
                row,
                manifest,
                row.legacy_path,
                _removed_text_fragments(row),
            )
            target_sections, target_link_invalid = _semantic_section_tokens(
                target_text,
                row,
                manifest,
                row.final_path,
            )
            if source_link_invalid or target_link_invalid:
                findings.append(
                    _finding(
                        "semantic-link-invalid",
                        row.final_path,
                        "semantic normalization requires safe repository-local Markdown targets",
                    )
                )
            sections_preserved = (
                source_text is not None
                and not source_link_invalid
                and not target_link_invalid
                and source_sections <= target_sections
            )
            if not sections_preserved or (
                row.semantic_action in {"rewrite", "merge"}
                and not all(
                    witness in target_text for witness in required_text
                )
            ):
                findings.append(_finding("preserved-semantics-mismatch", row.final_path, "final body must account for every frozen source section and required text witness"))
            for consumer_path, final_consumer_path in zip(
                row.active_consumers, row.final_consumers, strict=False
            ):
                consumer = final_root / final_consumer_path
                if not consumer.exists() and not consumer.is_symlink():
                    findings.append(
                        _finding(
                            "executed-consumer-missing",
                            final_consumer_path,
                            f"mapped active consumer is absent for {consumer_path}",
                        )
                    )
                    continue
                if (
                    not consumer.is_file()
                    or _has_symlink_component(final_root, final_consumer_path)
                    or not stat.S_ISREG(consumer.lstat().st_mode)
                ):
                    findings.append(
                        _finding(
                            "executed-consumer-symlink-invalid",
                            final_consumer_path,
                            "mapped consumer and its ancestors must be regular and symlink-free",
                        )
                    )
                    continue
                try:
                    consumer_text = consumer.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    findings.append(
                        _finding(
                            "executed-consumer-unreadable",
                            final_consumer_path,
                            "declared active consumer is not readable UTF-8",
                        )
                    )
                    continue
                stale_values = {
                    row.legacy_path.as_posix(),
                    row.legacy_path.parent.as_posix(),
                }
                if row.final_path is not None and (
                    row.final_path.parent.name != row.legacy_path.parent.name
                ):
                    stale_values.add(row.legacy_path.parent.name)
                if row.final_path != row.legacy_path and any(
                    value in consumer_text for value in stale_values
                ):
                    findings.append(
                        _finding(
                            "executed-stale-consumer",
                            final_consumer_path,
                            f"consumer still references predecessor {row.legacy_path}",
                        )
                    )
        if mode == "complete":
            findings.extend(
                _validate_complete_topology(final_root, manifest, domain_names)
            )
    return tuple(sorted(set(findings)))
