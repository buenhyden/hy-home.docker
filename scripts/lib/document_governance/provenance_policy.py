"""Repository provenance policy for current documentation and Stage 98 lookup."""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import stat

from scripts.lib.document_governance.links import parse_local_markdown_links


_ACTIVE_PREFIXES = (
    "docs/00.agent-governance/",
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
    "docs/90.references/",
    "docs/99.templates/",
)
_DOCUMENT_SCAN_PREFIXES = (*_ACTIVE_PREFIXES, "docs/98.archive/")
_DOCUMENT_STAGE_NAMES = frozenset(
    {
        "00.agent-governance",
        "01.requirements",
        "02.architecture",
        "03.specs",
        "05.operations",
        "90.references",
        "98.archive",
        "99.templates",
    }
)
_SCAN_ROOTS = frozenset(
    {"docs", "scripts", "tests", ".agents", ".claude", ".codex", ".github", "infra"}
)
_TEXT_SUFFIXES = frozenset(
    {".cfg", ".conf", ".ini", ".json", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
)
_ROOT_TEXT_NAMES = frozenset(
    {
        ".editorconfig",
        ".env.example",
        ".gitmodules",
        ".graphifyignore",
        ".prettierignore",
        ".shellcheckrc",
        ".yamllint",
        "docker-compose.yml.format",
        "llms.txt",
    }
)
_EXCLUDED_PREFIXES = (
    ".git/",
    ".worktrees/",
    "graphify-out/",
)
_EXCLUDED_DIRECTORY_NAMES = frozenset(
    {"__pycache__", ".pytest_cache", ".ruff_cache", "build", "dist", "generated", "node_modules"}
)
_MAX_FILES = 4_096
_MAX_FILE_BYTES = 4 * 1_048_576
_MAX_TOTAL_BYTES = 32 * 1_048_576
_MAX_DIRECTORY_ENTRIES = 2_048
_MAX_VISITED_ENTRIES = 16_384
_MAX_TRAVERSAL_DEPTH = 64


@dataclasses.dataclass(frozen=True, order=True)
class ProvenanceFinding:
    code: str
    path: str
    detail: str = ""


def _finding(path: pathlib.PurePosixPath, code: str) -> ProvenanceFinding:
    return ProvenanceFinding(code, path.as_posix())


def validate_provenance_text(
    path: pathlib.PurePosixPath,
    text: str,
) -> tuple[ProvenanceFinding, ...]:
    """Validate one current text without treating examples as executable proof."""

    findings: list[ProvenanceFinding] = []
    if re.search(r"(?mi)^\s*branch[_-]?snapshot\s*[:=]", text):
        findings.append(_finding(path, "branch-snapshot-prohibited"))
    if re.search(
        r"(?mi)^\s*(?:line[_-]?sha|recovery_commit|archived_commit)\s*[:=].*[0-9a-f]{7,64}:\d+.*$",
        text,
    ):
        findings.append(_finding(path, "line-sha-prohibited"))
    if re.search(r"(?mi)^\s*(?:archive_)?snapshot_count\s*:", text):
        findings.append(_finding(path, "snapshot-count-prohibited"))
    if re.search(
        r"(?m)^\s*EXPECTED_HEAD\s*(?::[^=\n]+)?=\s*['\"][0-9a-f]{40}['\"]\s*$",
        text,
    ):
        findings.append(_finding(path, "fixed-head-fixture-prohibited"))
    if (
        re.search(
            r"(?mi)^\s*content_sha256\s*[:=]\s*['\"]?[0-9a-f]{64}['\"]?\s*$",
            text,
        )
        and re.search(
            r"(?mi)^\s*archived_blob\s*[:=]\s*['\"]?(?:[0-9a-f]{40}|[0-9a-f]{64})['\"]?\s*$",
            text,
        )
    ):
        findings.append(_finding(path, "duplicate-digest-prohibited"))

    active = path.as_posix().startswith(_ACTIVE_PREFIXES)
    if active:
        for link in parse_local_markdown_links(path, text):
            if link.target.as_posix().startswith("docs/98.archive/tombstones/"):
                findings.append(_finding(path, "active-tombstone-link-prohibited"))
                break
    if path.as_posix().startswith("docs/98.archive/tombstones/02.architecture/") and re.search(
        r"docs/02\.architecture/decisions/", text
    ):
        findings.append(_finding(path, "superseded-adr-archive-prohibited"))
    return tuple(sorted(set(findings)))


@dataclasses.dataclass(frozen=True)
class _EntrySnapshot:
    name: str
    device: int
    inode: int
    mode: int
    size: int
    modified_ns: int


@dataclasses.dataclass
class _ScanBudget:
    selected_files: int = 0
    selected_bytes: int = 0
    visited_entries: int = 0
    halted: bool = False


class _DirectoryEntryLimit(ValueError):
    pass


def _directory_flags() -> int:
    return os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY


def _open_directory_path(path: pathlib.Path) -> int:
    """Open every path component without following an ancestor symlink."""

    absolute = pathlib.Path(os.path.abspath(path))
    descriptor = os.open("/", _directory_flags())
    try:
        for component in absolute.parts[1:]:
            child = os.open(component, _directory_flags(), dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _snapshot(metadata: os.stat_result, name: str) -> _EntrySnapshot:
    return _EntrySnapshot(
        name=name,
        device=metadata.st_dev,
        inode=metadata.st_ino,
        mode=metadata.st_mode,
        size=metadata.st_size,
        modified_ns=metadata.st_mtime_ns,
    )


def _same_entry(metadata: os.stat_result, expected: _EntrySnapshot) -> bool:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
    ) == (
        expected.device,
        expected.inode,
        expected.mode,
        expected.size,
        expected.modified_ns,
    )


def _directory_entries(descriptor: int) -> tuple[_EntrySnapshot, ...]:
    entries: list[_EntrySnapshot] = []
    with os.scandir(descriptor) as iterator:
        for entry in iterator:
            if len(entries) >= _MAX_DIRECTORY_ENTRIES:
                raise _DirectoryEntryLimit("provenance directory entry limit exceeded")
            entries.append(_snapshot(entry.stat(follow_symlinks=False), entry.name))
    return tuple(sorted(entries, key=lambda item: item.name.encode("utf-8")))


def _read_regular_at(directory: int, expected: _EntrySnapshot) -> bytes:
    descriptor = os.open(
        expected.name,
        os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
        dir_fd=directory,
    )
    try:
        metadata = os.fstat(descriptor)
        if not _same_entry(metadata, expected):
            raise ValueError("active provenance input changed before read")
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > _MAX_FILE_BYTES:
            raise ValueError("active provenance input is not a bounded regular file")
        payload = bytearray()
        while len(payload) < metadata.st_size:
            chunk = os.read(descriptor, min(65_536, metadata.st_size - len(payload)))
            if not chunk:
                raise ValueError("active provenance input ended prematurely")
            payload.extend(chunk)
        if os.read(descriptor, 1):
            raise ValueError("active provenance input grew during read")
        after = os.fstat(descriptor)
        if not _same_entry(after, expected):
            raise ValueError("active provenance input changed during read")
        return bytes(payload)
    finally:
        os.close(descriptor)


def _read_regular(path: pathlib.Path) -> bytes:
    directory = _open_directory_path(path.parent)
    try:
        metadata = os.stat(path.name, dir_fd=directory, follow_symlinks=False)
        return _read_regular_at(directory, _snapshot(metadata, path.name))
    finally:
        os.close(directory)


def _is_excluded(path: pathlib.PurePosixPath) -> bool:
    value = path.as_posix()
    if value in {prefix.rstrip("/") for prefix in _EXCLUDED_PREFIXES}:
        return True
    if value.startswith(_EXCLUDED_PREFIXES):
        return True
    return any(component in _EXCLUDED_DIRECTORY_NAMES for component in path.parts)


def _is_selected_file(path: pathlib.PurePosixPath) -> bool:
    if _is_excluded(path):
        return False
    if len(path.parts) == 1:
        return path.name in _ROOT_TEXT_NAMES or pathlib.PurePosixPath(path.name).suffix in _TEXT_SUFFIXES
    if path.parts[0] == "docs":
        return path.as_posix().startswith(_DOCUMENT_SCAN_PREFIXES) and path.suffix in _TEXT_SUFFIXES
    return path.parts[0] in _SCAN_ROOTS and path.suffix in _TEXT_SUFFIXES


def _should_descend(path: pathlib.PurePosixPath) -> bool:
    if _is_excluded(path):
        return False
    if len(path.parts) == 1:
        return path.name in _SCAN_ROOTS
    if path.parts[0] == "docs" and len(path.parts) == 2:
        return path.name in _DOCUMENT_STAGE_NAMES
    return path.parts[0] in _SCAN_ROOTS


def _record_payload(
    relative: pathlib.PurePosixPath,
    payload: bytes,
    budget: _ScanBudget,
    findings: list[ProvenanceFinding],
) -> None:
    budget.selected_files += 1
    if budget.selected_files > _MAX_FILES:
        findings.append(_finding(pathlib.PurePosixPath("."), "provenance-file-count-exceeded"))
        budget.halted = True
        return
    budget.selected_bytes += len(payload)
    if budget.selected_bytes > _MAX_TOTAL_BYTES:
        findings.append(_finding(pathlib.PurePosixPath("."), "provenance-byte-budget-exceeded"))
        budget.halted = True
        return
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        findings.append(_finding(relative, "provenance-input-invalid"))
        return
    findings.extend(validate_provenance_text(relative, text))


def _walk_directory(
    descriptor: int,
    relative: pathlib.PurePosixPath,
    depth: int,
    budget: _ScanBudget,
    findings: list[ProvenanceFinding],
) -> None:
    if budget.halted:
        return
    if depth > _MAX_TRAVERSAL_DEPTH:
        findings.append(_finding(relative, "provenance-traversal-depth-exceeded"))
        budget.halted = True
        return
    try:
        entries = _directory_entries(descriptor)
    except _DirectoryEntryLimit:
        findings.append(_finding(relative, "provenance-directory-entry-count-exceeded"))
        return
    except (OSError, ValueError):
        findings.append(_finding(relative, "provenance-input-invalid"))
        return
    budget.visited_entries += len(entries)
    if budget.visited_entries > _MAX_VISITED_ENTRIES:
        findings.append(_finding(relative, "provenance-entry-budget-exceeded"))
        budget.halted = True
        return

    for entry in entries:
        if budget.halted:
            break
        child_relative = relative / entry.name
        if _is_excluded(child_relative):
            continue
        if stat.S_ISDIR(entry.mode) and _should_descend(child_relative):
            try:
                child = os.open(entry.name, _directory_flags(), dir_fd=descriptor)
                try:
                    if not _same_entry(os.fstat(child), entry):
                        raise ValueError("provenance directory changed before traversal")
                    _walk_directory(child, child_relative, depth + 1, budget, findings)
                finally:
                    os.close(child)
            except (OSError, ValueError):
                findings.append(_finding(child_relative, "provenance-input-invalid"))
        elif stat.S_ISREG(entry.mode) and _is_selected_file(child_relative):
            try:
                payload = _read_regular_at(descriptor, entry)
            except (OSError, ValueError):
                findings.append(_finding(child_relative, "provenance-input-invalid"))
                continue
            _record_payload(child_relative, payload, budget, findings)
        elif not stat.S_ISREG(entry.mode) and (
            _is_selected_file(child_relative) or _should_descend(child_relative)
        ):
            findings.append(_finding(child_relative, "provenance-input-invalid"))


def validate_repository_provenance(root: pathlib.Path) -> tuple[ProvenanceFinding, ...]:
    """Scan bounded authored text without following repository symlinks."""

    findings: list[ProvenanceFinding] = []
    budget = _ScanBudget()
    try:
        descriptor = _open_directory_path(root)
    except (OSError, ValueError):
        return (_finding(pathlib.PurePosixPath("."), "provenance-input-invalid"),)
    try:
        _walk_directory(
            descriptor,
            pathlib.PurePosixPath("."),
            0,
            budget,
            findings,
        )
    finally:
        os.close(descriptor)
    return tuple(sorted(set(findings)))
