#!/usr/bin/env python3
"""Create and validate durable evidence for Spec 137 pre-deletion Gate 9."""

from __future__ import annotations

import argparse
import dataclasses
import enum
import hashlib
import json
import os
import pathlib
import re
import secrets
import shutil
import stat
import subprocess
import sys
from collections.abc import Mapping, Sequence
from typing import Any, Final


SCHEMA: Final = "agentic-research-gate9/v1"
OLD_PACK: Final = pathlib.PurePosixPath(
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh"
)
NEW_PACK: Final = pathlib.PurePosixPath(
    "docs/90.references/research/2026-08-08-agentic-engineering-research-pack"
)
INDEX: Final = pathlib.PurePosixPath(
    "docs/90.references/llm-wiki/llm-wiki-index.md"
)
COVERAGE: Final = pathlib.PurePosixPath(
    "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md"
)
INDEX_GENERATOR: Final = pathlib.PurePosixPath(
    "scripts/knowledge/generate-llm-wiki-index.sh"
)
COVERAGE_GENERATOR: Final = pathlib.PurePosixPath(
    "scripts/knowledge/generate-llm-wiki-coverage.sh"
)
REF_PREFIX: Final = "refs/codex/review-evidence/agentic-research/gate9/v1"
SPEC_PATH: Final = pathlib.PurePosixPath(
    "docs/03.specs/137-agentic-research-pack-rebuild/spec.md"
)
PLAN_PATH: Final = pathlib.PurePosixPath(
    "docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md"
)
TASK_PATH: Final = pathlib.PurePosixPath(
    "docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md"
)
ROLES: Final = ("migration-specification", "quality")
PACKAGE_ATTACHMENTS: Final = (
    "HEAD.txt",
    "SHA256SUMS",
    "assignments.json",
    "gate-results.json",
    "llm-wiki-index.md",
    "llm-wiki-stage-category-coverage.md",
    "new-manifest.tsv",
    "old-manifest.tsv",
    "package.json",
    "plan.md",
    "proposed-deletion.patch",
    "spec.md",
    "task-before.md",
    "task-before-to-candidate.patch",
    "task-candidate.md",
)
EVIDENCE_LEAF_PATHS: Final = frozenset(
    {
        *(f"package/{name}" for name in PACKAGE_ATTACHMENTS),
        "SHA256SUMS",
        "assignment-attestation.json",
        "closures/migration-specification/closure.json",
        "closures/migration-specification/report.md",
        "closures/quality/closure.json",
        "closures/quality/report.md",
        "drift/drift-proof.json",
        "evidence.json",
        "reviews/migration-specification/receipt.json",
        "reviews/migration-specification/report.md",
        "reviews/quality/receipt.json",
        "reviews/quality/report.md",
        "task/task-after.md",
        "task/task-candidate-to-after.patch",
        "terminal/report.md",
    }
)
MARKER_PATTERN: Final = re.compile(
    rb"<!-- GATE9-EVIDENCE/v1\n(?P<payload>\{[^\r\n]*\}\n)-->",
)


