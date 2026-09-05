"""Bounded immutable parsing for canonical Stage 03 Spec Packages."""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import selectors
import stat
import subprocess
import time
from collections.abc import Mapping, Sequence


from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.registry import (
    document_type,
    DocumentRegistry,
    load_registry,
)


MAX_SPEC_FILE_BYTES = 4 * 1024 * 1024
MAX_SPEC_PACKAGES = 256
MAX_PACKAGE_ENTRIES = 256
MAX_PACKAGE_TASKS = 128
MAX_PACKAGE_CONTRACTS = 3
MAX_TOTAL_ENTRIES = 4096
MAX_TOTAL_FILE_BYTES = 64 * 1024 * 1024
GIT_COMMAND_TIMEOUT_SECONDS = 30.0
GIT_REAP_TIMEOUT_SECONDS = 1.0
GIT_STREAM_CHUNK_BYTES = 64 * 1024

_PACKAGE_PATH = re.compile(r"(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)")
_TASK_PATH = re.compile(r"tsk-(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)\.md")
_SPEC_ID = re.compile(r"SPEC-[0-9]{4}")
_PLAN_ID = re.compile(r"SPEC-[0-9]{4}-PLAN-[0-9]{4}")
_TASK_ID = re.compile(r"SPEC-[0-9]{4}-TSK-[0-9]{4}")
_EXTERNAL_PARENT_ID = re.compile(r"(?:REQ|AD|ADR|SPEC)-[0-9]{4}")
_RECOVERY_COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_FORBIDDEN_PACKAGE_ROLES = frozenset({"design.md", "tests.md", "task.md"})
_CONTRACT_PROFILES = {
    "openapi.yaml": "openapi-contract",
    "schema.graphql": "graphql-contract",
    "service.proto": "proto-contract",
}
_EXPECTED_PROFILES = {
    "spec": (
        "docs/03.specs/{number:4}-{slug}/spec.md",
        "SPEC-{number:4}",
        "direct",
        "spec",
    ),
    "plan": (
        "docs/03.specs/{package_number:4}-{slug}/plan.md",
        "SPEC-{package_number:4}-PLAN-{member_number:4}",
        "package-member",
        "plan",
    ),
    "task": (
        "docs/03.specs/{package_number:4}-{slug}/tasks/tsk-{task_number:4}-{slug}.md",
        "SPEC-{package_number:4}-TSK-{task_number:4}",
        "package-member",
        "task",
    ),
}


class SpecPackageError(ValueError):
    """Raised when the Stage 03 package surface cannot be trusted."""


@dataclasses.dataclass(frozen=True)
class BranchIntegrationReceipt:
    """One typed handoff for an exact divergent historical package."""

    source_commit: str
    source_package_path: pathlib.PurePosixPath
    source_artifact_id: str
    preserved_package_path: pathlib.PurePosixPath
    target_package_path: pathlib.PurePosixPath
    target_artifact_id: str
    disposition: str


@dataclasses.dataclass(frozen=True)
class SpecDocument:
    """One immutable registered Markdown member of a Spec Package."""

    path: pathlib.PurePosixPath
    profile_id: str
    artifact_id: str
    status: str
    parent_ids: tuple[str, ...]
    branch_integration_receipts: tuple[BranchIntegrationReceipt, ...] = ()


@dataclasses.dataclass(frozen=True)
class SpecPackage:
    """One canonical prefixless Stage 03 package."""

    path: pathlib.Path
    number: str
    slug: str
    spec: SpecDocument
    plan: SpecDocument | None
    tasks: tuple[SpecDocument, ...]
    contracts: tuple[pathlib.PurePosixPath, ...]


@dataclasses.dataclass(frozen=True, order=True)
class SpecPackageFinding:
    """One deterministic Stage 03 lifecycle finding."""

    code: str
    path: str
    message: str


@dataclasses.dataclass(frozen=True)
class _LoadBudget:
    entries: int = 0
    file_bytes: int = 0


@dataclasses.dataclass(frozen=True)
class _ReceiptCarrier:
    receipt: BranchIntegrationReceipt
    task: SpecDocument
    package: SpecPackage
    completed_archive: bool = False


