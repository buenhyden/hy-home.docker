"""Monotonic document identity allocation derived from current and Git history."""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import selectors
import stat
import subprocess
import time
from collections.abc import Mapping
from types import MappingProxyType

from scripts.lib.document_governance.registry import DocumentRegistry, RegistryFinding


MAX_GIT_OUTPUT_BYTES = 16 * 1024 * 1024
MAX_GIT_SCAN_SECONDS = 45
MAX_IDENTITY_SOURCE_BYTES = 1024 * 1024
IDENTITY_SOURCE_SUFFIXES = frozenset({".md", ".json", ".yaml", ".yml"})
IDENTITY_SOURCE_PREFIXES = (
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
    "docs/90.references/",
    "docs/98.archive/",
)
GIT_HISTORY_QUERIES = (
    (
        "docs/01.requirements",
        "(REQ|PRD|SRS|IFR)-[0-9]{4}"
        "(-(FR|NFR|IF|R|AC)-?[0-9]{4})?",
    ),
    ("docs/02.architecture", "(AD|ADR)-[0-9]{4}"),
    ("docs/03.specs", "SPEC-[0-9]{4}"),
    (
        "docs/05.operations",
        "(GUIDE|POLICY|RUNBOOK|OPS|INC)-[0-9]{4}",
    ),
    (
        "docs/90.references",
        "(RES|REF|AUD|AUDIT|DATA)-[0-9]{4}",
    ),
    ("docs/98.archive", "(MIG|TOMBSTONE)-[0-9]{4}"),
)
HISTORICAL_ID_PATTERN = re.compile(
    r"(?i)\b(?:"
    r"REQ-[0-9]{4}(?:-(?:FR|NFR|IF)-[0-9]{4})?|"
    r"PRD-[0-9]{4}(?:-(?:R|AC|FR|NFR)-?[0-9]{4})?|"
    r"SRS-[0-9]{4}(?:-R[0-9]{4})?|IFR-[0-9]{4}(?:-R[0-9]{4})?|"
    r"(?:AD|ADR|SPEC|RES|AUD|DATA)-[0-9]{4}|"
    r"(?:ad|adr|spec|ref|audit|guide|policy|runbook|ops|inc|mig|tombstone)-[0-9]{4}"
    r")\b"
)
INTERNAL_REQUIREMENT_PATTERN = re.compile(
    r"(?i)\b(?:"
    r"REQ-[0-9]{4}-(?:FR|NFR|IF)-[0-9]{4}|"
    r"PRD-[0-9]{4}-(?:R|AC|FR|NFR)-?[0-9]{4}|"
    r"SRS-[0-9]{4}-R[0-9]{4}|IFR-[0-9]{4}-R[0-9]{4}"
    r")\b"
)


class IdentityHistoryError(RuntimeError):
    """Raised when Git history cannot be inspected safely."""


@dataclasses.dataclass(frozen=True)
class _GitOutput:
    text: str
    bytes_read: int


@dataclasses.dataclass(frozen=True)
class IssuedIdentities:
    numbers: Mapping[str, frozenset[int]]

    def high_water(self, space: str) -> int:
        values = self.numbers.get(space, frozenset())
        return max(values, default=0)


