"""Monotonic document identity allocation derived from current and Git history."""

from __future__ import annotations

import dataclasses
import json
import os
import pathlib
import re
import selectors
import stat
import subprocess
import time
from collections.abc import Mapping
from types import MappingProxyType

from scripts.lib.document_governance.registry import (
    DocumentRegistry,
    RegistryFinding,
    classify_path,
)
from scripts.lib.document_governance.frontmatter import parse_frontmatter_text


# Object-name listings plus Requirement identity-bearing blobs, not patch text.
# The six current name scans total less than 2 MiB and the historical
# Requirement sources less than 3 MiB, so this is a real shared ceiling.
MAX_GIT_OUTPUT_BYTES = 8 * 1024 * 1024
# One pinned repository snapshot, not cumulative patch history. This remains a
# separate ceiling because transition validation reads trusted predecessor
# documents rather than the compact issued-identity history projection.
MAX_TRANSITION_GIT_OUTPUT_BYTES = 64 * 1024 * 1024
MAX_GIT_SCAN_SECONDS = 45
MAX_IDENTITY_SOURCE_BYTES = 4 * 1024 * 1024
IDENTITY_SOURCE_SUFFIXES = frozenset({".md", ".json", ".yaml", ".yml"})
IDENTITY_SOURCE_PREFIXES = (
    "docs/01.requirements/",
    "docs/02.architecture/",
    "docs/03.specs/",
    "docs/05.operations/",
    "docs/90.references/",
    "docs/98.archive/",
)
GIT_HISTORY_QUERIES = tuple(
    prefix.removesuffix("/") for prefix in IDENTITY_SOURCE_PREFIXES
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
_OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
_ARTIFACT_ID_GREP = r"^[[:space:]]*artifact_id[[:space:]]*:"
_INTERNAL_REQUIREMENT_GREP = r"(REQ|PRD|SRS|IFR)-[0-9]{4}-(FR|NFR|IF|R|AC)-?[0-9]{4}"
_GIT_GREP_BATCH_SIZE = 256


class IdentityHistoryError(RuntimeError):
    """Raised when Git history cannot be inspected safely."""


@dataclasses.dataclass(frozen=True)
class _GitOutput:
    text: str
    bytes_read: int
    returncode: int = 0


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
    answer_codes: frozenset[int] = frozenset({0}),
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
    stderr = bytearray()
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
                else:
                    stderr.extend(chunk)
        remaining_seconds = deadline - time.monotonic()
        if remaining_seconds <= 0:
            _terminate_and_reap(process, selector)
            raise IdentityHistoryError("Git identity scan exceeded its time bound")
        returncode = process.wait(timeout=remaining_seconds)
        if returncode not in answer_codes:
            # Name the command and carry Git's own words. Five branches of this
            # function once raised one indistinguishable message and discarded
            # stderr, which made every failure here undiagnosable.
            detail = bytes(stderr).decode("utf-8", "replace").strip()
            raise IdentityHistoryError(
                "bounded Git identity scan failed: git "
                + " ".join(arguments)
                + f" exited {returncode}"
                + (f": {detail}" if detail else "")
            )
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
        return _GitOutput(stdout.decode("utf-8"), observed, returncode)
    except UnicodeError as error:
        raise IdentityHistoryError(
            "Git identity scan returned invalid UTF-8"
        ) from error


def git_predicate(repo: pathlib.Path, arguments: tuple[str, ...]) -> bool:
    """Run a Git predicate where exit 1 is the answer `false`, not a failure.

    `git merge-base --is-ancestor` documents 0 for true and 1 for false; only
    2 and above are errors. Reading 1 as a failure turns a legitimate verdict
    into `configuration-error: bounded Git identity scan failed`.
    """

    output = _run_git(repo, arguments, answer_codes=frozenset({0, 1}))
    return output.returncode == 0


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
    while (
        selector is not None
        and selector.get_map()
        and time.monotonic() < drain_deadline
    ):
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
            collected.setdefault(f"requirement.{package_id}.{child}", set()).add(
                numbers[-1]
            )
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


def _history_identity_group(path: str) -> tuple[str, bool] | None:
    """Return a stage-acceptance path and whether child IDs are required."""

    if path.startswith("docs/01.requirements/"):
        return "docs/01.requirements/history.md", True
    if path.startswith("docs/02.architecture/descriptions/"):
        return "docs/02.architecture/descriptions/history.md", False
    if path.startswith("docs/02.architecture/decisions/"):
        return "docs/02.architecture/decisions/history.md", False
    for prefix in (
        "docs/03.specs/",
        "docs/05.operations/",
        "docs/90.references/",
        "docs/98.archive/",
    ):
        if path.startswith(prefix):
            return f"{prefix}history.md", False
    return None


def _historical_objects(
    repo: pathlib.Path,
    prefix: str,
    refs: tuple[str, ...],
    *,
    max_output_bytes: int,
    timeout_seconds: float,
) -> tuple[tuple[tuple[str, str], ...], int]:
    """Return historical object/path names without reading a Git patch."""

    output = _run_git(
        repo,
        ("rev-list", "--objects", *refs, "--", prefix),
        max_output_bytes=max_output_bytes,
        timeout_seconds=timeout_seconds,
    )
    objects: set[tuple[str, str]] = set()
    for line in output.text.splitlines():
        object_id, separator, path = line.partition(" ")
        if not separator:
            continue
        if _OBJECT_ID.fullmatch(object_id) is None:
            raise IdentityHistoryError("Git identity object name is malformed")
        if not path:
            continue
        if path in {"docs", prefix}:
            continue
        if (
            not path.startswith(f"{prefix}/")
            or pathlib.PurePosixPath(path).as_posix() != path
            or pathlib.PurePosixPath(path).is_absolute()
            or any(
                part in {"", ".", ".."} for part in pathlib.PurePosixPath(path).parts
            )
            or any(ord(character) < 32 for character in path)
        ):
            raise IdentityHistoryError(f"Git identity object path is unsafe: {path}")
        objects.add((object_id, path))
    return tuple(sorted(objects)), output.bytes_read


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
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | os.O_NONBLOCK
    )
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
    *,
    include_current: bool = True,
) -> IssuedIdentities:
    """Return issued-number sets from current files and bounded Git objects."""

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
    deleted_files = frozenset(
        _run_git(
            root,
            ("ls-files", "-z", "--deleted"),
            timeout_seconds=_remaining_scan_seconds(deadline),
        ).text.split("\0")
    )
    collected: dict[str, set[int]] = {}
    for relative in current_files if include_current else ():
        _remaining_scan_seconds(deadline)
        if (
            relative in deleted_files
            or
            not relative.startswith(IDENTITY_SOURCE_PREFIXES)
            or pathlib.PurePosixPath(relative).suffix.casefold()
            not in IDENTITY_SOURCE_SUFFIXES
        ):
            continue
        path = root / relative
        for line in _read_identity_source(path).splitlines():
            _record_line(relative, line, collected)
    remaining_output_bytes = MAX_GIT_OUTPUT_BYTES
    identity_groups: dict[tuple[str, bool], set[str]] = {}
    for pathspec in GIT_HISTORY_QUERIES:
        objects, bytes_read = _historical_objects(
            root,
            pathspec,
            refs,
            max_output_bytes=remaining_output_bytes,
            timeout_seconds=_remaining_scan_seconds(deadline),
        )
        remaining_output_bytes -= bytes_read
        for object_id, path in objects:
            if (
                pathlib.PurePosixPath(path).suffix.casefold()
                not in IDENTITY_SOURCE_SUFFIXES
            ):
                continue
            group = _history_identity_group(path)
            if group is not None:
                identity_groups.setdefault(group, set()).add(object_id)
    for (path, include_internal), object_ids in sorted(identity_groups.items()):
        ordered = sorted(object_ids)
        for offset in range(0, len(ordered), _GIT_GREP_BATCH_SIZE):
            patterns = ["-e", _ARTIFACT_ID_GREP]
            if include_internal:
                patterns.extend(("-e", _INTERNAL_REQUIREMENT_GREP))
            output = _run_git(
                root,
                (
                    "grep",
                    "-h",
                    "-I",
                    "-i",
                    "-E",
                    *patterns,
                    *ordered[offset : offset + _GIT_GREP_BATCH_SIZE],
                ),
                max_output_bytes=remaining_output_bytes,
                timeout_seconds=_remaining_scan_seconds(deadline),
                answer_codes=frozenset({0, 1}),
            )
            remaining_output_bytes -= output.bytes_read
            for line in output.text.splitlines():
                _record_line(path, line, collected)
    return IssuedIdentities(
        numbers=MappingProxyType(
            {name: frozenset(values) for name, values in sorted(collected.items())}
        )
    )


