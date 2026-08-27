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

import yaml

from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    frontmatter_record_from_text,
)
from scripts.lib.document_governance.registry import DocumentRegistry, load_registry


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
_TASK_PATH = re.compile(
    r"tsk-(?P<number>[0-9]{4})-(?P<slug>[a-z0-9][a-z0-9-]*)\.md"
)
_SPEC_ID = re.compile(r"SPEC-[0-9]{4}")
_PLAN_ID = re.compile(r"plan-[0-9]{4}")
_TASK_ID = re.compile(r"task-[0-9]{4}-[0-9]{4}")
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
        "living",
    ),
    "plan": (
        "docs/03.specs/{package_number:4}-{slug}/plan.md",
        "plan-{package_number:4}",
        "package-member",
        "execution",
    ),
    "task": (
        "docs/03.specs/{package_number:4}-{slug}/tasks/"
        "tsk-{task_number:4}-{slug}.md",
        "task-{package_number:4}-{task_number:4}",
        "package-member",
        "execution",
    ),
}
_MIGRATION_PATH = pathlib.PurePosixPath(
    "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
)
_SINGULAR_TASK_FINALS = {
    "docs/03.specs/0123-agentic-engineering-audit-remediation/task.md": (
        "docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/"
        "tsk-0001-research-pack-extension.md"
    ),
    "docs/03.specs/0134-agent-governance-canonical-convergence/task.md": (
        "docs/03.specs/0134-agent-governance-canonical-convergence/tasks/"
        "tsk-0001-canonical-convergence.md"
    ),
    "docs/03.specs/0135-target-surface-delta-convergence/task.md": (
        "docs/03.specs/0135-target-surface-delta-convergence/tasks/"
        "tsk-0001-delta-convergence.md"
    ),
    "docs/03.specs/0136-sdlc-taxonomy-convergence/task.md": (
        "docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/"
        "tsk-0001-taxonomy-convergence.md"
    ),
    "docs/03.specs/0152-deleted-reference-leaf-disposition/task.md": (
        "docs/03.specs/0152-deleted-reference-leaf-disposition/tasks/"
        "tsk-0001-reference-disposition.md"
    ),
}


class SpecPackageError(ValueError):
    """Raised when the Stage 03 package surface cannot be trusted."""


@dataclasses.dataclass(frozen=True)
class SpecDocument:
    """One immutable registered Markdown member of a Spec Package."""

    path: pathlib.PurePosixPath
    profile_id: str
    artifact_id: str
    status: str
    parent_ids: tuple[str, ...]


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


