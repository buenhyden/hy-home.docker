"""Current-authority validation for Stage 90 reference packages.

Stage 99 defines the three package profiles and frozen Migration 0003 defines
the Task 9 source/target inventory.  Stage 90 is evidence only; it never owns
normative lifecycle policy.
"""

from __future__ import annotations

import dataclasses
import hashlib
import os
import pathlib
import re
import stat
from collections.abc import Sequence

import yaml

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
    parse_frontmatter_text,
)
from scripts.lib.document_governance.links import (
    DocumentLink,
    _unfenced_lines,
    _without_inline_code,
    parse_local_markdown_links,
)
from scripts.lib.document_governance.operations_catalog import read_bounded_regular


MIGRATION_PATH = pathlib.PurePosixPath(
    "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
)
MIGRATION_SHA256 = "271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9"
TASK9_ROW_IDS = tuple(f"mig-0003-r{number:04d}" for number in range(450, 566))
CATEGORIES = ("audits", "data", "research")
PREFIX_BY_CATEGORY = {"audits": "AUD-", "data": "DATA-", "research": "RES-"}
PROFILE_BY_CATEGORY = {"audits": "audit", "data": "data", "research": "research"}
PACKAGE_PATH = re.compile(r"(?:audits|data|research)/[0-9]{4}-[a-z0-9][a-z0-9-]*")
_DATED_PACKAGE = re.compile(r"(?:^|/)[0-9]{4}-[0-9]{2}-[0-9]{2}(?:-|$)")
_ROW = re.compile(r"^- \{row_id: (mig-0003-r[0-9]{4}), .+\}$")
_RETIRED_ROOTS = ("learning", "llm-wiki")
_NORMATIVE_STAGES = ("stage 00", "stage 01", "stage 02", "stage 03", "stage 05")
_ACTIVE_CONSUMER_PATHS = (
    pathlib.PurePosixPath("docs/99.templates/support/document-metadata-profiles.yaml"),
    pathlib.PurePosixPath("scripts/lib/document_governance/operations_catalog.py"),
    pathlib.PurePosixPath("scripts/validation/agent_output_eval.py"),
    pathlib.PurePosixPath("scripts/validation/check-document-corpus-lifecycle.py"),
    pathlib.PurePosixPath("scripts/validation/target_surface_contract.py"),
)
_RETIRED_ACTIVE_PATHS = (
    "docs/90.references/learning",
    "docs/90.references/llm-wiki",
    "docs/90.references/data/governance/",
    "docs/90.references/data/knowledge/",
    "docs/90.references/data/security/",
)

MAX_ROOT_ENTRIES = 8
MAX_CATEGORY_ENTRIES = 128
MAX_PACKAGE_ENTRIES = 64
MAX_REFERENCE_PACKAGES = 128
MAX_TOTAL_REFERENCE_ENTRIES = 512
MAX_REFERENCE_FILE_BYTES = 4 * 1024 * 1024
MAX_TOTAL_REFERENCE_BYTES = 64 * 1024 * 1024
MAX_ACTIVE_CONSUMERS = 32
MAX_ACTIVE_CONSUMER_BYTES = 4 * 1024 * 1024


class ReferenceCorpusError(ValueError):
    """Raised when Stage 90 cannot be enumerated as a trusted corpus."""


@dataclasses.dataclass(frozen=True)
class Task9Row:
    row_id: str
    source_path: pathlib.PurePosixPath
    target_path: pathlib.PurePosixPath | None
    artifact_id: str | None
    action: str


@dataclasses.dataclass(frozen=True)
class Task9Migration:
    rows: tuple[Task9Row, ...]

    @property
    def row_ids(self) -> tuple[str, ...]:
        return tuple(row.row_id for row in self.rows)


@dataclasses.dataclass(frozen=True)
class ReferencePackage:
    category: str
    relative_package: str
    artifact_id: str
    profile_id: str
    text: str
    documents: tuple["ReferenceDocument", ...]

    @property
    def overrides_normative_stage(self) -> bool:
        return _asserts_normative_authority(self.text)


@dataclasses.dataclass(frozen=True)
class ReferenceDocument:
    path: pathlib.PurePosixPath
    text: str


@dataclasses.dataclass(frozen=True)
class ReferenceCorpus:
    category_names: tuple[str, ...]
    packages: tuple[ReferencePackage, ...]
    documents: tuple[ReferenceDocument, ...]
    files: tuple[pathlib.PurePosixPath, ...]