def _directory_snapshot(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _open_directory_at(
    parent_descriptor: int,
    name: str,
    label: str,
) -> tuple[int, tuple[int, int, int, int, int, int]]:
    try:
        metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except OSError as error:
        raise SpecPackageError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise SpecPackageError(f"{label} must be a regular non-symlink directory")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(name, flags, dir_fd=parent_descriptor)
    except OSError as error:
        raise SpecPackageError(f"cannot open {label}: {error}") from error
    opened = os.fstat(descriptor)
    if not stat.S_ISDIR(opened.st_mode) or _directory_snapshot(
        opened
    ) != _directory_snapshot(metadata):
        os.close(descriptor)
        raise SpecPackageError(f"{label} changed while opening")
    return descriptor, _directory_snapshot(opened)


def _open_directory_path(
    path: pathlib.Path,
    label: str,
) -> tuple[int, int, str, tuple[int, int, int, int, int, int]]:
    absolute = pathlib.Path(os.path.abspath(path))
    parts = absolute.parts
    if not parts or parts[0] != os.path.sep or len(parts) < 2:
        raise SpecPackageError(f"{label} path must be an absolute contained path")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor = os.open(os.path.sep, flags)
    try:
        for component in parts[1:-1]:
            if component in {"", ".", ".."}:
                raise SpecPackageError(f"{label} path contains an unsafe component")
            child_descriptor, _ = _open_directory_at(
                parent_descriptor,
                component,
                f"{label} parent",
            )
            os.close(parent_descriptor)
            parent_descriptor = child_descriptor
        name = parts[-1]
        descriptor, snapshot = _open_directory_at(parent_descriptor, name, label)
        return parent_descriptor, descriptor, name, snapshot
    except BaseException:
        os.close(parent_descriptor)
        raise


def _verify_directory_entry(
    parent_descriptor: int,
    name: str,
    descriptor: int,
    snapshot: tuple[int, int, int, int, int, int],
    label: str,
) -> None:
    try:
        final = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        opened = os.fstat(descriptor)
    except OSError as error:
        raise SpecPackageError(f"{label} changed while loading: {error}") from error
    if (
        stat.S_ISLNK(final.st_mode)
        or not stat.S_ISDIR(final.st_mode)
        or _directory_snapshot(final) != snapshot
        or _directory_snapshot(opened) != snapshot
    ):
        raise SpecPackageError(f"{label} changed or became a symlink while loading")


def _bounded_directory_names(
    descriptor: int,
    *,
    label: str,
    limit: int,
    limit_message: str,
    budget: _LoadBudget,
) -> tuple[tuple[str, ...], _LoadBudget]:
    before = _directory_snapshot(os.fstat(descriptor))
    names: list[str] = []
    current = budget
    try:
        with os.scandir(descriptor) as iterator:
            for entry in iterator:
                if len(names) >= limit:
                    raise SpecPackageError(limit_message)
                if current.entries >= MAX_TOTAL_ENTRIES:
                    raise SpecPackageError(
                        "Stage 03 exceeds the aggregate entry budget"
                    )
                if entry.name in {"", ".", ".."}:
                    raise SpecPackageError(f"{label} contains an unsafe entry")
                names.append(entry.name)
                current = dataclasses.replace(
                    current,
                    entries=current.entries + 1,
                )
    except SpecPackageError:
        raise
    except OSError as error:
        raise SpecPackageError(f"cannot enumerate {label}: {error}") from error
    after = _directory_snapshot(os.fstat(descriptor))
    if after != before:
        raise SpecPackageError(f"{label} changed while enumerating")
    return tuple(sorted(names)), current


def _file_snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _read_regular_utf8_at(
    parent_descriptor: int,
    name: str,
    label: str,
    budget: _LoadBudget,
) -> tuple[str, _LoadBudget]:
    try:
        metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except OSError as error:
        raise SpecPackageError(f"cannot stat {label}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise SpecPackageError(f"{label} must be a regular non-symlink file")
    if metadata.st_size > MAX_SPEC_FILE_BYTES:
        raise SpecPackageError(f"{label} exceeds the byte limit")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | os.O_NONBLOCK
    )
    try:
        descriptor = os.open(name, flags, dir_fd=parent_descriptor)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise SpecPackageError(f"{label} changed to a non-regular file")
            if _file_snapshot(opened) != _file_snapshot(metadata):
                raise SpecPackageError(f"{label} changed while opening")
            if opened.st_size > MAX_SPEC_FILE_BYTES:
                raise SpecPackageError(f"{label} exceeds the byte limit")
            if budget.file_bytes + opened.st_size > MAX_TOTAL_FILE_BYTES:
                raise SpecPackageError("Stage 03 exceeds the aggregate byte budget")
            chunks: list[bytes] = []
            length = 0
            while True:
                chunk = os.read(
                    descriptor,
                    min(64 * 1024, MAX_SPEC_FILE_BYTES + 1 - length),
                )
                if not chunk:
                    break
                chunks.append(chunk)
                length += len(chunk)
                if length > MAX_SPEC_FILE_BYTES:
                    raise SpecPackageError(f"{label} exceeds the byte limit")
            verified = os.fstat(descriptor)
            if (
                _file_snapshot(verified) != _file_snapshot(opened)
                or length != opened.st_size
            ):
                raise SpecPackageError(
                    f"{label} changed while reading or produced a short read"
                )
            final = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(final.st_mode) or _file_snapshot(final) != _file_snapshot(
                opened
            ):
                raise SpecPackageError(
                    f"{label} changed or became a symlink while reading"
                )
        finally:
            os.close(descriptor)
    except SpecPackageError:
        raise
    except OSError as error:
        raise SpecPackageError(f"cannot read {label}: {error}") from error
    try:
        text = b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as error:
        raise SpecPackageError(f"{label} must be UTF-8") from error
    return text, dataclasses.replace(
        budget,
        file_bytes=budget.file_bytes + len(b"".join(chunks)),
    )


def _validate_registry_contract(registry: DocumentRegistry) -> None:
    for profile_id, expected in _EXPECTED_PROFILES.items():
        profile = registry.profiles.get(profile_id)
        if not isinstance(profile, Mapping):
            raise SpecPackageError(f"Stage 99 profile is missing: {profile_id}")
        path_pattern, artifact_pattern, identity_relation, lifecycle_id = expected
        if (
            profile.get("path_pattern") != path_pattern
            or profile.get("artifact_id_pattern") != artifact_pattern
            or profile.get("identity_relation") != identity_relation
            or profile.get("lifecycle_id") != lifecycle_id
        ):
            raise SpecPackageError(
                f"Stage 99 Spec Package profile is not canonical: {profile_id}"
            )
        lifecycle = registry.lifecycles.get(lifecycle_id)
        if not isinstance(lifecycle, tuple):
            raise SpecPackageError(f"Stage 99 lifecycle is missing: {lifecycle_id}")
    for filename, profile_id in _CONTRACT_PROFILES.items():
        profile = registry.profiles.get(profile_id)
        expected_path = "docs/03.specs/{package_number:4}-{slug}/contracts/" + filename
        if (
            not isinstance(profile, Mapping)
            or profile.get("path_pattern") != expected_path
            or profile.get("frontmatter_policy") != "absent"
        ):
            raise SpecPackageError(
                f"Stage 99 executable contract profile is not canonical: {profile_id}"
            )


def _string_tuple(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise SpecPackageError(
            f"Spec Package frontmatter {field} must be a string list"
        )
    if len(value) != len(set(value)):
        raise SpecPackageError(
            f"Spec Package frontmatter {field} contains duplicate identities"
        )
    return value


_RECEIPT_FIELDS = frozenset(
    {
        "source_commit",
        "source_package_path",
        "source_artifact_id",
        "preserved_package_path",
        "target_package_path",
        "target_artifact_id",
        "disposition",
    }
)


def _branch_integration_receipts(
    value: object,
) -> tuple[BranchIntegrationReceipt, ...]:
    if value is None:
        return ()
    if not isinstance(value, tuple) or not value:
        raise SpecPackageError(
            "branch_integration_receipts must be a non-empty receipt list"
        )
    receipts: list[BranchIntegrationReceipt] = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != _RECEIPT_FIELDS:
            raise SpecPackageError("branch integration receipt shape is invalid")
        if not all(isinstance(item[field], str) and item[field] for field in item):
            raise SpecPackageError("branch integration receipt values must be strings")
        if _RECOVERY_COMMIT.fullmatch(item["source_commit"]) is None:
            raise SpecPackageError(
                "branch integration receipt source_commit must be a full object ID"
            )
        if any(
            not _safe_repository_path(item[field])
            for field in (
                "source_package_path",
                "preserved_package_path",
                "target_package_path",
            )
        ):
            raise SpecPackageError("branch integration receipt path is unsafe")
        if item["disposition"] != "historical-superseded":
            raise SpecPackageError("branch integration receipt disposition is invalid")
        receipt = BranchIntegrationReceipt(
            source_commit=item["source_commit"],
            source_package_path=pathlib.PurePosixPath(item["source_package_path"]),
            source_artifact_id=item["source_artifact_id"],
            preserved_package_path=pathlib.PurePosixPath(
                item["preserved_package_path"]
            ),
            target_package_path=pathlib.PurePosixPath(item["target_package_path"]),
            target_artifact_id=item["target_artifact_id"],
            disposition=item["disposition"],
        )
        if receipt in receipts:
            raise SpecPackageError("branch integration receipt is duplicated")
        receipts.append(receipt)
    return tuple(receipts)


def _allowed_statuses(
    registry: DocumentRegistry,
    profile_id: str,
) -> tuple[str, ...]:
    lifecycle_id = _EXPECTED_PROFILES[profile_id][3]
    statuses = registry.lifecycles.get(lifecycle_id)
    if not isinstance(statuses, tuple):
        raise SpecPackageError(f"Stage 99 lifecycle is missing: {lifecycle_id}")
    if not all(isinstance(status, str) for status in statuses):
        raise SpecPackageError(
            f"Stage 99 lifecycle statuses are malformed: {lifecycle_id}"
        )
    return statuses


def _parse_document(
    parent_descriptor: int,
    name: str,
    display_path: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    profile_id: str,
    expected_artifact_id: str,
    registry: DocumentRegistry,
    budget: _LoadBudget,
) -> tuple[SpecDocument, _LoadBudget]:
    text, current = _read_regular_utf8_at(
        parent_descriptor,
        name,
        f"Stage 03 {profile_id}",
        budget,
    )
    try:
        record = frontmatter_record_from_text(display_path, text)
    except FrontmatterError as error:
        raise SpecPackageError(str(error)) from error
    if record.metadata.get("type") != document_type(profile_id):
        raise SpecPackageError(
            f"{relative} must declare type: {document_type(profile_id)}"
        )
    artifact_id = record.metadata.get("artifact_id")
    if artifact_id != expected_artifact_id:
        raise SpecPackageError(
            f"{relative} must own {expected_artifact_id}, found {artifact_id!r}"
        )
    status = record.metadata.get("status")
    if not isinstance(status, str) or status not in _allowed_statuses(
        registry, profile_id
    ):
        raise SpecPackageError(
            f"{relative} status is outside the {profile_id} lifecycle: {status!r}"
        )
    parent_ids = _string_tuple(record.metadata.get("parent_ids"), "parent_ids")
    receipts = (
        _branch_integration_receipts(
            record.metadata.get("branch_integration_receipts")
        )
        if profile_id == "task"
        else ()
    )
    return (
        SpecDocument(
            relative,
            profile_id,
            artifact_id,
            status,
            parent_ids,
            receipts,
        ),
        current,
    )


def _validate_spec_parents(document: SpecDocument) -> None:
    if any(
        _EXTERNAL_PARENT_ID.fullmatch(parent) is None for parent in document.parent_ids
    ):
        raise SpecPackageError(
            f"{document.path} Spec parents must use canonical uppercase stable IDs"
        )
    if document.artifact_id in document.parent_ids:
        raise SpecPackageError(f"{document.path} may not parent itself")


def _validate_plan_parents(document: SpecDocument, spec_id: str) -> None:
    if document.parent_ids != (spec_id,):
        raise SpecPackageError(
            f"{document.path} plan parent must be exactly its owning {spec_id}"
        )


def _validate_task_parents(
    document: SpecDocument,
    *,
    spec_id: str,
    plan_id: str | None,
    task_ids: frozenset[str],
) -> None:
    allowed = {spec_id, *task_ids}
    required = {spec_id}
    if plan_id is not None:
        allowed.add(plan_id)
        required.add(plan_id)
    if (
        not required.issubset(document.parent_ids)
        or any(parent not in allowed for parent in document.parent_ids)
        or document.artifact_id in document.parent_ids
    ):
        raise SpecPackageError(
            f"{document.path} task parent is dangling or outside its owning package"
        )


def _validate_execution_states(
    spec: SpecDocument,
    plan: SpecDocument | None,
    tasks: tuple[SpecDocument, ...],
) -> None:
    for task in tasks:
        if task.status not in {"in-progress", "blocked"}:
            continue
        if spec.status != "active":
            raise SpecPackageError(f"{task.path} current Task requires active Spec")
        if plan is not None and plan.status != "active":
            raise SpecPackageError(f"{task.path} current Task requires active Plan")
    if plan is not None and plan.status == "active" and spec.status != "active":
        raise SpecPackageError(f"{plan.path} active Plan requires active Spec")


def _load_contracts(
    package_descriptor: int,
    package_path: pathlib.Path,
    relative_package: pathlib.PurePosixPath,
    budget: _LoadBudget,
) -> tuple[tuple[pathlib.PurePosixPath, ...], _LoadBudget]:
    descriptor, snapshot = _open_directory_at(
        package_descriptor,
        "contracts",
        "Stage 03 contracts",
    )
    try:
        entries, current = _bounded_directory_names(
            descriptor,
            label="Stage 03 contracts",
            limit=MAX_PACKAGE_CONTRACTS,
            limit_message="Stage 03 package contains too many executable contracts",
            budget=budget,
        )
        contracts: list[pathlib.PurePosixPath] = []
        for name in entries:
            if name not in _CONTRACT_PROFILES:
                raise SpecPackageError(f"unregistered Stage 03 contract path: {name}")
            _, current = _read_regular_utf8_at(
                descriptor,
                name,
                "Stage 03 executable contract",
                current,
            )
            contracts.append(relative_package / "contracts" / name)
        _verify_directory_entry(
            package_descriptor,
            "contracts",
            descriptor,
            snapshot,
            "Stage 03 contracts",
        )
        return tuple(contracts), current
    finally:
        os.close(descriptor)


def _load_tasks(
    package_descriptor: int,
    package_path: pathlib.Path,
    relative_package: pathlib.PurePosixPath,
    *,
    package_number: str,
    registry: DocumentRegistry,
    budget: _LoadBudget,
) -> tuple[tuple[SpecDocument, ...], _LoadBudget]:
    descriptor, snapshot = _open_directory_at(
        package_descriptor,
        "tasks",
        "Stage 03 tasks",
    )
    try:
        entries, current = _bounded_directory_names(
            descriptor,
            label="Stage 03 tasks",
            limit=MAX_PACKAGE_TASKS,
            limit_message="Stage 03 package contains too many Task records",
            budget=budget,
        )
        tasks: list[SpecDocument] = []
        seen_numbers: set[str] = set()
        for name in entries:
            match = _TASK_PATH.fullmatch(name)
            if match is None:
                raise SpecPackageError(f"unregistered Stage 03 task path: {name}")
            task_number = match.group("number")
            if task_number in seen_numbers:
                raise SpecPackageError(
                    f"duplicate Task number in Stage 03 package: {task_number}"
                )
            seen_numbers.add(task_number)
            relative = relative_package / "tasks" / name
            task, current = _parse_document(
                descriptor,
                name,
                package_path / "tasks" / name,
                relative,
                profile_id="task",
                expected_artifact_id=f"SPEC-{package_number}-TSK-{task_number}",
                registry=registry,
                budget=current,
            )
            tasks.append(task)
        _verify_directory_entry(
            package_descriptor,
            "tasks",
            descriptor,
            snapshot,
            "Stage 03 tasks",
        )
        return tuple(tasks), current
    finally:
        os.close(descriptor)


def _load_package(
    stage_descriptor: int,
    package: pathlib.Path,
    match: re.Match[str],
    *,
    registry: DocumentRegistry,
    budget: _LoadBudget,
) -> tuple[SpecPackage, _LoadBudget]:
    descriptor, snapshot = _open_directory_at(
        stage_descriptor,
        package.name,
        "Stage 03 package",
    )
    number = match.group("number")
    slug = match.group("slug")
    relative_package = pathlib.PurePosixPath("docs/03.specs", package.name)
    try:
        entries, current = _bounded_directory_names(
            descriptor,
            label="Stage 03 package",
            limit=MAX_PACKAGE_ENTRIES,
            limit_message="Stage 03 package contains too many entries",
            budget=budget,
        )
        allowed = {"README.md", "spec.md", "plan.md", "tasks", "contracts"}
        for name in entries:
            if name in _FORBIDDEN_PACKAGE_ROLES:
                raise SpecPackageError(f"forbidden Stage 03 package role: {name}")
            if name not in allowed:
                raise SpecPackageError(f"unregistered Stage 03 package entry: {name}")
        if "README.md" in entries:
            _, current = _read_regular_utf8_at(
                descriptor,
                "README.md",
                "Stage 03 package README",
                current,
            )
        if "spec.md" not in entries:
            raise SpecPackageError(f"{relative_package} must retain spec.md")
        spec, current = _parse_document(
            descriptor,
            "spec.md",
            package / "spec.md",
            relative_package / "spec.md",
            profile_id="spec",
            expected_artifact_id=f"SPEC-{number}",
            registry=registry,
            budget=current,
        )
        _validate_spec_parents(spec)
        plan: SpecDocument | None = None
        if "plan.md" in entries:
            plan, current = _parse_document(
                descriptor,
                "plan.md",
                package / "plan.md",
                relative_package / "plan.md",
                profile_id="plan",
                expected_artifact_id=f"SPEC-{number}-PLAN-0001",
                registry=registry,
                budget=current,
            )
            _validate_plan_parents(plan, spec.artifact_id)
        tasks: tuple[SpecDocument, ...] = ()
        if "tasks" in entries:
            tasks, current = _load_tasks(
                descriptor,
                package,
                relative_package,
                package_number=number,
                registry=registry,
                budget=current,
            )
        task_ids = frozenset(task.artifact_id for task in tasks)
        if len(task_ids) != len(tasks):
            raise SpecPackageError(f"duplicate Task identity in {relative_package}")
        for task in tasks:
            _validate_task_parents(
                task,
                spec_id=spec.artifact_id,
                plan_id=None if plan is None else plan.artifact_id,
                task_ids=task_ids,
            )
        _validate_execution_states(spec, plan, tasks)
        contracts: tuple[pathlib.PurePosixPath, ...] = ()
        if "contracts" in entries:
            contracts, current = _load_contracts(
                descriptor,
                package,
                relative_package,
                current,
            )
        _verify_directory_entry(
            stage_descriptor,
            package.name,
            descriptor,
            snapshot,
            "Stage 03 package",
        )
        return SpecPackage(package, number, slug, spec, plan, tasks, contracts), current
    finally:
        os.close(descriptor)


def load_spec_packages(
    stage_root: pathlib.Path,
    *,
    registry: DocumentRegistry | None = None,
) -> tuple[SpecPackage, ...]:
    """Load and validate the complete canonical Stage 03 package surface."""

    stage_root = pathlib.Path(stage_root)
    active_registry = load_registry() if registry is None else registry
    _validate_registry_contract(active_registry)
    parent_descriptor, descriptor, stage_name, snapshot = _open_directory_path(
        stage_root,
        "Stage 03",
    )
    try:
        try:
            stage04 = os.stat(
                "04.execution",
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            stage04 = None
        except OSError as error:
            raise SpecPackageError(f"cannot inspect Stage 04: {error}") from error
        if stage04 is not None:
            raise SpecPackageError(
                "Stage 04 must not exist after Spec Package convergence"
            )
        entries, budget = _bounded_directory_names(
            descriptor,
            label="Stage 03",
            limit=MAX_SPEC_PACKAGES + 1,
            limit_message="Stage 03 exceeds the package count limit",
            budget=_LoadBudget(),
        )
        packages: list[SpecPackage] = []
        seen_numbers: set[str] = set()
        for name in entries:
            if name == "README.md":
                _, budget = _read_regular_utf8_at(
                    descriptor,
                    name,
                    "Stage 03 README",
                    budget,
                )
                continue
            match = _PACKAGE_PATH.fullmatch(name)
            if match is None:
                raise SpecPackageError(
                    f"Stage 03 package path is not canonical: {name}"
                )
            if len(packages) >= MAX_SPEC_PACKAGES:
                raise SpecPackageError("Stage 03 exceeds the package count limit")
            number = match.group("number")
            if number in seen_numbers:
                raise SpecPackageError(
                    f"duplicate Stage 03 package identity: SPEC-{number}"
                )
            seen_numbers.add(number)
            package, budget = _load_package(
                descriptor,
                stage_root / name,
                match,
                registry=active_registry,
                budget=budget,
            )
            packages.append(package)
        artifact_ids = tuple(package.spec.artifact_id for package in packages)
        if len(artifact_ids) != len(set(artifact_ids)):
            raise SpecPackageError("duplicate Stage 03 Spec identity")
        _verify_directory_entry(
            parent_descriptor,
            stage_name,
            descriptor,
            snapshot,
            "Stage 03",
        )
        return tuple(packages)
    finally:
        os.close(descriptor)
        os.close(parent_descriptor)


def _documents(
    packages: Sequence[SpecPackage],
) -> dict[pathlib.PurePosixPath, SpecDocument]:
    result: dict[pathlib.PurePosixPath, SpecDocument] = {}
    for package in packages:
        members = [package.spec, *package.tasks]
        if package.plan is not None:
            members.append(package.plan)
        for member in members:
            if member.path in result:
                raise SpecPackageError(
                    f"duplicate Spec Package member path: {member.path}"
                )
            result[member.path] = member
    return result


_TERMINAL_STATUSES = frozenset({"completed", "cancelled", "superseded", "retired"})


def validate_spec_package_lifecycle(
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    *,
    retired_paths: frozenset[pathlib.PurePosixPath] = frozenset(),
    preserved_paths: frozenset[pathlib.PurePosixPath] = frozenset(),
) -> tuple[SpecPackageFinding, ...]:
    """Enforce the Stage 00 retention contract on Spec Package removals.

    A retained package keeps its non-terminal members. A package that leaves
    Stage 03 is either completed or retired, and the two are not the same
    event: completion preserves the finished Spec outcome while transient Plan
    and Task bodies are recoverable from Git; retirement withdraws a package
    and records a Tombstone saying why. A Tombstone is required for the second,
    and asking for one after a completion would record a withdrawal that never
    happened.

    The Spec's terminal status is an authoring obligation recorded in the
    Tombstone's `Reason`, not a predicate here: the comparison base is the
    branch point, so a package that is `active` there can never be observed as
    terminal by the change that retires it.
    """

    previous_documents = _documents(previous)
    current_documents = _documents(current)
    retained_packages = frozenset(package.spec.path.parts[2] for package in current)
    findings: list[SpecPackageFinding] = []
    retired_packages: dict[str, SpecPackage] = {}
    for package in previous:
        if package.spec.path.parts[2] in retained_packages:
            continue
        retired_packages[package.spec.path.parts[2]] = package
    for path, document in sorted(previous_documents.items()):
        if path in current_documents or path.parts[2] not in retained_packages:
            continue
        if document.status not in _TERMINAL_STATUSES:
            findings.append(
                SpecPackageFinding(
                    "execution-evidence-deletion-forbidden",
                    path.as_posix(),
                    "a retained package keeps non-terminal Spec Package members",
                )
            )
    for name, package in sorted(retired_packages.items()):
        if package.spec.path in preserved_paths:
            continue
        if package.spec.path not in retired_paths:
            findings.append(
                SpecPackageFinding(
                    "package-retirement-unrecorded",
                    f"docs/03.specs/{name}",
                    "retirement requires one Stage 98 Tombstone",
                )
            )
    return tuple(findings)


def _bounded_git(
    root: pathlib.Path,
    *arguments: str,
    byte_limit: int,
) -> bytes:
    if type(byte_limit) is not int or byte_limit < 0:
        raise SpecPackageError("Spec Package Git snapshot byte budget is invalid")
    process: subprocess.Popen[bytes] | None = None
    selector = selectors.DefaultSelector()
    streams: list[object] = []

    def reap() -> None:
        if process is None or process.poll() is not None:
            return
        process.kill()
        try:
            process.wait(timeout=GIT_REAP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired as error:
            raise SpecPackageError(
                "cannot reap Spec Package Git snapshot process"
            ) from error

    try:
        process = subprocess.Popen(
            ["git", *arguments],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        if process.stdout is None or process.stderr is None:
            raise SpecPackageError("cannot open Spec Package Git snapshot streams")
        streams = [process.stdout, process.stderr]
        for stream in streams:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, stream is process.stdout)

        deadline = time.monotonic() + GIT_COMMAND_TIMEOUT_SECONDS
        total = 0
        stdout_chunks: list[bytes] = []
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SpecPackageError(
                    "Spec Package Git snapshot exceeded its deadline"
                )
            events = selector.select(remaining)
            if not events:
                if time.monotonic() >= deadline:
                    raise SpecPackageError(
                        "Spec Package Git snapshot exceeded its deadline"
                    )
                continue
            for key, _ in events:
                try:
                    chunk = os.read(
                        key.fd,
                        min(GIT_STREAM_CHUNK_BYTES, byte_limit + 1 - total),
                    )
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                total += len(chunk)
                if total > byte_limit:
                    raise SpecPackageError(
                        "Spec Package Git snapshot exceeds the byte budget"
                    )
                if key.data:
                    stdout_chunks.append(chunk)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise SpecPackageError("Spec Package Git snapshot exceeded its deadline")
        try:
            return_code = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            raise SpecPackageError(
                "Spec Package Git snapshot exceeded its deadline"
            ) from error
        if return_code != 0:
            raise SpecPackageError("cannot read Spec Package Git snapshot")
        return b"".join(stdout_chunks)
    except SpecPackageError:
        reap()
        raise
    except OSError as error:
        reap()
        raise SpecPackageError(
            f"cannot read Spec Package Git snapshot: {error}"
        ) from error
    finally:
        selector.close()
        for stream in streams:
            stream.close()


def _safe_repository_path(value: str) -> bool:
    path = pathlib.PurePosixPath(value)
    return (
        bool(value)
        and not value.startswith("-")
        and not path.is_absolute()
        and all(
            part not in {"", ".", ".."}
            and not part.startswith("-")
            and "\\" not in part
            and not any(ord(character) < 32 or ord(character) == 127 for character in part)
            for part in path.parts
        )
        and path.as_posix() == value
    )


def _canonical_package_path(path: pathlib.PurePosixPath) -> bool:
    return (
        len(path.parts) == 3
        and path.parts[:2] == ("docs", "03.specs")
        and _PACKAGE_PATH.fullmatch(path.parts[2]) is not None
        and _safe_repository_path(path.as_posix())
    )


def _filesystem_package_tree(
    root: pathlib.Path,
    package_path: pathlib.PurePosixPath,
) -> Mapping[pathlib.PurePosixPath, bytes]:
    if not _safe_repository_path(package_path.as_posix()):
        raise SpecPackageError("preserved package path is unsafe")
    absolute = pathlib.Path(root) / package_path.as_posix()
    parent, descriptor, name, snapshot = _open_directory_path(
        absolute,
        "preserved Spec Package",
    )
    files: dict[pathlib.PurePosixPath, bytes] = {}
    budget = _LoadBudget()

    def visit(
        directory_descriptor: int,
        relative: pathlib.PurePosixPath,
        depth: int,
    ) -> None:
        nonlocal budget
        if depth > 3:
            raise SpecPackageError("preserved Spec Package nesting is too deep")
        entries, budget = _bounded_directory_names(
            directory_descriptor,
            label="preserved Spec Package",
            limit=MAX_PACKAGE_ENTRIES,
            limit_message="preserved Spec Package contains too many entries",
            budget=budget,
        )
        for entry in entries:
            entry_path = relative / entry
            try:
                metadata = os.stat(
                    entry,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
            except OSError as error:
                raise SpecPackageError(
                    f"cannot stat preserved Spec Package entry: {error}"
                ) from error
            if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
                child, child_snapshot = _open_directory_at(
                    directory_descriptor,
                    entry,
                    "preserved Spec Package directory",
                )
                try:
                    visit(child, entry_path, depth + 1)
                    _verify_directory_entry(
                        directory_descriptor,
                        entry,
                        child,
                        child_snapshot,
                        "preserved Spec Package directory",
                    )
                finally:
                    os.close(child)
                continue
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise SpecPackageError(
                    "preserved Spec Package entries must be regular files or directories"
                )
            text, budget = _read_regular_utf8_at(
                directory_descriptor,
                entry,
                "preserved Spec Package file",
                budget,
            )
            files[entry_path] = text.encode("utf-8")
            if len(files) > MAX_PACKAGE_ENTRIES:
                raise SpecPackageError("preserved Spec Package file limit exceeded")

    try:
        visit(descriptor, pathlib.PurePosixPath(), 0)
        _verify_directory_entry(
            parent,
            name,
            descriptor,
            snapshot,
            "preserved Spec Package",
        )
    finally:
        os.close(descriptor)
        os.close(parent)
    return files


def _git_package_tree(
    root: pathlib.Path,
    commit: str,
    package_path: pathlib.PurePosixPath,
) -> Mapping[pathlib.PurePosixPath, bytes]:
    if not _canonical_package_path(package_path):
        raise SpecPackageError("source package path is not canonical")
    tree = _bounded_git(
        root,
        "ls-tree",
        "-r",
        "-z",
        commit,
        "--",
        package_path.as_posix(),
        byte_limit=4 * 1024 * 1024,
    )
    files: dict[pathlib.PurePosixPath, bytes] = {}
    total_bytes = 0
    prefix = package_path.as_posix() + "/"
    for raw in tree.split(b"\0"):
        if not raw:
            continue
        try:
            metadata, raw_path = raw.split(b"\t", 1)
            mode, object_type, _ = metadata.split(b" ", 2)
            source = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise SpecPackageError("source package Git tree is malformed") from error
        if mode not in {b"100644", b"100755"} or object_type != b"blob":
            raise SpecPackageError("source package contains a non-regular Git object")
        if not source.startswith(prefix) or not _safe_repository_path(source):
            raise SpecPackageError("source package Git path is unsafe")
        relative = pathlib.PurePosixPath(source[len(prefix) :])
        if not relative.parts or relative in files:
            raise SpecPackageError("source package Git path is duplicated")
        payload = _bounded_git(
            root,
            "show",
            f"{commit}:{source}",
            byte_limit=MAX_SPEC_FILE_BYTES,
        )
        total_bytes += len(payload)
        if total_bytes > MAX_TOTAL_FILE_BYTES:
            raise SpecPackageError("source package exceeds the aggregate byte limit")
        files[relative] = payload
        if len(files) > MAX_PACKAGE_ENTRIES:
            raise SpecPackageError("source package file limit exceeded")
    if pathlib.PurePosixPath("spec.md") not in files:
        raise SpecPackageError("source package has no spec.md")
    return files


def _matches_existing_regular_blob(
    root: pathlib.Path,
    path: pathlib.PurePosixPath,
    payload: bytes,
) -> bool:
    """Match an archive body only against an already committed lineage."""

    for reference in ("HEAD", "MERGE_HEAD"):
        try:
            commit = (
                _bounded_git(
                    root,
                    "rev-parse",
                    "--verify",
                    "--end-of-options",
                    f"{reference}^{{commit}}",
                    byte_limit=256,
                )
                .decode("ascii")
                .strip()
            )
            if _RECOVERY_COMMIT.fullmatch(commit) is None:
                continue
            listing = _bounded_git(
                root,
                "ls-tree",
                "-z",
                commit,
                "--",
                path.as_posix(),
                byte_limit=512,
            )
        except (SpecPackageError, UnicodeDecodeError):
            continue
        rows = tuple(row for row in listing.split(b"\0") if row)
        if len(rows) != 1:
            continue
        try:
            metadata, raw_path = rows[0].split(b"\t", 1)
            mode, object_type, object_id = metadata.split(b" ", 2)
            listed_path = raw_path.decode("utf-8")
            object_name = object_id.decode("ascii")
        except (ValueError, UnicodeDecodeError):
            continue
        if (
            mode not in {b"100644", b"100755"}
            or object_type != b"blob"
            or listed_path != path.as_posix()
            or _RECOVERY_COMMIT.fullmatch(object_name) is None
        ):
            continue
        try:
            size_text = _bounded_git(
                root,
                "cat-file",
                "-s",
                object_name,
                byte_limit=64,
            ).decode("ascii").strip()
            if not size_text.isdigit() or int(size_text) != len(payload):
                continue
            committed = _bounded_git(
                root,
                "cat-file",
                "blob",
                object_name,
                byte_limit=MAX_SPEC_FILE_BYTES,
            )
        except (SpecPackageError, UnicodeDecodeError):
            continue
        if committed == payload:
            return True
    return False


def _snapshot_document(
    path: pathlib.PurePosixPath,
    text: str,
) -> SpecDocument | None:
    package_match = (
        _PACKAGE_PATH.fullmatch(path.parts[2]) if len(path.parts) >= 4 else None
    )
    if path.parts[:2] != ("docs", "03.specs") or package_match is None:
        return None
    number = package_match.group("number")
    profile_id: str
    artifact_id: str
    if len(path.parts) == 4 and path.name == "spec.md":
        profile_id = "spec"
        artifact_id = f"SPEC-{number}"
    elif len(path.parts) == 4 and path.name == "plan.md":
        profile_id = "plan"
        artifact_id = f"SPEC-{number}-PLAN-0001"
    elif len(path.parts) == 5 and path.parts[3] == "tasks":
        match = _TASK_PATH.fullmatch(path.name)
        if match is None:
            raise SpecPackageError(f"base Task path is not canonical: {path}")
        profile_id = "task"
        artifact_id = f"SPEC-{number}-TSK-{match.group('number')}"
    else:
        return None
    try:
        record = frontmatter_record_from_text(pathlib.Path(path.as_posix()), text)
    except FrontmatterError as error:
        raise SpecPackageError(
            f"cannot parse base Spec Package member: {path}"
        ) from error
    status = record.metadata.get("status")
    parents = record.metadata.get("parent_ids")
    if (
        record.metadata.get("artifact_id") != artifact_id
        or not isinstance(status, str)
        or not isinstance(parents, tuple)
    ):
        raise SpecPackageError(f"base Spec Package metadata is malformed: {path}")
    parent_ids = tuple(parent for parent in parents if isinstance(parent, str))
    if len(parent_ids) != len(parents):
        raise SpecPackageError(f"base Spec Package parents are malformed: {path}")
    receipts = (
        _branch_integration_receipts(
            record.metadata.get("branch_integration_receipts")
        )
        if profile_id == "task"
        else ()
    )
    return SpecDocument(
        path,
        profile_id,
        artifact_id,
        status,
        parent_ids,
        receipts,
    )


def _load_base_spec_packages(
    root: pathlib.Path,
    *,
    base_ref: str,
) -> tuple[SpecPackage, ...]:
    commit = (
        _bounded_git(
            root,
            "rev-parse",
            "--verify",
            f"{base_ref}^{{commit}}",
            byte_limit=256,
        )
        .decode("ascii")
        .strip()
    )
    if _RECOVERY_COMMIT.fullmatch(commit) is None:
        raise SpecPackageError("Spec Package base ref did not resolve to a commit")
    tree = _bounded_git(
        root,
        "ls-tree",
        "-r",
        "-z",
        commit,
        "--",
        "docs/03.specs",
        "docs/04.execution",
        byte_limit=4 * 1024 * 1024,
    )
    documents: dict[pathlib.PurePosixPath, SpecDocument] = {}
    total_bytes = 0
    for raw in tree.split(b"\0"):
        if not raw:
            continue
        try:
            metadata, raw_path = raw.split(b"\t", 1)
            mode = metadata.split(b" ", 1)[0]
            source = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            raise SpecPackageError("Spec Package base tree is malformed") from error
        path = pathlib.PurePosixPath(source)
        if not (
            len(path.parts) >= 4
            and path.parts[:2] == ("docs", "03.specs")
            and _PACKAGE_PATH.fullmatch(path.parts[2]) is not None
            and (
                path.name in {"spec.md", "plan.md"}
                or (len(path.parts) == 5 and path.parts[3] == "tasks")
            )
        ):
            continue
        if mode not in {b"100644", b"100755"}:
            raise SpecPackageError(
                f"base Spec Package member is not a regular blob: {source}"
            )
        payload = _bounded_git(
            root,
            "show",
            f"{commit}:{source}",
            byte_limit=MAX_SPEC_FILE_BYTES,
        )
        if len(payload) > MAX_SPEC_FILE_BYTES:
            raise SpecPackageError(
                f"base Spec Package member exceeds the byte limit: {source}"
            )
        total_bytes += len(payload)
        if total_bytes > MAX_TOTAL_FILE_BYTES:
            raise SpecPackageError("base Spec Package snapshot exceeds aggregate bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise SpecPackageError(
                f"base Spec Package member is not UTF-8: {source}"
            ) from error
        document = _snapshot_document(path, text)
        if document is not None:
            if path in documents:
                raise SpecPackageError(f"duplicate base Spec Package member: {path}")
            documents[path] = document
        if len(documents) > MAX_TOTAL_ENTRIES:
            raise SpecPackageError(
                "base Spec Package snapshot exceeds aggregate entries"
            )
    grouped: dict[str, list[SpecDocument]] = {}
    for document in documents.values():
        grouped.setdefault(document.path.parts[2], []).append(document)
    packages: list[SpecPackage] = []
    for package_name, members in sorted(grouped.items()):
        match = _PACKAGE_PATH.fullmatch(package_name)
        assert match is not None
        specs = [member for member in members if member.profile_id == "spec"]
        plans = [member for member in members if member.profile_id == "plan"]
        tasks = tuple(
            sorted(
                (member for member in members if member.profile_id == "task"),
                key=lambda member: member.path.as_posix(),
            )
        )
        if len(specs) != 1 or len(plans) > 1:
            raise SpecPackageError(
                f"base Spec Package ownership is incomplete: {package_name}"
            )
        packages.append(
            SpecPackage(
                root / "docs/03.specs" / package_name,
                match.group("number"),
                match.group("slug"),
                specs[0],
                plans[0] if plans else None,
                tasks,
                (),
            )
        )
    return tuple(packages)


def _standard_preserved_package_path(
    disposition: str,
    origin: pathlib.PurePosixPath,
) -> pathlib.PurePosixPath:
    if not _canonical_package_path(origin):
        raise SpecPackageError("preserved origin package path is not canonical")
    return pathlib.PurePosixPath("docs/98.archive", disposition, *origin.parts[1:])


def _load_preserved_spec_packages(
    root: pathlib.Path,
    disposition: str,
) -> tuple[SpecPackage, ...]:
    stage = root / f"docs/98.archive/{disposition}/03.specs"
    try:
        metadata = os.lstat(stage)
    except FileNotFoundError:
        return ()
    except OSError as error:
        raise SpecPackageError(
            f"cannot inspect {disposition} Spec archive: {error}"
        ) from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise SpecPackageError(
            f"{disposition} Spec archive must be a non-symlink directory"
        )
    return load_spec_packages(stage)


def _archive_receipt_carriers(
    completed: Sequence[SpecPackage],
) -> tuple[_ReceiptCarrier, ...]:
    return tuple(
        _ReceiptCarrier(receipt, task, package, completed_archive=True)
        for package in completed
        for task in package.tasks
        for receipt in task.branch_integration_receipts
    )


def _current_receipt_carriers(
    current: Sequence[SpecPackage],
) -> tuple[_ReceiptCarrier, ...]:
    return tuple(
        _ReceiptCarrier(receipt, task, package)
        for package in current
        for task in package.tasks
        for receipt in task.branch_integration_receipts
    )


def _ordinary_preserved_paths(
    root: pathlib.Path,
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    completed: Sequence[SpecPackage],
) -> frozenset[pathlib.PurePosixPath]:
    current_names = {package.spec.path.parts[2] for package in current}
    preserved: set[pathlib.PurePosixPath] = set()
    for source in previous:
        if source.spec.path.parts[2] in current_names:
            continue
        for disposition, packages, required_status in (
            ("completed", completed, "completed"),
            ("superseded", (), "superseded"),
        ):
            if _preserved_package_is_terminal(
                root, source, disposition, packages, required_status
            ):
                preserved.add(source.spec.path)
                break
    return frozenset(preserved)


def _preserved_package_is_terminal(
    root: pathlib.Path,
    source: SpecPackage,
    disposition: str,
    packages: Sequence[SpecPackage],
    required_status: str,
) -> bool:
    package = next(
        (
            item
            for item in packages
            if item.spec.path.parent == source.spec.path.parent
        ),
        None,
    )
    if package is not None:
        spec = package.spec
        members = [package.spec, *package.tasks]
        if package.plan is not None:
            members.append(package.plan)
    else:
        try:
            tree = _filesystem_package_tree(
                root,
                _standard_preserved_package_path(
                    disposition, source.spec.path.parent
                ),
            )
            members = [
                document
                for relative, payload in tree.items()
                if (
                    document := _snapshot_document(
                        source.spec.path.parent / relative,
                        payload.decode("utf-8"),
                    )
                )
                is not None
            ]
            spec = next(
                (member for member in members if member.profile_id == "spec"),
                None,
            )
        except (FileNotFoundError, SpecPackageError, UnicodeDecodeError):
            return False
        if spec is None:
            return False
    return (
        spec.artifact_id == source.spec.artifact_id
        and spec.status == required_status
        and all(member.status in _TERMINAL_STATUSES for member in members)
    )


def _invalid_receipt(
    carrier: _ReceiptCarrier,
    message: str,
) -> SpecPackageFinding:
    return SpecPackageFinding(
        "branch-integration-receipt-invalid",
        carrier.task.path.as_posix(),
        message,
    )


def _validate_receipt_carrier(
    root: pathlib.Path,
    base_commit: str,
    source: SpecPackage,
    current: Sequence[SpecPackage],
    completed_packages: Sequence[SpecPackage],
    carrier: _ReceiptCarrier,
) -> SpecPackageFinding | None:
    receipt = carrier.receipt
    origin = source.spec.path.parent
    current_by_path = {package.spec.path.parent: package for package in current}
    if receipt.source_commit != base_commit:
        return _invalid_receipt(carrier, "source_commit is not the lifecycle base")
    if not _canonical_package_path(receipt.source_package_path):
        return _invalid_receipt(carrier, "source_package_path is not canonical")
    if receipt.source_package_path != origin:
        return _invalid_receipt(carrier, "source_package_path does not name the source")
    if receipt.source_artifact_id != source.spec.artifact_id:
        return _invalid_receipt(carrier, "source_artifact_id does not match Git source")
    if origin in current_by_path:
        return _invalid_receipt(carrier, "source package remains in current Stage 03")
    expected_preserved = _standard_preserved_package_path("superseded", origin)
    if receipt.preserved_package_path != expected_preserved:
        return _invalid_receipt(carrier, "preserved_package_path is not the exact handoff path")
    if not _canonical_package_path(receipt.target_package_path):
        return _invalid_receipt(carrier, "target_package_path is not canonical")
    if receipt.target_artifact_id == receipt.source_artifact_id:
        return _invalid_receipt(carrier, "source and target artifact identities must differ")
    if carrier.package.spec.path.parent != receipt.target_package_path:
        return _invalid_receipt(carrier, "receipt is hosted outside its target package")
    if carrier.package.spec.artifact_id != receipt.target_artifact_id:
        return _invalid_receipt(carrier, "target_artifact_id does not match its package")
    if not carrier.completed_archive:
        if carrier.package.spec.status != "active" or carrier.task.status != "in-progress":
            return _invalid_receipt(
                carrier,
                "current carrier requires an active target Spec and in-progress Task",
            )
    else:
        members = [carrier.package.spec, *carrier.package.tasks]
        if carrier.package.plan is not None:
            members.append(carrier.package.plan)
        if (
            carrier.package.plan is None
            or not carrier.package.tasks
            or any(member.status != "completed" for member in members)
        ):
            return _invalid_receipt(
                carrier,
                "archived carrier requires one full completed target package",
            )
    try:
        source_tree = _git_package_tree(root, base_commit, origin)
        preserved_tree = _filesystem_package_tree(
            root,
            receipt.preserved_package_path,
        )
    except (FileNotFoundError, SpecPackageError) as error:
        return _invalid_receipt(carrier, str(error))
    completed = next(
        (
            package
            for package in completed_packages
            if package.spec.path.parent == origin
        ),
        None,
    )
    if completed is None:
        return _invalid_receipt(carrier, "same-origin completed record is missing")
    completed_path = _standard_preserved_package_path("completed", origin)
    try:
        completed_spec_bytes = _filesystem_package_tree(root, completed_path)[
            pathlib.PurePosixPath("spec.md")
        ]
    except (KeyError, FileNotFoundError, SpecPackageError) as error:
        return _invalid_receipt(carrier, str(error))
    if not _matches_existing_regular_blob(
        root,
        completed_path / "spec.md",
        completed_spec_bytes,
    ):
        return _invalid_receipt(
            carrier,
            "completed Spec must match an existing regular Git blob",
        )
    completed_members = [completed.spec, *completed.tasks]
    if completed.plan is not None:
        completed_members.append(completed.plan)
    if (
        completed.spec.artifact_id != receipt.source_artifact_id
        or completed.spec.status != "completed"
        or any(member.status not in _TERMINAL_STATUSES for member in completed_members)
    ):
        return _invalid_receipt(
            carrier,
            "same-origin immutable completed record is missing or invalid",
        )
    if source_tree != preserved_tree:
        return _invalid_receipt(
            carrier,
            "preserved package file set or bytes differ from the Git source",
        )
    return None


def _validate_branch_integration_receipts(
    root: pathlib.Path,
    base_commit: str,
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    completed: Sequence[SpecPackage],
    ordinary_preserved: frozenset[pathlib.PurePosixPath],
) -> tuple[frozenset[pathlib.PurePosixPath], tuple[SpecPackageFinding, ...]]:
    removed = {
        package.spec.path.parent: package
        for package in previous
        if package.spec.path.parts[2]
        not in {item.spec.path.parts[2] for item in current}
    }
    carriers = (*_current_receipt_carriers(current), *_archive_receipt_carriers(completed))
    relevant = tuple(
        carrier
        for carrier in carriers
        if carrier.receipt.source_package_path in removed
        or carrier.receipt.source_commit == base_commit
    )
    findings: list[SpecPackageFinding] = []
    accepted: set[pathlib.PurePosixPath] = set()
    for source_path, source in sorted(removed.items(), key=lambda item: item[0]):
        matching = [
            carrier
            for carrier in relevant
            if carrier.receipt.source_package_path == source_path
        ]
        if len(matching) > 1:
            findings.append(
                SpecPackageFinding(
                    "branch-integration-receipt-duplicate",
                    source_path.as_posix(),
                    "exactly one current or completed Task may carry the receipt",
                )
            )
            continue
        if not matching:
            archived = root / _standard_preserved_package_path(
                "superseded", source_path
            ).as_posix()
            try:
                present = os.lstat(archived) is not None
            except FileNotFoundError:
                present = False
            except OSError:
                present = True
            if present:
                if _preserved_package_is_terminal(
                    root,
                    source,
                    "superseded",
                    (),
                    "superseded",
                ):
                    continue
                findings.append(
                    SpecPackageFinding(
                        "branch-integration-receipt-required",
                        source_path.as_posix(),
                        "a non-lifecycle branch preservation requires one typed Task receipt",
                    )
                )
            elif source.spec.path in ordinary_preserved:
                continue
            continue
        failure = _validate_receipt_carrier(
            root,
            base_commit,
            source,
            current,
            completed,
            matching[0],
        )
        if failure is None:
            accepted.add(source.spec.path)
        else:
            findings.append(failure)
    for carrier in relevant:
        if carrier.receipt.source_package_path not in removed:
            findings.append(
                _invalid_receipt(
                    carrier,
                    "source_package_path does not name a package removed from the base",
                )
            )
    return frozenset(accepted), tuple(findings)


def validate_repository_spec_package_lifecycle(
    root: pathlib.Path,
    current: Sequence[SpecPackage],
    *,
    base_ref: str | None = None,
) -> tuple[SpecPackageFinding, ...]:
    """Validate current removals against a bounded Git snapshot."""

    root = pathlib.Path(root)
    base_commit = resolve_lifecycle_base(root, base_ref)
    previous = _load_base_spec_packages(
        root,
        base_ref=base_commit,
    )
    completed = _load_preserved_spec_packages(root, "completed")
    ordinary_preserved = _ordinary_preserved_paths(
        root,
        previous,
        current,
        completed,
    )
    branch_preserved, receipt_findings = _validate_branch_integration_receipts(
        root,
        base_commit,
        previous,
        current,
        completed,
        ordinary_preserved,
    )
    lifecycle_findings = validate_spec_package_lifecycle(
        previous,
        current,
        retired_paths=_recorded_retirements(root),
        preserved_paths=ordinary_preserved | branch_preserved,
    )
    return tuple(sorted((*receipt_findings, *lifecycle_findings)))


def _recorded_retirements(root: pathlib.Path) -> frozenset[pathlib.PurePosixPath]:
    """Stage 98 Tombstones are the tracked record of an approved retirement."""

    from scripts.lib.document_governance.archive import load_archive

    try:
        inventory = load_archive(pathlib.Path(root) / "docs/98.archive")
    except (OSError, ValueError):
        # Stage 98 has its own gate. An unreadable archive grants no exemption:
        # every removal is judged as unrecorded until the archive is valid.
        return frozenset()
    return frozenset(record.retired_path for record in inventory.tombstones)


def resolve_lifecycle_base(root: pathlib.Path, explicit: str | None = None) -> str:
    """Pin the explicit/CI base; local no-base compares HEAD to working bytes."""

    selected = (
        explicit if explicit is not None else os.environ.get("TEMPLATE_GATE_BASE")
    )
    if selected is None:
        if os.environ.get("EVENT_NAME") in {"pull_request", "push"}:
            raise SpecPackageError("CI lifecycle comparison requires a trusted base")
        selected = "HEAD"
    if (
        not selected
        or selected.startswith("-")
        or any(ord(character) < 32 for character in selected)
    ):
        raise SpecPackageError("lifecycle comparison base is invalid")
    commit = (
        _bounded_git(
            root,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{selected}^{{commit}}",
            byte_limit=256,
        )
        .decode("ascii")
        .strip()
    )
    if _RECOVERY_COMMIT.fullmatch(commit) is None:
        raise SpecPackageError("lifecycle comparison base is not a commit")
    return commit
