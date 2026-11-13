#!/usr/bin/env python3
"""Lifecycle entrypoint shared names and bounded repository safety."""

from __future__ import annotations

import collections
import collections.abc
import os
import pathlib
import re
import stat
import subprocess
import sys
from typing import Any

_ROOT_ERROR = "FAIL: invalid HYHOME_CI_GATE_ROOT"


def _repository_root() -> pathlib.Path:
    fallback = pathlib.Path(__file__).resolve().parents[4]
    override = os.environ.get("HYHOME_CI_GATE_ROOT")
    if override is None:
        return fallback
    match = re.fullmatch(r"/proc/self/fd/(0|[1-9][0-9]*)", override)
    if match is None:
        raise SystemExit(_ROOT_ERROR)
    try:
        descriptor = os.fstat(int(match.group(1)))
        direct = fallback.stat()
    except (OSError, ValueError, OverflowError):
        raise SystemExit(_ROOT_ERROR) from None
    if not stat.S_ISDIR(descriptor.st_mode) or (
        descriptor.st_dev,
        descriptor.st_ino,
    ) != (direct.st_dev, direct.st_ino):
        raise SystemExit(_ROOT_ERROR)
    return pathlib.Path(override)


ROOT = _repository_root()
_REPOSITORY_DIRECTORY = str(ROOT)
if _REPOSITORY_DIRECTORY not in sys.path:
    sys.path.insert(0, _REPOSITORY_DIRECTORY)
_VALIDATION_DIRECTORY = str(ROOT / "scripts/validation")
if _VALIDATION_DIRECTORY not in sys.path:
    sys.path.insert(0, _VALIDATION_DIRECTORY)

from scripts.lib.document_governance import metadata_contract  # noqa: E402
from scripts.lib.document_governance.git_provenance import (  # noqa: E402
    HistoricalDocument,
)

DEFAULT_PROFILES = ROOT / "docs/99.templates/registry.json"
HISTORICAL_CONTRACT = HistoricalDocument(
    ROOT,
    "494065806794980080b081439298d7b534d10803",
    "docs/99.templates/support/document-corpus-migration-contract.yaml",
)
DEFAULT_CONTRACT = None

MODES = (
    "check-public",
    "check-contract",
)


class _BootstrapProfileError(ValueError):
    """Used only until the canonical metadata module is loaded safely."""


class _CorpusSafetyError(Exception):
    """Value-free corpus path failure that must cross the CLI safety boundary."""

    def __init__(self, path: str, code: str) -> None:
        super().__init__(code)
        self.path = path if path and _lexically_safe_path(path) else "corpus"
        self.code = code


metadata: Any = metadata_contract
Finding: Any = metadata.Finding
Record: Any = metadata.Record
ProfileError: type[Exception] = metadata.ProfileError


def _ensure_metadata_loaded() -> Any:
    """Load repository-backed metadata only after CLI-shape validation."""

    global metadata, Finding, Record, ProfileError
    return metadata


SENSITIVE_PAYLOAD_PATTERNS = (
    re.compile(
        rb"(?i)(?:password|passwd|credential|secret|token|access[_-]?token|refresh[_-]?token|api[_-]?key)\s*[:=]"
    ),
    re.compile(
        rb"(?i)(?:auth|authorization)\s*[:=]\s*(?:bearer|basic|[A-Za-z0-9+/]{16,})"
    ),
    re.compile(rb"(?is)\bmachine\s+\S+.{0,512}\blogin\s+\S+.{0,512}\bpassword\s+\S+"),
    re.compile(rb'(?i)"auths?"\s*:\s*\{|"auth"\s*:\s*"[A-Za-z0-9+/=_-]{8,}"'),
    re.compile(rb"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{12,}\b"),
    re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{12,}\b"),
    re.compile(rb"-----BEGIN [A-Z0-9 ]*(?:PRIVATE KEY|PGP PRIVATE KEY BLOCK)-----"),
    re.compile(
        rb"(?i)(?:^|/|\\)(?:\.netrc|\.docker/config\.json|auth\.json|credentials)(?:\s|$)"
    ),
    re.compile(rb"(?i)(?:^|/|\\)\.(?:bash|zsh|sh)_history(?:\s|$)|\bHISTFILE\s*="),
    re.compile(rb"(?m)^\d{4}-\d{2}-\d{2}(?:T|\s).*(?:ERROR|WARN|DEBUG|TRACE)\b"),
    re.compile(rb"(?mi)^(?:TRACE|DEBUG|INFO|WARN|ERROR|FATAL)\b"),
    re.compile(
        rb'(?is)"(?:timestamp|time|ts)"\s*:\s*"[^"]+".{0,512}"level"\s*:\s*"(?:trace|debug|info|warn|error|fatal)"'
    ),
    re.compile(
        rb'(?is)\{.{0,512}"level"\s*:\s*"(?:trace|debug|info|warn|error|fatal)"'
    ),
    re.compile(
        rb"(?m)^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+(?:\[\d+\])?:"
    ),
)