@dataclasses.dataclass(frozen=True)
class Finding:
    code: str
    path: pathlib.PurePosixPath
    detail: str


def _parse_task9_row(line: str) -> Task9Row | None:
    match = _ROW.fullmatch(line)
    if match is None or match.group(1) not in TASK9_ROW_IDS:
        return None
    parsed = yaml.safe_load(line[2:])
    if not isinstance(parsed, dict):
        raise ValueError("Task 9 migration row must be a mapping")
    required = {
        "row_id", "source_path", "target_path", "artifact_id", "action",
        "owner_task", "source_kind", "source_owner_task", "active_consumers",
        "recovery_commit", "status",
    }
    if set(parsed) != required or parsed["owner_task"] != 9:
        raise ValueError("Task 9 migration row has an invalid field contract")
    action = parsed["action"]
    if action not in {"rename", "delete"}:
        raise ValueError("Task 9 migration action must be rename or delete")
    target = parsed["target_path"]
    if action == "rename" and not isinstance(target, str):
        raise ValueError("Task 9 rename row must have a target")
    if action == "delete" and target is not None:
        raise ValueError("Task 9 delete row cannot have a target")
    return Task9Row(
        row_id=parsed["row_id"],
        source_path=pathlib.PurePosixPath(parsed["source_path"]),
        target_path=pathlib.PurePosixPath(target) if target is not None else None,
        artifact_id=parsed["artifact_id"],
        action=action,
    )


def load_task9_migration(root: pathlib.Path) -> Task9Migration:
    raw = read_bounded_regular(root, MIGRATION_PATH)
    if hashlib.sha256(raw).hexdigest() != MIGRATION_SHA256:
        raise ValueError("frozen Migration 0003 hash changed")
    rows = tuple(
        row
        for line in raw.decode("utf-8").splitlines()
        if (row := _parse_task9_row(line)) is not None
    )
    if tuple(row.row_id for row in rows) != TASK9_ROW_IDS:
        raise ValueError("Task 9 migration row range is incomplete or reordered")
    if sum(row.action == "rename" for row in rows) != 105:
        raise ValueError("Task 9 migration must contain exactly 105 renames")
    if sum(row.action == "delete" for row in rows) != 11:
        raise ValueError("Task 9 migration must contain exactly 11 deletions")
    return Task9Migration(rows)


@dataclasses.dataclass(frozen=True)
class _LoadBudget:
    entries: int = 0
    file_bytes: int = 0
    packages: int = 0


def _directory_snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _file_snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _directory_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _open_directory_at(parent: int, name: str, label: str) -> tuple[int, tuple[int, int, int, int, int, int]]:
    try:
        before = os.stat(name, dir_fd=parent, follow_symlinks=False)
    except OSError as exc:
        raise ReferenceCorpusError(f"cannot stat {label}: {exc}") from exc
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISDIR(before.st_mode):
        raise ReferenceCorpusError(f"{label} must be a non-symlink directory")
    try:
        descriptor = os.open(name, _directory_flags(), dir_fd=parent)
    except OSError as exc:
        raise ReferenceCorpusError(f"cannot open {label}: {exc}") from exc
    opened = os.fstat(descriptor)
    if not stat.S_ISDIR(opened.st_mode) or _directory_snapshot(opened) != _directory_snapshot(before):
        os.close(descriptor)
        raise ReferenceCorpusError(f"{label} changed while opening")
    return descriptor, _directory_snapshot(opened)


def _open_directory_path(path: pathlib.Path, label: str) -> tuple[int, int, str, tuple[int, int, int, int, int, int]]:
    absolute = pathlib.Path(os.path.abspath(path))
    if not absolute.is_absolute() or len(absolute.parts) < 2:
        raise ReferenceCorpusError(f"{label} must be an absolute contained path")
    parent = os.open(os.path.sep, _directory_flags())
    try:
        for part in absolute.parts[1:-1]:
            if part in {"", ".", ".."}:
                raise ReferenceCorpusError(f"{label} contains an unsafe path component")
            child, _ = _open_directory_at(parent, part, f"{label} parent")
            os.close(parent)
            parent = child
        name = absolute.parts[-1]
        descriptor, snapshot = _open_directory_at(parent, name, label)
        return parent, descriptor, name, snapshot
    except BaseException:
        os.close(parent)
        raise