class Gate9Error(RuntimeError):
    """A stable fail-closed Gate 9 contract error."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def fail(code: str, detail: str) -> None:
    raise Gate9Error(code, detail)


@dataclasses.dataclass(frozen=True)
class RegisteredScratchEntry:
    parent_fd: int
    name: str
    identity: tuple[int, int]
    mode: int
    is_directory: bool


class ScratchOwnership(enum.Enum):
    ABSENT = "absent"
    CREATED_UNBOUND = "created-unbound"
    BOUND = "bound"


class PinnedScratch:
    """Own scratch objects only through pinned directory descriptors."""

    def __init__(self, prefix: str = "gate9-") -> None:
        self._owner_pid = os.getpid()
        base_path = pathlib.Path(os.environ.get("TMPDIR", "/tmp")).absolute()
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        self._base_fd: int | None = None
        self._holding_fd: int | None = None
        self._scratch_fd: int | None = None
        self._holding_name: str | None = None
        self._base_identity: tuple[int, int, int] | None = None
        self._holding_identity: tuple[int, int, int] | None = None
        self._scratch_identity: tuple[int, int, int] | None = None
        self._holding_state = ScratchOwnership.ABSENT
        self._scratch_state = ScratchOwnership.ABSENT
        try:
            self._base_fd = os.open(base_path, flags)
            self._base_path = base_path
            self._base_identity = self._directory_identity(self._base_fd)
            for _ in range(128):
                holding_name = f"{prefix}{secrets.token_hex(12)}"
                try:
                    os.mkdir(holding_name, mode=0o700, dir_fd=self._base_fd)
                    break
                except FileExistsError:
                    continue
            else:
                fail("SCRATCH_SCOPE_DRIFT", "cannot allocate unique scratch holding")
            self._holding_name = holding_name
            self.holding_path = self._base_path / holding_name
            self._holding_state = ScratchOwnership.CREATED_UNBOUND
            self._holding_fd = os.open(holding_name, flags, dir_fd=self._base_fd)
            self._holding_identity = self._directory_identity(self._holding_fd)
            holding_metadata = os.stat(
                holding_name,
                dir_fd=self._base_fd,
                follow_symlinks=False,
            )
            if not stat.S_ISDIR(holding_metadata.st_mode):
                fail("SCRATCH_SCOPE_DRIFT", "scratch holding is not a directory")
            observed_holding_identity = (
                holding_metadata.st_dev,
                holding_metadata.st_ino,
                stat.S_IMODE(holding_metadata.st_mode),
            )
            if observed_holding_identity != self._holding_identity:
                fail("SCRATCH_SCOPE_DRIFT", "scratch holding identity changed")
            self._holding_state = ScratchOwnership.BOUND
            os.mkdir("scratch", mode=0o700, dir_fd=self._holding_fd)
            self._scratch_state = ScratchOwnership.CREATED_UNBOUND
            self._scratch_fd = os.open("scratch", flags, dir_fd=self._holding_fd)
            self._scratch_identity = self._directory_identity(self._scratch_fd)
            scratch_metadata = os.stat(
                "scratch",
                dir_fd=self._holding_fd,
                follow_symlinks=False,
            )
            if not stat.S_ISDIR(scratch_metadata.st_mode):
                fail("SCRATCH_SCOPE_DRIFT", "scratch directory is not a directory")
            observed_scratch_identity = (
                scratch_metadata.st_dev,
                scratch_metadata.st_ino,
                stat.S_IMODE(scratch_metadata.st_mode),
            )
            if observed_scratch_identity != self._scratch_identity:
                fail("SCRATCH_SCOPE_DRIFT", "scratch directory identity changed")
            self._scratch_state = ScratchOwnership.BOUND
            self._path = pathlib.Path(
                f"/proc/{self._owner_pid}/fd/{self._scratch_fd}"
            )
            self._directories: dict[str, tuple[int, RegisteredScratchEntry]] = {}
            self._files: dict[str, RegisteredScratchEntry] = {}
            self._file_contracts: dict[
                str, tuple[int, tuple[int, int] | None]
            ] = {}
            self._closed = False
            self._prove_process_fd_path()
        except BaseException as error:
            primary_error = error
            if isinstance(error, OSError):
                primary_error = Gate9Error(
                    "SCRATCH_SCOPE_DRIFT",
                    f"cannot pin scratch directories: {error}",
                )
            self._rollback_initialization(primary_error)

    @staticmethod
    def _directory_identity(descriptor: int) -> tuple[int, int, int]:
        metadata = os.fstat(descriptor)
        if not stat.S_ISDIR(metadata.st_mode):
            fail("SCRATCH_SCOPE_DRIFT", "pinned descriptor is not a directory")
        return metadata.st_dev, metadata.st_ino, stat.S_IMODE(metadata.st_mode)

    def _prove_process_fd_path(self) -> None:
        if os.getpid() != self._owner_pid:
            fail("SCRATCH_SCOPE_DRIFT", "scratch owner process changed")
        expected_path = pathlib.Path(
            f"/proc/{self._owner_pid}/fd/{self._scratch_fd}"
        )
        if self._path != expected_path:
            fail("SCRATCH_SCOPE_DRIFT", "scratch process descriptor path changed")
        if self._directory_identity(self._scratch_fd) != self._scratch_identity:
            fail("SCRATCH_SCOPE_DRIFT", "scratch descriptor identity changed")
        try:
            link_metadata = self._path.lstat()
            if not stat.S_ISLNK(link_metadata.st_mode):
                fail("SCRATCH_SCOPE_DRIFT", "scratch process descriptor is not a symlink")
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
            descriptor = os.open(self._path, flags)
            try:
                observed = self._directory_identity(descriptor)
            finally:
                os.close(descriptor)
        except OSError as error:
            fail(
                "SCRATCH_SCOPE_DRIFT",
                f"cannot prove scratch process descriptor: {error}",
            )
        if observed != self._scratch_identity:
            fail("SCRATCH_SCOPE_DRIFT", "scratch process descriptor identity changed")

    def _rollback_initialization(self, primary_error: BaseException) -> None:
        cleanup_error: BaseException | None = None
        try:
            if self._base_fd is not None:
                if self._base_identity is None:
                    raise OSError("pinned scratch base identity is unavailable")
                if self._directory_identity(self._base_fd) != self._base_identity:
                    raise OSError("pinned scratch base identity changed")
            if self._holding_state is ScratchOwnership.CREATED_UNBOUND:
                raise OSError(
                    "pinned scratch holding identity is unbound; retained without removal"
                )
            if self._holding_state is ScratchOwnership.BOUND:
                if (
                    self._base_fd is None
                    or self._holding_fd is None
                    or self._holding_name is None
                    or self._holding_identity is None
                ):
                    raise OSError("pinned scratch holding identity is unavailable")
                if self._directory_identity(self._holding_fd) != self._holding_identity:
                    raise OSError("pinned scratch holding descriptor identity changed")
                holding_metadata = os.stat(
                    self._holding_name,
                    dir_fd=self._base_fd,
                    follow_symlinks=False,
                )
                if (
                    not stat.S_ISDIR(holding_metadata.st_mode)
                    or (
                        holding_metadata.st_dev,
                        holding_metadata.st_ino,
                        stat.S_IMODE(holding_metadata.st_mode),
                    )
                    != self._holding_identity
                ):
                    raise OSError("pinned scratch holding identity changed")
            if self._scratch_state is ScratchOwnership.CREATED_UNBOUND:
                raise OSError(
                    "pinned scratch directory identity is unbound; retained without removal"
                )
            if self._scratch_state is ScratchOwnership.BOUND:
                if (
                    self._holding_fd is None
                    or self._scratch_fd is None
                    or self._scratch_identity is None
                ):
                    raise OSError("pinned scratch directory identity is unavailable")
                if self._directory_identity(self._scratch_fd) != self._scratch_identity:
                    raise OSError("pinned scratch descriptor identity changed")
                scratch_metadata = os.stat(
                    "scratch",
                    dir_fd=self._holding_fd,
                    follow_symlinks=False,
                )
                if (
                    not stat.S_ISDIR(scratch_metadata.st_mode)
                    or (
                        scratch_metadata.st_dev,
                        scratch_metadata.st_ino,
                        stat.S_IMODE(scratch_metadata.st_mode),
                    )
                    != self._scratch_identity
                ):
                    raise OSError("pinned scratch directory identity changed")
            if self._scratch_state is ScratchOwnership.BOUND:
                os.rmdir("scratch", dir_fd=self._holding_fd)
            if self._holding_state is ScratchOwnership.BOUND:
                os.rmdir(self._holding_name, dir_fd=self._base_fd)
        except BaseException as error:
            cleanup_error = error
        finally:
            self._closed = True
            for descriptor in (self._scratch_fd, self._holding_fd, self._base_fd):
                if descriptor is None:
                    continue
                try:
                    os.close(descriptor)
                except OSError:
                    pass
        if cleanup_error is not None:
            raise Gate9Error(
                "SCRATCH_CLEANUP_FAILURE",
                f"initial scratch rollback failed: {cleanup_error}; "
                f"{self._retained_holding_identity()}",
            ) from primary_error
        raise primary_error

    def _retained_holding_identity(self) -> str:
        if self._holding_identity is None:
            return "retained holding identity unavailable"
        device, inode, mode = self._holding_identity
        return f"retained holding identity dev={device} ino={inode} mode={mode:#o}"

    @property
    def path(self) -> pathlib.Path:
        self._prove_process_fd_path()
        return self._path

    @property
    def pass_fds(self) -> tuple[int, ...]:
        self._prove_process_fd_path()
        return (
            self._base_fd,
            self._holding_fd,
            self._scratch_fd,
            *(descriptor for descriptor, _ in self._directories.values()),
        )

    def _parent_for(self, relative: pathlib.PurePosixPath) -> tuple[int, str]:
        if relative.is_absolute() or ".." in relative.parts or not relative.parts:
            fail("SCRATCH_SCOPE_DRIFT", f"unsafe scratch path: {relative}")
        parent_fd = self._scratch_fd
        accumulated: list[str] = []
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        for part in relative.parts[:-1]:
            accumulated.append(part)
            key = "/".join(accumulated)
            if key not in self._directories:
                descriptor: int | None = None
                try:
                    os.mkdir(part, mode=0o700, dir_fd=parent_fd)
                    descriptor = os.open(part, flags, dir_fd=parent_fd)
                    identity = self._directory_identity(descriptor)
                    metadata = os.stat(part, dir_fd=parent_fd, follow_symlinks=False)
                    observed = (
                        metadata.st_dev,
                        metadata.st_ino,
                        stat.S_IMODE(metadata.st_mode),
                    )
                    if not stat.S_ISDIR(metadata.st_mode) or observed != identity:
                        fail(
                            "SCRATCH_SCOPE_DRIFT",
                            "scratch directory changed before identity binding",
                        )
                except BaseException as error:
                    if descriptor is not None:
                        os.close(descriptor)
                    if isinstance(error, OSError):
                        fail(
                            "SCRATCH_SCOPE_DRIFT",
                            f"cannot create scratch directory: {error}",
                        )
                    raise
                entry = RegisteredScratchEntry(
                    parent_fd,
                    part,
                    (identity[0], identity[1]),
                    identity[2],
                    True,
                )
                self._directories[key] = descriptor, entry
            parent_fd = self._directories[key][0]
        return parent_fd, relative.name

    def create_file(
        self,
        relative: str,
        value: bytes = b"",
        *,
        mode: int = 0o600,
    ) -> pathlib.Path:
        pure = pathlib.PurePosixPath(relative)
        parent_fd, name = self._parent_for(pure)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
        try:
            descriptor = os.open(name, flags, mode, dir_fd=parent_fd)
            try:
                offset = 0
                while offset < len(value):
                    offset += os.write(descriptor, value[offset:])
                metadata = os.fstat(descriptor)
                observed = os.stat(
                    name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
            finally:
                os.close(descriptor)
        except OSError as error:
            fail("SCRATCH_SCOPE_DRIFT", f"cannot create scratch file {relative}: {error}")
        identity = (metadata.st_dev, metadata.st_ino)
        file_mode = stat.S_IMODE(metadata.st_mode)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or not stat.S_ISREG(observed.st_mode)
            or observed.st_nlink != 1
            or (observed.st_dev, observed.st_ino) != identity
            or stat.S_IMODE(observed.st_mode) != file_mode
        ):
            fail("SCRATCH_SCOPE_DRIFT", f"scratch file changed before binding: {relative}")
        self._files[pure.as_posix()] = RegisteredScratchEntry(
            parent_fd,
            name,
            identity,
            file_mode,
            False,
        )
        return self.path / pathlib.Path(*pure.parts)

    def register_file(
        self,
        relative: str,
        *,
        forbidden_identity: tuple[int, int] | None = None,
    ) -> pathlib.Path:
        pure = pathlib.PurePosixPath(relative)
        parent_fd, name = self._parent_for(pure)
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
        try:
            descriptor = os.open(name, flags, dir_fd=parent_fd)
            try:
                metadata = os.fstat(descriptor)
                observed = os.stat(
                    name,
                    dir_fd=parent_fd,
                    follow_symlinks=False,
                )
            finally:
                os.close(descriptor)
        except OSError as error:
            fail("PROJECTED_INDEX_SCOPE_DRIFT", f"scratch file is missing: {error}")
        identity = (metadata.st_dev, metadata.st_ino)
        mode = stat.S_IMODE(metadata.st_mode)
        contract = self._file_contracts.get(pure.as_posix())
        if contract is None:
            contract = (mode, forbidden_identity)
            self._file_contracts[pure.as_posix()] = contract
        expected_mode, forbidden = contract
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or not stat.S_ISREG(observed.st_mode)
            or observed.st_nlink != 1
            or (observed.st_dev, observed.st_ino) != identity
            or stat.S_IMODE(observed.st_mode) != mode
            or mode != expected_mode
            or (forbidden is not None and identity == forbidden)
        ):
            fail("PROJECTED_INDEX_SCOPE_DRIFT", f"scratch file is not exclusive: {relative}")
        self._files[pure.as_posix()] = RegisteredScratchEntry(
            parent_fd,
            name,
            identity,
            mode,
            False,
        )
        return self.path / pathlib.Path(*pure.parts)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        cleanup_errors: list[str] = []
        try:
            self._prove_process_fd_path()
            base_metadata = self._base_path.lstat()
            holding_metadata = self.holding_path.lstat()
            if (
                (
                    base_metadata.st_dev,
                    base_metadata.st_ino,
                    stat.S_IMODE(base_metadata.st_mode),
                )
                != self._base_identity
                or not stat.S_ISDIR(base_metadata.st_mode)
                or (
                    holding_metadata.st_dev,
                    holding_metadata.st_ino,
                    stat.S_IMODE(holding_metadata.st_mode),
                )
                != self._holding_identity
                or not stat.S_ISDIR(holding_metadata.st_mode)
            ):
                fail(
                    "SCRATCH_SCOPE_DRIFT",
                    "visible scratch ancestor changed; "
                    f"{self._retained_holding_identity()}",
                )
            scratch_metadata = os.stat(
                "scratch", dir_fd=self._holding_fd, follow_symlinks=False
            )
            if (
                scratch_metadata.st_dev,
                scratch_metadata.st_ino,
                stat.S_IMODE(scratch_metadata.st_mode),
            ) != self._scratch_identity:
                fail("SCRATCH_SCOPE_DRIFT", "pinned scratch directory changed")
            for key in sorted(self._files, key=lambda value: value.count("/"), reverse=True):
                entry = self._files[key]
                try:
                    metadata = os.stat(
                        entry.name,
                        dir_fd=entry.parent_fd,
                        follow_symlinks=False,
                    )
                    if (
                        not stat.S_ISREG(metadata.st_mode)
                        or metadata.st_nlink != 1
                        or (metadata.st_dev, metadata.st_ino) != entry.identity
                        or stat.S_IMODE(metadata.st_mode) != entry.mode
                    ):
                        raise OSError(f"registered file identity changed: {key}")
                    os.unlink(entry.name, dir_fd=entry.parent_fd)
                except OSError as error:
                    cleanup_errors.append(str(error))
            for key in sorted(
                self._directories,
                key=lambda value: value.count("/"),
                reverse=True,
            ):
                descriptor, entry = self._directories[key]
                try:
                    metadata = os.stat(
                        entry.name,
                        dir_fd=entry.parent_fd,
                        follow_symlinks=False,
                    )
                    if (
                        not stat.S_ISDIR(metadata.st_mode)
                        or (metadata.st_dev, metadata.st_ino) != entry.identity
                        or stat.S_IMODE(metadata.st_mode) != entry.mode
                    ):
                        raise OSError(f"registered directory identity changed: {key}")
                    os.rmdir(entry.name, dir_fd=entry.parent_fd)
                except OSError as error:
                    cleanup_errors.append(str(error))
                finally:
                    os.close(descriptor)
            if cleanup_errors:
                fail(
                    "SCRATCH_CLEANUP_FAILURE",
                    "; ".join(cleanup_errors)
                    + f"; {self._retained_holding_identity()}",
                )
            try:
                os.rmdir("scratch", dir_fd=self._holding_fd)
            except OSError as error:
                fail(
                    "SCRATCH_CLEANUP_FAILURE",
                    f"scratch directory is not proved empty: {error}; "
                    f"{self._retained_holding_identity()}",
                )
            try:
                os.rmdir(self._holding_name, dir_fd=self._base_fd)
            except OSError as error:
                fail(
                    "SCRATCH_CLEANUP_FAILURE",
                    f"holding directory cannot be removed: {error}; "
                    f"{self._retained_holding_identity()}",
                )
        finally:
            for descriptor in (self._scratch_fd, self._holding_fd, self._base_fd):
                try:
                    os.close(descriptor)
                except OSError:
                    pass

    def __enter__(self) -> PinnedScratch:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def run_git(
    root: pathlib.Path,
    args: Sequence[str],
    *,
    env: Mapping[str, str] | None = None,
    input_bytes: bytes | None = None,
    check: bool = True,
    pass_fds: Sequence[int] = (),
) -> subprocess.CompletedProcess[bytes]:
    command_env = os.environ.copy()
    command_env["GIT_NO_REPLACE_OBJECTS"] = "1"
    if env:
        command_env.update(env)
    command_env["GIT_NO_REPLACE_OBJECTS"] = "1"
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        env=command_env,
        input=input_bytes,
        capture_output=True,
        check=False,
        pass_fds=tuple(pass_fds),
    )
    if check and result.returncode:
        stderr = result.stderr.decode("utf-8", "replace").strip()
        fail("GIT_FAILURE", f"git {' '.join(args)}: {stderr}")
    return result


def repository_root() -> pathlib.Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail("NOT_A_REPOSITORY", result.stderr.strip())
    return pathlib.Path(result.stdout.strip()).resolve()


def repo_path(root: pathlib.Path, raw: str) -> tuple[pathlib.PurePosixPath, pathlib.Path]:
    relative = pathlib.PurePosixPath(raw)
    if relative.is_absolute() or ".." in relative.parts:
        fail("UNSAFE_PATH", raw)
    absolute = (root / pathlib.Path(*relative.parts)).resolve()
    try:
        absolute.relative_to(root)
    except ValueError:
        fail("UNSAFE_PATH", raw)
    return relative, absolute


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def load_canonical_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        fail("INVALID_JSON", f"{path.name}: {error}")
    if not isinstance(value, dict):
        fail("INVALID_JSON", f"{path.name}: root must be an object")
    if raw != canonical_json(value):
        fail("NON_CANONICAL_JSON", path.name)
    if value.get("schema") != SCHEMA:
        fail("INVALID_SCHEMA", path.name)
    return value


def parse_marker(value: bytes) -> tuple[dict[str, Any], tuple[int, int]]:
    matches = list(MARKER_PATTERN.finditer(value))
    if len(matches) != 1:
        fail("INVALID_TASK_MARKER", f"expected one marker, found {len(matches)}")
    raw = matches[0].group("payload")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail("INVALID_TASK_MARKER", str(error))
    if not isinstance(payload, dict) or canonical_json(payload) != raw:
        fail("INVALID_TASK_MARKER", "marker JSON is not canonical")
    if payload.get("schema") != SCHEMA:
        fail("INVALID_TASK_MARKER", "schema mismatch")
    return payload, matches[0].span()


def replace_marker(value: bytes, replacement: bytes) -> bytes:
    _, (start, end) = parse_marker(value)
    return value[:start] + replacement + value[end:]


def marker_bytes(payload: dict[str, Any]) -> bytes:
    return b"<!-- GATE9-EVIDENCE/v1\n" + canonical_json(payload) + b"-->"


def head(root: pathlib.Path) -> str:
    return run_git(root, ["rev-parse", "HEAD"]).stdout.decode().strip()


def assert_clean_real_index(root: pathlib.Path) -> None:
    result = run_git(root, ["diff", "--cached", "--quiet"], check=False)
    if result.returncode != 0:
        fail("DIRTY_REAL_INDEX", "the current repository index has staged changes")


def porcelain_paths(root: pathlib.Path) -> set[str]:
    raw = run_git(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    entries = raw.split(b"\0")
    paths: set[str] = set()
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        decoded = entry.decode("utf-8", "surrogateescape")
        status_code = decoded[:2]
        path = decoded[3:]
        if status_code[0] in "RC" and index < len(entries):
            path = entries[index].decode("utf-8", "surrogateescape")
            index += 1
        paths.add(path)
    return paths


def assert_task_only_worktree(root: pathlib.Path, task: pathlib.PurePosixPath) -> None:
    paths = porcelain_paths(root)
    expected = {task.as_posix()}
    if paths != expected:
        fail("WORKTREE_SCOPE_DRIFT", f"expected {sorted(expected)}, found {sorted(paths)}")


def tree_manifest(root: pathlib.Path, commit: str, prefix: pathlib.PurePosixPath) -> bytes:
    raw = run_git(
        root,
        ["ls-tree", "-r", "--full-tree", commit, "--", prefix.as_posix()],
    ).stdout
    rows: list[bytes] = []
    for line in raw.splitlines():
        metadata, separator, path = line.partition(b"\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            fail("INVALID_TREE_MANIFEST", line.decode("utf-8", "replace"))
        rows.append(b"\t".join((*fields, path)) + b"\n")
    return b"".join(sorted(rows))


def manifest_paths(value: bytes) -> list[str]:
    paths: list[str] = []
    for line in value.splitlines():
        fields = line.split(b"\t", 3)
        if len(fields) != 4:
            fail("INVALID_TREE_MANIFEST", line.decode("utf-8", "replace"))
        paths.append(fields[3].decode("utf-8"))
    return paths


def write_task_patch(
    root: pathlib.Path,
    commit: str,
    task: pathlib.PurePosixPath,
    candidate: bytes,
) -> bytes:
    with PinnedScratch("gate9-task-index-") as scratch:
        index_path = scratch.path / "index"
        environment = {"GIT_INDEX_FILE": os.fspath(index_path)}
        run_git(
            root,
            ["read-tree", commit],
            env=environment,
            pass_fds=scratch.pass_fds,
        )
        scratch.register_file("index")
        candidate_oid = run_git(
            root,
            ["hash-object", "-w", "--stdin"],
            input_bytes=candidate,
        ).stdout.decode().strip()
        run_git(
            root,
            ["update-index", "--cacheinfo", "100644", candidate_oid, task.as_posix()],
            env=environment,
            pass_fds=scratch.pass_fds,
        )
        scratch.register_file("index")
        result = run_git(
            root,
            ["diff", "--cached", "--binary", "--full-index", commit, "--", task.as_posix()],
            env=environment,
            pass_fds=scratch.pass_fds,
        ).stdout
        scratch.register_file("index")
        return result


def exclusive_regular_bytes(
    path: pathlib.Path,
    code: str,
    label: str,
) -> tuple[tuple[int, int], int, bytes]:
    try:
        metadata = path.lstat()
        canonical = path.resolve(strict=True)
        literal = path.absolute()
        if (
            canonical != literal
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
        ):
            fail(code, f"{label} is not canonical, exclusive, and regular")
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            opened = os.fstat(descriptor)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_nlink != 1
                or (opened.st_dev, opened.st_ino)
                != (metadata.st_dev, metadata.st_ino)
            ):
                fail(code, f"{label} changed before safe read")
            chunks: list[bytes] = []
            while chunk := os.read(descriptor, 1024 * 1024):
                chunks.append(chunk)
        finally:
            os.close(descriptor)
    except OSError as error:
        fail(code, f"{label} cannot be read safely: {error}")
    return (
        (metadata.st_dev, metadata.st_ino),
        stat.S_IMODE(metadata.st_mode),
        b"".join(chunks),
    )


def capture_real_index(
    root: pathlib.Path,
) -> tuple[pathlib.Path, tuple[int, int], int, bytes]:
    git_dir_value = run_git(root, ["rev-parse", "--absolute-git-dir"]).stdout.decode().strip()
    index_value = run_git(
        root,
        ["rev-parse", "--path-format=absolute", "--git-path", "index"],
    ).stdout.decode().strip()
    top_level_value = run_git(root, ["rev-parse", "--show-toplevel"]).stdout.decode().strip()
    try:
        git_dir = pathlib.Path(git_dir_value).resolve(strict=True)
        top_level = pathlib.Path(top_level_value).resolve(strict=True)
    except OSError as error:
        fail("REAL_INDEX_SCOPE_DRIFT", f"caller Git identity cannot be resolved: {error}")
    index_path = pathlib.Path(index_value).absolute()
    if top_level != root.resolve(strict=True) or index_path != git_dir / "index":
        fail("REAL_INDEX_SCOPE_DRIFT", "caller index path is not owned by the repository")
    identity, mode, value = exclusive_regular_bytes(
        index_path,
        "REAL_INDEX_SCOPE_DRIFT",
        "caller index",
    )
    return index_path, identity, mode, value


def prove_real_index_unchanged(
    snapshot: tuple[pathlib.Path, tuple[int, int], int, bytes],
) -> None:
    path, expected_identity, expected_mode, expected_value = snapshot
    identity, mode, value = exclusive_regular_bytes(
        path,
        "REAL_INDEX_SCOPE_DRIFT",
        "caller index",
    )
    if (
        identity != expected_identity
        or mode != expected_mode
        or value != expected_value
    ):
        fail("REAL_INDEX_SCOPE_DRIFT", "caller index changed during projection")


@dataclasses.dataclass(frozen=True)
class AuthorityProof:
    live_head: str
    reviewed_code_head: str
    code_blob_oids: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class AuthoritativeProjection:
    package_head: str
    live_reviewed_head: str
    reviewed_code_head: str
    initial_tree_oid: str
    final_tree_oid: str
    old_paths: tuple[str, ...]
    deletion_statuses: tuple[tuple[str, str], ...]
    proposed_deletion_patch: bytes
    index_markdown: bytes
    coverage_markdown: bytes


@dataclasses.dataclass(frozen=True)
class RepositorySnapshot:
    head: str
    real_index: tuple[pathlib.Path, tuple[int, int], int, bytes]
    old_files: tuple[tuple[str, tuple[tuple[int, int], int, bytes]], ...]
    outputs: tuple[tuple[str, tuple[tuple[int, int], int, bytes]], ...]
    worktree_registry: tuple[tuple[str, str, int, int, int, bytes], ...]
    evidence_refs: bytes


def trusted_system_tool(name: str) -> str:
    candidate = shutil.which(name, path=os.defpath)
    if candidate is None:
        fail("GENERATOR_FAILURE", f"trusted system tool is unavailable: {name}")
    try:
        resolved = pathlib.Path(candidate).resolve(strict=True)
        metadata = resolved.lstat()
    except OSError as error:
        fail("GENERATOR_FAILURE", f"trusted system tool cannot be resolved: {error}")
    if not stat.S_ISREG(metadata.st_mode) or not os.access(resolved, os.X_OK):
        fail("GENERATOR_FAILURE", f"trusted system tool is not executable: {name}")
    return os.fspath(resolved)


def git_common_dir(root: pathlib.Path) -> pathlib.Path:
    raw = run_git(
        root,
        ["rev-parse", "--path-format=absolute", "--git-common-dir"],
    ).stdout.decode().strip()
    try:
        return pathlib.Path(raw).resolve(strict=True)
    except OSError as error:
        fail("AMBIGUOUS_GIT_HISTORY", f"Git common directory cannot be proved: {error}")


def object_format_width(root: pathlib.Path) -> int:
    result = run_git(root, ["rev-parse", "--show-object-format"])
    value = result.stdout.decode().strip()
    widths = {"sha1": 40, "sha256": 64}
    if value not in widths:
        fail("AMBIGUOUS_GIT_HISTORY", f"unsupported object format: {value}")
    return widths[value]


def require_full_commit_oid(
    root: pathlib.Path,
    value: object,
    *,
    code: str,
) -> str:
    width = object_format_width(root)
    if not isinstance(value, str) or re.fullmatch(rf"[0-9a-f]{{{width}}}", value) is None:
        fail(code, "a full immutable commit OID is required")
    result = run_git(root, ["cat-file", "-t", value], check=False)
    if result.returncode or result.stdout != b"commit\n":
        fail(code, "the supplied full OID is not a commit")
    return value


def prove_live_head(
    root: pathlib.Path,
    expected: str,
    *,
    code: str,
) -> None:
    current = require_full_commit_oid(root, head(root), code=code)
    if current != expected:
        fail(code, "current HEAD differs from the preflight live HEAD")


def assert_unambiguous_history(root: pathlib.Path) -> None:
    replacements = run_git(
        root,
        ["for-each-ref", "--format=%(refname)", "refs/replace/"],
    ).stdout
    common_dir = git_common_dir(root)
    grafts = common_dir / "info/grafts"
    shallow = common_dir / "shallow"
    try:
        graft_bytes = grafts.read_bytes() if grafts.exists() else b""
        shallow_exists = shallow.exists()
    except OSError as error:
        fail("AMBIGUOUS_GIT_HISTORY", f"history boundary cannot be inspected: {error}")
    shallow_result = run_git(root, ["rev-parse", "--is-shallow-repository"])
    if (
        replacements.strip()
        or graft_bytes
        or shallow_exists
        or shallow_result.stdout.strip() != b"false"
    ):
        fail("AMBIGUOUS_GIT_HISTORY", "replace, graft, or shallow history is forbidden")


def commit_tree_oid(root: pathlib.Path, commit: str) -> str:
    value = run_git(root, ["cat-file", "commit", commit]).stdout
    first = value.splitlines()[0] if value else b""
    if not first.startswith(b"tree "):
        fail("AMBIGUOUS_GIT_HISTORY", "commit tree header is missing")
    tree_oid = first.removeprefix(b"tree ").decode("ascii", "strict")
    width = object_format_width(root)
    if re.fullmatch(rf"[0-9a-f]{{{width}}}", tree_oid) is None:
        fail("AMBIGUOUS_GIT_HISTORY", "commit tree OID is malformed")
    return tree_oid


def tracked_blob_oid(
    root: pathlib.Path,
    commit: str,
    path: pathlib.PurePosixPath,
) -> str:
    raw = run_git(
        root,
        ["ls-tree", "--full-tree", commit, "--", path.as_posix()],
    ).stdout
    rows = raw.splitlines()
    if len(rows) != 1:
        fail("REVIEWED_CODE_DRIFT", f"tracked code path is missing: {path}")
    metadata, separator, raw_path = rows[0].partition(b"\t")
    fields = metadata.split()
    if (
        not separator
        or raw_path.decode("utf-8", "surrogateescape") != path.as_posix()
        or len(fields) != 3
        or fields[1] != b"blob"
    ):
        fail("REVIEWED_CODE_DRIFT", f"tracked code identity is malformed: {path}")
    return fields[2].decode("ascii")


def authority_preflight(
    root: pathlib.Path,
    live_reviewed_head: object,
    reviewed_code_head: object,
) -> AuthorityProof:
    assert_unambiguous_history(root)
    live_oid = require_full_commit_oid(
        root,
        live_reviewed_head,
        code="LIVE_HEAD_REQUIRED",
    )
    reviewed_oid = require_full_commit_oid(
        root,
        reviewed_code_head,
        code="LIVE_HEAD_REQUIRED",
    )
    current = require_full_commit_oid(root, head(root), code="AMBIGUOUS_GIT_HISTORY")
    if current != live_oid:
        fail("UNTRUSTED_PACKAGE_HEAD", "current HEAD differs from live reviewed HEAD")
    ancestor = run_git(
        root,
        ["merge-base", "--is-ancestor", reviewed_oid, live_oid],
        check=False,
    )
    if ancestor.returncode != 0:
        fail("REVIEWED_CODE_DRIFT", "reviewed code commit is not an ancestor of live HEAD")
    code_paths = (
        pathlib.PurePosixPath(
            "scripts/validation/agentic-research-gate9-evidence.py"
        ),
        INDEX_GENERATOR,
        COVERAGE_GENERATOR,
    )
    live_blobs: list[str] = []
    for path in code_paths:
        live_blob = tracked_blob_oid(root, live_oid, path)
        reviewed_blob = tracked_blob_oid(root, reviewed_oid, path)
        if live_blob != reviewed_blob:
            fail("REVIEWED_CODE_DRIFT", f"reviewed code blob differs: {path}")
        if (
            run_git(root, ["diff", "--quiet", "--", path.as_posix()], check=False).returncode
            or run_git(
                root,
                ["diff", "--cached", "--quiet", "--", path.as_posix()],
                check=False,
            ).returncode
        ):
            fail("REVIEWED_CODE_DRIFT", f"reviewed code path is dirty: {path}")
        live_blobs.append(live_blob)
    try:
        task_bytes = (root / pathlib.Path(*TASK_PATH.parts)).read_bytes()
    except OSError as error:
        fail("REVIEWED_CODE_DRIFT", f"Task code binding cannot be read: {error}")
    bindings = re.findall(
        rb"GATE9_REVIEWED_CODE_HEAD:\s*`([0-9a-f]+)`",
        task_bytes,
    )
    if bindings != [reviewed_oid.encode()]:
        fail("REVIEWED_CODE_DRIFT", "Task does not bind the exact reviewed code OID")
    prove_live_head(root, live_oid, code="UNTRUSTED_PACKAGE_HEAD")
    return AuthorityProof(live_oid, reviewed_oid, tuple(live_blobs))


def authority_from_args(root: pathlib.Path, args: argparse.Namespace) -> AuthorityProof:
    if (
        not getattr(args, "require_live_head", False)
        or getattr(args, "live_reviewed_head", None) is None
        or getattr(args, "reviewed_code_head", None) is None
    ):
        fail("LIVE_HEAD_REQUIRED", "all live authority bindings are mandatory")
    return authority_preflight(
        root,
        args.live_reviewed_head,
        args.reviewed_code_head,
    )


def snapshot_directory_tree(root: pathlib.Path) -> tuple[tuple[str, str, int, int, int, bytes], ...]:
    if not root.exists():
        return ()
    rows: list[tuple[str, str, int, int, int, bytes]] = []

    def visit(current: pathlib.Path, relative: pathlib.PurePosixPath) -> None:
        try:
            entries = sorted(os.scandir(current), key=lambda entry: os.fsencode(entry.name))
        except OSError as error:
            fail("SCRATCH_SCOPE_DRIFT", f"worktree registry cannot be read: {error}")
        for entry in entries:
            child_relative = relative / entry.name
            metadata = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(metadata.st_mode):
                kind = "directory"
                payload = b""
            elif stat.S_ISREG(metadata.st_mode):
                kind = "file"
                payload = pathlib.Path(entry.path).read_bytes()
            elif stat.S_ISLNK(metadata.st_mode):
                kind = "symlink"
                payload = os.fsencode(os.readlink(entry.path))
            else:
                kind = "other"
                payload = b""
            rows.append(
                (
                    child_relative.as_posix(),
                    kind,
                    stat.S_IMODE(metadata.st_mode),
                    metadata.st_dev,
                    metadata.st_ino,
                    payload,
                )
            )
            if kind == "directory":
                visit(pathlib.Path(entry.path), child_relative)

    visit(root, pathlib.PurePosixPath())
    return tuple(rows)


def capture_repository_snapshot(
    root: pathlib.Path,
    expected_head: str,
) -> RepositorySnapshot:
    prove_live_head(root, expected_head, code="PROJECTED_INDEX_SCOPE_DRIFT")
    old_paths = tuple(manifest_paths(tree_manifest(root, expected_head, OLD_PACK)))
    old_files = tuple(
        (
            path,
            exclusive_regular_bytes(
                root / pathlib.Path(*pathlib.PurePosixPath(path).parts),
                "PROJECTED_INDEX_SCOPE_DRIFT",
                path,
            ),
        )
        for path in old_paths
    )
    outputs = tuple(
        (
            path.as_posix(),
            exclusive_regular_bytes(
                root / pathlib.Path(*path.parts),
                "PROJECTED_INDEX_SCOPE_DRIFT",
                path.as_posix(),
            ),
        )
        for path in (INDEX, COVERAGE)
    )
    registry = git_common_dir(root) / "worktrees"
    refs = run_git(
        root,
        ["for-each-ref", "--format=%(refname) %(objectname)", f"{REF_PREFIX}/"],
    ).stdout
    return RepositorySnapshot(
        expected_head,
        capture_real_index(root),
        old_files,
        outputs,
        snapshot_directory_tree(registry),
        refs,
    )


def prove_repository_snapshot(root: pathlib.Path, snapshot: RepositorySnapshot) -> None:
    if head(root) != snapshot.head:
        fail("PROJECTED_INDEX_SCOPE_DRIFT", "branch HEAD changed during projection")
    prove_real_index_unchanged(snapshot.real_index)
    for path, expected in snapshot.old_files:
        observed = exclusive_regular_bytes(
            root / pathlib.Path(*pathlib.PurePosixPath(path).parts),
            "PROJECTED_INDEX_SCOPE_DRIFT",
            path,
        )
        if observed != expected:
            fail("PROJECTED_INDEX_SCOPE_DRIFT", f"old-pack file changed: {path}")
    for path, expected in snapshot.outputs:
        observed = exclusive_regular_bytes(
            root / pathlib.Path(*pathlib.PurePosixPath(path).parts),
            "PROJECTED_INDEX_SCOPE_DRIFT",
            path,
        )
        if observed != expected:
            fail("PROJECTED_INDEX_SCOPE_DRIFT", f"generated output changed: {path}")
    if snapshot_directory_tree(git_common_dir(root) / "worktrees") != snapshot.worktree_registry:
        fail("PROJECTED_INDEX_SCOPE_DRIFT", "linked-worktree registry changed")
    refs = run_git(
        root,
        ["for-each-ref", "--format=%(refname) %(objectname)", f"{REF_PREFIX}/"],
    ).stdout
    if refs != snapshot.evidence_refs:
        fail("PROJECTED_INDEX_SCOPE_DRIFT", "Gate 9 evidence refs changed")


def nul_paths(value: bytes, *, code: str) -> list[str]:
    if not value:
        return []
    if not value.endswith(b"\0"):
        fail(code, "Git path output is not NUL-terminated")
    return [
        raw.decode("utf-8", "surrogateescape")
        for raw in value[:-1].split(b"\0")
    ]


def generator_stdout(
    root: pathlib.Path,
    scratch: PinnedScratch,
    index_environment: Mapping[str, str],
    generator_bytes: bytes,
    expected_live: bytes,
    expected_package: bytes | None,
    label: pathlib.PurePosixPath,
) -> bytes:
    trusted_bash = trusted_system_tool("bash")
    trusted_git = pathlib.Path(trusted_system_tool("git"))
    trusted_python = pathlib.Path(trusted_system_tool("python3"))
    environment = {
        "GIT_INDEX_FILE": index_environment["GIT_INDEX_FILE"],
        "GIT_NO_REPLACE_OBJECTS": "1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.pathsep.join(
            dict.fromkeys(
                (os.fspath(trusted_git.parent), os.fspath(trusted_python.parent))
            )
        ),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "PYTHONSAFEPATH": "1",
    }
    result = subprocess.run(
        [trusted_bash, "-s", "--", "--stdout"],
        cwd=root,
        env=environment,
        input=generator_bytes,
        capture_output=True,
        check=False,
        pass_fds=scratch.pass_fds,
    )
    scratch.register_file("index")
    if result.returncode:
        fail(
            "GENERATOR_STDOUT_DRIFT",
            f"{label} exited {result.returncode}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}",
        )
    try:
        decoded = result.stdout.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        fail("GENERATOR_STDOUT_DRIFT", f"{label} is not UTF-8: {error}")
    if (
        not result.stdout
        or result.stderr
        or "\r" in decoded
        or not result.stdout.endswith(b"\n")
        or result.stdout.endswith(b"\n\n")
    ):
        fail("GENERATOR_STDOUT_DRIFT", f"{label} stdout is not canonical LF Markdown")
    if result.stdout != expected_live:
        fail("GENERATOR_STDOUT_DRIFT", f"{label} stdout differs from live HEAD")
    if expected_package is not None and result.stdout != expected_package:
        fail("PACKAGE_SEMANTIC_DRIFT", f"{label} attachment differs from projection")
    return result.stdout


def authoritative_projection(
    root: pathlib.Path,
    package_head: object,
    live_reviewed_head: object,
    reviewed_code_head: object,
    *,
    expected_index: bytes | None = None,
    expected_coverage: bytes | None = None,
) -> AuthoritativeProjection:
    proof = authority_preflight(root, live_reviewed_head, reviewed_code_head)
    package_oid = require_full_commit_oid(
        root,
        package_head,
        code="UNTRUSTED_PACKAGE_HEAD",
    )
    if package_oid != proof.live_head:
        fail("UNTRUSTED_PACKAGE_HEAD", "package HEAD differs from live reviewed HEAD")
    prove_live_head(root, proof.live_head, code="PROJECTED_INDEX_SCOPE_DRIFT")
    snapshot = capture_repository_snapshot(root, proof.live_head)
    primary_error: BaseException | None = None
    projection: AuthoritativeProjection | None = None
    try:
        prove_live_head(root, proof.live_head, code="PROJECTED_INDEX_SCOPE_DRIFT")
        generator_blobs = {
            INDEX_GENERATOR: run_git(
                root, ["cat-file", "blob", proof.code_blob_oids[1]]
            ).stdout,
            COVERAGE_GENERATOR: run_git(
                root, ["cat-file", "blob", proof.code_blob_oids[2]]
            ).stdout,
        }
        tracked_outputs = {
            INDEX: run_git(
                root,
                ["cat-file", "blob", tracked_blob_oid(root, proof.live_head, INDEX)],
            ).stdout,
            COVERAGE: run_git(
                root,
                ["cat-file", "blob", tracked_blob_oid(root, proof.live_head, COVERAGE)],
            ).stdout,
        }
        initial_tree = commit_tree_oid(root, package_oid)
        with PinnedScratch("gate9-index-") as scratch:
            index_path = scratch.path / "index"
            environment = {"GIT_INDEX_FILE": os.fspath(index_path)}
            run_git(
                root,
                ["read-tree", package_oid],
                env=environment,
                pass_fds=scratch.pass_fds,
            )
            scratch.register_file(
                "index",
                forbidden_identity=snapshot.real_index[1],
            )
            indexed_tree = run_git(
                root,
                ["write-tree"],
                env=environment,
                pass_fds=scratch.pass_fds,
            ).stdout.decode().strip()
            if indexed_tree != initial_tree or initial_tree != commit_tree_oid(root, proof.live_head):
                fail("PROJECTED_INDEX_SCOPE_DRIFT", "initial projected tree differs from live HEAD")
            tree_paths = tuple(
                sorted(
                    manifest_paths(tree_manifest(root, package_oid, OLD_PACK)),
                    key=os.fsencode,
                )
            )
            indexed_paths = tuple(
                sorted(
                    nul_paths(
                        run_git(
                            root,
                            ["ls-files", "-z", "--", OLD_PACK.as_posix()],
                            env=environment,
                            pass_fds=scratch.pass_fds,
                        ).stdout,
                        code="PROJECTED_INDEX_SCOPE_DRIFT",
                    )
                )
            )
            if tree_paths != indexed_paths or len(tree_paths) != 20:
                fail(
                    "PROJECTED_DELETION_DRIFT",
                    f"retiring path tuple is not exact 20/20: tree={tree_paths!r} index={indexed_paths!r}",
                )
            removal = b"".join(os.fsencode(path) + b"\0" for path in tree_paths)
            run_git(
                root,
                ["update-index", "--force-remove", "-z", "--stdin"],
                env=environment,
                input_bytes=removal,
                pass_fds=scratch.pass_fds,
            )
            scratch.register_file("index")
            raw_status = run_git(
                root,
                [
                    "diff",
                    "--cached",
                    "--name-status",
                    "--no-renames",
                    "-z",
                    package_oid,
                    "--",
                ],
                env=environment,
                pass_fds=scratch.pass_fds,
            ).stdout
            fields = nul_paths(raw_status, code="PROJECTED_DELETION_DRIFT")
            if len(fields) % 2:
                fail("PROJECTED_DELETION_DRIFT", "projected status is malformed")
            statuses = tuple(
                (fields[index], fields[index + 1])
                for index in range(0, len(fields), 2)
            )
            expected_statuses = tuple(("D", path) for path in tree_paths)
            if statuses != expected_statuses:
                fail(
                    "PROJECTED_DELETION_DRIFT",
                    f"expected exact twenty deletions, found {statuses!r}",
                )
            if run_git(
                root,
                ["ls-files", "-z", "--", OLD_PACK.as_posix()],
                env=environment,
                pass_fds=scratch.pass_fds,
            ).stdout:
                fail("PROJECTED_DELETION_DRIFT", "retiring paths remain in projected index")
            final_tree = run_git(
                root,
                ["write-tree"],
                env=environment,
                pass_fds=scratch.pass_fds,
            ).stdout.decode().strip()
            if final_tree == initial_tree:
                fail("PROJECTED_DELETION_DRIFT", "projected deletion did not change the tree")
            patch = run_git(
                root,
                ["diff", "--cached", "--binary", "--full-index", package_oid, "--"],
                env=environment,
                pass_fds=scratch.pass_fds,
            ).stdout
            prove_live_head(root, proof.live_head, code="PROJECTED_INDEX_SCOPE_DRIFT")
            index_bytes = generator_stdout(
                root,
                scratch,
                environment,
                generator_blobs[INDEX_GENERATOR],
                tracked_outputs[INDEX],
                expected_index,
                INDEX_GENERATOR,
            )
            prove_live_head(root, proof.live_head, code="PROJECTED_INDEX_SCOPE_DRIFT")
            coverage_bytes = generator_stdout(
                root,
                scratch,
                environment,
                generator_blobs[COVERAGE_GENERATOR],
                tracked_outputs[COVERAGE],
                expected_coverage,
                COVERAGE_GENERATOR,
            )
            projection = AuthoritativeProjection(
                package_oid,
                proof.live_head,
                proof.reviewed_code_head,
                initial_tree,
                final_tree,
                tree_paths,
                statuses,
                patch,
                index_bytes,
                coverage_bytes,
            )
    except BaseException as error:
        primary_error = error
    try:
        prove_repository_snapshot(root, snapshot)
        prove_live_head(root, proof.live_head, code="PROJECTED_INDEX_SCOPE_DRIFT")
    except BaseException as invariant_error:
        primary_error = invariant_error
    if primary_error is not None:
        raise primary_error
    if projection is None:
        fail("PROJECTED_INDEX_SCOPE_DRIFT", "projection produced no result")
    return projection


def assignment_run_id(commit: str, attempt: int, role: str) -> str:
    return sha256_bytes(f"{commit}\0{attempt}\0{role}".encode())


def fixed_evidence_ref(attempt: int, package_sha256: str) -> str:
    return f"{REF_PREFIX}/attempt-{attempt}/{package_sha256}"


def existing_evidence_refs(root: pathlib.Path) -> list[str]:
    result = run_git(
        root,
        ["for-each-ref", "--format=%(refname)", f"{REF_PREFIX}/"],
    )
    return sorted(filter(None, result.stdout.decode().splitlines()))


def derive_attempt(
    root: pathlib.Path,
    marker: dict[str, Any],
    authority: AuthorityProof,
) -> int:
    refs = existing_evidence_refs(root)
    if len(refs) > 2:
        fail("THIRD_ATTEMPT", "more than two durable Gate 9 refs exist")
    state = marker.get("state")
    attempt = marker.get("attempt")
    if not refs:
        if state != "PACKAGE_REVIEW_PENDING" or attempt != 1:
            fail("ATTEMPT_STATE_MISMATCH", "first attempt requires pending marker attempt 1")
        return 1
    if len(refs) == 1 and state == "ATTEMPT_2_PENDING" and attempt == 2:
        evidence_ref = refs[0]
        terminal = replay_terminal_evidence_ref(
            root,
            evidence_ref,
            authority.live_head,
            authority.reviewed_code_head,
        )
        terminal_state = terminal["state"]
        package_sha256 = terminal["package_sha256"]
        tree_oid = terminal["tree"]
        reason = terminal["reason"]
        if terminal["attempt"] != 1:
            fail("ATTEMPT_STATE_MISMATCH", "attempt 1 ref identity mismatch")
        expected_attempt_1 = {
            "evidence_ref": evidence_ref,
            "evidence_tree": tree_oid,
            "package_sha256": package_sha256,
            "reason": reason,
            "terminal_state": terminal_state,
        }
        if marker.get("attempt_1") != expected_attempt_1:
            fail("ATTEMPT_STATE_MISMATCH", "attempt 2 marker does not bind terminal ref")
        return 2
    fail("ATTEMPT_STATE_MISMATCH", "durable refs and Task marker do not authorize an attempt")


def validate_package_prehistory(
    root: pathlib.Path,
    attempt: int,
    marker: dict[str, Any],
    live_reviewed_head: str,
    reviewed_code_head: str,
) -> None:
    if attempt == 1:
        return
    if attempt != 2 or marker.get("state") != "ATTEMPT_2_PENDING":
        fail("ATTEMPT_PREHISTORY_INVALID", "package is not a bounded attempt 2")
    attempt_one = marker.get("attempt_1")
    expected_keys = {
        "evidence_ref",
        "evidence_tree",
        "package_sha256",
        "reason",
        "terminal_state",
    }
    if not isinstance(attempt_one, dict) or set(attempt_one) != expected_keys:
        fail("ATTEMPT_PREHISTORY_INVALID", "attempt-1 marker binding is malformed")
    evidence_ref = attempt_one.get("evidence_ref")
    if not isinstance(evidence_ref, str):
        fail("ATTEMPT_PREHISTORY_INVALID", "attempt-1 evidence ref is missing")
    try:
        terminal = replay_terminal_evidence_ref(
            root,
            evidence_ref,
            live_reviewed_head,
            reviewed_code_head,
        )
    except Gate9Error as error:
        fail("ATTEMPT_PREHISTORY_INVALID", f"{error.code}: {error.detail}")
    expected_attempt_one = {
        "evidence_ref": evidence_ref,
        "evidence_tree": terminal["tree"],
        "package_sha256": terminal["package_sha256"],
        "reason": terminal["reason"],
        "terminal_state": terminal["state"],
    }
    if terminal["attempt"] != 1 or attempt_one != expected_attempt_one:
        fail("ATTEMPT_PREHISTORY_INVALID", "attempt-1 terminal binding differs")


def package_records(payloads: Mapping[str, bytes]) -> list[dict[str, object]]:
    return [
        {"bytes": len(payloads[path]), "path": path, "sha256": sha256_bytes(payloads[path])}
        for path in sorted(payloads)
    ]


def checksum_manifest(payloads: Mapping[str, bytes]) -> bytes:
    return b"".join(
        f"{sha256_bytes(payloads[path])}  {path}\n".encode()
        for path in sorted(payloads)
    )


def ensure_empty_output(path: pathlib.Path) -> None:
    if path.exists():
        if not path.is_dir() or any(path.iterdir()):
            fail("OUTPUT_NOT_EMPTY", os.fspath(path))
    else:
        path.mkdir(parents=True)


def write_package(output: pathlib.Path, payloads: Mapping[str, bytes]) -> str:
    for name, value in payloads.items():
        (output / name).write_bytes(value)
    sums = checksum_manifest(payloads)
    (output / "SHA256SUMS").write_bytes(sums)
    package_id = sha256_bytes(sums)
    for attachment in output.iterdir():
        attachment.chmod(0o444)
    return package_id


def build_package(args: argparse.Namespace) -> None:
    if args.attempt not in (1, 2):
        fail("THIRD_ATTEMPT", f"attempt {args.attempt} is forbidden")
    root = repository_root()
    authority = authority_from_args(root, args)
    task_relative, task_path = repo_path(root, args.task)
    spec_relative, spec_path = repo_path(root, args.spec)
    plan_relative, plan_path = repo_path(root, args.plan)
    del spec_relative, plan_relative
    assert_clean_real_index(root)
    assert_task_only_worktree(root, task_relative)
    current_head = authority.live_head
    before = run_git(root, ["show", f"{current_head}:{task_relative.as_posix()}"]).stdout
    candidate = task_path.read_bytes()
    marker, _ = parse_marker(candidate)
    derived_attempt = derive_attempt(root, marker, authority)
    if args.attempt != derived_attempt:
        fail("ATTEMPT_STATE_MISMATCH", f"derived {derived_attempt}, asserted {args.attempt}")
    old_manifest = tree_manifest(root, current_head, OLD_PACK)
    new_manifest = tree_manifest(root, current_head, NEW_PACK)
    if len(manifest_paths(old_manifest)) != 20 or len(manifest_paths(new_manifest)) != 20:
        fail("PACK_CARDINALITY", "old and new packs must each contain exactly 20 files")
    task_patch = write_task_patch(
        root, current_head, task_relative, candidate
    )
    projection = authoritative_projection(
        root,
        current_head,
        authority.live_head,
        authority.reviewed_code_head,
    )
    assignments = {
        "assignments": [
            {
                "role": role,
                "run_id": assignment_run_id(current_head, args.attempt, role),
            }
            for role in ROLES
        ],
        "attempt": args.attempt,
        "package_head": current_head,
        "schema": SCHEMA,
    }
    gates = {
        "attempt": args.attempt,
        "gates": [
            {
                "gate": ordinal,
                "predecessor_classification": (
                    "pinned-184-attributable-delta-zero"
                    if ordinal == 7
                    else "pinned-9-26-9"
                    if ordinal == 8
                    else "none"
                ),
                "result": "PASS",
            }
            for ordinal in range(1, 9)
        ],
        "package_head": current_head,
        "schema": SCHEMA,
    }
    payloads: dict[str, bytes] = {
        "HEAD.txt": f"{current_head}\n".encode(),
        "assignments.json": canonical_json(assignments),
        "gate-results.json": canonical_json(gates),
        "llm-wiki-index.md": projection.index_markdown,
        "llm-wiki-stage-category-coverage.md": projection.coverage_markdown,
        "new-manifest.tsv": new_manifest,
        "old-manifest.tsv": old_manifest,
        "plan.md": plan_path.read_bytes(),
        "proposed-deletion.patch": projection.proposed_deletion_patch,
        "spec.md": spec_path.read_bytes(),
        "task-before.md": before,
        "task-before-to-candidate.patch": task_patch,
        "task-candidate.md": candidate,
    }
    package_document = {
        "attachments": package_records(payloads),
        "attempt": args.attempt,
        "evidence_ref": "PENDING_PACKAGE_SHA256",
        "package_head": current_head,
        "schema": SCHEMA,
    }
    payloads["package.json"] = canonical_json(package_document)
    output = pathlib.Path(args.output).resolve()
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    ensure_empty_output(output)
    package_id = write_package(output, payloads)
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(canonical_json({"package_sha256": package_id, "state": "BUILT"}).decode(), end="")


def read_checksum_manifest(package: pathlib.Path) -> dict[str, str]:
    raw = (package / "SHA256SUMS").read_bytes()
    rows = raw.splitlines(keepends=True)
    result: dict[str, str] = {}
    pattern = re.compile(rb"^(?P<digest>[0-9a-f]{64})  (?P<path>[^\r\n]+)\n$")
    for row in rows:
        match = pattern.fullmatch(row)
        if not match:
            fail("INVALID_CHECKSUM_MANIFEST", row.decode("utf-8", "replace"))
        name = match.group("path").decode("utf-8")
        if name in result:
            fail("INVALID_CHECKSUM_MANIFEST", f"duplicate {name}")
        result[name] = match.group("digest").decode()
    if list(result) != sorted(result):
        fail("UNSORTED_ATTACHMENTS", "SHA256SUMS paths are not byte-sorted")
    return result


def verify_package_path(
    root: pathlib.Path,
    package: pathlib.Path,
    *,
    live_reviewed_head: str,
    reviewed_code_head: str,
    require_read_only: bool = True,
) -> dict[str, Any]:
    if not package.is_dir():
        fail("MISSING_PACKAGE", os.fspath(package))
    actual_paths = sorted(path.name for path in package.iterdir())
    if actual_paths != sorted(PACKAGE_ATTACHMENTS):
        fail("ATTACHMENT_SET_DRIFT", repr(actual_paths))
    try:
        package_head = (package / "HEAD.txt").read_text(encoding="ascii").strip()
    except (OSError, UnicodeDecodeError) as error:
        fail("UNTRUSTED_PACKAGE_HEAD", f"package HEAD cannot be read: {error}")
    projection = authoritative_projection(
        root,
        package_head,
        live_reviewed_head,
        reviewed_code_head,
        expected_index=(package / "llm-wiki-index.md").read_bytes(),
        expected_coverage=(
            package / "llm-wiki-stage-category-coverage.md"
        ).read_bytes(),
    )
    if require_read_only:
        for path in package.iterdir():
            metadata = path.lstat()
            if not stat.S_ISREG(metadata.st_mode):
                fail("ATTACHMENT_TYPE_DRIFT", path.name)
            if stat.S_IMODE(metadata.st_mode) != 0o444:
                fail("ATTACHMENT_MODE_DRIFT", path.name)
    package_doc = load_canonical_json(package / "package.json")
    assignments = load_canonical_json(package / "assignments.json")
    gates = load_canonical_json(package / "gate-results.json")
    checksums = read_checksum_manifest(package)
    expected_checksum_paths = sorted(set(PACKAGE_ATTACHMENTS) - {"SHA256SUMS"})
    if sorted(checksums) != expected_checksum_paths:
        fail("ATTACHMENT_SET_DRIFT", "checksum path set mismatch")
    for name, expected in checksums.items():
        if sha256_bytes((package / name).read_bytes()) != expected:
            fail("CHECKSUM_DRIFT", name)
    attempt = package_doc.get("attempt")
    if not nonnegative_int(attempt) or attempt not in (1, 2):
        fail("PACKAGE_SEMANTIC_DRIFT", "invalid package attempt")
    payloads = {
        name: (package / name).read_bytes()
        for name in expected_checksum_paths
        if name != "package.json"
    }
    expected_package = {
        "attachments": package_records(payloads),
        "attempt": attempt,
        "evidence_ref": "PENDING_PACKAGE_SHA256",
        "package_head": package_head,
        "schema": SCHEMA,
    }
    if package_doc != expected_package:
        fail("PACKAGE_SEMANTIC_DRIFT", "package.json")
    expected_assignments = {
        "assignments": [
            {
                "role": role,
                "run_id": assignment_run_id(package_head, attempt, role),
            }
            for role in ROLES
        ],
        "attempt": attempt,
        "package_head": package_head,
        "schema": SCHEMA,
    }
    if assignments != expected_assignments:
        fail("PACKAGE_SEMANTIC_DRIFT", "assignments.json")
    expected_gates = {
        "attempt": attempt,
        "gates": [
            {
                "gate": ordinal,
                "predecessor_classification": (
                    "pinned-184-attributable-delta-zero"
                    if ordinal == 7
                    else "pinned-9-26-9"
                    if ordinal == 8
                    else "none"
                ),
                "result": "PASS",
            }
            for ordinal in range(1, 9)
        ],
        "package_head": package_head,
        "schema": SCHEMA,
    }
    if gates != expected_gates:
        fail("PACKAGE_SEMANTIC_DRIFT", "gate-results.json")
    if (package / "HEAD.txt").read_bytes() != f"{package_head}\n".encode():
        fail("PACKAGE_SEMANTIC_DRIFT", "HEAD.txt")
    old_manifest = tree_manifest(root, package_head, OLD_PACK)
    new_manifest = tree_manifest(root, package_head, NEW_PACK)
    if (package / "old-manifest.tsv").read_bytes() != old_manifest:
        fail("PACKAGE_SEMANTIC_DRIFT", "old-manifest.tsv")
    if (package / "new-manifest.tsv").read_bytes() != new_manifest:
        fail("PACKAGE_SEMANTIC_DRIFT", "new-manifest.tsv")
    old_paths = manifest_paths(old_manifest)
    if len(old_paths) != 20 or len(manifest_paths(new_manifest)) != 20:
        fail("PACK_CARDINALITY", "manifest cardinality")
    del old_paths
    task_before = run_git(root, ["show", f"{package_head}:{TASK_PATH.as_posix()}"]).stdout
    candidate = (package / "task-candidate.md").read_bytes()
    candidate_marker, _ = parse_marker(candidate)
    expected_state = "PACKAGE_REVIEW_PENDING" if attempt == 1 else "ATTEMPT_2_PENDING"
    if candidate_marker.get("attempt") != attempt or candidate_marker.get("state") != expected_state:
        fail("PACKAGE_SEMANTIC_DRIFT", "task-candidate.md marker")
    validate_package_prehistory(
        root,
        attempt,
        candidate_marker,
        live_reviewed_head,
        reviewed_code_head,
    )
    task_patch = write_task_patch(root, package_head, TASK_PATH, candidate)
    semantic_payloads = {
        "task-before.md": task_before,
        "task-before-to-candidate.patch": task_patch,
        "proposed-deletion.patch": projection.proposed_deletion_patch,
        "spec.md": run_git(root, ["show", f"{package_head}:{SPEC_PATH.as_posix()}"]).stdout,
        "plan.md": run_git(root, ["show", f"{package_head}:{PLAN_PATH.as_posix()}"]).stdout,
    }
    for name, expected in semantic_payloads.items():
        if (package / name).read_bytes() != expected:
            fail("PACKAGE_SEMANTIC_DRIFT", name)
    if (package / "llm-wiki-index.md").read_bytes() != projection.index_markdown:
        fail("PACKAGE_SEMANTIC_DRIFT", INDEX.as_posix())
    if (
        package / "llm-wiki-stage-category-coverage.md"
    ).read_bytes() != projection.coverage_markdown:
        fail("PACKAGE_SEMANTIC_DRIFT", COVERAGE.as_posix())
    prove_live_head(root, live_reviewed_head, code="UNTRUSTED_PACKAGE_HEAD")
    return {
        "attempt": attempt,
        "assignments": assignments,
        "head": package_head,
        "package_doc": package_doc,
        "package_sha256": sha256_bytes((package / "SHA256SUMS").read_bytes()),
    }


def verify_package(args: argparse.Namespace) -> None:
    root = repository_root()
    authority = authority_from_args(root, args)
    result = verify_package_path(
        root,
        pathlib.Path(args.package).resolve(),
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(canonical_json({"package_sha256": result["package_sha256"], "state": "VERIFIED"}).decode(), end="")


def load_attestation(
    package_result: dict[str, Any], attestation_path: pathlib.Path
) -> dict[str, Any]:
    attestation = load_canonical_json(attestation_path)
    expected_keys = {
        "assignments",
        "attempt",
        "controller_task",
        "kind",
        "package_head",
        "package_sha256",
        "schema",
        "source",
    }
    if set(attestation) != expected_keys or attestation.get("kind") != "assignment-attestation":
        fail("INVALID_ATTESTATION", "unexpected assignment-attestation schema")
    if (
        attestation.get("attempt") != package_result["attempt"]
        or attestation.get("package_head") != package_result["head"]
        or attestation.get("package_sha256") != package_result["package_sha256"]
        or attestation.get("source") != "collaboration.spawn_agent/result"
        or attestation.get("controller_task") != "/root"
    ):
        fail("INVALID_ATTESTATION", "package/controller binding mismatch")
    package_assignments = package_result["assignments"]["assignments"]
    rows = attestation.get("assignments")
    if not isinstance(rows, list) or len(rows) != 2:
        fail("INVALID_ATTESTATION", "exactly two role assignments are required")
    expected_rows: list[dict[str, str]] = []
    for package_row in package_assignments:
        role = package_row["role"]
        matches = [row for row in rows if isinstance(row, dict) and row.get("role") == role]
        if len(matches) != 1:
            fail("INVALID_ATTESTATION", f"missing or duplicate role {role}")
        row = matches[0]
        if set(row) != {"agent_id", "role", "run_id", "task_path"}:
            fail("INVALID_ATTESTATION", f"unexpected fields for {role}")
        if row.get("run_id") != package_row["run_id"]:
            fail("INVALID_ATTESTATION", f"run-id mismatch for {role}")
        if not all(isinstance(row.get(key), str) and row[key] for key in ("agent_id", "task_path")):
            fail("INVALID_ATTESTATION", f"empty identity for {role}")
        expected_rows.append(row)
    if rows != expected_rows:
        fail("INVALID_ATTESTATION", "role records must follow package role order")
    if len({row["agent_id"] for row in rows}) != 2 or len({row["task_path"] for row in rows}) != 2:
        fail("IDENTITY_COLLISION", "reviewers must have distinct agent IDs and task paths")
    return attestation


def verify_assignments(args: argparse.Namespace) -> None:
    root = repository_root()
    authority = authority_from_args(root, args)
    package_result = verify_package_path(
        root,
        pathlib.Path(args.package).resolve(),
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    attestation_path = pathlib.Path(args.attestation).resolve()
    load_attestation(package_result, attestation_path)
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(
        canonical_json(
            {
                "assignment_attestation_sha256": sha256_bytes(attestation_path.read_bytes()),
                "state": "ASSIGNED",
            }
        ).decode(),
        end="",
    )


def validate_receipt(
    path: pathlib.Path,
    role: str,
    package_result: dict[str, Any],
    attestation: dict[str, Any],
    attestation_sha256: str,
    *,
    require_approved: bool,
) -> dict[str, Any]:
    receipt = load_canonical_json(path)
    expected_keys = {
        "agent_id",
        "assignment_attestation_sha256",
        "attempt",
        "findings",
        "kind",
        "package_head",
        "package_sha256",
        "report",
        "role",
        "run_id",
        "schema",
        "task_path",
        "verdict",
    }
    if set(receipt) != expected_keys or receipt.get("kind") != "package-review-receipt":
        fail("INVALID_RECEIPT", f"{role}: unexpected receipt schema")
    identity = next(row for row in attestation["assignments"] if row["role"] == role)
    bindings = {
        "agent_id": identity["agent_id"],
        "assignment_attestation_sha256": attestation_sha256,
        "attempt": package_result["attempt"],
        "package_head": package_result["head"],
        "package_sha256": package_result["package_sha256"],
        "role": role,
        "run_id": identity["run_id"],
        "task_path": identity["task_path"],
    }
    if any(receipt.get(key) != value for key, value in bindings.items()):
        fail("RECEIPT_BINDING_DRIFT", role)
    report = receipt.get("report")
    if not isinstance(report, dict) or set(report) != {"bytes", "sha256"}:
        fail("INVALID_RECEIPT", f"{role}: invalid report record")
    if not nonnegative_int(report["bytes"]) or not re.fullmatch(
        r"[0-9a-f]{64}", str(report["sha256"])
    ):
        fail("INVALID_RECEIPT", f"{role}: invalid report identity")
    findings = receipt.get("findings")
    if not isinstance(findings, dict) or set(findings) != {"critical", "important", "minor"}:
        fail("INVALID_RECEIPT", f"{role}: invalid findings")
    if any(not nonnegative_int(findings[key]) for key in findings):
        fail("INVALID_RECEIPT", f"{role}: invalid finding count")
    if receipt.get("verdict") not in {"Approved", "Approved-with-Minor", "Needs fixes"}:
        fail("INVALID_RECEIPT", f"{role}: invalid verdict")
    if require_approved and (findings["critical"] or findings["important"]):
        fail("LOAD_BEARING_FINDING", role)
    if require_approved and receipt.get("verdict") != "Approved":
        fail("REJECTED_REVIEW", role)
    return receipt


def expected_backfilled_marker(
    package: pathlib.Path,
    package_result: dict[str, Any],
    receipt_paths: Mapping[str, pathlib.Path],
    receipts: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    reviews: dict[str, Any] = {}
    for role in ROLES:
        receipt = receipts[role]
        reviews[role] = {
            "agent_id": receipt["agent_id"],
            "assignment_attestation_sha256": receipt[
                "assignment_attestation_sha256"
            ],
            "findings": receipt["findings"],
            "receipt_sha256": sha256_bytes(receipt_paths[role].read_bytes()),
            "role": role,
            "run_id": receipt["run_id"],
            "task_path": receipt["task_path"],
            "verdict": receipt["verdict"],
        }
    return {
        "actual_committed_deletion_review": "Not Run",
        "actual_staged_deletion_review": "Not Run",
        "attempt": package_result["attempt"],
        "evidence_ref": fixed_evidence_ref(
            package_result["attempt"], package_result["package_sha256"]
        ),
        "new_manifest_sha256": sha256_bytes((package / "new-manifest.tsv").read_bytes()),
        "old_manifest_sha256": sha256_bytes((package / "old-manifest.tsv").read_bytes()),
        "package_sha256": package_result["package_sha256"],
        "proposed_deletion_patch_sha256": sha256_bytes(
            (package / "proposed-deletion.patch").read_bytes()
        ),
        "recovery_head": package_result["head"],
        "reviews": reviews,
        "schema": SCHEMA,
        "state": "TASK_BACKFILLED",
    }


def validate_task_state(
    package: pathlib.Path,
    package_result: dict[str, Any],
    task_path: pathlib.Path,
    expect_state: str,
    receipt_paths: Mapping[str, pathlib.Path],
    receipts: Mapping[str, dict[str, Any]],
) -> None:
    candidate = (package / "task-candidate.md").read_bytes()
    current = task_path.read_bytes()
    candidate_marker, candidate_span = parse_marker(candidate)
    current_marker, current_span = parse_marker(current)
    if expect_state == "PACKAGE_REVIEWED":
        if current != candidate:
            fail("TASK_CANDIDATE_DRIFT", "Task differs before backfill")
        if candidate_marker.get("state") not in {"PACKAGE_REVIEW_PENDING", "ATTEMPT_2_PENDING"}:
            fail("TASK_STATE_MISMATCH", str(candidate_marker.get("state")))
        return
    if expect_state != "TASK_BACKFILLED":
        fail("TASK_STATE_MISMATCH", expect_state)
    candidate_without_marker = candidate[: candidate_span[0]] + candidate[candidate_span[1] :]
    current_without_marker = current[: current_span[0]] + current[current_span[1] :]
    if candidate_without_marker != current_without_marker:
        fail("TASK_OUTSIDE_MARKER_DRIFT", "bytes outside the Gate 9 marker changed")
    expected_marker = expected_backfilled_marker(
        package, package_result, receipt_paths, receipts
    )
    if current_marker != expected_marker:
        fail("TASK_MARKER_DRIFT", "TASK_BACKFILLED marker does not match receipts/package")


def verify_backfill(args: argparse.Namespace) -> None:
    root = repository_root()
    authority = authority_from_args(root, args)
    package = pathlib.Path(args.package).resolve()
    package_result = verify_package_path(
        root,
        package,
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    attestation_path = pathlib.Path(args.assignment_attestation).resolve()
    attestation = load_attestation(package_result, attestation_path)
    attestation_sha256 = sha256_bytes(attestation_path.read_bytes())
    receipt_paths = {
        "migration-specification": pathlib.Path(args.migration_receipt).resolve(),
        "quality": pathlib.Path(args.quality_receipt).resolve(),
    }
    receipts = {
        role: validate_receipt(
            receipt_paths[role],
            role,
            package_result,
            attestation,
            attestation_sha256,
            require_approved=True,
        )
        for role in ROLES
    }
    task_relative, task_path = repo_path(root, args.task)
    del task_relative
    validate_task_state(
        package,
        package_result,
        task_path,
        args.expect_state,
        receipt_paths,
        receipts,
    )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(canonical_json({"state": args.expect_state}).decode(), end="")


def task_transition_patch(
    root: pathlib.Path,
    before: bytes,
    after: bytes,
    task: pathlib.PurePosixPath,
) -> bytes:
    with PinnedScratch("gate9-task-transition-") as scratch:
        environment = {"GIT_INDEX_FILE": os.fspath(scratch.path / "index")}
        run_git(
            root,
            ["read-tree", "--empty"],
            env=environment,
            pass_fds=scratch.pass_fds,
        )
        scratch.register_file("index")
        before_oid = run_git(
            root, ["hash-object", "-w", "--stdin"], env=environment, input_bytes=before
        ).stdout.decode().strip()
        run_git(
            root,
            ["update-index", "--add", "--cacheinfo", "100644", before_oid, task.as_posix()],
            env=environment,
            pass_fds=scratch.pass_fds,
        )
        scratch.register_file("index")
        before_tree = run_git(
            root,
            ["write-tree"],
            env=environment,
            pass_fds=scratch.pass_fds,
        ).stdout.decode().strip()
        after_oid = run_git(
            root, ["hash-object", "-w", "--stdin"], env=environment, input_bytes=after
        ).stdout.decode().strip()
        run_git(
            root,
            ["update-index", "--cacheinfo", "100644", after_oid, task.as_posix()],
            env=environment,
            pass_fds=scratch.pass_fds,
        )
        scratch.register_file("index")
        result = run_git(
            root,
            [
                "diff",
                "--cached",
                "--binary",
                "--full-index",
                before_tree,
                "--",
                task.as_posix(),
            ],
            env=environment,
            pass_fds=scratch.pass_fds,
        ).stdout
        scratch.register_file("index")
        return result


def file_record(path: str, value: bytes) -> dict[str, object]:
    return {"bytes": len(value), "path": path, "sha256": sha256_bytes(value)}


def blob_record(root: pathlib.Path, value: bytes) -> dict[str, object]:
    oid = run_git(root, ["hash-object", "--stdin"], input_bytes=value).stdout.decode().strip()
    return {"blob_oid": oid, "bytes": len(value), "sha256": sha256_bytes(value)}


def checked_report(path: pathlib.Path, label: str) -> bytes:
    try:
        value = path.read_bytes()
        decoded = value.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        fail("INVALID_REPORT", f"{label}: {error}")
    if "\r" in decoded or not value.endswith(b"\n"):
        fail("INVALID_REPORT", f"{label}: require UTF-8/LF and final newline")
    return value


def validate_report_binding(receipt: dict[str, Any], report: bytes, role: str) -> None:
    if receipt["report"] != {
        "bytes": len(report),
        "sha256": sha256_bytes(report),
    }:
        fail("REPORT_BINDING_DRIFT", role)


def validate_closure(
    path: pathlib.Path,
    report: bytes,
    role: str,
    receipt_path: pathlib.Path,
    receipt: dict[str, Any],
    attestation_sha256: str,
    task_tuple: dict[str, Any],
) -> dict[str, Any]:
    closure = load_canonical_json(path)
    expected_keys = {
        "agent_id",
        "assignment_attestation_sha256",
        "attempt",
        "findings",
        "kind",
        "marker_match",
        "non_marker_unchanged",
        "package_receipt_sha256",
        "package_sha256",
        "report",
        "role",
        "run_id",
        "schema",
        "task",
        "task_path",
        "verdict",
    }
    if set(closure) != expected_keys or closure.get("kind") != "closure":
        fail("INVALID_CLOSURE", f"{role}: unexpected schema")
    expected_bindings = {
        "agent_id": receipt["agent_id"],
        "assignment_attestation_sha256": attestation_sha256,
        "attempt": receipt["attempt"],
        "package_receipt_sha256": sha256_bytes(receipt_path.read_bytes()),
        "package_sha256": receipt["package_sha256"],
        "role": role,
        "run_id": receipt["run_id"],
        "task_path": receipt["task_path"],
    }
    if any(closure.get(key) != value for key, value in expected_bindings.items()):
        fail("CLOSURE_BINDING_DRIFT", role)
    if closure.get("task") != task_tuple:
        fail("CLOSURE_TASK_DRIFT", role)
    if closure.get("report") != {"bytes": len(report), "sha256": sha256_bytes(report)}:
        fail("CLOSURE_REPORT_DRIFT", role)
    findings = closure.get("findings")
    if (
        not isinstance(findings, dict)
        or set(findings) != {"critical", "important", "minor"}
        or any(not nonnegative_int(findings[key]) for key in findings)
        or findings["critical"] != 0
        or findings["important"] != 0
    ):
        fail("LOAD_BEARING_FINDING", f"closure {role}")
    if (
        closure.get("verdict") != "Approved"
        or closure.get("marker_match") is not True
        or closure.get("non_marker_unchanged") is not True
    ):
        fail("REJECTED_CLOSURE", role)
    return closure


def sentinel_json(kind: str, role: str | None = None, state: str = "NOT_RUN") -> bytes:
    value: dict[str, object] = {"kind": kind, "schema": SCHEMA, "state": state}
    if role is not None:
        value["role"] = role
    return canonical_json(value)


def evidence_commit_message(attempt: int, package_sha256: str, state: str) -> bytes:
    lines = sorted(
        (
            f"attempt={attempt}",
            f"package-sha256={package_sha256}",
            f"state={state}",
        )
    )
    return (
        "agentic-research-gate9-evidence/v1\n\n" + "\n".join(lines) + "\n"
    ).encode()


def write_evidence_tree(root: pathlib.Path, leaves: Mapping[str, bytes]) -> str:
    with PinnedScratch("gate9-evidence-index-") as scratch:
        environment = {"GIT_INDEX_FILE": os.fspath(scratch.path / "index")}
        run_git(
            root,
            ["read-tree", "--empty"],
            env=environment,
            pass_fds=scratch.pass_fds,
        )
        scratch.register_file("index")
        for path in sorted(leaves):
            oid = run_git(
                root,
                ["hash-object", "-w", "--stdin"],
                env=environment,
                input_bytes=leaves[path],
                pass_fds=scratch.pass_fds,
            ).stdout.decode().strip()
            run_git(
                root,
                ["update-index", "--add", "--cacheinfo", "100644", oid, path],
                env=environment,
                pass_fds=scratch.pass_fds,
            )
            scratch.register_file("index")
        result = run_git(
            root,
            ["write-tree"],
            env=environment,
            pass_fds=scratch.pass_fds,
        ).stdout.decode().strip()
        scratch.register_file("index")
        return result


def commit_identity(root: pathlib.Path, commit: str) -> tuple[str, str, bytes]:
    raw = run_git(root, ["cat-file", "commit", commit]).stdout
    header, separator, message = raw.partition(b"\n\n")
    if not separator:
        fail("INVALID_EVIDENCE_COMMIT", commit)
    parents = [line.split(b" ", 1)[1].decode() for line in header.splitlines() if line.startswith(b"parent ")]
    tree_lines = [line.split(b" ", 1)[1].decode() for line in header.splitlines() if line.startswith(b"tree ")]
    if len(parents) != 1 or len(tree_lines) != 1:
        fail("INVALID_EVIDENCE_COMMIT", "expected one parent and one tree")
    return parents[0], tree_lines[0], message


def create_or_reuse_ref(
    root: pathlib.Path,
    evidence_ref: str,
    package_head: str,
    tree_oid: str,
    message: bytes,
) -> str:
    existing_result = run_git(root, ["show-ref", "--verify", "--hash", evidence_ref], check=False)
    existing = existing_result.stdout.decode().strip() if existing_result.returncode == 0 else ""
    desired_identity = (package_head, tree_oid, message)

    def matches(commit: str) -> bool:
        try:
            return commit_identity(root, commit) == desired_identity
        except Gate9Error:
            return False

    if existing:
        if matches(existing):
            return existing
        fail("FOREIGN_REF", evidence_ref)
    commit = run_git(
        root,
        ["commit-tree", tree_oid, "-p", package_head],
        input_bytes=message,
    ).stdout.decode().strip()
    update = run_git(
        root,
        ["update-ref", evidence_ref, commit, "0" * 40],
        check=False,
    )
    if update.returncode == 0:
        return commit
    raced = run_git(root, ["show-ref", "--verify", "--hash", evidence_ref], check=False)
    raced_commit = raced.stdout.decode().strip() if raced.returncode == 0 else ""
    if raced_commit and matches(raced_commit):
        return raced_commit
    fail("FOREIGN_REF", evidence_ref)


def build_evidence_leaves(
    root: pathlib.Path,
    package: pathlib.Path,
    package_result: dict[str, Any],
    task_relative: pathlib.PurePosixPath,
    task_path: pathlib.Path,
    state: str,
    terminal_report_path: pathlib.Path,
    attestation_path: pathlib.Path,
    optional_paths: Mapping[str, pathlib.Path | None],
) -> dict[str, bytes]:
    attestation = load_attestation(package_result, attestation_path)
    attestation_bytes = attestation_path.read_bytes()
    attestation_sha256 = sha256_bytes(attestation_bytes)
    leaves = {
        f"package/{name}": (package / name).read_bytes() for name in PACKAGE_ATTACHMENTS
    }
    leaves["assignment-attestation.json"] = attestation_bytes
    terminal_report = checked_report(terminal_report_path, "terminal report")
    leaves["terminal/report.md"] = terminal_report
    candidate = (package / "task-candidate.md").read_bytes()
    task_after = task_path.read_bytes() if state == "AUTHORIZED" else candidate
    task_patch = task_transition_patch(root, candidate, task_after, task_relative) if state == "AUTHORIZED" else b""
    leaves["task/task-after.md"] = task_after
    leaves["task/task-candidate-to-after.patch"] = task_patch
    task_tuple = {
        "after": blob_record(root, task_after),
        "before": blob_record(root, candidate),
        "diff": {"bytes": len(task_patch), "sha256": sha256_bytes(task_patch)},
    }
    receipt_paths: dict[str, pathlib.Path] = {}
    receipts: dict[str, dict[str, Any]] = {}
    closures: dict[str, dict[str, Any]] = {}
    review_records: dict[str, Any] = {}
    closure_records: dict[str, Any] = {}
    for role in ROLES:
        prefix = "migration" if role == "migration-specification" else "quality"
        report_path = optional_paths.get(f"{prefix}_report")
        receipt_path = optional_paths.get(f"{prefix}_receipt")
        closure_report_path = optional_paths.get(f"{prefix}_closure_report")
        closure_path = optional_paths.get(f"{prefix}_closure")
        review_report_leaf = f"reviews/{role}/report.md"
        review_receipt_leaf = f"reviews/{role}/receipt.json"
        closure_report_leaf = f"closures/{role}/report.md"
        closure_leaf = f"closures/{role}/closure.json"
        if state != "AUTHORIZED" and (
            closure_report_path is not None or closure_path is not None
        ):
            fail("INCOMPLETE_EVIDENCE", f"{state} requires NOT_RUN closure for {role}")
        if report_path is not None and receipt_path is not None:
            report = checked_report(report_path, f"{role} review")
            receipt = validate_receipt(
                receipt_path,
                role,
                package_result,
                attestation,
                attestation_sha256,
                require_approved=state == "AUTHORIZED",
            )
            validate_report_binding(receipt, report, role)
            leaves[review_report_leaf] = report
            leaves[review_receipt_leaf] = receipt_path.read_bytes()
            receipt_paths[role] = receipt_path
            receipts[role] = receipt
            review_records[role] = {
                **{key: receipt[key] for key in ("agent_id", "assignment_attestation_sha256", "role", "run_id", "task_path", "verdict", "findings")},
                "receipt": file_record(review_receipt_leaf, leaves[review_receipt_leaf]),
                "report": file_record(review_report_leaf, report),
            }
        else:
            leaves[review_report_leaf] = b"NOT_RUN\n"
            leaves[review_receipt_leaf] = sentinel_json("package-review-receipt", role)
            review_records[role] = {
                "receipt": file_record(review_receipt_leaf, leaves[review_receipt_leaf]),
                "report": file_record(review_report_leaf, leaves[review_report_leaf]),
                "state": "NOT_RUN",
            }
        if closure_report_path is not None and closure_path is not None:
            if role not in receipts:
                fail("INCOMPLETE_EVIDENCE", f"closure without review for {role}")
            closure_report = checked_report(closure_report_path, f"{role} closure")
            closure = validate_closure(
                closure_path,
                closure_report,
                role,
                receipt_paths[role],
                receipts[role],
                attestation_sha256,
                task_tuple,
            )
            leaves[closure_report_leaf] = closure_report
            leaves[closure_leaf] = closure_path.read_bytes()
            closures[role] = closure
            closure_records[role] = {
                **{key: closure[key] for key in ("agent_id", "role", "run_id", "task_path", "verdict", "findings")},
                "closure": file_record(closure_leaf, leaves[closure_leaf]),
                "report": file_record(closure_report_leaf, closure_report),
            }
        else:
            leaves[closure_report_leaf] = b"NOT_RUN\n"
            leaves[closure_leaf] = sentinel_json("closure", role)
            closure_records[role] = {
                "closure": file_record(closure_leaf, leaves[closure_leaf]),
                "report": file_record(closure_report_leaf, leaves[closure_report_leaf]),
                "state": "NOT_RUN",
            }
    if state == "AUTHORIZED":
        if set(receipts) != set(ROLES) or set(closures) != set(ROLES):
            fail("INCOMPLETE_EVIDENCE", "AUTHORIZED requires two reviews and two closures")
        validate_task_state(
            package, package_result, task_path, "TASK_BACKFILLED", receipt_paths, receipts
        )
    elif state == "REJECTED":
        if set(receipts) != set(ROLES):
            fail("INCOMPLETE_EVIDENCE", "REJECTED requires both completed review pairs")
        if not any(
            receipt["findings"]["critical"]
            or receipt["findings"]["important"]
            or receipt["verdict"] == "Needs fixes"
            for receipt in receipts.values()
        ):
            fail("REJECTED_WITHOUT_FINDING", "both completed reviews are load-bearing clean")
    drift_path = optional_paths.get("drift_proof")
    invalidation_reason: str | None = None
    if state == "INVALIDATED":
        if drift_path is None:
            fail("INCOMPLETE_EVIDENCE", "INVALIDATED requires drift proof")
        drift_value = load_canonical_json(drift_path)
        invalidation_reason = drift_value.get("reason")
        if (
            not isinstance(invalidation_reason, str)
            or not invalidation_reason.strip()
            or invalidation_reason != invalidation_reason.strip()
            or "\n" in invalidation_reason
            or "\r" in invalidation_reason
        ):
            fail("INVALIDATED_REASON_INVALID", os.fspath(drift_path))
        if set(drift_value) != {"kind", "reason", "schema", "state"} or (
            drift_value.get("kind") != "drift-proof"
            or drift_value.get("state") != "INVALIDATED"
        ):
            fail("INVALID_DRIFT_PROOF", os.fspath(drift_path))
        leaves["drift/drift-proof.json"] = drift_path.read_bytes()
    else:
        leaves["drift/drift-proof.json"] = sentinel_json(
            "drift-proof", state="NOT_APPLICABLE"
        )
    expected_terminal = (
        b"AUTHORIZED\n"
        if state == "AUTHORIZED"
        else b"REJECTED: package-review-rejected\n"
        if state == "REJECTED"
        else f"INVALIDATED: {invalidation_reason}\n".encode()
    )
    if terminal_report != expected_terminal:
        fail("TERMINAL_REPORT_DRIFT", state)
    evidence_ref = fixed_evidence_ref(
        package_result["attempt"], package_result["package_sha256"]
    )
    evidence = {
        "assignment": file_record("assignment-attestation.json", attestation_bytes),
        "attempt": package_result["attempt"],
        "closures": closure_records,
        "drift": file_record("drift/drift-proof.json", leaves["drift/drift-proof.json"]),
        "evidence_ref": evidence_ref,
        "package_head": package_result["head"],
        "package_sha256": package_result["package_sha256"],
        "reviews": review_records,
        "schema": SCHEMA,
        "state": state,
        "task": {
            "after": file_record("task/task-after.md", task_after),
            "candidate_to_after_patch": file_record(
                "task/task-candidate-to-after.patch", task_patch
            ),
        },
        "terminal_report": file_record("terminal/report.md", terminal_report),
    }
    leaves["evidence.json"] = canonical_json(evidence)
    non_sum_leaves = dict(leaves)
    leaves["SHA256SUMS"] = checksum_manifest(non_sum_leaves)
    return leaves


def publish_evidence_ref(args: argparse.Namespace) -> None:
    root = repository_root()
    authority = authority_from_args(root, args)
    package = pathlib.Path(args.package).resolve()
    package_result = verify_package_path(
        root,
        package,
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    task_relative, task_path = repo_path(root, args.task)
    evidence_ref = fixed_evidence_ref(
        package_result["attempt"], package_result["package_sha256"]
    )
    if args.evidence_ref != "auto" and args.evidence_ref != evidence_ref:
        fail("EVIDENCE_REF_MISMATCH", args.evidence_ref)
    optional_names = (
        "migration_report",
        "migration_receipt",
        "quality_report",
        "quality_receipt",
        "migration_closure_report",
        "migration_closure",
        "quality_closure_report",
        "quality_closure",
        "drift_proof",
    )
    optional_paths = {
        name: pathlib.Path(getattr(args, name)).resolve() if getattr(args, name) else None
        for name in optional_names
    }
    leaves = build_evidence_leaves(
        root,
        package,
        package_result,
        task_relative,
        task_path,
        args.terminal_state,
        pathlib.Path(args.terminal_report).resolve(),
        pathlib.Path(args.assignment_attestation).resolve(),
        optional_paths,
    )
    if set(leaves) != EVIDENCE_LEAF_PATHS:
        fail(
            "EVIDENCE_PATH_SET_DRIFT",
            repr(sorted(set(leaves) ^ EVIDENCE_LEAF_PATHS)),
        )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    tree_oid = write_evidence_tree(root, leaves)
    message = evidence_commit_message(
        package_result["attempt"], package_result["package_sha256"], args.terminal_state
    )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    evidence_commit = create_or_reuse_ref(
        root, evidence_ref, package_result["head"], tree_oid, message
    )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(
        canonical_json(
            {
                "evidence_commit": evidence_commit,
                "evidence_ref": evidence_ref,
                "state": args.terminal_state,
            }
        ).decode(),
        end="",
    )


def resolve_evidence_ref(
    task_marker: dict[str, Any], requested: str
) -> str:
    marker_ref = task_marker.get("evidence_ref")
    if not isinstance(marker_ref, str) or not marker_ref.startswith(f"{REF_PREFIX}/attempt-"):
        fail("INVALID_TASK_MARKER", "missing fixed evidence ref")
    if requested != "auto" and requested != marker_ref:
        fail("EVIDENCE_REF_MISMATCH", requested)
    return marker_ref


def read_ref_leaves(
    root: pathlib.Path, evidence_ref: str
) -> tuple[str, dict[str, bytes]]:
    ref_result = run_git(
        root, ["show-ref", "--verify", "--hash", evidence_ref], check=False
    )
    if ref_result.returncode:
        fail("MISSING_EVIDENCE_REF", evidence_ref)
    commit = ref_result.stdout.decode().strip()
    listing = run_git(root, ["ls-tree", "-r", "--full-tree", commit]).stdout
    leaves: dict[str, bytes] = {}
    for line in listing.splitlines():
        metadata, separator, raw_path = line.partition(b"\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            fail("INVALID_EVIDENCE_TREE", line.decode("utf-8", "replace"))
        mode, object_type, _ = fields
        path = raw_path.decode("utf-8")
        if mode != b"100644" or object_type != b"blob":
            fail("EVIDENCE_MODE_DRIFT", path)
        leaves[path] = run_git(root, ["show", f"{commit}:{path}"]).stdout
    if set(leaves) != EVIDENCE_LEAF_PATHS:
        fail(
            "EVIDENCE_PATH_SET_DRIFT",
            repr(sorted(set(leaves) ^ EVIDENCE_LEAF_PATHS)),
        )
    expected_sums = checksum_manifest(
        {path: value for path, value in leaves.items() if path != "SHA256SUMS"}
    )
    if leaves["SHA256SUMS"] != expected_sums:
        fail("EVIDENCE_CHECKSUM_DRIFT", evidence_ref)
    return commit, leaves


def preflight_evidence_ref_authority(
    root: pathlib.Path,
    evidence_commit: str,
    leaves: Mapping[str, bytes],
    live_reviewed_head: str,
) -> None:
    parent, _, _ = commit_identity(root, evidence_commit)
    if parent != live_reviewed_head:
        fail(
            "EVIDENCE_COMMIT_IDENTITY_DRIFT",
            "evidence commit parent differs from live reviewed HEAD",
        )
    raw_package_head = leaves.get("package/HEAD.txt")
    try:
        package_head = (
            raw_package_head.decode("ascii").strip()
            if raw_package_head is not None
            else ""
        )
    except UnicodeDecodeError as error:
        fail("EVIDENCE_COMMIT_IDENTITY_DRIFT", f"package HEAD is not ASCII: {error}")
    package_oid = require_full_commit_oid(
        root,
        package_head,
        code="EVIDENCE_COMMIT_IDENTITY_DRIFT",
    )
    if (
        package_oid != live_reviewed_head
        or raw_package_head != f"{package_oid}\n".encode()
    ):
        fail(
            "EVIDENCE_COMMIT_IDENTITY_DRIFT",
            "evidence package HEAD differs from live reviewed HEAD",
        )
    prove_live_head(
        root,
        live_reviewed_head,
        code="EVIDENCE_COMMIT_IDENTITY_DRIFT",
    )


def materialize_evidence(
    leaves: Mapping[str, bytes], scratch: PinnedScratch
) -> pathlib.Path:
    for relative, value in leaves.items():
        scratch.create_file(relative, value, mode=0o444)
    return scratch.path


def replay_terminal_evidence_ref(
    root: pathlib.Path,
    evidence_ref: str,
    live_reviewed_head: str,
    reviewed_code_head: str,
) -> dict[str, object]:
    evidence_commit, leaves = read_ref_leaves(root, evidence_ref)
    preflight_evidence_ref_authority(
        root,
        evidence_commit,
        leaves,
        live_reviewed_head,
    )
    with PinnedScratch("gate9-terminal-replay-") as scratch:
        evidence_root = materialize_evidence(leaves, scratch)
        package = evidence_root / "package"
        package_result = verify_package_path(
            root,
            package,
            live_reviewed_head=live_reviewed_head,
            reviewed_code_head=reviewed_code_head,
        )
        evidence = load_canonical_json(evidence_root / "evidence.json")
        state = evidence.get("state")
        if state not in {"REJECTED", "INVALIDATED"}:
            fail("ATTEMPT_STATE_MISMATCH", "attempt 1 is not pre-backfill terminal")
        expected_ref = fixed_evidence_ref(
            package_result["attempt"], package_result["package_sha256"]
        )
        if evidence_ref != expected_ref:
            fail("EVIDENCE_REF_MISMATCH", evidence_ref)
        optional_paths: dict[str, pathlib.Path | None] = {
            "migration_closure_report": None,
            "migration_closure": None,
            "quality_closure_report": None,
            "quality_closure": None,
            "drift_proof": (
                evidence_root / "drift/drift-proof.json"
                if state == "INVALIDATED"
                else None
            ),
        }
        for role in ROLES:
            prefix = "migration" if role == "migration-specification" else "quality"
            receipt_leaf = f"reviews/{role}/receipt.json"
            if leaves[receipt_leaf] == sentinel_json("package-review-receipt", role):
                optional_paths[f"{prefix}_report"] = None
                optional_paths[f"{prefix}_receipt"] = None
            else:
                optional_paths[f"{prefix}_report"] = evidence_root / f"reviews/{role}/report.md"
                optional_paths[f"{prefix}_receipt"] = evidence_root / receipt_leaf
        reconstructed = build_evidence_leaves(
            root,
            package,
            package_result,
            TASK_PATH,
            evidence_root / "task/task-after.md",
            state,
            evidence_root / "terminal/report.md",
            evidence_root / "assignment-attestation.json",
            optional_paths,
        )
        if reconstructed != leaves:
            fail("EVIDENCE_SCHEMA_DRIFT", evidence_ref)
        expected_tree = write_evidence_tree(root, reconstructed)
        parent, tree_oid, message = commit_identity(root, evidence_commit)
        expected_message = evidence_commit_message(
            package_result["attempt"], package_result["package_sha256"], state
        )
        if (
            parent != package_result["head"]
            or tree_oid != expected_tree
            or message != expected_message
        ):
            fail("EVIDENCE_COMMIT_IDENTITY_DRIFT", evidence_ref)
        reason = "package-review-rejected"
        if state == "INVALIDATED":
            drift = load_canonical_json(evidence_root / "drift/drift-proof.json")
            reason = drift["reason"]
        return {
            "attempt": package_result["attempt"],
            "package_sha256": package_result["package_sha256"],
            "reason": reason,
            "state": state,
            "tree": tree_oid,
        }


def verify_authorized(args: argparse.Namespace) -> None:
    root = repository_root()
    authority = authority_from_args(root, args)
    if args.package:
        external_package = pathlib.Path(args.package).resolve()
        if not external_package.is_dir():
            fail("MISSING_PACKAGE", os.fspath(external_package))
        try:
            external_head = (external_package / "HEAD.txt").read_text(
                encoding="ascii"
            ).strip()
        except (OSError, UnicodeDecodeError) as error:
            fail("UNTRUSTED_PACKAGE_HEAD", f"package HEAD cannot be read: {error}")
        external_oid = require_full_commit_oid(
            root,
            external_head,
            code="UNTRUSTED_PACKAGE_HEAD",
        )
        if external_oid != authority.live_head:
            fail(
                "UNTRUSTED_PACKAGE_HEAD",
                "package HEAD differs from live reviewed HEAD",
            )
    task_relative, task_path = repo_path(root, args.task)
    live_task = task_path.read_bytes()
    task_marker, _ = parse_marker(live_task)
    evidence_ref = resolve_evidence_ref(task_marker, args.evidence_ref)
    evidence_commit, leaves = read_ref_leaves(root, evidence_ref)
    preflight_evidence_ref_authority(
        root,
        evidence_commit,
        leaves,
        authority.live_head,
    )
    with PinnedScratch("gate9-ref-replay-") as scratch:
        evidence_root = materialize_evidence(leaves, scratch)
        package = evidence_root / "package"
        package_result = verify_package_path(
            root,
            package,
            live_reviewed_head=authority.live_head,
            reviewed_code_head=authority.reviewed_code_head,
        )
        if args.package:
            external_package = pathlib.Path(args.package).resolve()
            external_result = verify_package_path(
                root,
                external_package,
                live_reviewed_head=authority.live_head,
                reviewed_code_head=authority.reviewed_code_head,
            )
            if external_result["package_sha256"] != package_result["package_sha256"]:
                fail("PACKAGE_ID_DRIFT", os.fspath(external_package))
            for name in PACKAGE_ATTACHMENTS:
                if (external_package / name).read_bytes() != (package / name).read_bytes():
                    fail("PACKAGE_ATTACHMENT_DRIFT", name)
        evidence = load_canonical_json(evidence_root / "evidence.json")
        expected_evidence_keys = {
            "assignment",
            "attempt",
            "closures",
            "drift",
            "evidence_ref",
            "package_head",
            "package_sha256",
            "reviews",
            "schema",
            "state",
            "task",
            "terminal_report",
        }
        if set(evidence) != expected_evidence_keys or evidence.get("state") != "AUTHORIZED":
            fail("NOT_AUTHORIZED", evidence_ref)
        if (
            evidence.get("attempt") != package_result["attempt"]
            or evidence.get("package_head") != package_result["head"]
            or evidence.get("package_sha256") != package_result["package_sha256"]
            or evidence.get("evidence_ref") != evidence_ref
        ):
            fail("EVIDENCE_BINDING_DRIFT", evidence_ref)
        expected_message = evidence_commit_message(
            package_result["attempt"], package_result["package_sha256"], "AUTHORIZED"
        )
        commit_parent, commit_tree, commit_message = commit_identity(root, evidence_commit)
        expected_tree = write_evidence_tree(root, leaves)
        if (
            commit_parent != package_result["head"]
            or commit_tree != expected_tree
            or commit_message != expected_message
        ):
            fail("EVIDENCE_COMMIT_IDENTITY_DRIFT", evidence_ref)
        if live_task != leaves["task/task-after.md"]:
            fail("TASK_AFTER_DRIFT", task_relative.as_posix())
        candidate = leaves["package/task-candidate.md"]
        expected_task_patch = task_transition_patch(root, candidate, live_task, task_relative)
        if leaves["task/task-candidate-to-after.patch"] != expected_task_patch:
            fail("TASK_PATCH_DRIFT", task_relative.as_posix())
        attestation_path = evidence_root / "assignment-attestation.json"
        attestation = load_attestation(package_result, attestation_path)
        attestation_sha256 = sha256_bytes(attestation_path.read_bytes())
        receipt_paths = {
            role: evidence_root / f"reviews/{role}/receipt.json" for role in ROLES
        }
        receipts: dict[str, dict[str, Any]] = {}
        review_records: dict[str, dict[str, Any]] = {}
        for role in ROLES:
            report_path = f"reviews/{role}/report.md"
            receipt_leaf = f"reviews/{role}/receipt.json"
            report = checked_report(evidence_root / report_path, f"{role} review")
            receipt = validate_receipt(
                receipt_paths[role],
                role,
                package_result,
                attestation,
                attestation_sha256,
                require_approved=True,
            )
            validate_report_binding(receipt, report, role)
            receipts[role] = receipt
            review_records[role] = {
                **{
                    key: receipt[key]
                    for key in (
                        "agent_id",
                        "assignment_attestation_sha256",
                        "role",
                        "run_id",
                        "task_path",
                        "verdict",
                        "findings",
                    )
                },
                "receipt": file_record(receipt_leaf, leaves[receipt_leaf]),
                "report": file_record(report_path, report),
            }
        validate_task_state(
            package,
            package_result,
            task_path,
            "TASK_BACKFILLED",
            receipt_paths,
            receipts,
        )
        task_tuple = {
            "after": blob_record(root, live_task),
            "before": blob_record(root, candidate),
            "diff": {
                "bytes": len(expected_task_patch),
                "sha256": sha256_bytes(expected_task_patch),
            },
        }
        closure_records: dict[str, dict[str, Any]] = {}
        for role in ROLES:
            closure_report_path = f"closures/{role}/report.md"
            closure_leaf = f"closures/{role}/closure.json"
            closure_report = checked_report(
                evidence_root / closure_report_path, f"{role} closure"
            )
            closure = validate_closure(
                evidence_root / closure_leaf,
                closure_report,
                role,
                receipt_paths[role],
                receipts[role],
                attestation_sha256,
                task_tuple,
            )
            closure_records[role] = {
                **{
                    key: closure[key]
                    for key in (
                        "agent_id",
                        "role",
                        "run_id",
                        "task_path",
                        "verdict",
                        "findings",
                    )
                },
                "closure": file_record(closure_leaf, leaves[closure_leaf]),
                "report": file_record(closure_report_path, closure_report),
            }
        drift = load_canonical_json(evidence_root / "drift/drift-proof.json")
        if drift != {
            "kind": "drift-proof",
            "schema": SCHEMA,
            "state": "NOT_APPLICABLE",
        }:
            fail("INVALID_DRIFT_PROOF", "AUTHORIZED drift slot")
        terminal_report = checked_report(
            evidence_root / "terminal/report.md", "terminal report"
        )
        expected_evidence = {
            "assignment": file_record(
                "assignment-attestation.json", leaves["assignment-attestation.json"]
            ),
            "attempt": package_result["attempt"],
            "closures": closure_records,
            "drift": file_record(
                "drift/drift-proof.json", leaves["drift/drift-proof.json"]
            ),
            "evidence_ref": evidence_ref,
            "package_head": package_result["head"],
            "package_sha256": package_result["package_sha256"],
            "reviews": review_records,
            "schema": SCHEMA,
            "state": "AUTHORIZED",
            "task": {
                "after": file_record("task/task-after.md", live_task),
                "candidate_to_after_patch": file_record(
                    "task/task-candidate-to-after.patch", expected_task_patch
                ),
            },
            "terminal_report": file_record("terminal/report.md", terminal_report),
        }
        if evidence != expected_evidence:
            fail("EVIDENCE_SCHEMA_DRIFT", evidence_ref)
    if args.require_clean_real_index:
        assert_clean_real_index(root)
    if args.require_task_only_worktree:
        assert_task_only_worktree(root, task_relative)
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(
        canonical_json(
            {
                "evidence_commit": evidence_commit,
                "evidence_ref": evidence_ref,
                "state": "AUTHORIZED",
            }
        ).decode(),
        end="",
    )


def add_authority_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--require-live-head", action="store_true")
    parser.add_argument("--live-reviewed-head")
    parser.add_argument("--reviewed-code-head")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    build = subparsers.add_parser("build-package")
    build.add_argument("--attempt", type=int, required=True)
    build.add_argument("--output", required=True)
    build.add_argument("--spec", required=True)
    build.add_argument("--plan", required=True)
    build.add_argument("--task", required=True)
    add_authority_arguments(build)
    verify = subparsers.add_parser("verify-package")
    verify.add_argument("--package", required=True)
    add_authority_arguments(verify)
    assignments = subparsers.add_parser("verify-assignments")
    assignments.add_argument("--package", required=True)
    assignments.add_argument("--attestation", required=True)
    add_authority_arguments(assignments)
    backfill = subparsers.add_parser("verify-backfill")
    backfill.add_argument("--package", required=True)
    backfill.add_argument("--migration-receipt", required=True)
    backfill.add_argument("--quality-receipt", required=True)
    backfill.add_argument("--assignment-attestation", required=True)
    backfill.add_argument("--task", required=True)
    backfill.add_argument(
        "--expect-state", choices=("PACKAGE_REVIEWED", "TASK_BACKFILLED"), required=True
    )
    add_authority_arguments(backfill)
    publish = subparsers.add_parser("publish-evidence-ref")
    publish.add_argument("--package", required=True)
    publish.add_argument("--task", required=True)
    publish.add_argument(
        "--terminal-state", choices=("AUTHORIZED", "REJECTED", "INVALIDATED"), required=True
    )
    publish.add_argument("--terminal-report", required=True)
    publish.add_argument("--migration-report")
    publish.add_argument("--migration-receipt")
    publish.add_argument("--quality-report")
    publish.add_argument("--quality-receipt")
    publish.add_argument("--assignment-attestation", required=True)
    publish.add_argument("--migration-closure-report")
    publish.add_argument("--migration-closure")
    publish.add_argument("--quality-closure-report")
    publish.add_argument("--quality-closure")
    publish.add_argument("--drift-proof")
    publish.add_argument("--evidence-ref", required=True)
    add_authority_arguments(publish)
    authorized = subparsers.add_parser("verify-authorized")
    package_source = authorized.add_mutually_exclusive_group(required=True)
    package_source.add_argument("--package")
    package_source.add_argument("--package-from-ref", action="store_true")
    authorized.add_argument("--task", required=True)
    authorized.add_argument("--evidence-ref", required=True)
    add_authority_arguments(authorized)
    authorized.add_argument("--require-clean-real-index", action="store_true")
    authorized.add_argument("--require-task-only-worktree", action="store_true")
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    try:
        if args.mode == "build-package":
            build_package(args)
        elif args.mode == "verify-package":
            verify_package(args)
        elif args.mode == "verify-assignments":
            verify_assignments(args)
        elif args.mode == "verify-backfill":
            verify_backfill(args)
        elif args.mode == "publish-evidence-ref":
            publish_evidence_ref(args)
        elif args.mode == "verify-authorized":
            verify_authorized(args)
        else:
            fail("MODE_NOT_IMPLEMENTED", args.mode)
    except Gate9Error as error:
        print(str(error), file=sys.stderr)
        return 2 if error.code == "LIVE_HEAD_REQUIRED" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