def _sensitive_value_is_present(value: str) -> bool:
    """Apply one value-free confidentiality classifier to durable and printed data."""

    payload = value.encode("utf-8", errors="replace")
    return any(pattern.search(payload) for pattern in SENSITIVE_PAYLOAD_PATTERNS)


SAFETY_FINDING_CODES = frozenset(
    {
        "manifest-static-invalid",
        "manifest-source-path-invalid",
        "manifest-source-not-at-baseline",
        "manifest-source-mode-invalid",
        "manifest-source-parse-invalid",
        "manifest-target-path-invalid",
        "manifest-target-file-invalid",
        "manifest-target-metadata-forbidden",
        "manifest-consumer-path-invalid",
        "manifest-evidence-path-invalid",
        "manifest-evidence-confidential",
        "manifest-partition-plan-invalid",
        "corpus-markdown-path-invalid",
        "corpus-markdown-mode-invalid",
        "corpus-markdown-file-invalid",
        "manifest-baseline-commit-invalid",
        "manifest-serialization-stale",
        "frontmatter-malformed-yaml",
        "frontmatter-duplicate-key",
        "exception-schema-invalid",
        "exception-order-invalid",
        "exception-code-unknown",
        "exception-scope-invalid",
        "exception-owner-required",
        "exception-reason-required",
        "exception-exit-condition-required",
        "exception-approval-invalid",
        "exception-expired",
        "exception-expiry-invalid",
        "exception-evidence-invalid",
        "exception-static-invalid",
        "exception-safety-code-forbidden",
        "contract-invalid",
        "spec-package-invalid",
        "diagnostic-redaction-unsafe",
        "internal-error",
    }
)


def _finding(
    path: str | pathlib.PurePath,
    code: str,
    message: str,
    severity: str = "error",
) -> Finding:
    return Finding(pathlib.PurePosixPath(path).as_posix(), code, message, severity)


def _run_git(
    root: pathlib.Path,
    args: collections.abc.Sequence[str],
    *,
    text: bool = True,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=text,
            check=False,
        )
    except OSError as error:
        raise ProfileError("Git executable is unavailable") from error


def _safe_path(value: object) -> bool:
    return (
        bool(metadata._safe_repo_path(value))
        and isinstance(value, str)
        and not any(marker in value for marker in "*?[]{}")
    )


def _lexically_safe_path(value: object) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or "|" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        return False
    path = pathlib.PurePosixPath(value)
    return (
        not path.is_absolute()
        and bool(path.parts)
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _open_regular_repo_descriptor(root: pathlib.Path, relative_path: str) -> int | None:
    """Open one in-root regular file without following any path component."""

    if not _lexically_safe_path(relative_path):
        return None
    parts = pathlib.PurePosixPath(relative_path).parts
    directory_flags = (
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    parent_descriptor: int | None = None
    descriptor: int | None = None
    try:
        parent_descriptor = os.open(root.resolve(), directory_flags)
        for part in parts[:-1]:
            child_descriptor = os.open(
                part,
                directory_flags,
                dir_fd=parent_descriptor,
            )
            os.close(parent_descriptor)
            parent_descriptor = child_descriptor
        descriptor = os.open(parts[-1], file_flags, dir_fd=parent_descriptor)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            os.close(descriptor)
            descriptor = None
        return descriptor
    except OSError:
        if descriptor is not None:
            os.close(descriptor)
        return None
    finally:
        if parent_descriptor is not None:
            os.close(parent_descriptor)


def _read_regular_repo_bytes(
    root: pathlib.Path,
    relative_path: str,
    *,
    require_tracked: bool,
) -> bytes | None:
    """Read a regular in-root file through a no-follow directory-fd chain."""

    if not _safe_path(relative_path):
        return None
    if require_tracked:
        tracked = _run_git(
            root,
            ["ls-files", "--stage", "-z", "--", relative_path],
            text=False,
        )
        if tracked.returncode != 0 or not tracked.stdout:
            return None
        modes = {
            record.split(b" ", 1)[0] for record in tracked.stdout.split(b"\0") if record
        }
        if not modes or not modes <= {b"100644", b"100755"}:
            return None
    descriptor = _open_regular_repo_descriptor(root, relative_path)
    if descriptor is None:
        return None
    try:
        before = os.fstat(descriptor)
        limit = 4 * 1024 * 1024
        if before.st_size > limit:
            return None
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65_536, limit + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > limit:
                return None
        after = os.fstat(descriptor)
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            return None
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(descriptor)


def _rooted(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path