def _verify_directory(parent: int, name: str, descriptor: int, snapshot: tuple[int, int, int, int, int, int], label: str) -> None:
    try:
        current = os.stat(name, dir_fd=parent, follow_symlinks=False)
        opened = os.fstat(descriptor)
    except OSError as exc:
        raise ReferenceCorpusError(f"{label} changed while loading: {exc}") from exc
    if (
        stat.S_ISLNK(current.st_mode)
        or not stat.S_ISDIR(current.st_mode)
        or _directory_snapshot(current) != snapshot
        or _directory_snapshot(opened) != snapshot
    ):
        raise ReferenceCorpusError(f"{label} changed while loading")


def _bounded_names(descriptor: int, *, label: str, limit: int, budget: _LoadBudget) -> tuple[tuple[str, ...], _LoadBudget]:
    before = _directory_snapshot(os.fstat(descriptor))
    names: list[str] = []
    current = budget
    try:
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                if len(names) >= limit:
                    raise ReferenceCorpusError(f"{label} exceeds its entry limit")
                if current.entries >= MAX_TOTAL_REFERENCE_ENTRIES:
                    raise ReferenceCorpusError("Stage 90 exceeds the aggregate entry limit")
                if entry.name in {"", ".", ".."}:
                    raise ReferenceCorpusError(f"{label} contains an unsafe entry")
                names.append(entry.name)
                current = dataclasses.replace(current, entries=current.entries + 1)
    except ReferenceCorpusError:
        raise
    except OSError as exc:
        raise ReferenceCorpusError(f"cannot enumerate {label}: {exc}") from exc
    if _directory_snapshot(os.fstat(descriptor)) != before:
        raise ReferenceCorpusError(f"{label} changed while enumerating")
    return tuple(sorted(names)), current


def _entry_metadata(parent: int, name: str, label: str) -> os.stat_result:
    try:
        metadata = os.stat(name, dir_fd=parent, follow_symlinks=False)
    except OSError as exc:
        raise ReferenceCorpusError(f"cannot stat {label}: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ReferenceCorpusError(f"{label} must not be a symlink")
    return metadata


def _read_regular_utf8(parent: int, name: str, label: str, budget: _LoadBudget) -> tuple[str, _LoadBudget]:
    before = _entry_metadata(parent, name, label)
    if not stat.S_ISREG(before.st_mode):
        raise ReferenceCorpusError(f"{label} must be a regular file")
    if before.st_size > MAX_REFERENCE_FILE_BYTES:
        raise ReferenceCorpusError(f"{label} exceeds the file byte limit")
    if budget.file_bytes + before.st_size > MAX_TOTAL_REFERENCE_BYTES:
        raise ReferenceCorpusError("Stage 90 exceeds the aggregate byte limit")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    try:
        descriptor = os.open(name, flags, dir_fd=parent)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode) or _file_snapshot(opened) != _file_snapshot(before):
                raise ReferenceCorpusError(f"{label} changed while opening")
            chunks: list[bytes] = []
            length = 0
            while True:
                chunk = os.read(descriptor, min(64 * 1024, MAX_REFERENCE_FILE_BYTES + 1 - length))
                if not chunk:
                    break
                chunks.append(chunk)
                length += len(chunk)
                if length > MAX_REFERENCE_FILE_BYTES:
                    raise ReferenceCorpusError(f"{label} exceeds the file byte limit")
            verified = os.fstat(descriptor)
            current = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if (
                length != opened.st_size
                or _file_snapshot(verified) != _file_snapshot(opened)
                or stat.S_ISLNK(current.st_mode)
                or _file_snapshot(current) != _file_snapshot(opened)
            ):
                raise ReferenceCorpusError(f"{label} changed or produced a short read")
        finally:
            os.close(descriptor)
    except ReferenceCorpusError:
        raise
    except OSError as exc:
        raise ReferenceCorpusError(f"cannot read {label}: {exc}") from exc
    payload = b"".join(chunks)
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReferenceCorpusError(f"{label} must be UTF-8") from exc
    return text, dataclasses.replace(budget, file_bytes=budget.file_bytes + len(payload))


