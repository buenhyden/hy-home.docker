"""Fail-closed Git provenance resolution for repository documents."""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import signal
import subprocess
import threading
import time
from collections.abc import Iterable


_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
_RECOVERY_COMMIT = re.compile(r"[0-9a-f]{40}\Z")
_GIT_TIMEOUT_SECONDS = 15
_GIT_OUTPUT_BYTES = 1_048_576
_GIT_TOTAL_BYTES = 2 * _GIT_OUTPUT_BYTES
_GIT_INPUT_BYTES = 1_048_576


@dataclasses.dataclass(frozen=True)
class Provenance:
    """The resolved Git object state for one path at one verified commit."""

    path: pathlib.PurePosixPath
    requested_commit: str
    commit: str | None
    mode: str | None
    object_type: str | None
    object_id: str | None
    exists: bool
    is_regular_blob: bool


@dataclasses.dataclass(frozen=True)
class ArchivedMetadata:
    """The exact legacy recovery fields found on one baseline document."""

    source: pathlib.PurePosixPath
    archived_commit: str
    archived_from: pathlib.PurePosixPath


def _safe_relative_path(path: pathlib.PurePosixPath) -> bool:
    return bool(path.parts) and not path.is_absolute() and all(
        part not in {"", ".", ".."}
        and not part.startswith("-")
        and "\\" not in part
        and ":" not in part
        and all(ord(character) >= 32 and ord(character) != 127 for character in part)
        for part in path.parts
    )