def _run_git(
    repo: pathlib.Path,
    arguments: tuple[str, ...],
    *,
    max_output_bytes: int = MAX_GIT_OUTPUT_BYTES,
    timeout_seconds: float = MAX_GIT_SCAN_SECONDS,
) -> _GitOutput:
    if max_output_bytes <= 0 or timeout_seconds <= 0:
        raise IdentityHistoryError("Git identity scan exhausted its bound")
    deadline = time.monotonic() + timeout_seconds
    try:
        process = subprocess.Popen(
            ["git", *arguments],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise IdentityHistoryError("bounded Git identity scan failed") from error
    if process.stdout is None or process.stderr is None:
        _terminate_and_reap(process, None)
        raise IdentityHistoryError("bounded Git identity scan failed")
    selector = selectors.DefaultSelector()
    stdout = bytearray()
    observed = 0
    try:
        for stream, name in ((process.stdout, "stdout"), (process.stderr, "stderr")):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
        while selector.get_map():
            remaining_seconds = deadline - time.monotonic()
            if remaining_seconds <= 0:
                _terminate_and_reap(process, selector)
                raise IdentityHistoryError("Git identity scan exceeded its time bound")
            events = selector.select(remaining_seconds)
            if not events:
                continue
            for key, _ in events:
                remaining_bytes = max_output_bytes - observed
                try:
                    chunk = os.read(
                        key.fileobj.fileno(),
                        min(64 * 1024, remaining_bytes + 1),
                    )
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                if len(chunk) > remaining_bytes:
                    _terminate_and_reap(process, selector)
                    raise IdentityHistoryError(
                        "Git identity scan exceeded its output bound"
                    )
                observed += len(chunk)
                if key.data == "stdout":
                    stdout.extend(chunk)
        remaining_seconds = deadline - time.monotonic()
        if remaining_seconds <= 0:
            _terminate_and_reap(process, selector)
            raise IdentityHistoryError("Git identity scan exceeded its time bound")
        returncode = process.wait(timeout=remaining_seconds)
        if returncode != 0:
            raise IdentityHistoryError("bounded Git identity scan failed")
    except subprocess.SubprocessError as error:
        _terminate_and_reap(process, selector)
        raise IdentityHistoryError("bounded Git identity scan failed") from error
    except OSError as error:
        _terminate_and_reap(process, selector)
        raise IdentityHistoryError("bounded Git identity scan failed") from error
    finally:
        if process.poll() is None:
            _terminate_and_reap(process, selector)
        selector.close()
        process.stdout.close()
        process.stderr.close()
    try:
        return _GitOutput(stdout.decode("utf-8"), observed)
    except UnicodeError as error:
        raise IdentityHistoryError("Git identity scan returned invalid UTF-8") from error


def _terminate_and_reap(
    process: subprocess.Popen[bytes],
    selector: selectors.BaseSelector | None,
) -> None:
    """Stop one child, drain ready pipe bytes, and always reap it."""

    if process.poll() is None:
        try:
            process.terminate()
        except OSError:
            pass
    drain_deadline = time.monotonic() + 0.25
    while selector is not None and selector.get_map() and time.monotonic() < drain_deadline:
        for key, _ in selector.select(0.02):
            try:
                chunk = os.read(key.fileobj.fileno(), 64 * 1024)
            except (BlockingIOError, OSError):
                continue
            if not chunk:
                try:
                    selector.unregister(key.fileobj)
                except (KeyError, ValueError):
                    pass
    if process.poll() is None:
        try:
            process.kill()
        except OSError as error:
            raise IdentityHistoryError(
                "failed to terminate bounded Git identity scan"
            ) from error
    try:
        process.wait()
    except (OSError, subprocess.SubprocessError) as error:
        raise IdentityHistoryError(
            "failed to reap bounded Git identity scan"
        ) from error
    if process.poll() is None:
        raise IdentityHistoryError("failed to reap bounded Git identity scan")


def _record(identity: str, collected: dict[str, set[int]]) -> None:
    upper = identity.upper()
    numbers = tuple(int(item) for item in re.findall(r"[0-9]{4}", upper))
    if not numbers:
        return
    package = numbers[0]
    if upper.startswith(("REQ-", "PRD-", "SRS-", "IFR-")):
        collected.setdefault("requirement", set()).add(package)
        if len(numbers) > 1:
            if upper.startswith("IFR-") or "-IF-" in upper:
                child = "IF"
            elif "-NFR" in upper or upper.startswith("SRS-"):
                child = "NFR"
            else:
                child = "FR"
            package_id = f"REQ-{package:04d}"
            collected.setdefault(
                f"requirement.{package_id}.{child}", set()
            ).add(numbers[-1])
        return
    prefixes = {
        "AD-": "architecture-description",
        "ADR-": "adr",
        "SPEC-": "spec",
        "RES-": "research",
        "REF-": "research",
        "AUD-": "audit",
        "AUDIT-": "audit",
        "DATA-": "data",
        "GUIDE-": "operations-subject",
        "POLICY-": "operations-subject",
        "RUNBOOK-": "operations-subject",
        "OPS-": "operations-subject",
        "INC-": "incident",
        "MIG-": "migration",
        "TOMBSTONE-": "tombstone",
    }
    for prefix, space in prefixes.items():
        if upper.startswith(prefix):
            collected.setdefault(space, set()).add(package)
            return


def _path_accepts_identity(path: str, identity: str) -> bool:
    upper = identity.upper()
    if upper.startswith(("REQ-", "PRD-", "SRS-", "IFR-")):
        return path.startswith("docs/01.requirements/")
    if upper.startswith("AD-") and not upper.startswith("ADR-"):
        return path.startswith("docs/02.architecture/descriptions/")
    if upper.startswith("ADR-"):
        return path.startswith("docs/02.architecture/decisions/")
    if upper.startswith("SPEC-"):
        return path.startswith("docs/03.specs/")
    if upper.startswith(("GUIDE-", "POLICY-", "RUNBOOK-", "OPS-", "INC-")):
        return path.startswith("docs/05.operations/")
    if upper.startswith(("RES-", "REF-", "AUD-", "AUDIT-", "DATA-")):
        return path.startswith("docs/90.references/")
    if upper.startswith(("MIG-", "TOMBSTONE-")):
        return path.startswith("docs/98.archive/")
    return False


def _record_line(path: str, line: str, collected: dict[str, set[int]]) -> None:
    normalized = line[1:] if line.startswith(("+", "-")) else line
    if re.match(r"^[ \t]*artifact_id[ \t]*:", normalized, re.IGNORECASE):
        for match in HISTORICAL_ID_PATTERN.finditer(normalized):
            if _path_accepts_identity(path, match.group(0)):
                _record(match.group(0), collected)
    if path.startswith("docs/01.requirements/"):
        for match in INTERNAL_REQUIREMENT_PATTERN.finditer(normalized):
            _record(match.group(0), collected)


def _record_history_patch(history: str, collected: dict[str, set[int]]) -> None:
    """Record identities from one bounded Git patch without losing rename paths."""

    history_paths = ("", "")
    for line in history.splitlines():
        if line.startswith("diff --git a/"):
            parts = line.split(" ", 3)
            history_paths = (
                parts[2][2:] if len(parts) >= 3 else "",
                parts[3][2:] if len(parts) >= 4 else "",
            )
            continue
        old_path, new_path = history_paths
        selected_path = new_path if line.startswith("+") else old_path
        if selected_path:
            _record_line(selected_path, line, collected)


def _remaining_scan_seconds(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise IdentityHistoryError("Git identity scan exceeded its time bound")
    return remaining


def _read_identity_source(path: pathlib.Path) -> str:
    """Read one tracked identity-bearing source without following links."""

    try:
        metadata = path.lstat()
    except OSError as error:
        raise IdentityHistoryError("tracked identity source is unavailable") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise IdentityHistoryError(
            "tracked identity source must be a regular non-symlink file"
        )
    if metadata.st_size > MAX_IDENTITY_SOURCE_BYTES:
        raise IdentityHistoryError("tracked identity source exceeds its byte bound")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise IdentityHistoryError(
                    "tracked identity source changed to a non-regular file"
                )
            content = os.read(descriptor, MAX_IDENTITY_SOURCE_BYTES + 1)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise IdentityHistoryError("tracked identity source cannot be read") from error
    if len(content) > MAX_IDENTITY_SOURCE_BYTES:
        raise IdentityHistoryError("tracked identity source exceeds its byte bound")
    try:
        return content.decode("utf-8")
    except UnicodeError as error:
        raise IdentityHistoryError("tracked identity source must be UTF-8") from error


def collect_issued_identities(
    repo: pathlib.Path,
    refs: tuple[str, ...] = ("--all",),
) -> IssuedIdentities:
    """Return immutable issued-number sets from current files plus bounded Git patches."""

    root = repo.resolve()
    deadline = time.monotonic() + MAX_GIT_SCAN_SECONDS
    _run_git(
        root,
        ("rev-parse", "--is-inside-work-tree"),
        timeout_seconds=_remaining_scan_seconds(deadline),
    )
    current_files = _run_git(
        root,
        ("ls-files", "-z"),
        timeout_seconds=_remaining_scan_seconds(deadline),
    ).text.split("\0")
    collected: dict[str, set[int]] = {}
    for relative in current_files:
        _remaining_scan_seconds(deadline)
        if (
            not relative.startswith(IDENTITY_SOURCE_PREFIXES)
            or pathlib.PurePosixPath(relative).suffix.casefold()
            not in IDENTITY_SOURCE_SUFFIXES
        ):
            continue
        path = root / relative
        for line in _read_identity_source(path).splitlines():
            _record_line(relative, line, collected)
    remaining_output_bytes = MAX_GIT_OUTPUT_BYTES
    for pathspec, pattern in GIT_HISTORY_QUERIES:
        output = _run_git(
            root,
            (
                "log",
                "--no-ext-diff",
                "--format=",
                "-U0",
                "--regexp-ignore-case",
                "-G",
                pattern,
                *refs,
                "--",
                pathspec,
            ),
            max_output_bytes=remaining_output_bytes,
            timeout_seconds=_remaining_scan_seconds(deadline),
        )
        remaining_output_bytes -= output.bytes_read
        _record_history_patch(output.text, collected)
    return IssuedIdentities(
        numbers=MappingProxyType(
            {name: frozenset(values) for name, values in sorted(collected.items())}
        )
    )


def validate_identity_history(
    registry: DocumentRegistry,
    issued: IssuedIdentities,
) -> tuple[RegistryFinding, ...]:
    """Reject allocation state below any observed current or historical identity."""

    findings: list[RegistryFinding] = []
    for name, space in registry.identity_spaces.items():
        observed = issued.high_water(name)
        if space.high_water < observed:
            findings.append(
                RegistryFinding(
                    "identity-history-regression",
                    f"identity_spaces.{name}",
                    f"registry high_water={space.high_water} observed={observed}",
                )
            )
        for child_name, child in space.child_spaces.items():
            qualified = f"{name}.{child_name}"
            child_observed = issued.high_water(qualified)
            if child.high_water < child_observed:
                findings.append(
                    RegistryFinding(
                        "identity-history-regression",
                        f"identity_spaces.{name}.child_spaces.{child_name}",
                        f"registry high_water={child.high_water} observed={child_observed}",
                    )
                )
    requirement = registry.identity_spaces.get("requirement")
    registered_requirement_children = (
        {
            f"requirement.{child_name}"
            for child_name in requirement.child_spaces
        }
        if requirement is not None
        else set()
    )
    for issued_space in sorted(issued.numbers):
        if (
            issued_space.startswith("requirement.REQ-")
            and issued_space not in registered_requirement_children
        ):
            findings.append(
                RegistryFinding(
                    "identity-history-space-missing",
                    f"identity_spaces.{issued_space}",
                    "issued Requirement child space is not registered",
                )
            )
    return tuple(sorted(findings))