def _load_package(
    category: str,
    category_descriptor: int,
    package_name: str,
    budget: _LoadBudget,
) -> tuple[ReferencePackage, tuple[pathlib.PurePosixPath, ...], _LoadBudget]:
    if budget.packages >= MAX_REFERENCE_PACKAGES:
        raise ReferenceCorpusError("Stage 90 exceeds the package limit")
    relative_package = f"{category}/{package_name}"
    descriptor, snapshot = _open_directory_at(category_descriptor, package_name, relative_package)
    try:
        names, current = _bounded_names(
            descriptor,
            label=relative_package,
            limit=MAX_PACKAGE_ENTRIES,
            budget=dataclasses.replace(budget, packages=budget.packages + 1),
        )
        if "README.md" not in names:
            raise ReferenceCorpusError(f"{relative_package} is missing README.md")
        documents: list[ReferenceDocument] = []
        files: list[pathlib.PurePosixPath] = []
        readme_text = ""
        for name in names:
            metadata = _entry_metadata(descriptor, name, f"{relative_package}/{name}")
            if not stat.S_ISREG(metadata.st_mode):
                raise ReferenceCorpusError(f"{relative_package}/{name} must be a regular file")
            text, current = _read_regular_utf8(descriptor, name, f"{relative_package}/{name}", current)
            relative = pathlib.PurePosixPath(relative_package) / name
            files.append(relative)
            if name.endswith(".md"):
                documents.append(
                    ReferenceDocument(pathlib.PurePosixPath("docs/90.references") / relative, text)
                )
            if name == "README.md":
                readme_text = text
        _verify_directory(category_descriptor, package_name, descriptor, snapshot, relative_package)
    finally:
        os.close(descriptor)
    try:
        metadata = parse_frontmatter_text(readme_text)
    except FrontmatterError as exc:
        raise ReferenceCorpusError(f"invalid package frontmatter: {relative_package}: {exc}") from exc
    return (
        ReferencePackage(
            category=category,
            relative_package=relative_package,
            artifact_id=str(metadata.get("artifact_id", "")),
            profile_id=str(metadata.get("profile_id", "")),
            text=readme_text,
            documents=tuple(documents),
        ),
        tuple(files),
        current,
    )


def load_reference_packages(references_root: pathlib.Path) -> ReferenceCorpus:
    parent, root_descriptor, root_name, root_snapshot = _open_directory_path(
        references_root, "docs/90.references"
    )
    packages: list[ReferencePackage] = []
    documents: list[ReferenceDocument] = []
    files: list[pathlib.PurePosixPath] = []
    budget = _LoadBudget()
    category_names: list[str] = []
    try:
        root_names, budget = _bounded_names(
            root_descriptor,
            label="docs/90.references",
            limit=MAX_ROOT_ENTRIES,
            budget=budget,
        )
        if "README.md" not in root_names:
            raise ReferenceCorpusError("docs/90.references is missing README.md")
        for name in root_names:
            metadata = _entry_metadata(root_descriptor, name, f"docs/90.references/{name}")
            if name == "README.md":
                text, budget = _read_regular_utf8(
                    root_descriptor, name, "docs/90.references/README.md", budget
                )
                relative = pathlib.PurePosixPath("README.md")
                files.append(relative)
                documents.append(
                    ReferenceDocument(pathlib.PurePosixPath("docs/90.references") / relative, text)
                )
            elif stat.S_ISDIR(metadata.st_mode):
                category_names.append(name)
            else:
                raise ReferenceCorpusError(f"docs/90.references/{name} must be a category directory")

        for category in CATEGORIES:
            if category not in category_names:
                continue
            category_descriptor, category_snapshot = _open_directory_at(
                root_descriptor, category, f"docs/90.references/{category}"
            )
            try:
                names, budget = _bounded_names(
                    category_descriptor,
                    label=f"docs/90.references/{category}",
                    limit=MAX_CATEGORY_ENTRIES,
                    budget=budget,
                )
                if "README.md" not in names:
                    raise ReferenceCorpusError(f"docs/90.references/{category} is missing README.md")
                for name in names:
                    metadata = _entry_metadata(
                        category_descriptor, name, f"docs/90.references/{category}/{name}"
                    )
                    if name == "README.md":
                        text, budget = _read_regular_utf8(
                            category_descriptor,
                            name,
                            f"docs/90.references/{category}/README.md",
                            budget,
                        )
                        relative = pathlib.PurePosixPath(category) / name
                        files.append(relative)
                        documents.append(
                            ReferenceDocument(pathlib.PurePosixPath("docs/90.references") / relative, text)
                        )
                    elif stat.S_ISDIR(metadata.st_mode):
                        package, package_files, budget = _load_package(
                            category, category_descriptor, name, budget
                        )
                        packages.append(package)
                        files.extend(package_files)
                        documents.extend(package.documents)
                    else:
                        raise ReferenceCorpusError(
                            f"docs/90.references/{category}/{name} must be a package directory"
                        )
                _verify_directory(
                    root_descriptor,
                    category,
                    category_descriptor,
                    category_snapshot,
                    f"docs/90.references/{category}",
                )
            finally:
                os.close(category_descriptor)
        _verify_directory(parent, root_name, root_descriptor, root_snapshot, "docs/90.references")
    finally:
        os.close(root_descriptor)
        os.close(parent)
    return ReferenceCorpus(
        tuple(sorted(category_names)),
        tuple(sorted(packages, key=lambda item: item.relative_package)),
        tuple(sorted(documents, key=lambda item: item.path.as_posix())),
        tuple(sorted(files, key=lambda item: item.as_posix())),
    )