def validate_allocation_transition(
    root: pathlib.Path,
    registry: DocumentRegistry,
    current: Mapping[str, str],
    base_commit: str,
    *,
    recovery_evidence: Mapping[str, object] | None = None,
    decision_evidence: Mapping[str, object] | None = None,
) -> tuple[RegistryFinding, ...]:
    """Compare stable package issuance with one pinned, regular Git predecessor."""

    if re.fullmatch(r"[0-9a-f]{40}", base_commit) is None:
        raise IdentityHistoryError("allocation predecessor must be a full commit")
    deadline = time.monotonic() + MAX_GIT_SCAN_SECONDS
    remaining_bytes = MAX_TRANSITION_GIT_OUTPUT_BYTES

    def git(*args: str, maximum: int = MAX_TRANSITION_GIT_OUTPUT_BYTES) -> str:
        nonlocal remaining_bytes
        output = _run_git(
            root,
            args,
            max_output_bytes=min(maximum, remaining_bytes),
            timeout_seconds=_remaining_scan_seconds(deadline),
        )
        remaining_bytes -= output.bytes_read
        return output.text

    def require_ancestor(ancestor: str, descendant: str, subject: str) -> None:
        """Assert one commit precedes another, and say so when it does not.

        These four checks are preconditions, not scans. Reading the predicate's
        exit 1 as a scan failure reported a true verdict as
        `configuration-error` and named neither commit.
        """

        nonlocal remaining_bytes
        output = _run_git(
            root,
            ("merge-base", "--is-ancestor", ancestor, descendant),
            max_output_bytes=min(MAX_TRANSITION_GIT_OUTPUT_BYTES, remaining_bytes),
            timeout_seconds=_remaining_scan_seconds(deadline),
            answer_codes=frozenset({0, 1}),
        )
        remaining_bytes -= output.bytes_read
        if output.returncode != 0:
            raise IdentityHistoryError(
                f"{subject} {ancestor} does not precede {descendant}"
            )

    require_ancestor(base_commit, "HEAD", "allocation predecessor")
    listing = git(
        "ls-tree",
        "-r",
        "-z",
        base_commit,
        "--",
        "docs/99.templates/registry.json",
        *IDENTITY_SOURCE_PREFIXES,
    )
    entries: dict[str, str] = {}
    for row in filter(None, listing.split("\0")):
        match = re.fullmatch(r"(100644|100755) blob ([0-9a-f]{40,64})\t([^\0]+)", row)
        if match is None:
            raise IdentityHistoryError(
                "allocation predecessor contains a nonregular blob"
            )
        entries[match[3]] = match[2]
    previous: dict[str, set[int]] = {}
    for path, oid in entries.items():
        if not path.endswith(".md"):
            continue
        text = git("cat-file", "blob", oid, maximum=MAX_IDENTITY_SOURCE_BYTES)
        try:
            identity = parse_frontmatter_text(text).get("artifact_id")
        except ValueError as error:
            raise IdentityHistoryError(
                "allocation predecessor frontmatter is invalid"
            ) from error
        if isinstance(identity, str) and _path_accepts_identity(path, identity):
            _record(identity, previous)
    registry_oid = entries.get("docs/99.templates/registry.json")
    # Exact reviewed renames preserve identity even when the predecessor's
    # migrated envelope had not yet acquired its canonical artifact_id.
    migration_path = (
        root / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
    )
    if migration_path.exists():
        from scripts.lib.document_governance.archive import _approved_migration_document

        try:
            approved_selection = _approved_migration_document(root)
            require_ancestor(
                approved_selection["baseline_commit"],
                "HEAD",
                "approved migration baseline",
            )
            for row in approved_selection["rows"]:
                target = row.get("target_path")
                identity = row.get("artifact_id")
                if (
                    row.get("action") == "rename"
                    and isinstance(identity, str)
                    and (row["source_path"] in entries or target in entries)
                    and current.get(target) == identity
                ):
                    _record(identity, previous)
        except (KeyError, ValueError) as error:
            raise IdentityHistoryError(
                "identity-preserving mapping cannot be verified"
            ) from error
    if registry_oid is None:
        # Only the reviewed pre-introduction lineage can bootstrap a Registry.
        from scripts.lib.document_governance.archive import _approved_migration_document

        try:
            approved = _approved_migration_document(root)
            approved_base = approved["baseline_commit"]
            require_ancestor(base_commit, approved_base, "allocation predecessor")
            require_ancestor(approved_base, "HEAD", "approved migration baseline")
            prior_registry = git(
                "log",
                "--format=%H",
                "-1",
                base_commit,
                "--",
                "docs/99.templates/registry.json",
            ).strip()
            if prior_registry:
                raise IdentityHistoryError("a removed Registry cannot bootstrap again")
            historical = collect_issued_identities(
                root, refs=(base_commit,), include_current=False
            )
            high_water = {
                name: historical.high_water(name) for name in registry.identity_spaces
            }
        except (KeyError, ValueError) as error:
            raise IdentityHistoryError(
                "allocation bootstrap lacks approved lineage"
            ) from error
    else:
        try:
            from scripts.lib.document_governance.registry import _unique_object

            raw = json.loads(
                git("cat-file", "blob", registry_oid), object_pairs_hook=_unique_object
            )
            spaces = raw["identity_spaces"]
            high_water = {}
            for name in registry.identity_spaces:
                space = spaces[name]
                mark = space["high_water"]
                if (
                    type(mark) is not int
                    or mark < 0
                    or space["next_number"] != mark + 1
                ):
                    raise ValueError("invalid allocation")
                high_water[name] = mark
        except (KeyError, TypeError, ValueError) as error:
            raise IdentityHistoryError(
                "allocation predecessor Registry is invalid"
            ) from error
    recovery_findings: list[RegistryFinding] = []
    for target_path, raw in sorted((recovery_evidence or {}).items()):
        finding = RegistryFinding(
            "identity-recovery-invalid",
            target_path,
            "identity recovery must prove one deleted regular predecessor blob",
        )
        if not isinstance(raw, Mapping) or set(raw) != {
            "source_commit",
            "source_path",
            "source_artifact_id",
            "decision_path",
            "decision_artifact_id",
            "disposition",
        }:
            recovery_findings.append(finding)
            continue
        source_commit = raw.get("source_commit")
        source_path = raw.get("source_path")
        source_artifact_id = raw.get("source_artifact_id")
        decision_path = raw.get("decision_path")
        decision_artifact_id = raw.get("decision_artifact_id")
        target_artifact_id = current.get(target_path)
        decision_rows = (decision_evidence or {}).get(decision_path)
        expected_decision = {
            "source_commit": source_commit,
            "source_path": source_path,
            "source_artifact_id": source_artifact_id,
            "target_path": target_path,
            "target_artifact_id": target_artifact_id,
            "disposition": "consolidated",
        }
        matching_decisions = (
            [
                row
                for row in decision_rows
                if isinstance(row, Mapping) and dict(row) == expected_decision
            ]
            if isinstance(decision_rows, (list, tuple))
            else []
        )
        if (
            not isinstance(source_commit, str)
            or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None
            or not isinstance(source_path, str)
            or pathlib.PurePosixPath(source_path).as_posix() != source_path
            or pathlib.PurePosixPath(source_path).is_absolute()
            or any(part in {"", ".", ".."} for part in source_path.split("/"))
            or not source_path.startswith(IDENTITY_SOURCE_PREFIXES)
            or not isinstance(source_artifact_id, str)
            or not isinstance(decision_path, str)
            or pathlib.PurePosixPath(decision_path).as_posix() != decision_path
            or pathlib.PurePosixPath(decision_path).is_absolute()
            or any(part in {"", ".", ".."} for part in decision_path.split("/"))
            or not decision_path.startswith(IDENTITY_SOURCE_PREFIXES)
            or not isinstance(decision_artifact_id, str)
            or current.get(decision_path) != decision_artifact_id
            or classify_path(decision_path, registry) != "task"
            or not _path_accepts_identity(decision_path, decision_artifact_id)
            or not isinstance(target_artifact_id, str)
            or classify_path(target_path, registry) != "research-member"
            or classify_path(source_path, registry) is not None
            or pathlib.PurePosixPath(source_path).parent
            != pathlib.PurePosixPath(target_path).parent
            or source_artifact_id == target_artifact_id
            or len(matching_decisions) != 1
            or raw.get("disposition") != "consolidated"
            or source_path in entries
        ):
            recovery_findings.append(finding)
            continue
        try:
            require_ancestor(source_commit, base_commit, "identity recovery source")
            source_listing = git(
                "ls-tree", "-z", source_commit, "--", source_path
            )
            source_rows = tuple(filter(None, source_listing.split("\0")))
            source_entry = (
                re.fullmatch(
                    r"(100644|100755) blob ([0-9a-f]{40,64})\t([^\0]+)",
                    source_rows[0],
                )
                if len(source_rows) == 1
                else None
            )
            if source_entry is None or source_entry[3] != source_path:
                recovery_findings.append(finding)
                continue
            source_metadata = parse_frontmatter_text(
                git("cat-file", "blob", source_entry[2], maximum=MAX_IDENTITY_SOURCE_BYTES)
            )
            target_base_metadata = (
                parse_frontmatter_text(
                    git(
                        "cat-file",
                        "blob",
                        entries[target_path],
                        maximum=MAX_IDENTITY_SOURCE_BYTES,
                    )
                )
                if target_path in entries
                else None
            )
        except (IdentityHistoryError, ValueError):
            recovery_findings.append(finding)
            continue
        source_slots: dict[str, set[int]] = {}
        target_slots: dict[str, set[int]] = {}
        _record(source_artifact_id, source_slots)
        _record(target_artifact_id, target_slots)
        if (
            source_metadata.get("artifact_id") != source_artifact_id
            or target_base_metadata is not None
            and target_base_metadata.get("artifact_id") != target_artifact_id
            or not _path_accepts_identity(source_path, source_artifact_id)
            or not _path_accepts_identity(target_path, target_artifact_id)
            or not source_slots
            or source_slots != target_slots
        ):
            recovery_findings.append(finding)
            continue
        for name, numbers in source_slots.items():
            previous.setdefault(name, set()).update(numbers)

    observed: dict[str, set[int]] = {}
    for path, identity in current.items():
        if _path_accepts_identity(path, identity):
            _record(identity, observed)
    findings: list[RegistryFinding] = list(recovery_findings)
    for name, space in registry.identity_spaces.items():
        mark = high_water[name]
        if space.high_water < mark:
            findings.append(
                RegistryFinding(
                    "identity-allocation-regression",
                    f"identity_spaces.{name}",
                    "allocation cannot move below its trusted predecessor",
                )
            )
        added = observed.get(name, set()) - previous.get(name, set())
        if any(number <= mark for number in added):
            findings.append(
                RegistryFinding(
                    "identity-reuse-forbidden",
                    f"identity_spaces.{name}",
                    "new package identity is already reserved by its predecessor",
                )
            )
        if added and (
            space.high_water < max(added) or space.next_number != space.high_water + 1
        ):
            findings.append(
                RegistryFinding(
                    "identity-allocation-not-advanced",
                    f"identity_spaces.{name}",
                    "new identity requires atomic allocation advancement",
                )
            )
    return tuple(sorted(findings))


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
        {f"requirement.{child_name}" for child_name in requirement.child_spaces}
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