def _kill_and_reap(process: subprocess.Popen[bytes], *, timeout_seconds: float = 1.0) -> bool:
    """Kill a process group and attempt a strictly bounded reap."""

    deadline = time.monotonic() + max(0.01, timeout_seconds)
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            try:
                process.kill()
            except OSError:
                pass
    try:
        process.wait(timeout=max(0.01, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            pass
        try:
            process.wait(timeout=max(0.01, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            return False
    return process.poll() is not None


def _run_git(
    repo_root: pathlib.Path,
    args: list[str],
    *,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """Run fixed-argv Git with simultaneous bounded drains and hard cleanup."""

    if not args or any(
        not isinstance(argument, str)
        or not argument
        or any(ord(character) < 32 or ord(character) == 127 for character in argument)
        for argument in args
    ):
        return subprocess.CompletedProcess(["git", *args], 126, b"", b"invalid arguments")
    if input_bytes is not None and len(input_bytes) > _GIT_INPUT_BYTES:
        return subprocess.CompletedProcess(
            ["git", *args], 126, b"", b"input bound exceeded"
        )
    argv = ["git", *args]
    try:
        process = subprocess.Popen(
            argv,
            cwd=repo_root,
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            close_fds=True,
        )
    except OSError:
        return subprocess.CompletedProcess(argv, 127, b"", b"git unavailable")
    assert process.stdout is not None and process.stderr is not None
    output = {"stdout": bytearray(), "stderr": bytearray()}
    overflow = threading.Event()
    output_lock = threading.Lock()

    def drain(stream: object, label: str) -> None:
        reader = stream
        while not overflow.is_set():
            try:
                chunk = reader.read(65_536)
            except OSError:
                return
            if not chunk:
                return
            with output_lock:
                if (
                    len(output[label]) + len(chunk) > _GIT_OUTPUT_BYTES
                    or len(output["stdout"]) + len(output["stderr"]) + len(chunk)
                    > _GIT_TOTAL_BYTES
                ):
                    overflow.set()
                    return
                output[label].extend(chunk)

    readers = (
        threading.Thread(target=drain, args=(process.stdout, "stdout"), daemon=True),
        threading.Thread(target=drain, args=(process.stderr, "stderr"), daemon=True),
    )
    writer_error = threading.Event()

    def write_input() -> None:
        assert process.stdin is not None and input_bytes is not None
        try:
            process.stdin.write(input_bytes)
            process.stdin.close()
        except (BrokenPipeError, OSError):
            writer_error.set()

    writer = (
        threading.Thread(target=write_input, daemon=True)
        if input_bytes is not None
        else None
    )
    started = time.monotonic()
    for reader in readers:
        reader.start()
    if writer is not None:
        writer.start()
    try:
        while process.poll() is None and not overflow.is_set():
            remaining = _GIT_TIMEOUT_SECONDS - (time.monotonic() - started)
            if remaining <= 0:
                _kill_and_reap(process)
                return subprocess.CompletedProcess(argv, 124, b"", b"deadline exceeded")
            try:
                process.wait(timeout=min(0.05, remaining))
            except subprocess.TimeoutExpired:
                continue
        if overflow.is_set():
            _kill_and_reap(process)
            return subprocess.CompletedProcess(argv, 125, b"", b"output bound exceeded")
        if writer is not None:
            remaining = _GIT_TIMEOUT_SECONDS - (time.monotonic() - started)
            writer.join(timeout=max(0.0, remaining))
            if writer.is_alive():
                _kill_and_reap(process)
                return subprocess.CompletedProcess(argv, 124, b"", b"input deadline exceeded")
        for reader in readers:
            remaining = _GIT_TIMEOUT_SECONDS - (time.monotonic() - started)
            reader.join(timeout=max(0.0, remaining))
        if any(reader.is_alive() for reader in readers):
            _kill_and_reap(process)
            return subprocess.CompletedProcess(argv, 124, b"", b"drain deadline exceeded")
        if writer_error.is_set() and process.returncode == 0:
            return subprocess.CompletedProcess(argv, 125, b"", b"input write failed")
        return subprocess.CompletedProcess(
            argv,
            process.returncode,
            bytes(output["stdout"]),
            bytes(output["stderr"]),
        )
    finally:
        if process.stdin is not None and not process.stdin.closed:
            process.stdin.close()
        for stream in (process.stdout, process.stderr):
            if not stream.closed:
                stream.close()
        if process.poll() is None:
            _kill_and_reap(process)


def verify_recovery_blobs_batch(
    rows: Iterable[tuple[pathlib.PurePosixPath | pathlib.Path | str, str]],
    *,
    repo_root: pathlib.Path,
) -> tuple[Provenance, ...]:
    """Resolve at most 512 recovery references with bounded Git batches.

    Commit object kinds are checked in one ``cat-file --batch-check`` process.
    Paths are then resolved by one exact ``ls-tree`` call per distinct commit,
    and every listed object is proved to exist with a second bounded
    ``cat-file`` batch. This avoids trusting a tree entry whose blob is absent.
    """

    selected = tuple((pathlib.PurePosixPath(path), commit) for path, commit in rows)
    if len(selected) > 512:
        raise ValueError("recovery reference count exceeds 512")
    empty = tuple(
        Provenance(path, commit, None, None, None, None, False, False)
        for path, commit in selected
    )
    if not selected:
        return empty
    if any(
        not recovery_commit_is_valid(commit) or not _safe_relative_path(path)
        for path, commit in selected
    ):
        raise ValueError("batch recovery identity is invalid")

    commits = tuple(sorted({commit for _, commit in selected}))
    checked = _run_git(
        repo_root,
        ["cat-file", "--batch-check=%(objectname) %(objecttype)"],
        input_bytes=("\n".join(commits) + "\n").encode("ascii"),
    )
    if checked.returncode != 0:
        raise ValueError("bounded commit-kind batch failed")
    commit_rows = checked.stdout.decode("ascii", errors="strict").splitlines()
    valid_commits: set[str] = set()
    if len(commit_rows) != len(commits):
        raise ValueError("bounded commit-kind batch returned an unexpected row count")
    for expected, rendered in zip(commits, commit_rows, strict=True):
        parts = rendered.split(" ")
        if len(parts) == 2 and parts[0] == expected and parts[1] == "commit":
            valid_commits.add(expected)

    resolved: dict[tuple[str, pathlib.PurePosixPath], Provenance] = {}
    for commit in commits:
        paths = tuple(path for path, candidate in selected if candidate == commit)
        if commit not in valid_commits:
            continue
        listed = _run_git(
            repo_root,
            ["ls-tree", "-z", commit, "--", *(path.as_posix() for path in paths)],
        )
        if listed.returncode != 0:
            raise ValueError(f"bounded path batch failed for commit {commit}")
        for raw in (row for row in listed.stdout.split(b"\0") if row):
            try:
                header, raw_path = raw.split(b"\t", 1)
                mode_bytes, type_bytes, object_bytes = header.split(b" ", 2)
                path = pathlib.PurePosixPath(raw_path.decode("utf-8"))
                mode = mode_bytes.decode("ascii")
                object_type = type_bytes.decode("ascii")
                object_id = object_bytes.decode("ascii")
            except (UnicodeError, ValueError) as error:
                raise ValueError("bounded path batch output is malformed") from error
            if path not in paths or _OBJECT_ID.fullmatch(object_id) is None:
                raise ValueError("bounded path batch returned an unexpected entry")
            key = (commit, path)
            if key in resolved:
                raise ValueError("bounded path batch returned a duplicate entry")
            resolved[key] = Provenance(
                path,
                commit,
                commit,
                mode,
                object_type,
                object_id,
                True,
                False,
            )

    object_ids = tuple(
        sorted(
            {
                item.object_id
                for item in resolved.values()
                if item.object_id is not None
            }
        )
    )
    object_kinds: dict[str, str] = {}
    if object_ids:
        checked_objects = _run_git(
            repo_root,
            ["cat-file", "--batch-check=%(objectname) %(objecttype)"],
            input_bytes=("\n".join(object_ids) + "\n").encode("ascii"),
        )
        if checked_objects.returncode != 0:
            raise ValueError("bounded recovery-object batch failed")
        object_rows = checked_objects.stdout.decode("ascii", errors="strict").splitlines()
        if len(object_rows) != len(object_ids):
            raise ValueError("bounded recovery-object batch returned an unexpected row count")
        for expected, rendered in zip(object_ids, object_rows, strict=True):
            parts = rendered.split(" ")
            if len(parts) != 2 or parts[0] != expected:
                raise ValueError("bounded recovery-object batch returned an unexpected entry")
            if parts[1] != "missing":
                object_kinds[expected] = parts[1]

    for key, item in tuple(resolved.items()):
        proven_type = object_kinds.get(item.object_id or "")
        exists = proven_type is not None
        resolved[key] = dataclasses.replace(
            item,
            exists=exists,
            is_regular_blob=(
                exists
                and item.object_type == "blob"
                and proven_type == "blob"
                and item.mode in {"100644", "100755"}
            ),
        )

    return tuple(
        resolved.get(
            (commit, path),
            Provenance(
                path,
                commit,
                commit if commit in valid_commits else None,
                None,
                None,
                None,
                False,
                False,
            ),
        )
        for path, commit in selected
    )


def recovery_commit_is_valid(commit: object) -> bool:
    """Return whether a recovery identity is one exact immutable commit OID."""

    return isinstance(commit, str) and _RECOVERY_COMMIT.fullmatch(commit) is not None


def read_archived_metadata_batch(
    paths: Iterable[pathlib.PurePosixPath | pathlib.Path | str],
    commit: str,
    *,
    repo_root: pathlib.Path,
) -> tuple[ArchivedMetadata, ...]:
    """Read legacy recovery fields in one bounded Git invocation.

    Missing records are omitted so the caller can apply its exact reviewed
    exception authority. Duplicate fields and malformed values fail closed.
    """

    if not recovery_commit_is_valid(commit):
        raise ValueError("baseline commit must be one full lowercase commit ID")
    selected = tuple(pathlib.PurePosixPath(path) for path in paths)
    if not selected or len(selected) > 512 or len(set(selected)) != len(selected):
        raise ValueError("baseline metadata paths must be 1..512 unique entries")
    if any(not _safe_relative_path(path) for path in selected):
        raise ValueError("baseline metadata path is unsafe")
    result = _run_git(
        repo_root,
        [
            "grep",
            "-z",
            "-E",
            "^archived_(commit|from):",
            commit,
            "--",
            *(path.as_posix() for path in selected),
        ],
    )
    if result.returncode not in {0, 1}:
        raise ValueError("bounded Git metadata scan failed")
    found: dict[pathlib.PurePosixPath, dict[str, str]] = {}
    prefix = f"{commit}:"
    for raw in result.stdout.splitlines():
        try:
            raw_path, raw_field = raw.split(b"\0", 1)
            rendered_path = raw_path.decode("utf-8")
            rendered_field = raw_field.decode("utf-8")
            key, value = rendered_field.split(":", 1)
        except (UnicodeError, ValueError) as error:
            raise ValueError("bounded Git metadata output is malformed") from error
        if not rendered_path.startswith(prefix):
            raise ValueError("bounded Git metadata output has a foreign commit")
        source = pathlib.PurePosixPath(rendered_path.removeprefix(prefix))
        if source not in selected or key not in {"archived_commit", "archived_from"}:
            raise ValueError("bounded Git metadata output is outside the request")
        values = found.setdefault(source, {})
        if key in values:
            raise ValueError(f"duplicate legacy recovery field: {source}:{key}")
        values[key] = value.strip()
    records: list[ArchivedMetadata] = []
    for source, values in sorted(found.items()):
        if set(values) != {"archived_commit", "archived_from"}:
            raise ValueError(f"partial legacy recovery metadata: {source}")
        archived_commit = values["archived_commit"]
        archived_from = pathlib.PurePosixPath(values["archived_from"])
        if not recovery_commit_is_valid(archived_commit) or not _safe_relative_path(archived_from):
            raise ValueError(f"invalid legacy recovery metadata: {source}")
        records.append(ArchivedMetadata(source, archived_commit, archived_from))
    return tuple(records)


def resolve_git_provenance(
    path: pathlib.PurePosixPath | pathlib.Path | str,
    commit: str,
    *,
    repo_root: pathlib.Path,
) -> Provenance:
    """Resolve ``commit:path`` and prove whether it is a regular tracked blob."""

    relative = pathlib.PurePosixPath(path)
    empty = Provenance(relative, commit, None, None, None, None, False, False)
    if (
        not _safe_relative_path(relative)
        or not isinstance(commit, str)
        or not commit
        or "\x00" in commit
    ):
        return empty
    verified = _run_git(
        repo_root,
        ["rev-parse", "--verify", "--end-of-options", f"{commit}^{{commit}}"],
    )
    if verified.returncode != 0:
        return empty
    commit_id = verified.stdout.decode("ascii", errors="ignore").strip()
    if _OBJECT_ID.fullmatch(commit_id) is None:
        return empty
    listed = _run_git(
        repo_root,
        ["ls-tree", "-z", commit_id, "--", relative.as_posix()],
    )
    if listed.returncode != 0 or not listed.stdout:
        return dataclasses.replace(empty, commit=commit_id)
    rows = [row for row in listed.stdout.split(b"\0") if row]
    if len(rows) != 1:
        return dataclasses.replace(empty, commit=commit_id)
    row = rows[0]
    try:
        header, raw_path = row.split(b"\t", 1)
        mode_bytes, type_bytes, object_bytes = header.split(b" ", 2)
        listed_path = raw_path.decode("utf-8")
        mode = mode_bytes.decode("ascii")
        object_type = type_bytes.decode("ascii")
        object_id = object_bytes.decode("ascii")
    except (UnicodeError, ValueError):
        return dataclasses.replace(empty, commit=commit_id)
    exists = listed_path == relative.as_posix() and _OBJECT_ID.fullmatch(object_id) is not None
    object_kind = _run_git(repo_root, ["cat-file", "-t", object_id]) if exists else None
    proven_blob = bool(
        object_kind is not None
        and object_kind.returncode == 0
        and object_kind.stdout.decode("ascii", errors="ignore").strip() == "blob"
    )
    regular = (
        exists
        and object_type == "blob"
        and mode in {"100644", "100755"}
        and proven_blob
    )
    return Provenance(
        relative,
        commit,
        commit_id,
        mode if exists else None,
        object_type if exists else None,
        object_id if exists else None,
        exists,
        regular,
    )


def verify_recovery_blob(
    path: pathlib.PurePosixPath | pathlib.Path | str,
    commit: str,
    *,
    repo_root: pathlib.Path,
) -> Provenance:
    """Prove one safe ``commit:path`` recovery reference as a regular blob.

    Recovery references deliberately require a full lowercase commit OID.  The
    lower-level resolver continues to accept refs such as ``HEAD`` for current
    repository inspections, while this API cannot drift with a branch.
    """

    relative = pathlib.PurePosixPath(path)
    empty = Provenance(relative, commit, None, None, None, None, False, False)
    if not recovery_commit_is_valid(commit) or not _safe_relative_path(relative):
        return empty
    object_name = f"{commit}:{relative.as_posix()}"
    present = _run_git(repo_root, ["cat-file", "-e", object_name])
    if present.returncode != 0:
        return empty
    object_type = _run_git(repo_root, ["cat-file", "-t", object_name])
    if object_type.returncode != 0 or object_type.stdout.strip() != b"blob":
        return empty
    return resolve_git_provenance(relative, commit, repo_root=repo_root)


def read_recovery_blob(
    path: pathlib.PurePosixPath | pathlib.Path | str,
    commit: str,
    *,
    repo_root: pathlib.Path,
) -> bytes | None:
    """Read one already bounded recovery blob without shell interpolation."""

    provenance = verify_recovery_blob(path, commit, repo_root=repo_root)
    if not provenance.is_regular_blob or provenance.object_id is None:
        return None
    shown = _run_git(repo_root, ["cat-file", "blob", provenance.object_id])
    return shown.stdout if shown.returncode == 0 else None