def _finding(code: str, path: str | pathlib.PurePosixPath, detail: str) -> Finding:
    return Finding(code, pathlib.PurePosixPath(path), detail)


def _rendered_lines(text: str) -> tuple[str, ...]:
    try:
        body = frontmatter_record_from_text(pathlib.Path("document.md"), text).body
    except FrontmatterError:
        body = text
    return tuple(_without_inline_code(line) for _, line in _unfenced_lines(body))


def _asserts_normative_authority(text: str) -> bool:
    prose = " ".join(_rendered_lines(text)).lower().replace("’", "'")
    prose = re.sub(r"stage\s*([0-9]{1,2})", lambda item: f"stage {int(item.group(1)):02d}", prose)
    prose = prose.replace("stage 90", "stage90")
    for stage in _NORMATIVE_STAGES:
        prose = prose.replace(stage, stage.replace(" ", ""))

    def negated(tokens: list[str], verb_index: int) -> bool:
        authority_predicates = {
            "override", "overrides", "overrode", "overridden", "supersede",
            "supersedes", "superseded", "govern", "governs", "authoritative",
            "normative", "precedence",
        }
        boundaries: set[int] = set()
        for index, token in enumerate(tokens[:verb_index]):
            if token in {"but", "however", "yet", "although", "though", "whereas"}:
                boundaries.add(index)
                continue
            if token == "and":
                previous = max(boundaries, default=-1) + 1
                if not authority_predicates.intersection(tokens[previous:index]):
                    boundaries.add(index)
        clause_start = max(boundaries, default=-1) + 1
        predicate = tokens[clause_start:verb_index]
        return any(
            token in {"not", "never", "cannot", "cant", "mustnt", "shouldnt", "doesnt"}
            for token in predicate
        ) or bool(predicate and predicate[-1] == "non")

    for sentence in re.split(r"(?<=[.!?])\s+|\n+", prose):
        tokens = re.findall(r"[a-z0-9]+", sentence)
        if "stage90" not in tokens:
            continue
        for target in (stage.replace(" ", "") for stage in _NORMATIVE_STAGES):
            if target not in tokens:
                continue
            for stage90_index in (index for index, token in enumerate(tokens) if token == "stage90"):
                for target_index in (index for index, token in enumerate(tokens) if token == target):
                    if stage90_index < target_index:
                        segment = tokens[stage90_index + 1 : target_index]
                        for index, token in enumerate(segment):
                            if token in {
                                "override", "overrides", "overrode", "supersede",
                                "supersedes", "superseded", "govern", "governs",
                                "authoritative", "normative",
                            } and not negated(segment, index):
                                return True
                            if (
                                token in {"take", "takes"}
                                and segment[index : index + 3] in (
                                    ["take", "precedence", "over"],
                                    ["takes", "precedence", "over"],
                                )
                                and not negated(segment, index)
                            ):
                                return True
                    elif target_index < stage90_index:
                        segment = tokens[target_index + 1 : stage90_index]
                        for index, token in enumerate(segment):
                            if (
                                token in {"overridden", "superseded"}
                                and "by" in segment[index + 1 :]
                                and not negated(segment, index)
                            ):
                                return True
    return False


