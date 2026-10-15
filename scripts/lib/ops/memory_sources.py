"""Bounded, caller-worktree source checks for shared memory provenance."""

from __future__ import annotations

import hashlib
import os
import re
import stat
import subprocess
from pathlib import Path

MAX_SOURCE_BYTES = 16 * 1024 * 1024
REVIEW_STATES = ("candidate", "current", "needs-review", "superseded", "withdrawn")


def source_is_current(reference: object, cwd: Path) -> bool:
    """Only explicit, tracked repository-file pins can establish currentness.

    Old strings (including approved native imports) are retained as provenance;
    this operation never opens native memory or fetches external URLs.
    """
    if not isinstance(reference, dict) or reference.get("kind") != "repository-file":
        return False
    required = {"kind", "path", "revision", "hash_algorithm", "digest", "context"}
    if set(reference) != required or any(
        not isinstance(v, str) or not v for v in reference.values()
    ):
        return False
    relative = Path(reference["path"])
    if relative.is_absolute() or any(p in {"", ".", ".."} for p in relative.parts):
        return False
    if any(
        p.startswith(".") and p not in {".agents", ".claude", ".codex"}
        for p in relative.parts
    ):
        return False
    if any(
        p.lower() in {"secrets", "auth", "credentials"} or p.startswith("agent-memory")
        for p in relative.parts
    ):
        return False
    algorithm = reference["hash_algorithm"]
    if algorithm not in {"sha256", "git-blob"} or not re.fullmatch(
        r"[0-9a-f]{40}|[0-9a-f]{64}", reference["digest"]
    ):
        return False
    try:
        root = Path(
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        )
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative.as_posix()],
            cwd=root,
            capture_output=True,
            check=True,
        )
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
                    return False
                content = stream.read(MAX_SOURCE_BYTES + 1)
                if len(content) > MAX_SOURCE_BYTES:
                    return False
        finally:
            os.close(descriptor)
        digest = (
            hashlib.sha256(content).hexdigest()
            if algorithm == "sha256"
            else subprocess.run(
                ["git", "hash-object", "--stdin"],
                cwd=root,
                input=content,
                capture_output=True,
                check=True,
            )
            .stdout.decode()
            .strip()
        )
        return digest == reference["digest"]
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        return False


def reuse_state(review_state: str, source_refs: list[object], cwd: Path) -> str:
    if review_state != "current":
        return review_state
    return (
        "current"
        if source_refs and all(source_is_current(r, cwd) for r in source_refs)
        else "needs-review"
    )