def _directory_snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
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
    if (
        not stat.S_ISDIR(opened.st_mode)
        or _directory_snapshot(opened) != _directory_snapshot(metadata)
    ):
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
                    raise SpecPackageError("Stage 03 exceeds the aggregate entry budget")
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
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
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
            if (
                stat.S_ISLNK(final.st_mode)
                or _file_snapshot(final) != _file_snapshot(opened)
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
        expected_path = (
            "docs/03.specs/{package_number:4}-{slug}/contracts/" + filename
        )
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
        raise SpecPackageError(f"Spec Package frontmatter {field} must be a string list")
    if len(value) != len(set(value)):
        raise SpecPackageError(
            f"Spec Package frontmatter {field} contains duplicate identities"
        )
    return value


def _allowed_statuses(
    registry: DocumentRegistry,
    profile_id: str,
) -> tuple[str, ...]:
    lifecycle_id = _EXPECTED_PROFILES[profile_id][3]
    statuses = registry.lifecycles.get(lifecycle_id)
    if not isinstance(statuses, tuple):
        raise SpecPackageError(f"Stage 99 lifecycle is missing: {lifecycle_id}")
    if not all(isinstance(status, str) for status in statuses):
        raise SpecPackageError(f"Stage 99 lifecycle statuses are malformed: {lifecycle_id}")
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
    if record.metadata.get("profile_id") != profile_id:
        raise SpecPackageError(f"{relative} must declare profile_id: {profile_id}")
    if record.metadata.get("artifact_type") != profile_id:
        raise SpecPackageError(f"{relative} must declare artifact_type: {profile_id}")
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
    return SpecDocument(relative, profile_id, artifact_id, status, parent_ids), current


def _validate_spec_parents(document: SpecDocument) -> None:
    if any(_EXTERNAL_PARENT_ID.fullmatch(parent) is None for parent in document.parent_ids):
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
                expected_artifact_id=f"task-{package_number}-{task_number}",
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
                expected_artifact_id=f"plan-{number}",
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
                raise SpecPackageError(f"duplicate Spec Package member path: {member.path}")
            result[member.path] = member
    return result


def _has_recovery(
    path: pathlib.PurePosixPath,
    recovery_commits: Mapping[pathlib.PurePosixPath, str | None],
) -> bool:
    value = recovery_commits.get(path)
    return isinstance(value, str) and _RECOVERY_COMMIT.fullmatch(value) is not None


def validate_spec_package_lifecycle(
    previous: Sequence[SpecPackage],
    current: Sequence[SpecPackage],
    *,
    recovery_commits: Mapping[pathlib.PurePosixPath, str | None] | None = None,
    one_time_package_ids: frozenset[str] = frozenset(),
) -> tuple[SpecPackageFinding, ...]:
    """Validate removals without treating Git history as implicit approval."""

    recoveries = {} if recovery_commits is None else recovery_commits
    previous_documents = _documents(previous)
    current_documents = _documents(current)
    current_spec_ids = frozenset(package.spec.artifact_id for package in current)
    previous_spec_paths = {
        package.spec.artifact_id: package.spec.path for package in previous
    }
    findings: list[SpecPackageFinding] = []
    for path, document in sorted(previous_documents.items()):
        if path in current_documents:
            continue
        if document.profile_id == "spec":
            if document.artifact_id not in one_time_package_ids:
                findings.append(
                    SpecPackageFinding(
                        "living-spec-deletion-forbidden",
                        path.as_posix(),
                        "living completed Specs retain spec.md",
                    )
                )
            elif not _has_recovery(path, recoveries):
                findings.append(
                    SpecPackageFinding(
                        "one-time-package-recovery-missing",
                        path.as_posix(),
                        "one-time package deletion requires an approved recovery commit",
                    )
                )
            continue
        package_spec_id = (
            f"SPEC-{document.artifact_id.split('-')[1]}"
            if document.profile_id in {"plan", "task"}
            else ""
        )
        deleting_one_time_package = package_spec_id in one_time_package_ids
        whole_package_retirement_proven = (
            deleting_one_time_package
            and package_spec_id not in current_spec_ids
            and package_spec_id in previous_spec_paths
            and _has_recovery(previous_spec_paths[package_spec_id], recoveries)
        )
        if whole_package_retirement_proven:
            continue
        if document.status not in {"completed", "cancelled"} or not _has_recovery(
            path, recoveries
        ):
            findings.append(
                SpecPackageFinding(
                    "execution-evidence-recovery-missing",
                    path.as_posix(),
                    "completed Plan/Task removal requires terminal state and approved recovery",
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
            raise SpecPackageError("cannot reap Spec Package Git snapshot process") from error

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
                raise SpecPackageError("Spec Package Git snapshot exceeded its deadline")
            events = selector.select(remaining)
            if not events:
                if time.monotonic() >= deadline:
                    raise SpecPackageError("Spec Package Git snapshot exceeded its deadline")
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
        raise SpecPackageError(f"cannot read Spec Package Git snapshot: {error}") from error
    finally:
        selector.close()
        for stream in streams:
            stream.close()


def _read_migration_authority(
    root: pathlib.Path,
) -> tuple[
    dict[str, str],
    dict[pathlib.PurePosixPath, str | None],
    frozenset[str],
]:
    migration = root / _MIGRATION_PATH
    parent_descriptor, descriptor, name, snapshot = _open_directory_path(
        migration.parent,
        "Task 7 Migration parent",
    )
    try:
        text, _ = _read_regular_utf8_at(
            descriptor,
            migration.name,
            "Task 7 Migration",
            _LoadBudget(),
        )
        _verify_directory_entry(
            parent_descriptor,
            name,
            descriptor,
            snapshot,
            "Task 7 Migration parent",
        )
    finally:
        os.close(descriptor)
        os.close(parent_descriptor)
    try:
        yaml_text = text.split("```yaml\n", 1)[1].split("\n```", 1)[0]
        document = yaml.safe_load(yaml_text)
    except (IndexError, yaml.YAMLError) as error:
        raise SpecPackageError("Task 7 Migration authority is malformed") from error
    if not isinstance(document, Mapping):
        raise SpecPackageError("Task 7 Migration authority must be a mapping")
    approval = document.get("approval")
    rows = document.get("rows")
    if (
        not isinstance(approval, Mapping)
        or approval.get("status") != "approved"
        or not isinstance(rows, list)
        or len(rows) > 2048
    ):
        raise SpecPackageError("Task 7 Migration authority is not approved and bounded")
    source_to_final: dict[str, str] = {}
    recovery_commits: dict[pathlib.PurePosixPath, str | None] = {}
    one_time_package_ids: set[str] = set()
    task7_rows = 0
    for row in rows:
        if not isinstance(row, Mapping):
            raise SpecPackageError("Task 7 Migration row is malformed")
        source = row.get("source_path")
        target = row.get("target_path")
        action = row.get("action")
        recovery = row.get("recovery_commit")
        owner_task = row.get("owner_task")
        if not isinstance(source, str) or not _safe_repository_path(source):
            raise SpecPackageError("Task 7 Migration source path is unsafe")
        if target is not None and (
            not isinstance(target, str) or not _safe_repository_path(target)
        ):
            raise SpecPackageError("Task 7 Migration target path is unsafe")
        if recovery is not None and (
            not isinstance(recovery, str) or _RECOVERY_COMMIT.fullmatch(recovery) is None
        ):
            raise SpecPackageError("Task 7 Migration recovery is malformed")
        final = target
        if final is not None:
            final = _SINGULAR_TASK_FINALS.get(final, final)
            recovery_commits[pathlib.PurePosixPath(final)] = recovery
        if owner_task == 7:
            task7_rows += 1
            if action == "rename" and final is not None:
                if source in source_to_final:
                    raise SpecPackageError("Task 7 Migration source is duplicated")
                source_to_final[source] = final
        if action == "delete":
            match = re.fullmatch(
                r"docs/03\.specs/(?:spec-)?(?P<number>[0-9]{4})-[^/]+/spec\.md",
                source,
            )
            if match is not None:
                package_id = f"SPEC-{match.group('number')}"
                one_time_package_ids.add(package_id)
                canonical = pathlib.PurePosixPath(
                    re.sub(r"/spec-([0-9]{4})-", r"/\1-", source)
                )
                recovery_commits[canonical] = recovery
    if task7_rows != 49 or len(source_to_final) != 46:
        raise SpecPackageError("Task 7 Migration authority row set is incomplete")
    return source_to_final, recovery_commits, frozenset(one_time_package_ids)


def _safe_repository_path(value: str) -> bool:
    path = pathlib.PurePosixPath(value)
    return (
        bool(value)
        and not path.is_absolute()
        and ".." not in path.parts
        and path.as_posix() == value
    )


def _snapshot_document(
    path: pathlib.PurePosixPath,
    text: str,
) -> SpecDocument | None:
    package_match = _PACKAGE_PATH.fullmatch(path.parts[2]) if len(path.parts) >= 4 else None
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
        artifact_id = f"plan-{number}"
    elif len(path.parts) == 5 and path.parts[3] == "tasks":
        match = _TASK_PATH.fullmatch(path.name)
        if match is None:
            raise SpecPackageError(f"base Task path is not canonical: {path}")
        profile_id = "task"
        artifact_id = f"task-{number}-{match.group('number')}"
    else:
        return None
    try:
        record = frontmatter_record_from_text(pathlib.Path(path.as_posix()), text)
    except FrontmatterError as error:
        raise SpecPackageError(f"cannot parse base Spec Package member: {path}") from error
    status = record.metadata.get("status")
    parents = record.metadata.get("parent_ids")
    if not isinstance(status, str) or not isinstance(parents, tuple):
        raise SpecPackageError(f"base Spec Package metadata is malformed: {path}")
    parent_ids = tuple(parent for parent in parents if isinstance(parent, str))
    if len(parent_ids) != len(parents):
        raise SpecPackageError(f"base Spec Package parents are malformed: {path}")
    return SpecDocument(path, profile_id, artifact_id, status, parent_ids)


def _load_base_spec_packages(
    root: pathlib.Path,
    *,
    base_ref: str,
    source_to_final: Mapping[str, str],
) -> tuple[SpecPackage, ...]:
    commit = _bounded_git(
        root,
        "rev-parse",
        "--verify",
        f"{base_ref}^{{commit}}",
        byte_limit=256,
    ).decode("ascii").strip()
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
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
        final = source_to_final.get(source, source)
        path = pathlib.PurePosixPath(final)
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
            raise SpecPackageError(f"base Spec Package member is not a regular blob: {source}")
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
            raise SpecPackageError(f"base Spec Package member is not UTF-8: {source}") from error
        document = _snapshot_document(path, text)
        if document is not None:
            if path in documents:
                raise SpecPackageError(f"duplicate base Spec Package member: {path}")
            documents[path] = document
        if len(documents) > MAX_TOTAL_ENTRIES:
            raise SpecPackageError("base Spec Package snapshot exceeds aggregate entries")
    grouped: dict[str, list[SpecDocument]] = {}
    for document in documents.values():
        grouped.setdefault(document.path.parts[2], []).append(document)
    packages: list[SpecPackage] = []
    for package_name, members in sorted(grouped.items()):
        match = _PACKAGE_PATH.fullmatch(package_name)
        assert match is not None
        specs = [member for member in members if member.profile_id == "spec"]
        plans = [member for member in members if member.profile_id == "plan"]
        tasks = tuple(sorted(
            (member for member in members if member.profile_id == "task"),
            key=lambda member: member.path.as_posix(),
        ))
        if len(specs) != 1 or len(plans) > 1:
            raise SpecPackageError(f"base Spec Package ownership is incomplete: {package_name}")
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


def validate_repository_spec_package_lifecycle(
    root: pathlib.Path,
    current: Sequence[SpecPackage],
    *,
    base_ref: str = "HEAD",
) -> tuple[SpecPackageFinding, ...]:
    """Validate current removals against a bounded Git/Migration snapshot."""

    root = pathlib.Path(root)
    source_to_final, recoveries, one_time_ids = _read_migration_authority(root)
    previous = _load_base_spec_packages(
        root,
        base_ref=base_ref,
        source_to_final=source_to_final,
    )
    return validate_spec_package_lifecycle(
        previous,
        current,
        recovery_commits=recoveries,
        one_time_package_ids=one_time_ids,
    )
