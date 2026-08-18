"""Fail-closed Git provenance resolution for repository documents."""

from __future__ import annotations

import dataclasses
import pathlib
import re
import subprocess


_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


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


def _safe_relative_path(path: pathlib.PurePosixPath) -> bool:
    return bool(path.parts) and not path.is_absolute() and "\x00" not in path.as_posix() and all(
        part not in {"", ".", ".."} and "\\" not in part and "\x00" not in part
        for part in path.parts
    )


def _run_git(repo_root: pathlib.Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )


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