def _is_confined_redirect_target(link: DocumentLink) -> bool:
    return (
        not link.has_unsafe_target
        and re.fullmatch(r"[A-Za-z0-9._~/-]+", link.decoded_target) is not None
    )


def _is_redirect_only(text: str) -> bool:
    lines = tuple(line.strip() for line in _rendered_lines(text) if line.strip())
    if not lines or lines[0].lower() not in {"# redirect", "# moved", "# deprecated"}:
        return False
    transition = lines[1:]
    if not transition or len(transition) > 4 or sum(map(len, transition)) > 2_048:
        return False
    if any(line.startswith("#") for line in transition):
        return False
    for source in transition:
        line = source.lstrip("-* ")
        if line.endswith((".", "!")):
            line = line[:-1].rstrip()
        destination = line
        for prefix in ("replaced by", "redirect to", "moved to", "see", "use"):
            marker = f"{prefix} "
            if line.lower().startswith(marker):
                destination = line[len(marker) :].strip()
                break
        if not destination:
            return False
        source_path = pathlib.PurePosixPath("docs/90.references/redirect.md")
        links = parse_local_markdown_links(source_path, destination)
        if len(links) == 1:
            link = links[0]
            if (
                destination
                in {
                    f"[{link.label}]({link.raw_target})",
                    f"[{link.label}](<{link.raw_target}>)",
                }
                and _is_confined_redirect_target(link)
            ):
                continue
            return False
        if not re.fullmatch(r"[A-Za-z0-9._~%/-]+", destination):
            return False
        raw_links = parse_local_markdown_links(
            source_path, f"[destination](<{destination}>)"
        )
        if (
            len(raw_links) != 1
            or raw_links[0].raw_target != destination
            or not _is_confined_redirect_target(raw_links[0])
        ):
            return False
    return True


def _document_links(document: ReferenceDocument):
    ordinary = parse_local_markdown_links(document.path, document.text)
    with_images = parse_local_markdown_links(document.path, document.text.replace("![", "["))
    unique = {
        (item.line, item.raw_target, item.target.as_posix(), item.absolute, item.outside_repository): item
        for item in (*ordinary, *with_images)
    }
    return tuple(unique[key] for key in sorted(unique))


def _is_retired_reference_target(target: pathlib.PurePosixPath) -> bool:
    if len(target.parts) >= 3 and target.parts[:2] == ("docs", "90.references"):
        if target.parts[2] in _RETIRED_ROOTS:
            return True
        if target.parts[2] == "data" and len(target.parts) >= 4:
            package = target.parts[3]
            return package != "README.md" and PACKAGE_PATH.fullmatch(
                f"data/{package}"
            ) is None
    return False


def _retired_links(document: ReferenceDocument) -> Sequence[str]:
    targets: list[str] = []
    for link in _document_links(document):
        if _is_retired_reference_target(link.target):
            targets.append(link.raw_target)
    return tuple(targets)


_REPOSITORY_MAP_PATH = pathlib.PurePosixPath(
    "docs/90.references/data/0083-repository-map/README.md"
)


def _missing_repository_map_links(
    root: pathlib.Path,
    document: ReferenceDocument,
) -> Sequence[str]:
    if document.path != _REPOSITORY_MAP_PATH:
        return ()
    missing: list[str] = []
    for link in _document_links(document):
        target = root / link.target
        if link.has_unsafe_target or target.is_symlink() or not target.exists():
            missing.append(link.raw_target)
    return tuple(missing)


def validate_active_reference_consumers(
    root: pathlib.Path,
    paths: Sequence[pathlib.PurePosixPath] = _ACTIVE_CONSUMER_PATHS,
) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    if len(paths) > MAX_ACTIVE_CONSUMERS:
        return (_finding("active-consumer-limit", "scripts", "too many consumers"),)
    total = 0
    for relative in sorted(set(paths), key=lambda item: item.as_posix()):
        try:
            raw = read_bounded_regular(root, relative, max_bytes=MAX_ACTIVE_CONSUMER_BYTES)
            text = raw.decode("utf-8")
        except (OSError, UnicodeError, ValueError) as exc:
            findings.append(_finding("active-consumer-unreadable", relative, str(exc)))
            continue
        total += len(raw)
        if total > MAX_ACTIVE_CONSUMER_BYTES:
            findings.append(_finding("active-consumer-limit", relative, "aggregate byte limit"))
            break
        for retired in _RETIRED_ACTIVE_PATHS:
            if retired in text:
                findings.append(_finding("retired-active-reference-path", relative, retired))
    return tuple(findings)


