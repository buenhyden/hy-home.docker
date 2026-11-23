"""Bounded, caller-worktree source checks for shared memory provenance."""

from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import stat
import subprocess
from pathlib import Path

MAX_SOURCE_BYTES = 16 * 1024 * 1024
REVIEW_STATES = ("candidate", "current", "needs-review", "superseded", "withdrawn")
_GIT_TIMEOUT_SECONDS = 5


def run_git(
    arguments: tuple[str, ...], cwd: Path, input_data: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    environment = {
        "GIT_ALLOW_PROTOCOL": "",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.defpath,
    }
    common = {
        "cwd": cwd,
        "env": environment,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.DEVNULL,
        "timeout": _GIT_TIMEOUT_SECONDS,
    }
    if input_data is None:
        return subprocess.run(
            ("git", *arguments),
            stdin=subprocess.DEVNULL,
            check=True,
            **common,
        )
    return subprocess.run(("git", *arguments), input=input_data, check=True, **common)


SOURCE_STATES = ("current", "changed", "unavailable", "content_expired")


def source_state(reference: object, cwd: Path, as_of: str | None = None) -> str:
    """D09 state of one source reference at `as_of` (UTC ISO, default now).

    A `session-events` reference is `content_expired` once its captured content
    passed retention, and `current` before. A repository-file pin is `current`
    when the worktree still holds the pinned content, `changed` when the
    tracked file differs and `unavailable` when it cannot be checked. Any other
    reference, such as an old string, is kept as provenance but `unavailable`.
    This never opens native memory or fetches an external URL.
    """
    if isinstance(reference, dict) and reference.get("kind") == "session-events":
        expires = reference.get("content_expires_at")
        if not isinstance(expires, str):
            return "unavailable"
        try:
            expiry = dt.datetime.fromisoformat(expires)
            now = dt.datetime.fromisoformat(as_of) if as_of else dt.datetime.now(dt.UTC)
        except ValueError:
            return "unavailable"
        if expiry.tzinfo is None or now.tzinfo is None:
            return "unavailable"
        return "content_expired" if now >= expiry else "current"
    return _pin_state(reference, cwd)


def source_is_current(reference: object, cwd: Path) -> bool:
    """Only explicit, tracked repository-file pins can establish currentness."""
    return _pin_state(reference, cwd) == "current"


def _pin_state(reference: object, cwd: Path) -> str:
    if not isinstance(reference, dict) or reference.get("kind") != "repository-file":
        return "unavailable"
    required = {"kind", "path", "revision", "hash_algorithm", "digest", "context"}
    if set(reference) != required or any(
        not isinstance(v, str) or not v for v in reference.values()
    ):
        return "unavailable"
    relative = Path(reference["path"])
    if relative.is_absolute() or any(p in {"", ".", ".."} for p in relative.parts):
        return "unavailable"
    if any(
        p.startswith(".") and p not in {".agents", ".claude", ".codex"}
        for p in relative.parts
    ):
        return "unavailable"
    if any(
        p.lower() in {"secrets", "auth", "credentials"} or p.startswith("agent-memory")
        for p in relative.parts
    ):
        return "unavailable"
    algorithm = reference["hash_algorithm"]
    if (
        algorithm not in {"sha256", "git-blob"}
        or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", reference["digest"])
        or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", reference["revision"])
    ):
        return "unavailable"
    try:
        root = Path(
            os.fsdecode(run_git(("rev-parse", "--show-toplevel"), cwd).stdout.strip())
        )
        run_git(
            (
                "--literal-pathspecs",
                "ls-files",
                "--error-unmatch",
                "--",
                relative.as_posix(),
            ),
            root,
        )
        resolved_revision = run_git(
            ("rev-parse", "--verify", f"{reference['revision']}^{{commit}}"), root
        ).stdout.strip()
        if resolved_revision != reference["revision"].encode("ascii"):
            return "unavailable"
        tree_entry = run_git(
            (
                "--literal-pathspecs",
                "ls-tree",
                "-z",
                reference["revision"],
                "--",
                relative.as_posix(),
            ),
            root,
        ).stdout
        entry, separator, remainder = tree_entry.partition(b"\0")
        if not separator or remainder or b"\t" not in entry:
            return "unavailable"
        header, recorded_path = entry.split(b"\t", 1)
        fields = header.split(b" ")
        if len(fields) != 3:
            return "unavailable"
        mode, object_type, object_id = fields
        if (
            mode not in {b"100644", b"100755"}
            or object_type != b"blob"
            or recorded_path != os.fsencode(relative.as_posix())
        ):
            return "unavailable"
        # Open every component relative to the already opened parent: replacing a
        # path with a symlink cannot redirect a source read outside this worktree.
        descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for component in relative.parts[:-1]:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
                os.close(descriptor)
                descriptor = child
            source = os.open(
                relative.name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=descriptor,
            )
            with os.fdopen(source, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SOURCE_BYTES:
                    return "unavailable"
                content = stream.read(MAX_SOURCE_BYTES + 1)
                if len(content) > MAX_SOURCE_BYTES:
                    return "unavailable"
        finally:
            os.close(descriptor)
        current_blob = run_git(("hash-object", "--stdin"), root, content).stdout.strip()
        if current_blob != object_id:
            return "changed"
        digest = (
            hashlib.sha256(content).hexdigest()
            if algorithm == "sha256"
            else current_blob.decode()
        )
        return "current" if digest == reference["digest"] else "changed"
    except (
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        UnicodeError,
    ):
        return "unavailable"


def reuse_state(review_state: str, source_refs: list[object], cwd: Path) -> str:
    if review_state != "current":
        return review_state
    return (
        "current"
        if source_refs and all(source_is_current(r, cwd) for r in source_refs)
        else "needs-review"
    )


def sources_state(source_refs: list[object], cwd: Path, as_of: str | None) -> str:
    """The least usable state over every reference; no reference is unavailable."""
    states = {source_state(r, cwd, as_of) for r in source_refs} or {"unavailable"}
    return next(s for s in reversed(SOURCE_STATES) if s in states)
