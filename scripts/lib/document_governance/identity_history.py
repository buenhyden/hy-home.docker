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
from typing import TYPE_CHECKING

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

if TYPE_CHECKING:
    from scripts.lib.document_governance.registry import (
        DocumentRegistry,
        RegistryFinding,
    )


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
    r"inc-[0-9]{4}-[0-9]{4}(?:-PM)?|"
    r"(?:AD|ADR|SPEC|RES|AUD|DATA|GDE|POL|RUN|MIG)-[0-9]{4}"
    r")\b"
)
# Current Registry artifact_id_pattern prefixes and their identity spaces.
# Tombstone IDs embed the retired identity and carry no number of their own,
# and incident IDs (inc-YYYY-NNNN) are handled separately in _record.
IDENTITY_PREFIX_SPACES = (
    ("ADR-", "adr", "docs/02.architecture/decisions/"),
    ("AD-", "architecture-description", "docs/02.architecture/descriptions/"),
    ("SPEC-", "spec", "docs/03.specs/"),
    ("GDE-", "operations-subject", "docs/05.operations/"),
    ("POL-", "operations-subject", "docs/05.operations/"),
    ("RUN-", "operations-subject", "docs/05.operations/"),
    ("INC-", "incident", "docs/05.operations/"),
    ("RES-", "research", "docs/90.references/"),
    ("AUD-", "audit", "docs/90.references/"),
    ("DATA-", "data", "docs/90.references/"),
    ("MIG-", "migration", "docs/98.archive/"),
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
_TRUSTED_LEGACY_REQUIREMENT_PATH = re.compile(
    r"docs/01\.requirements/prd-(?P<package>[0-9]{4})-"
    r"[a-z0-9][a-z0-9-]*\.md"
)
_TRUSTED_LEGACY_CHILD_ID = re.compile(
    r"PRD-(?P<package>[0-9]{4})-R(?P<number>[0-9]{4})"
)
_TRUSTED_LEGACY_REQUIREMENT_SECTION = re.compile(
    r"(?ms)^## (?P<name>Requirements|Non-functional Requirements)\n"
    r"(?P<body>.*?)(?=^## |\Z)"
)
_TRUSTED_LEGACY_SECTION_KIND = {
    "Requirements": "FR",
    "Non-functional Requirements": "NFR",
}
_TRUSTED_LEGACY_REQUIREMENT_SUBSECTION = re.compile(
    r"(?ms)^### (?P<name>Functional requirements|Non-functional requirements)\n"
    r"(?P<body>.*?)(?=^### |\Z)"
)
_TRUSTED_LEGACY_SUBSECTION_KIND = {
    "Functional requirements": "FR",
    "Non-functional requirements": "NFR",
}


class IdentityHistoryError(RuntimeError):
    """Raised when Git history cannot be inspected safely."""


def match_historical_requirement_path(path: str) -> re.Match[str] | None:
    """Match one immutable pre-taxonomy Requirement package path."""

    return _TRUSTED_LEGACY_REQUIREMENT_PATH.fullmatch(path)


def parse_historical_requirement_declarations(
    package_texts: Mapping[str, str],
) -> tuple[bool, dict[str, set[int]]]:
    """Recover child allocations only when a trusted snapshot uses old grammar."""

    historical_paths = {
        path: match
        for path in package_texts
        if (match := match_historical_requirement_path(path)) is not None
    }
    if not historical_paths:
        return False, {}
    if len(historical_paths) != len(package_texts):
        raise IdentityHistoryError(
            "trusted Requirement predecessor mixes current and legacy package paths"
        )

    declarations: dict[str, set[int]] = {}
    for path, path_match in historical_paths.items():
        package_number = path_match.group("package")
        for section in _TRUSTED_LEGACY_REQUIREMENT_SECTION.finditer(
            package_texts[path]
        ):
            bodies = (
                (
                    _TRUSTED_LEGACY_SECTION_KIND[section.group("name")],
                    section.group("body"),
                ),
            )
            if section.group("name") == "Requirements":
                subsections = tuple(
                    _TRUSTED_LEGACY_REQUIREMENT_SUBSECTION.finditer(
                        section.group("body")
                    )
                )
                if subsections:
                    bodies = tuple(
                        (
                            _TRUSTED_LEGACY_SUBSECTION_KIND[subsection.group("name")],
                            subsection.group("body"),
                        )
                        for subsection in subsections
                    )
            for expected_kind, body in bodies:
                for match in _TRUSTED_LEGACY_CHILD_ID.finditer(body):
                    if match.group("package") != package_number:
                        raise IdentityHistoryError(
                            "trusted Requirement predecessor has a foreign child ID: "
                            f"{path}"
                        )
                    name = f"REQ-{package_number}.{expected_kind}"
                    declarations.setdefault(name, set()).add(int(match.group("number")))
    return True, declarations


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
    if upper.startswith("INC-"):
        # inc-YYYY-NNNN: the allocation follows the year.
        collected.setdefault("incident", set()).add(
            numbers[1] if len(numbers) > 1 else package
        )
        return
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
    for prefix, space, _root in IDENTITY_PREFIX_SPACES:
        if upper.startswith(prefix):
            collected.setdefault(space, set()).add(package)
            return


def _path_accepts_identity(path: str, identity: str) -> bool:
    upper = identity.upper()
    if upper.startswith(("REQ-", "PRD-", "SRS-", "IFR-")):
        return path.startswith("docs/01.requirements/")
    for prefix, _space, root in IDENTITY_PREFIX_SPACES:
        if upper.startswith(prefix):
            return path.startswith(root)
    return False


def _is_decision_task(path: str, identity: str, registry: DocumentRegistry) -> bool:
    """A recovery decision is owned by a current Stage 03 Task."""

    from scripts.lib.document_governance.registry import classify_path

    return classify_path(path, registry) == "task" and _path_accepts_identity(
        path, identity
    )


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
    refs: tuple[str, ...] = ("HEAD",),
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
            or not relative.startswith(IDENTITY_SOURCE_PREFIXES)
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

    from scripts.lib.document_governance.registry import (
        RegistryFinding,
        classify_path,
        preserved_origin_path,
    )

    if re.fullmatch(r"[0-9a-f]{40}", base_commit) is None:
        raise IdentityHistoryError("allocation predecessor must be a full commit")
    deadline = time.monotonic() + MAX_GIT_SCAN_SECONDS
    remaining_bytes = MAX_TRANSITION_GIT_OUTPUT_BYTES

    # Merged forks share most blobs; a blob is immutable, so each is read once.
    blobs: dict[str, tuple[str, int]] = {}

    def git(*args: str, maximum: int = MAX_TRANSITION_GIT_OUTPUT_BYTES) -> str:
        nonlocal remaining_bytes
        blob = args[2] if args[:2] == ("cat-file", "blob") and len(args) == 3 else None
        if blob is not None and blob in blobs and blobs[blob][1] <= maximum:
            return blobs[blob][0]
        output = _run_git(
            root,
            args,
            max_output_bytes=min(maximum, remaining_bytes),
            timeout_seconds=_remaining_scan_seconds(deadline),
        )
        remaining_bytes -= output.bytes_read
        if blob is not None:
            blobs[blob] = (output.text, output.bytes_read)
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

    def is_ancestor(ancestor: str, descendant: str) -> bool:
        nonlocal remaining_bytes
        output = _run_git(
            root,
            ("merge-base", "--is-ancestor", ancestor, descendant),
            max_output_bytes=min(MAX_TRANSITION_GIT_OUTPUT_BYTES, remaining_bytes),
            timeout_seconds=_remaining_scan_seconds(deadline),
            answer_codes=frozenset({0, 1}),
        )
        remaining_bytes -= output.bytes_read
        return output.returncode == 0

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
    # Requirement child numbers (FR/NFR/IF) live in requirement bodies.
    previous_children: dict[str, set[int]] = {}
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
        origin = preserved_origin_path(path) or path
        if isinstance(identity, str) and _path_accepts_identity(origin, identity):
            _record(identity, previous)
            # Same file set as the current side: identified requirement bodies.
            if origin.startswith("docs/01.requirements/"):
                for line in text.splitlines():
                    _record_line(origin, line, previous_children)
    registry_oid = entries.get("docs/99.templates/registry.json")
    if registry_oid is None:
        # Every supported base already carries the Registry.
        raise IdentityHistoryError("allocation predecessor lacks a Registry")
    try:
        from scripts.lib.document_governance.registry import _unique_object

        raw = json.loads(
            git("cat-file", "blob", registry_oid), object_pairs_hook=_unique_object
        )
        spaces = raw["identity_spaces"]
        high_water = {}
        base_reserved: dict[str, frozenset[int]] = {}
        for name in registry.identity_spaces:
            space = spaces[name]
            mark = space["high_water"]
            if type(mark) is not int or mark < 0 or space["next_number"] != mark + 1:
                raise ValueError("invalid allocation")
            high_water[name] = mark
            reserved = space.get("reserved_history", [])
            if not isinstance(reserved, list) or any(
                type(number) is not int for number in reserved
            ):
                raise ValueError("invalid reserved history")
            base_reserved[name] = frozenset(reserved)
    except (KeyError, TypeError, ValueError) as error:
        raise IdentityHistoryError(
            "allocation predecessor Registry is invalid"
        ) from error

    observed: dict[str, set[int]] = {}
    candidate_current: dict[str, str] = {}
    candidate_slots: dict[str, dict[str, set[int]]] = {}
    candidate_origins: dict[str, str] = {}

    def identity_owner(path: str, identity: str) -> str:
        numbers = re.findall(r"[0-9]{4}", identity)
        if not numbers:
            return path
        for offset, part in enumerate(pathlib.PurePosixPath(path).parts):
            if part.startswith(numbers[0]):
                return pathlib.PurePosixPath(
                    *pathlib.PurePosixPath(path).parts[: offset + 1]
                ).as_posix()
        return path

    for path, identity in current.items():
        origin = preserved_origin_path(path) or path
        if not _path_accepts_identity(origin, identity):
            continue
        slots: dict[str, set[int]] = {}
        _record(identity, slots)
        for name, numbers in slots.items():
            if name in high_water and any(
                number <= high_water[name] and number not in previous.get(name, set())
                for number in numbers
            ):
                candidate_current[path] = identity
                candidate_slots[path] = slots
                candidate_origins[path] = origin
        for name, numbers in slots.items():
            observed.setdefault(name, set()).update(numbers)
    current_children: dict[str, set[int]] = {}
    for path, identity in current.items():
        origin = preserved_origin_path(path) or path
        if origin.startswith("docs/01.requirements/") and _path_accepts_identity(
            origin, identity
        ):
            for line in _read_identity_source(root / path).splitlines():
                _record_line(origin, line, current_children)

    merged_proven_paths: set[str] = set()
    merged_owners: dict[tuple[str, int], set[str]] = {}
    merge_rows = git(
        "rev-list",
        "--parents",
        "--merges",
        "--ancestry-path",
        f"{base_commit}..HEAD",
    )
    for row in merge_rows.splitlines():
        commits = row.split()
        if len(commits) < 3 or not all(_OBJECT_ID.fullmatch(item) for item in commits):
            raise IdentityHistoryError("merged allocation lineage is malformed")
        first_parent = commits[1]
        if not is_ancestor(base_commit, first_parent):
            continue
        for merged_parent in commits[2:]:
            if is_ancestor(merged_parent, base_commit):
                continue
            fork = git("merge-base", first_parent, merged_parent).strip()
            if _OBJECT_ID.fullmatch(fork) is None:
                raise IdentityHistoryError("merged allocation fork is malformed")
            fork_listing = git(
                "ls-tree",
                "-z",
                fork,
                "--",
                "docs/99.templates/registry.json",
            )
            fork_entry = re.fullmatch(
                r"(100644|100755) blob ([0-9a-f]{40,64})\t"
                r"docs/99\.templates/registry\.json\0?",
                fork_listing,
            )
            if fork_entry is None:
                raise IdentityHistoryError(
                    "merged allocation fork lacks a regular Registry"
                )
            declarations = git(
                "grep",
                "-z",
                "-I",
                "-i",
                "-E",
                _ARTIFACT_ID_GREP,
                merged_parent,
                "--",
                *GIT_HISTORY_QUERIES,
            )
            for declaration in declarations.splitlines():
                label, separator, line = declaration.partition("\0")
                prefix = f"{merged_parent}:"
                if not separator or not label.startswith(prefix):
                    raise IdentityHistoryError(
                        "merged allocation declaration is malformed"
                    )
                path = label.removeprefix(prefix)
                candidate_path = pathlib.PurePosixPath(path)
                if (
                    candidate_path.as_posix() != path
                    or candidate_path.is_absolute()
                    or any(part in {"", ".", ".."} for part in candidate_path.parts)
                    or not path.startswith(IDENTITY_SOURCE_PREFIXES)
                ):
                    raise IdentityHistoryError(
                        "merged allocation declaration path is unsafe"
                    )
                origin = preserved_origin_path(path) or path
                for match in HISTORICAL_ID_PATTERN.finditer(line):
                    declared_identity = match.group(0)
                    if not _path_accepts_identity(origin, declared_identity):
                        continue
                    slots: dict[str, set[int]] = {}
                    _record(declared_identity, slots)
                    owner = identity_owner(origin, declared_identity)
                    for name, numbers in slots.items():
                        for number in numbers:
                            merged_owners.setdefault((name, number), set()).add(owner)
            snapshot = git(
                "ls-tree",
                "-r",
                "-z",
                merged_parent,
                "--",
                "docs/99.templates/registry.json",
                *candidate_origins.values(),
            )
            snapshot_entries: dict[str, str] = {}
            for snapshot_row in filter(None, snapshot.split("\0")):
                match = re.fullmatch(
                    r"(100644|100755) blob ([0-9a-f]{40,64})\t([^\0]+)",
                    snapshot_row,
                )
                if match is None:
                    raise IdentityHistoryError(
                        "merged allocation lineage contains a nonregular blob"
                    )
                snapshot_entries[match[3]] = match[2]
            merged_registry_oid = snapshot_entries.get(
                "docs/99.templates/registry.json"
            )
            if merged_registry_oid is None:
                continue
            try:
                from scripts.lib.document_governance.registry import _unique_object

                merged_registry = json.loads(
                    git("cat-file", "blob", merged_registry_oid),
                    object_pairs_hook=_unique_object,
                )["identity_spaces"]
                fork_registry = json.loads(
                    git("cat-file", "blob", fork_entry[2]),
                    object_pairs_hook=_unique_object,
                )["identity_spaces"]
                merged_marks: dict[str, int] = {}
                fork_marks: dict[str, int] = {}
                for name in registry.identity_spaces:
                    merged_space = merged_registry[name]
                    fork_space = fork_registry[name]
                    merged_mark = merged_space["high_water"]
                    fork_mark = fork_space["high_water"]
                    if (
                        type(merged_mark) is not int
                        or merged_mark < 0
                        or merged_space["next_number"] != merged_mark + 1
                        or type(fork_mark) is not int
                        or fork_mark < 0
                        or fork_space["next_number"] != fork_mark + 1
                    ):
                        raise ValueError("invalid allocation")
                    merged_marks[name] = merged_mark
                    fork_marks[name] = fork_mark
            except (KeyError, TypeError, ValueError) as error:
                raise IdentityHistoryError(
                    "merged allocation lineage Registry is invalid"
                ) from error
            for path, identity in candidate_current.items():
                identity_oid = snapshot_entries.get(candidate_origins[path])
                if identity_oid is None:
                    continue
                try:
                    merged_identity = parse_frontmatter_text(
                        git(
                            "cat-file",
                            "blob",
                            identity_oid,
                            maximum=MAX_IDENTITY_SOURCE_BYTES,
                        )
                    ).get("artifact_id")
                except ValueError as error:
                    raise IdentityHistoryError(
                        "merged allocation lineage frontmatter is invalid"
                    ) from error
                if merged_identity != identity:
                    continue
                issued_slots: dict[str, set[int]] = {}
                _record(identity, issued_slots)
                if all(
                    name not in high_water
                    or (
                        name in merged_marks
                        and all(
                            fork_marks[name] < number <= merged_marks[name]
                            for number in numbers
                        )
                    )
                    for name, numbers in issued_slots.items()
                ):
                    merged_proven_paths.add(path)
    merged_issuance: dict[str, set[int]] = {}
    for path, slots in candidate_slots.items():
        if path not in merged_proven_paths:
            continue
        for name, numbers in slots.items():
            for number in numbers:
                claimants = {
                    candidate_path
                    for candidate_path, candidate_numbers in candidate_slots.items()
                    if number in candidate_numbers.get(name, set())
                }
                if claimants <= merged_proven_paths:
                    current_owners = {
                        identity_owner(
                            candidate_origins[claimant], candidate_current[claimant]
                        )
                        for claimant in claimants
                    }
                    if merged_owners.get((name, number), set()) == current_owners:
                        merged_issuance.setdefault(name, set()).add(number)
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
            or not _is_decision_task(decision_path, decision_artifact_id, registry)
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
            source_listing = git("ls-tree", "-z", source_commit, "--", source_path)
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
                git(
                    "cat-file",
                    "blob",
                    source_entry[2],
                    maximum=MAX_IDENTITY_SOURCE_BYTES,
                )
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
            or (
                target_base_metadata is not None
                and target_base_metadata.get("artifact_id") != target_artifact_id
            )
            or not _path_accepts_identity(source_path, source_artifact_id)
            or not _path_accepts_identity(target_path, target_artifact_id)
            or not source_slots
            or source_slots != target_slots
        ):
            recovery_findings.append(finding)
            continue
        for name, numbers in source_slots.items():
            previous.setdefault(name, set()).update(numbers)

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
        # A retired number stays retired: reserved_history only grows.
        if not base_reserved[name] <= frozenset(space.reserved_history):
            findings.append(
                RegistryFinding(
                    "identity-reserved-history-dropped",
                    f"identity_spaces.{name}",
                    "reserved_history cannot drop a number its predecessor reserved",
                )
            )
        # A removed identity is retired in the same change (retirement
        # precondition 4 in documentation-protocol.md).
        if (previous.get(name, set()) - observed.get(name, set())) - frozenset(
            space.reserved_history
        ):
            findings.append(
                RegistryFinding(
                    "identity-retired-not-reserved",
                    f"identity_spaces.{name}",
                    "a removed identity must be added to reserved_history",
                )
            )
        # A reserved number is retired: no current document may carry it.
        if frozenset(space.reserved_history) & observed.get(name, set()):
            findings.append(
                RegistryFinding(
                    "identity-reserved-history-live",
                    f"identity_spaces.{name}",
                    "reserved_history names a number a current document carries",
                )
            )
        issued_before = previous.get(name, set()) | merged_issuance.get(name, set())
        added = observed.get(name, set()) - issued_before
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
    requirement = registry.identity_spaces.get("requirement")
    for child_name, child in (
        requirement.child_spaces.items() if requirement is not None else ()
    ):
        key = f"requirement.{child_name}"
        # A body may mention an unissued ID (a malformed cross-reference); only
        # numbers within the allocation were ever issued.
        removed = {
            number
            for number in previous_children.get(key, set())
            - current_children.get(key, set())
            if number <= child.high_water
        }
        if removed - frozenset(child.reserved_history):
            findings.append(
                RegistryFinding(
                    "identity-retired-not-reserved",
                    f"identity_spaces.requirement.child_spaces.{child_name}",
                    "a removed requirement child must be added to reserved_history",
                )
            )
    return tuple(sorted(findings))


def validate_identity_history(
    registry: DocumentRegistry,
    issued: IssuedIdentities,
) -> tuple[RegistryFinding, ...]:
    """Reject allocation state below any observed current or historical identity."""

    from scripts.lib.document_governance.registry import RegistryFinding

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