def validate_current_references(root: pathlib.Path) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    references_root = root / "docs/90.references"
    migration = load_task9_migration(root)

    try:
        corpus = load_reference_packages(references_root)
    except (OSError, UnicodeError, ValueError) as exc:
        return (_finding("reference-corpus-invalid", "docs/90.references", str(exc)),)

    if corpus.category_names != CATEGORIES:
        findings.append(_finding("category-root-invalid", "docs/90.references", repr(corpus.category_names)))
    for retired in _RETIRED_ROOTS:
        if retired in corpus.category_names:
            findings.append(
                _finding(
                    "retired-root-present",
                    pathlib.PurePosixPath("docs/90.references") / retired,
                    retired,
                )
            )

    expected_packages = {
        row.target_path.parent.relative_to(pathlib.PurePosixPath("docs/90.references")).as_posix()
        for row in migration.rows
        if row.target_path is not None
        and row.target_path.parts[:2] == ("docs", "90.references")
    }
    observed_packages = {item.relative_package for item in corpus.packages}
    observed_directories = {item.relative_package for item in corpus.packages}
    for relative in sorted(expected_packages - observed_packages):
        findings.append(_finding("package-missing", f"docs/90.references/{relative}", "missing README"))
    for relative in sorted(observed_packages - expected_packages):
        findings.append(_finding("redirect-document-present", f"docs/90.references/{relative}/README.md", "unregistered package"))
    for relative in sorted(observed_directories - expected_packages):
        findings.append(_finding("package-path-invalid", f"docs/90.references/{relative}", "unregistered or empty package directory"))

    allowed_files = {
        pathlib.PurePosixPath("README.md"),
        *(pathlib.PurePosixPath(category) / "README.md" for category in CATEGORIES),
        *(row.target_path.relative_to(pathlib.PurePosixPath("docs/90.references"))
          for row in migration.rows
          if row.target_path is not None
          and row.target_path.parts[:2] == ("docs", "90.references")),
    }
    # Structured Data payloads carry a package README beside their registered
    # machine file; generated LLM Wiki packages are registered by their owner.
    allowed_files.update(
        pathlib.PurePosixPath(item.relative_package) / "README.md"
        for item in corpus.packages
    )
    for relative in corpus.files:
        if relative not in allowed_files:
            findings.append(_finding("unregistered-reference-file", pathlib.PurePosixPath("docs/90.references") / relative, "not declared by the frozen Task 9 topology"))

    for item in corpus.packages:
        path = pathlib.PurePosixPath("docs/90.references") / item.relative_package / "README.md"
        if not PACKAGE_PATH.fullmatch(item.relative_package) or _DATED_PACKAGE.search(item.relative_package):
            findings.append(_finding("package-path-invalid", path, item.relative_package))
        number = item.relative_package.split("/", 1)[1].split("-", 1)[0]
        expected_id = f"{PREFIX_BY_CATEGORY[item.category]}{number}"
        if item.artifact_id != expected_id or item.profile_id != PROFILE_BY_CATEGORY[item.category]:
            findings.append(_finding("package-identity-invalid", path, f"expected {expected_id}"))
    for document in corpus.documents:
        if _asserts_normative_authority(document.text):
            findings.append(
                _finding(
                    "normative-authority-override",
                    document.path,
                    "Stage 90 is supplementary",
                )
            )
        if _is_redirect_only(document.text):
            findings.append(
                _finding("redirect-document-present", document.path, "redirect-only document")
            )
        for target in _retired_links(document):
            findings.append(_finding("retired-link-present", document.path, target))
        for target in _missing_repository_map_links(root, document):
            findings.append(
                _finding("generated-data-link-missing", document.path, target)
            )

    for row in migration.rows:
        source = root / row.source_path
        if source.exists() or source.is_symlink():
            findings.append(_finding("migration-source-present", row.source_path, row.row_id))
        if row.target_path is not None:
            relative_target = row.target_path.relative_to(
                pathlib.PurePosixPath("docs/90.references")
            )
            if relative_target not in corpus.files:
                findings.append(_finding("migration-target-missing", row.target_path, row.row_id))

    findings.extend(validate_active_reference_consumers(root))

    return tuple(findings)
