#!/usr/bin/env python3
"""Create and validate durable evidence for Spec 137 pre-deletion Gate 9."""

from __future__ import annotations

import argparse
import base64
import contextlib
import dataclasses
import fcntl
import hashlib
import json
import os
import pathlib
import re
import secrets
import select
import shutil
import signal
import stat
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Final


SCHEMA: Final = "agentic-research-gate9/v1"
BUNDLE_SCHEMA: Final = "agentic-research-gate9-bundle/v1"
BUILD_RECEIPT_SCHEMA: Final = "agentic-research-gate9-build-receipt/v1"
BUNDLE_MAX_BYTES: Final = 32 * 1024 * 1024
CONTROL_MAX_BYTES: Final = 4 * 1024 * 1024
OLD_PACK: Final = pathlib.PurePosixPath(
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh"
)
NEW_PACK: Final = pathlib.PurePosixPath(
    "docs/90.references/research/2026-08-08-agentic-engineering-research-pack"
)
INDEX: Final = pathlib.PurePosixPath(
    "docs/90.references/data/0082-llm-wiki-index/README.md"
)
COVERAGE: Final = pathlib.PurePosixPath(
    "docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md"
)
LLM_WIKI_GENERATOR: Final = pathlib.PurePosixPath(
    "scripts/knowledge/generate-llm-wiki.py"
)
REF_PREFIX: Final = "refs/codex/review-evidence/agentic-research/gate9/v1"
EVIDENCE_REF_PATTERN: Final = re.compile(
    rf"{re.escape(REF_PREFIX)}/attempt-[12]/[0-9a-f]{{64}}"
)
SPEC_PATH: Final = pathlib.PurePosixPath(
    "docs/03.specs/0137-agentic-research-pack-rebuild/spec.md"
)
PLAN_PATH: Final = pathlib.PurePosixPath(
    "docs/03.specs/0137-agentic-research-pack-rebuild/plan.md"
)
TASK_PATH: Final = pathlib.PurePosixPath(
    "docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md"
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
REQUIREMENT_PATTERN: Final = re.compile(
    rb"(?<![A-Za-z0-9_-])REQ-[0-9]+(?![A-Za-z0-9_-])"
)
EXPECTED_REQUIREMENTS: Final = frozenset(
    f"REQ-{ordinal:02d}".encode() for ordinal in range(1, 37)
)
TASK_REQUIREMENT_SUMMARY_PATTERN: Final = re.compile(
    rb"(?<![0-9])36/36 requirements(?![A-Za-z0-9_-])"
)
FUNNEL_SECONDS: Final = 2.0
FUNNEL_GRACE_SECONDS: Final = 0.5
FOR_EACH_REF_MAX_BYTES: Final = 4 * 1024
LOOSE_LEAF_MIN_BYTES: Final = 1
LOOSE_LEAF_MAX_BYTES: Final = 65
NAMESPACE_COMPONENTS: Final = tuple(REF_PREFIX.split("/"))
ATTEMPT_DIRECTORY_PATTERN: Final = re.compile(r"attempt-[12]")
LOOSE_LEAF_PATTERN: Final = re.compile(r"[0-9a-f]{64}")
EXPECTED_HEX_PATTERN: Final = re.compile(r"[0-9a-f]{64}")
EXTERNAL_BUNDLE_MODES: Final = (
    "verify-package",
    "verify-assignments",
    "verify-backfill",
    "publish-evidence-ref",
    "verify-authorized",
)
REF_RECORD_FORMAT: Final = "%(refname)%00%(objectname)%00%(objecttype)%00%(symref)%00"


class Gate9Error(RuntimeError):
    """A stable fail-closed Gate 9 contract error."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def fail(code: str, detail: str) -> None:
    raise Gate9Error(code, detail)


class FunnelDeadline(Exception):
    """Raised by the ``ITIMER_REAL`` handler that bounds a Gate 9 funnel."""


def _raise_funnel_deadline(signum: int, frame: object) -> None:
    del signum, frame
    raise FunnelDeadline()


def _reap_funnel_child(process: subprocess.Popen[bytes]) -> None:
    """Terminate, grace, conditionally kill, and synchronously reap one child.

    Funnel 1 signals only a process group this gate created; it never signals
    its own group, its session, or its parent.
    """
    own_group = os.getpgrp()
    try:
        group = os.getpgid(process.pid)
    except OSError:
        group = None
    signalled_group = group is not None and group != own_group
    try:
        if signalled_group:
            os.killpg(group, signal.SIGTERM)
        else:
            process.terminate()
    except OSError:
        pass
    try:
        process.communicate(timeout=FUNNEL_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        try:
            if signalled_group:
                os.killpg(group, signal.SIGKILL)
            else:
                process.kill()
        except OSError:
            pass
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.communicate(timeout=FUNNEL_GRACE_SECONDS)
    except OSError:
        pass
    process.wait()


def funnel_spawn(
    argv: Sequence[str],
    *,
    cwd: pathlib.Path | None,
    env: Mapping[str, str],
    input_bytes: bytes | None = None,
    pass_fds: Sequence[int] = (),
    code: str,
    label: str,
) -> subprocess.CompletedProcess[bytes]:
    """Funnel 1 — every Gate 9 subprocess invocation, bounded and reaped."""
    try:
        process = subprocess.Popen(
            list(argv),
            cwd=cwd,
            env=dict(env),
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            pass_fds=tuple(pass_fds),
        )
    except OSError as error:
        fail(code, f"{label} cannot be spawned: {error}")
    try:
        stdout, stderr = process.communicate(input_bytes, timeout=FUNNEL_SECONDS)
    except subprocess.TimeoutExpired:
        _reap_funnel_child(process)
        fail(code, f"{label} exceeded the {FUNNEL_SECONDS}s Gate 9 funnel bound")
    except BaseException:
        _reap_funnel_child(process)
        raise
    return subprocess.CompletedProcess(list(argv), process.returncode, stdout, stderr)


def funnel_descriptor_read(
    opener: Callable[[], int],
    *,
    code: str,
    label: str,
    max_bytes: int,
    require: Callable[[os.stat_result], str | None] | None = None,
) -> tuple[os.stat_result, os.stat_result, bytes]:
    """Funnels 2 and 3 — one bounded, non-following, non-blocking read.

    The ``ITIMER_REAL`` alarm is armed **before** ``open`` because a park
    inside ``open`` is the residual hazard this deadline exists for. ``poll()``
    is used only as an additional read-phase cap. A late alarm arriving after
    the guarded call returned and before the disarm is caught at this funnel
    boundary and mapped to this site's fail-closed code.
    """
    slot: list[int] = []
    payload: bytes | None = None
    before: os.stat_result | None = None
    after: os.stat_result | None = None
    previous = signal.signal(signal.SIGALRM, _raise_funnel_deadline)
    signal.setitimer(signal.ITIMER_REAL, FUNNEL_SECONDS)
    deadline = time.monotonic() + FUNNEL_SECONDS
    try:
        try:
            slot.append(opener())
            descriptor = slot[0]
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                fail(code, f"{label} is not a regular file")
            if require is not None:
                complaint = require(before)
                if complaint is not None:
                    fail(code, complaint)
            if before.st_size > max_bytes:
                fail(code, f"{label} exceeds its {max_bytes}-byte bound")
            if os.lseek(descriptor, 0, os.SEEK_CUR) != 0:
                fail(code, f"{label} descriptor offset is not zero")
            chunks: list[bytes] = []
            observed = 0
            poller = select.poll()
            poller.register(descriptor, select.POLLIN)
            while observed < before.st_size:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not poller.poll(remaining * 1000.0):
                    fail(
                        code,
                        f"{label} exceeded the {FUNNEL_SECONDS}s Gate 9 funnel bound",
                    )
                chunk = os.read(descriptor, min(1024 * 1024, before.st_size - observed))
                if not chunk:
                    fail(code, f"{label} ended before its stated size")
                chunks.append(chunk)
                observed += len(chunk)
            if before.st_size and os.read(descriptor, 1):
                fail(code, f"{label} exceeds its stated size")
            after = os.fstat(descriptor)
            payload = b"".join(chunks)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)
    except FunnelDeadline:
        fail(code, f"{label} exceeded the {FUNNEL_SECONDS}s Gate 9 funnel bound")
    except Gate9Error:
        raise
    except OSError as error:
        fail(code, f"{label}: {error}")
    finally:
        for descriptor in slot:
            os.close(descriptor)
    if before is None or after is None or payload is None:
        fail(code, f"{label} produced no bounded observation")
    return before, after, payload


def whole_file_bytes(
    path: "pathlib.Path | MemoryBlob", *, code: str, label: str
) -> bytes:
    if isinstance(path, MemoryBlob):
        return path.read_bytes()
    return funnel_whole_file(path, code=code, label=label)


def funnel_whole_file(path: pathlib.Path, *, code: str, label: str) -> bytes:
    """Funnel 3 — every ``Path.read_bytes()``-class whole-file read."""
    literal = pathlib.Path(path).absolute()

    def opener() -> int:
        return os.open(
            literal,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
        )

    def require(metadata: os.stat_result) -> str | None:
        if metadata.st_size > BUNDLE_MAX_BYTES:
            return f"{label} exceeds the Gate 9 whole-file bound"
        return None

    before, after, payload = funnel_descriptor_read(
        opener,
        code=code,
        label=label,
        max_bytes=BUNDLE_MAX_BYTES,
        require=require,
    )
    if (before.st_dev, before.st_ino, before.st_size) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
    ):
        fail(code, f"{label} changed during its bounded read")
    return payload


@dataclasses.dataclass(frozen=True)
class RawTreeEntry:
    mode: bytes
    object_type: bytes
    oid: bytes
    name: bytes


def _parse_raw_tree_records(
    raw: bytes,
    object_width: int,
    *,
    allow_paths: bool,
) -> tuple[RawTreeEntry, ...]:
    if object_width not in {40, 64} or (raw and not raw.endswith(b"\0")):
        fail("PROJECTED_TREE_SCOPE_DRIFT", "malformed raw tree stream")
    records: list[RawTreeEntry] = []
    previous_key: bytes | None = None
    for row in raw[:-1].split(b"\0") if raw else ():
        metadata, separator, name = row.partition(b"\t")
        fields = metadata.split(b" ")
        if not separator or len(fields) != 3:
            fail("PROJECTED_TREE_SCOPE_DRIFT", "malformed raw tree record")
        mode, object_type, oid = fields
        valid_pair = (mode, object_type) in {
            (b"040000", b"tree"),
            (b"100644", b"blob"),
            (b"100755", b"blob"),
            (b"120000", b"blob"),
            (b"160000", b"commit"),
        }
        components = name.split(b"/")
        if (
            not valid_pair
            or len(oid) != object_width
            or re.fullmatch(rb"[0-9a-f]+", oid) is None
            or not name
            or b"\0" in name
            or (not allow_paths and b"/" in name)
            or any(component in {b"", b".", b".."} for component in components)
        ):
            fail("PROJECTED_TREE_SCOPE_DRIFT", "unsafe or noncanonical raw tree record")
        ordering_key = name + (b"/" if object_type == b"tree" else b"")
        if previous_key is not None and ordering_key <= previous_key:
            fail("PROJECTED_TREE_SCOPE_DRIFT", "raw tree records are not Git-sorted")
        records.append(RawTreeEntry(mode, object_type, oid, name))
        previous_key = ordering_key
    return tuple(records)


def parse_raw_tree_records(raw: bytes, object_width: int) -> tuple[RawTreeEntry, ...]:
    """Parse one raw ``git ls-tree -z`` level with byte-exact names."""
    return _parse_raw_tree_records(raw, object_width, allow_paths=False)


def run_git(
    root: pathlib.Path,
    args: Sequence[str],
    *,
    env: Mapping[str, str] | None = None,
    input_bytes: bytes | None = None,
    check: bool = True,
    pass_fds: Sequence[int] = (),
    isolate_config: bool = False,
    funnel_code: str = "GIT_FAILURE",
) -> subprocess.CompletedProcess[bytes]:
    command_env = (
        {
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": os.defpath,
        }
        if isolate_config
        else os.environ.copy()
    )
    command_env["GIT_NO_REPLACE_OBJECTS"] = "1"
    if env:
        command_env.update(env)
    command_env["GIT_NO_REPLACE_OBJECTS"] = "1"
    result = funnel_spawn(
        ["git", *args],
        cwd=root,
        env=command_env,
        input_bytes=input_bytes,
        pass_fds=pass_fds,
        code=(
            "FOREIGN_REF" if any(REF_PREFIX in value for value in args) else funnel_code
        ),
        label=f"git {' '.join(args)}",
    )
    if check and result.returncode:
        stderr = result.stderr.decode("utf-8", "replace").strip()
        fail("GIT_FAILURE", f"git {' '.join(args)}: {stderr}")
    return result


def repository_root() -> pathlib.Path:
    result = funnel_spawn(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=None,
        env=os.environ.copy(),
        code="NOT_A_REPOSITORY",
        label="git rev-parse --show-toplevel",
    )
    if result.returncode:
        fail("NOT_A_REPOSITORY", result.stderr.decode("utf-8", "replace").strip())
    return pathlib.Path(result.stdout.decode("utf-8", "replace").strip()).resolve()


def repository_index_path(root: pathlib.Path) -> pathlib.Path:
    raw = (
        run_git(root, ["rev-parse", "--absolute-git-dir"])
        .stdout.decode("utf-8", "replace")
        .strip()
    )
    if not raw:
        fail("NON_REGULAR_INDEX", "the repository index path cannot be resolved")
    return pathlib.Path(raw) / "index"


def assert_regular_repository_index(root: pathlib.Path) -> None:
    """Reject a non-regular index before the first index-reading Git call.

    This guard is unconditional. It runs immediately after the repository-root
    probe and before the authority preflight in every mode, because the first
    index-reading Git invocation is the preflight's ``git diff`` pair.
    """
    index_path = repository_index_path(root)
    try:
        metadata = os.lstat(index_path)
    except FileNotFoundError:
        return
    except OSError as error:
        fail("NON_REGULAR_INDEX", f"the repository index cannot be inspected: {error}")
    if not stat.S_ISREG(metadata.st_mode):
        fail(
            "NON_REGULAR_INDEX",
            f"the repository index is not a regular file: {os.fspath(index_path)}",
        )


def gate9_repository(root: pathlib.Path | None = None) -> pathlib.Path:
    resolved = repository_root() if root is None else root
    assert_regular_repository_index(resolved)
    return resolved


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


def load_canonical_json(path: pathlib.Path | MemoryBlob) -> dict[str, Any]:
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


def load_canonical_json_bytes(
    raw: bytes,
    label: str,
    *,
    schema: str = SCHEMA,
) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail("INVALID_JSON", f"{label}: {error}")
    if not isinstance(value, dict) or raw != canonical_json(value):
        fail("NON_CANONICAL_JSON", label)
    if value.get("schema") != schema:
        fail("INVALID_SCHEMA", label)
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
        ["ls-tree", "-r", "-z", "--full-tree", commit, "--", prefix.as_posix()],
    ).stdout
    try:
        records = _parse_raw_tree_records(
            raw,
            object_format_width(root),
            allow_paths=True,
        )
    except Gate9Error as error:
        fail("INVALID_TREE_MANIFEST", f"{error.code}: {error.detail}")
    rows: list[bytes] = []
    prefix_bytes = prefix.as_posix().encode("utf-8", "strict") + b"/"
    for record in records:
        if record.mode != b"100644" or record.object_type != b"blob":
            fail("INVALID_TREE_MANIFEST", "manifest contains a non-regular blob")
        _verify_object(root, record, "INVALID_TREE_MANIFEST")
        if not record.name.startswith(prefix_bytes) or any(
            byte in record.name for byte in (b"\t", b"\r", b"\n")
        ):
            fail("INVALID_TREE_MANIFEST", "manifest path is outside prefix or not TSV-safe")
        try:
            path = record.name.decode("utf-8", "strict")
            _safe_mapping_path(path)
        except (UnicodeDecodeError, Gate9Error) as error:
            fail("INVALID_TREE_MANIFEST", f"unsafe manifest path: {error}")
        rows.append(
            b"\t".join((record.mode, record.object_type, record.oid, record.name))
            + b"\n"
        )
    return b"".join(sorted(rows))


def manifest_paths(value: bytes) -> list[str]:
    paths: list[str] = []
    for line in value.splitlines():
        fields = line.split(b"\t", 3)
        if len(fields) != 4:
            fail("INVALID_TREE_MANIFEST", line.decode("utf-8", "replace"))
        paths.append(fields[3].decode("utf-8"))
    return paths


def validate_pack_semantics(
    spec: bytes,
    task: bytes,
    new_manifest: bytes,
    old_manifest: bytes | None = None,
) -> None:
    """Validate the semantic pack shape shared by build and every replay."""
    new_paths = manifest_paths(new_manifest)
    readme = (NEW_PACK / "README.md").as_posix()
    if (
        len(new_paths) != 21
        or len(set(new_paths)) != 21
        or readme not in new_paths
        or any(pathlib.PurePosixPath(path).parent != NEW_PACK for path in new_paths)
    ):
        fail(
            "PACK_CARDINALITY",
            "new pack must be one README and twenty flat leaf paths",
        )
    if old_manifest is not None:
        old_paths = manifest_paths(old_manifest)
        if len(old_paths) != 20 or len(set(old_paths)) != 20:
            fail("PACK_CARDINALITY", "old pack must contain exactly twenty files")
    for label, value in (("spec", spec), ("task", task)):
        if frozenset(REQUIREMENT_PATTERN.findall(value)) != EXPECTED_REQUIREMENTS:
            fail(
                "PACKAGE_SEMANTIC_DRIFT",
                f"{label} requirement set is not exact REQ-01 through REQ-36",
            )
    if TASK_REQUIREMENT_SUMMARY_PATTERN.search(task) is None:
        fail("PACKAGE_SEMANTIC_DRIFT", "task lacks token-bounded 36/36 requirements")


def _mapping_patch(
    root: pathlib.Path,
    task: pathlib.PurePosixPath,
    before: bytes,
    after: bytes,
) -> bytes:
    before_tree = build_tree_from_mapping(
        root, {task.as_posix(): ("100644", before)}
    )
    after_tree = build_tree_from_mapping(
        root, {task.as_posix(): ("100644", after)}
    )
    return run_git(
        root,
        [
            "-c",
            "core.attributesFile=/dev/null",
            "diff-tree",
            "-r",
            "--no-commit-id",
            "--no-ext-diff",
            "--no-textconv",
            "--binary",
            "--full-index",
            before_tree,
            after_tree,
            "--",
            task.as_posix(),
        ],
        isolate_config=True,
    ).stdout


def _task_candidate_patch(
    root: pathlib.Path,
    commit: str,
    task: pathlib.PurePosixPath,
    candidate: bytes,
) -> bytes:
    before = run_git(root, ["show", f"{commit}:{task.as_posix()}"]).stdout
    return _mapping_patch(root, task, before, candidate)


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
class ProjectedRootTree:
    initial_tree_oid: str
    final_tree_oid: str
    old_paths: tuple[str, ...]
    projected_paths: tuple[str, ...]
    deletion_statuses: tuple[tuple[str, str], ...]
    proposed_deletion_patch: bytes


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


def object_format_name(root: pathlib.Path) -> str:
    value = run_git(root, ["rev-parse", "--show-object-format"]).stdout.decode().strip()
    if value not in {"sha1", "sha256"}:
        fail("PROJECTED_TREE_SCOPE_DRIFT", f"unsupported object format: {value}")
    return value


def _raw_tree_bytes(entries: Sequence[RawTreeEntry]) -> bytes:
    return b"".join(
        entry.mode
        + b" "
        + entry.object_type
        + b" "
        + entry.oid
        + b"\t"
        + entry.name
        + b"\0"
        for entry in entries
    )


def _verify_object(root: pathlib.Path, entry: RawTreeEntry, code: str) -> None:
    result = run_git(root, ["cat-file", "-t", entry.oid.decode("ascii")], check=False)
    expected = entry.object_type + b"\n"
    if result.returncode or result.stdout != expected:
        fail(code, f"missing or mistyped object for {entry.name!r}")


def _emit_verified_tree(
    root: pathlib.Path,
    entries: Sequence[RawTreeEntry],
    *,
    code: str,
) -> str:
    ordered = tuple(
        sorted(
            entries,
            key=lambda entry: entry.name
            + (b"/" if entry.object_type == b"tree" else b""),
        )
    )
    if len({entry.name for entry in ordered}) != len(ordered):
        fail(code, "duplicate tree entry")
    for entry in ordered:
        _verify_object(root, entry, code)
    value = _raw_tree_bytes(ordered)
    result = run_git(root, ["mktree", "-z"], input_bytes=value)
    tree_oid = result.stdout.decode("ascii", "strict").strip()
    width = object_format_width(root)
    if re.fullmatch(rf"[0-9a-f]{{{width}}}", tree_oid) is None:
        fail(code, "mktree returned a malformed OID")
    reread = run_git(root, ["ls-tree", "-z", tree_oid]).stdout
    if parse_raw_tree_records(reread, width) != ordered:
        fail(code, "mktree reread differs from supplied entries")
    return tree_oid


def _safe_mapping_path(raw: object) -> tuple[bytes, ...]:
    if not isinstance(raw, str) or not raw or raw.startswith("/"):
        fail("PROJECTED_TREE_SCOPE_DRIFT", "mapping path is not relative")
    try:
        encoded = raw.encode("utf-8", "strict")
    except UnicodeEncodeError as error:
        fail("PROJECTED_TREE_SCOPE_DRIFT", f"mapping path is not UTF-8: {error}")
    components = tuple(encoded.split(b"/"))
    if any(part in {b"", b".", b".."} or b"\0" in part for part in components):
        fail("PROJECTED_TREE_SCOPE_DRIFT", "mapping path contains unsafe components")
    return components


def build_tree_from_mapping(
    root: pathlib.Path,
    mapping: Mapping[str, tuple[str, bytes]],
) -> str:
    """Hash a validated path/mode/bytes mapping into a verified Git tree."""
    trie: dict[bytes, object] = {}
    for raw_path, raw_leaf in mapping.items():
        if (
            not isinstance(raw_leaf, tuple)
            or len(raw_leaf) != 2
            or raw_leaf[0] not in {"100644", "100755", "120000"}
            or not isinstance(raw_leaf[1], bytes)
        ):
            fail("PROJECTED_TREE_SCOPE_DRIFT", "invalid logical leaf")
        parts = _safe_mapping_path(raw_path)
        node = trie
        for part in parts[:-1]:
            child = node.get(part)
            if child is None:
                child = {}
                node[part] = child
            if not isinstance(child, dict):
                fail("PROJECTED_TREE_SCOPE_DRIFT", "file/directory prefix collision")
            node = child
        if parts[-1] in node:
            fail("PROJECTED_TREE_SCOPE_DRIFT", "duplicate or prefix-colliding path")
        node[parts[-1]] = raw_leaf

    width = object_format_width(root)

    def emit(node: Mapping[bytes, object]) -> str:
        entries: list[RawTreeEntry] = []
        for name in sorted(node):
            value = node[name]
            if isinstance(value, dict):
                child_oid = emit(value)
                entry = RawTreeEntry(
                    b"040000", b"tree", child_oid.encode("ascii"), name
                )
            else:
                logical_mode, content = value
                oid = run_git(
                    root,
                    ["hash-object", "-w", "--stdin"],
                    input_bytes=content,
                ).stdout.strip()
                if len(oid) != width:
                    fail("PROJECTED_TREE_SCOPE_DRIFT", "hash-object OID width drift")
                entry = RawTreeEntry(
                    logical_mode.encode("ascii"), b"blob", oid, name
                )
            entries.append(entry)
        return _emit_verified_tree(root, entries, code="PROJECTED_TREE_SCOPE_DRIFT")

    return emit(trie)


def _tree_level(root: pathlib.Path, tree_oid: str, width: int) -> tuple[RawTreeEntry, ...]:
    entries = parse_raw_tree_records(
        run_git(root, ["ls-tree", "-z", tree_oid]).stdout,
        width,
    )
    for entry in entries:
        _verify_object(root, entry, "PROJECTED_TREE_SCOPE_DRIFT")
    return entries


def _recursive_tree_paths(
    root: pathlib.Path,
    tree_oid: str,
    width: int,
) -> tuple[bytes, ...]:
    records = _parse_raw_tree_records(
        run_git(root, ["ls-tree", "-r", "-z", "--full-tree", tree_oid]).stdout,
        width,
        allow_paths=True,
    )
    paths: list[bytes] = []
    for entry in records:
        if entry.object_type != b"blob":
            fail("PROJECTED_TREE_SCOPE_DRIFT", "projected recursive entry is not a blob")
        _verify_object(root, entry, "PROJECTED_TREE_SCOPE_DRIFT")
        paths.append(entry.name)
    if len(set(paths)) != len(paths):
        fail("PROJECTED_TREE_SCOPE_DRIFT", "projected paths are not unique")
    return tuple(sorted(paths))


def _decode_projected_paths(paths: Sequence[bytes]) -> tuple[str, ...]:
    decoded: list[str] = []
    for raw in paths:
        try:
            value = raw.decode("utf-8", "strict")
        except UnicodeDecodeError as error:
            fail("PROJECTED_TREE_SCOPE_DRIFT", f"projected path is not UTF-8: {error}")
        _safe_mapping_path(value)
        decoded.append(value)
    return tuple(decoded)


def _diff_tree_bytes(
    root: pathlib.Path,
    initial_tree: str,
    final_tree: str,
    mode_args: Sequence[str],
) -> bytes:
    return run_git(
        root,
        [
            "-c",
            "core.attributesFile=/dev/null",
            "diff-tree",
            "-r",
            "--no-commit-id",
            "--no-renames",
            "--no-ext-diff",
            "--no-textconv",
            *mode_args,
            initial_tree,
            final_tree,
        ],
        env={"GIT_ATTR_SOURCE": initial_tree},
        isolate_config=True,
    ).stdout


def project_root_tree(
    root: pathlib.Path,
    commit: str,
    retiring_path: pathlib.PurePosixPath = OLD_PACK,
) -> ProjectedRootTree:
    """Remove one exact subtree by rebuilding only its four ancestor trees."""
    width = object_format_width(root)
    initial_tree = commit_tree_oid(root, commit)
    if len(retiring_path.parts) != 4:
        fail("PROJECTED_TREE_SCOPE_DRIFT", "retiring path must have four components")
    ancestry: list[tuple[tuple[RawTreeEntry, ...], RawTreeEntry]] = []
    current_tree = initial_tree
    for component in retiring_path.parts:
        entries = _tree_level(root, current_tree, width)
        component_bytes = component.encode("utf-8", "strict")
        matches = [entry for entry in entries if entry.name == component_bytes]
        if len(matches) != 1 or matches[0].mode != b"040000" or matches[0].object_type != b"tree":
            fail("PROJECTED_TREE_SCOPE_DRIFT", f"missing tree ancestor: {component}")
        ancestry.append((entries, matches[0]))
        current_tree = matches[0].oid.decode("ascii")

    old_records = _parse_raw_tree_records(
        run_git(root, ["ls-tree", "-r", "-z", "--full-tree", current_tree]).stdout,
        width,
        allow_paths=True,
    )
    old_relative: list[bytes] = []
    for entry in old_records:
        if entry.mode != b"100644" or entry.object_type != b"blob":
            fail("PROJECTED_DELETION_DRIFT", "retiring subtree is not all regular blobs")
        _verify_object(root, entry, "PROJECTED_TREE_SCOPE_DRIFT")
        old_relative.append(entry.name)
    if len(old_relative) != 20 or len(set(old_relative)) != 20:
        fail("PROJECTED_DELETION_DRIFT", "retiring subtree is not exact 20/20")

    replacement_oid: str | None = None
    for depth, (entries, target) in enumerate(reversed(ancestry)):
        if depth == 0:
            replaced = [entry for entry in entries if entry.name != target.name]
        else:
            if replacement_oid is None:
                fail("PROJECTED_TREE_SCOPE_DRIFT", "ancestor replacement is missing")
            replaced = [
                RawTreeEntry(entry.mode, entry.object_type, replacement_oid.encode(), entry.name)
                if entry.name == target.name
                else entry
                for entry in entries
            ]
        replacement_oid = _emit_verified_tree(
            root,
            replaced,
            code="PROJECTED_TREE_SCOPE_DRIFT",
        )
    if replacement_oid is None or replacement_oid == initial_tree:
        fail("PROJECTED_DELETION_DRIFT", "projected root tree did not change")
    final_tree = replacement_oid

    initial_paths = _recursive_tree_paths(root, initial_tree, width)
    final_paths = _recursive_tree_paths(root, final_tree, width)
    old_prefix = retiring_path.as_posix().encode() + b"/"
    expected_deleted = tuple(sorted(old_prefix + path for path in old_relative))
    observed_deleted = tuple(sorted(set(initial_paths) - set(final_paths)))
    if (
        observed_deleted != expected_deleted
        or set(final_paths) - set(initial_paths)
        or any(path.startswith(old_prefix) for path in final_paths)
    ):
        fail("PROJECTED_DELETION_DRIFT", "projected path-set delta is not exact")

    name_status = _diff_tree_bytes(
        root, initial_tree, final_tree, ("--name-status", "-z")
    )
    fields = nul_paths(name_status, code="PROJECTED_DELETION_DRIFT")
    if len(fields) % 2:
        fail("PROJECTED_DELETION_DRIFT", "name-status output is malformed")
    statuses = tuple((fields[index], fields[index + 1]) for index in range(0, len(fields), 2))
    expected_decoded = _decode_projected_paths(expected_deleted)
    expected_statuses = tuple(("D", path) for path in expected_decoded)
    if statuses != expected_statuses:
        fail("PROJECTED_DELETION_DRIFT", "name-status deletion set drift")

    raw_diff = _diff_tree_bytes(root, initial_tree, final_tree, ("--raw", "-z"))
    raw_fields = raw_diff[:-1].split(b"\0") if raw_diff.endswith(b"\0") else []
    if len(raw_fields) != 40:
        fail("PROJECTED_DELETION_DRIFT", "raw deletion output cardinality drift")
    for index in range(0, len(raw_fields), 2):
        header, raw_path = raw_fields[index], raw_fields[index + 1]
        if not header.endswith(b" D") or raw_path != expected_deleted[index // 2]:
            fail("PROJECTED_DELETION_DRIFT", "raw deletion output drift")

    patch = _diff_tree_bytes(
        root,
        initial_tree,
        final_tree,
        ("--binary", "--full-index"),
    )
    if patch.count(b"deleted file mode 100644") != 20:
        fail("PROJECTED_DELETION_DRIFT", "binary patch deletion cardinality drift")
    return ProjectedRootTree(
        initial_tree,
        final_tree,
        expected_decoded,
        _decode_projected_paths(final_paths),
        statuses,
        patch,
    )


def _generator_manifest_bytes(
    root: pathlib.Path,
    live_commit: str,
    projected: ProjectedRootTree,
) -> bytes:
    fields = (
        b"schema=agentic-research-llm-wiki-manifest/v1",
        f"object-format={object_format_name(root)}".encode(),
        f"live-commit={live_commit}".encode(),
        f"projected-tree={projected.final_tree_oid}".encode(),
        f"count={len(projected.projected_paths)}".encode(),
        *(path.encode("utf-8", "strict") for path in projected.projected_paths),
    )
    value = b"\0".join(fields) + b"\0"
    if len(value) > 8 * 1024 * 1024:
        fail("GENERATOR_MANIFEST_OVERSIZE", "projected manifest exceeds 8 MiB")
    return value


def _sealed_manifest_fd(value: bytes) -> int:
    try:
        descriptor = os.memfd_create(
            "gate9-llm-manifest",
            os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING,
        )
        offset = 0
        while offset < len(value):
            written = os.write(descriptor, value[offset:])
            if written <= 0:
                fail("GENERATOR_MANIFEST_INVALID", "manifest write did not progress")
            offset += written
        os.lseek(descriptor, 0, os.SEEK_SET)
        required = (
            fcntl.F_SEAL_SEAL
            | fcntl.F_SEAL_SHRINK
            | fcntl.F_SEAL_GROW
            | fcntl.F_SEAL_WRITE
        )
        fcntl.fcntl(descriptor, fcntl.F_ADD_SEALS, required)
        if fcntl.fcntl(descriptor, fcntl.F_GET_SEALS) & required != required:
            fail("GENERATOR_MANIFEST_INVALID", "manifest seals are incomplete")
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 0:
            fail("GENERATOR_MANIFEST_INVALID", "manifest is not an anonymous memfd")
        return descriptor
    except Gate9Error:
        raise
    except (AttributeError, OSError) as error:
        fail("GENERATOR_MANIFEST_INVALID", f"cannot seal manifest: {error}")


def _run_generator_from_manifest(
    root: pathlib.Path,
    generator_bytes: bytes,
    manifest: bytes,
    expected_live: bytes,
    expected_package: bytes | None,
    label: pathlib.PurePosixPath,
    artifact: str,
) -> bytes:
    descriptor = _sealed_manifest_fd(manifest)
    try:
        trusted_python_text = trusted_system_tool("python3")
        trusted_python = pathlib.Path(trusted_python_text)
        environment = {
            "GATE9_LLM_MANIFEST_FD": str(descriptor),
            "GATE9_LLM_MANIFEST_SHA256": sha256_bytes(manifest),
            "GATE9_LLM_MANIFEST_SIZE": str(len(manifest)),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": os.fspath(trusted_python.parent),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
            "PYTHONSAFEPATH": "1",
        }
        result = funnel_spawn(
            [trusted_python_text, "-", "--stdout", "--artifact", artifact],
            cwd=root,
            env=environment,
            input_bytes=generator_bytes,
            pass_fds=(descriptor,),
            code="GENERATOR_STDOUT_DRIFT",
            label=f"sealed-manifest generator {label}",
        )
    finally:
        os.close(descriptor)
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
        or result.stdout != expected_live
    ):
        fail("GENERATOR_STDOUT_DRIFT", f"{label} output is not canonical/live")
    if expected_package is not None and result.stdout != expected_package:
        fail("PACKAGE_SEMANTIC_DRIFT", f"{label} attachment differs from projection")
    return result.stdout


def fresh_authority_replay(
    root: pathlib.Path,
    proof: AuthorityProof,
    projected: ProjectedRootTree,
    *,
    expected_index: bytes | None = None,
    expected_coverage: bytes | None = None,
) -> tuple[bytes, bytes]:
    manifest = _generator_manifest_bytes(root, proof.live_head, projected)
    outputs: list[bytes] = []
    for generator_path, output_path, expected_package in (
        (LLM_WIKI_GENERATOR, INDEX, expected_index),
        (LLM_WIKI_GENERATOR, COVERAGE, expected_coverage),
    ):
        generator_bytes = run_git(
            root, ["cat-file", "blob", proof.code_blob_oids[1]]
        ).stdout
        expected_live = run_git(
            root,
            ["cat-file", "blob", tracked_blob_oid(root, proof.live_head, output_path)],
        ).stdout
        outputs.append(
            _run_generator_from_manifest(
                root,
                generator_bytes,
                manifest,
                expected_live,
                expected_package,
                generator_path,
                "index" if output_path == INDEX else "coverage",
            )
        )
    return outputs[0], outputs[1]


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
        graft_bytes = (
            funnel_whole_file(
                grafts, code="AMBIGUOUS_GIT_HISTORY", label="Git grafts file"
            )
            if grafts.exists()
            else b""
        )
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
        ["ls-tree", "-z", "--full-tree", commit, "--", path.as_posix()],
    ).stdout
    try:
        records = _parse_raw_tree_records(
            raw,
            object_format_width(root),
            allow_paths=True,
        )
    except Gate9Error as error:
        fail("REVIEWED_CODE_DRIFT", f"{path}: {error.code}: {error.detail}")
    if len(records) != 1:
        fail("REVIEWED_CODE_DRIFT", f"tracked code path is missing: {path}")
    record = records[0]
    expected_mode = (
        b"100755"
        if path
        in {
            pathlib.PurePosixPath(
                "scripts/validation/agentic-research-gate9-evidence.py"
            ),
            LLM_WIKI_GENERATOR,
        }
        else b"100644"
    )
    if (
        record.name != path.as_posix().encode("utf-8", "strict")
        or record.mode != expected_mode
        or record.object_type != b"blob"
    ):
        fail("REVIEWED_CODE_DRIFT", f"tracked code identity is malformed: {path}")
    _verify_object(root, record, "REVIEWED_CODE_DRIFT")
    return record.oid.decode("ascii", "strict")


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
        LLM_WIKI_GENERATOR,
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
        task_bytes = funnel_whole_file(
            root / pathlib.Path(*TASK_PATH.parts),
            code="REVIEWED_CODE_DRIFT",
            label="tracked Task code binding",
        )
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
                payload = funnel_whole_file(
                    pathlib.Path(entry.path),
                    code="SCRATCH_SCOPE_DRIFT",
                    label=f"worktree registry entry {entry.name}",
                )
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


def strict_evidence_namespace_evidence(root: pathlib.Path) -> object:
    """Reuse the strict namespace snapshot for before/after drift evidence.

    ``PROJECTED_INDEX_SCOPE_DRIFT`` wins over ``FOREIGN_REF`` on this path so
    the operator diagnosis names the failing invariant, except for the
    ``STALE_REF_LOCK`` residue diagnosis, which stays distinct.
    """
    try:
        return evidence_namespace_snapshot(root)
    except Gate9Error as error:
        if error.code == "STALE_REF_LOCK":
            raise
        fail(
            "PROJECTED_INDEX_SCOPE_DRIFT",
            f"the Gate 9 evidence namespace is not provable: {error.code}: {error.detail}",
        )


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
    refs = strict_evidence_namespace_evidence(root)
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
    refs = strict_evidence_namespace_evidence(root)
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
    snapshot = capture_repository_snapshot(root, proof.live_head)
    primary_error: BaseException | None = None
    result: AuthoritativeProjection | None = None
    try:
        projected = project_root_tree(root, package_oid)
        if (
            projected.initial_tree_oid != commit_tree_oid(root, proof.live_head)
            or projected.initial_tree_oid != commit_tree_oid(root, package_oid)
        ):
            fail("PROJECTED_TREE_SCOPE_DRIFT", "initial root tree binding drift")
        index_bytes, coverage_bytes = fresh_authority_replay(
            root,
            proof,
            projected,
            expected_index=expected_index,
            expected_coverage=expected_coverage,
        )
        result = AuthoritativeProjection(
            package_oid,
            proof.live_head,
            proof.reviewed_code_head,
            projected.initial_tree_oid,
            projected.final_tree_oid,
            projected.old_paths,
            projected.deletion_statuses,
            projected.proposed_deletion_patch,
            index_bytes,
            coverage_bytes,
        )
    except BaseException as error:
        primary_error = error
    try:
        prove_repository_snapshot(root, snapshot)
        prove_live_head(root, proof.live_head, code="PROJECTED_TREE_SCOPE_DRIFT")
    except BaseException as invariant_error:
        primary_error = invariant_error
    if primary_error is not None:
        raise primary_error
    if result is None:
        fail("PROJECTED_TREE_SCOPE_DRIFT", "projection produced no result")
    return result

def assignment_run_id(commit: str, attempt: int, role: str) -> str:
    return sha256_bytes(f"{commit}\0{attempt}\0{role}".encode())


def fixed_evidence_ref(attempt: int, package_sha256: str) -> str:
    return f"{REF_PREFIX}/attempt-{attempt}/{package_sha256}"


@dataclasses.dataclass(frozen=True)
class LooseEvidenceLeaf:
    """One raw loose evidence leaf observed without following any symlink."""

    name: str
    oid: str
    identity: tuple[int, int, int, int]
    payload: bytes


def _open_namespace_directory(root: pathlib.Path) -> tuple[int | None, pathlib.Path]:
    """Open the fixed evidence namespace with descriptor-relative traversal.

    Absence of the namespace is an empty loose snapshot; a symlink, a
    non-directory ancestor, or an unreadable or ambiguous entry is
    ``FOREIGN_REF``.
    """
    common = git_common_dir(root)
    try:
        current = os.open(
            os.fspath(common), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        )
    except OSError as error:
        fail("FOREIGN_REF", f"the Git common directory cannot be opened: {error}")
    try:
        for component in NAMESPACE_COMPONENTS:
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                    dir_fd=current,
                )
            except FileNotFoundError:
                os.close(current)
                return None, common
            except OSError as error:
                fail(
                    "FOREIGN_REF",
                    f"evidence namespace component {component!r} is not a "
                    f"plain directory: {error}",
                )
            os.close(current)
            current = child
    except BaseException:
        os.close(current)
        raise
    return current, common


def _stale_ref_lock(
    root: pathlib.Path,
    common: pathlib.Path,
    attempt_fd: int,
    attempt: str,
    lock_name: str,
    leaf_names: Sequence[str],
) -> None:
    """Diagnose an evidence-ref lock residue read-only, and stop.

    The gate never removes, truncates, renames, opens for writing, or otherwise
    touches the lock, its siblings, its directory, the corresponding ref leaf,
    any object, the branch, the index, or the worktree. Byte size is not a
    discriminator and no ownership claim is made.
    """
    leaf_name = lock_name[: -len(".lock")]
    try:
        metadata = os.stat(lock_name, dir_fd=attempt_fd, follow_symlinks=False)
    except OSError as error:
        fail(
            "STALE_REF_LOCK",
            f"an evidence-ref lock residue cannot be inspected: {error}",
        )
    if stat.S_ISREG(metadata.st_mode):
        kind = "regular file"
    elif stat.S_ISDIR(metadata.st_mode):
        kind = "directory"
    elif stat.S_ISLNK(metadata.st_mode):
        kind = "symlink"
    elif stat.S_ISFIFO(metadata.st_mode):
        kind = "fifo"
    elif stat.S_ISSOCK(metadata.st_mode):
        kind = "socket"
    else:
        kind = "device or other"
    if leaf_name not in leaf_names:
        leaf_state = "absent"
    else:
        leaf_state = "present"
    literal = common / pathlib.Path(REF_PREFIX) / attempt / lock_name
    fail(
        "STALE_REF_LOCK",
        "an evidence-ref lock residue must be inspected and removed by an "
        f"operator: common_dir={os.fspath(common)} lock={os.fspath(literal)} "
        f"type={kind} bytes={metadata.st_size} "
        f"mtime_ns={metadata.st_mtime_ns} ref_leaf={leaf_state}",
    )


def _read_loose_leaf(
    root: pathlib.Path,
    attempt_fd: int,
    attempt: str,
    leaf_name: str,
    width: int,
) -> LooseEvidenceLeaf:
    directory = attempt_fd

    def opener() -> int:
        return os.open(
            leaf_name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
            dir_fd=directory,
        )

    def require(metadata: os.stat_result) -> str | None:
        if metadata.st_nlink != 1:
            return f"loose evidence leaf {attempt}/{leaf_name} is not exclusive"
        if not (LOOSE_LEAF_MIN_BYTES <= metadata.st_size <= LOOSE_LEAF_MAX_BYTES):
            return f"loose evidence leaf {attempt}/{leaf_name} has an unadmitted size"
        return None

    before, after, payload = funnel_descriptor_read(
        opener,
        code="FOREIGN_REF",
        label=f"loose evidence leaf {attempt}/{leaf_name}",
        max_bytes=LOOSE_LEAF_MAX_BYTES,
        require=require,
    )
    if (
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        or after.st_nlink != 1
        or not stat.S_ISREG(after.st_mode)
    ):
        fail("FOREIGN_REF", f"loose evidence leaf {attempt}/{leaf_name} is unstable")
    if len(payload) != width + 1 or not payload.endswith(b"\n"):
        fail(
            "FOREIGN_REF",
            f"loose evidence leaf {attempt}/{leaf_name} is not one direct ref",
        )
    raw_oid = payload[:-1]
    if re.fullmatch(rb"[0-9a-f]+", raw_oid) is None or len(raw_oid) != width:
        fail(
            "FOREIGN_REF",
            f"loose evidence leaf {attempt}/{leaf_name} is not a full object-format OID",
        )
    oid = raw_oid.decode("ascii", "strict")
    kind = run_git(
        root,
        ["cat-file", "-t", oid],
        check=False,
        funnel_code="FOREIGN_REF",
    )
    if kind.returncode or kind.stdout != b"commit\n":
        fail(
            "FOREIGN_REF",
            f"loose evidence leaf {attempt}/{leaf_name} does not name a commit",
        )
    return LooseEvidenceLeaf(
        f"{attempt}/{leaf_name}",
        oid,
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
        payload,
    )


def raw_loose_snapshot(root: pathlib.Path, width: int) -> tuple[LooseEvidenceLeaf, ...]:
    """Enumerate every loose descendant as raw names and bytes."""
    namespace_fd, common = _open_namespace_directory(root)
    if namespace_fd is None:
        return ()
    leaves: list[LooseEvidenceLeaf] = []
    try:
        try:
            attempts = sorted(os.listdir(namespace_fd), key=os.fsencode)
        except OSError as error:
            fail("FOREIGN_REF", f"the evidence namespace cannot be read: {error}")
        for attempt in attempts:
            if ATTEMPT_DIRECTORY_PATTERN.fullmatch(attempt) is None:
                fail(
                    "FOREIGN_REF",
                    f"evidence namespace entry {attempt!r} is not an admitted "
                    "attempt directory",
                )
            try:
                attempt_fd = os.open(
                    attempt,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                    dir_fd=namespace_fd,
                )
            except OSError as error:
                fail(
                    "FOREIGN_REF",
                    f"evidence attempt directory {attempt!r} is not a plain "
                    f"directory: {error}",
                )
            try:
                try:
                    names = sorted(os.listdir(attempt_fd), key=os.fsencode)
                except OSError as error:
                    fail(
                        "FOREIGN_REF",
                        f"evidence attempt directory {attempt!r} cannot be "
                        f"read: {error}",
                    )
                admitted = [
                    name
                    for name in names
                    if LOOSE_LEAF_PATTERN.fullmatch(name) is not None
                ]
                for name in names:
                    if name.endswith(".lock") and LOOSE_LEAF_PATTERN.fullmatch(
                        name[: -len(".lock")]
                    ):
                        _stale_ref_lock(
                            root, common, attempt_fd, attempt, name, admitted
                        )
                for name in names:
                    if LOOSE_LEAF_PATTERN.fullmatch(name) is None:
                        fail(
                            "FOREIGN_REF",
                            f"evidence leaf name {attempt}/{name!r} is not "
                            "admitted by EVIDENCE_REF_PATTERN",
                        )
                    leaves.append(
                        _read_loose_leaf(root, attempt_fd, attempt, name, width)
                    )
            finally:
                os.close(attempt_fd)
    finally:
        os.close(namespace_fd)
    return tuple(sorted(leaves, key=lambda leaf: os.fsencode(leaf.name)))


def for_each_ref_records(
    root: pathlib.Path, selector: str
) -> tuple[tuple[str, str, str, str], ...]:
    """The packed/direct-ref view, read through one trailing-NUL format."""
    result = run_git(
        root,
        ["for-each-ref", f"--format={REF_RECORD_FORMAT}", selector],
        check=False,
        env={
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "LANG": "C",
            "LC_ALL": "C",
        },
        funnel_code="FOREIGN_REF",
    )
    if (
        result.returncode != 0
        or result.stderr
        or len(result.stdout) > FOR_EACH_REF_MAX_BYTES
    ):
        fail("FOREIGN_REF", "the evidence ref namespace cannot be inspected")
    raw = result.stdout
    if not raw:
        return ()
    if not raw.endswith(b"\0\n"):
        fail("FOREIGN_REF", "the evidence ref record stream is malformed")
    records: list[tuple[str, str, str, str]] = []
    for chunk in raw.split(b"\0\n")[:-1]:
        fields = chunk.split(b"\0")
        if len(fields) != 4:
            fail("FOREIGN_REF", "an evidence ref record is incomplete")
        try:
            decoded = tuple(field.decode("ascii", "strict") for field in fields)
        except UnicodeDecodeError as error:
            fail("FOREIGN_REF", f"an evidence ref record is not ASCII: {error}")
        records.append(decoded)
    return tuple(records)


def evidence_namespace_snapshot(
    root: pathlib.Path,
) -> tuple[tuple[str, str, object], ...]:
    """One complete namespace snapshot: raw loose first, packed view second."""
    width = object_format_width(root)
    loose = raw_loose_snapshot(root, width)
    packed = for_each_ref_records(root, f"{REF_PREFIX}/")
    loose_by_name = {f"{REF_PREFIX}/{leaf.name}": leaf for leaf in loose}
    packed_by_name: dict[str, str] = {}
    for name, oid, object_type, symref in packed:
        if (
            EVIDENCE_REF_PATTERN.fullmatch(name) is None
            or re.fullmatch(rf"[0-9a-f]{{{width}}}", oid) is None
            or object_type != "commit"
            or symref
        ):
            fail("FOREIGN_REF", "evidence ref discovery is not one direct commit ref")
        if name in packed_by_name:
            fail("FOREIGN_REF", "the evidence ref namespace reports a duplicate row")
        packed_by_name[name] = oid
    rows: list[tuple[str, str, object]] = []
    for name in sorted(set(loose_by_name) | set(packed_by_name)):
        leaf = loose_by_name.get(name)
        packed_oid = packed_by_name.get(name)
        if leaf is not None and packed_oid is None:
            fail(
                "FOREIGN_REF",
                "a raw loose evidence leaf is omitted from the packed/direct view",
            )
        if leaf is None:
            rows.append((name, packed_oid, None))
            continue
        if leaf.oid != packed_oid:
            fail(
                "FOREIGN_REF",
                "the raw loose and packed/direct views disagree on an evidence ref",
            )
        rows.append((name, packed_oid, (leaf.identity, leaf.payload)))
    return tuple(rows)


def existing_evidence_refs(root: pathlib.Path) -> list[str]:
    first = evidence_namespace_snapshot(root)
    second = evidence_namespace_snapshot(root)
    if first != second:
        fail("FOREIGN_REF", "the evidence ref namespace changed during validation")
    refs = [name for name, _, _ in first]
    for evidence_ref in refs:
        if (
            EVIDENCE_REF_PATTERN.fullmatch(evidence_ref) is None
            or direct_evidence_ref_oid(root, evidence_ref) is None
        ):
            fail("FOREIGN_REF", "evidence ref discovery is not one direct commit ref")
    return refs


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
        bundle_sha256 = terminal["bundle_sha256"]
        package_sha256 = terminal["package_sha256"]
        tree_oid = terminal["tree"]
        reason = terminal["reason"]
        if terminal["attempt"] != 1:
            fail("ATTEMPT_STATE_MISMATCH", "attempt 1 ref identity mismatch")
        expected_attempt_1 = {
            "bundle_sha256": bundle_sha256,
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
        "bundle_sha256",
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
        "bundle_sha256": terminal["bundle_sha256"],
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


@dataclasses.dataclass(frozen=True)
class BundleData:
    path: pathlib.Path | None
    outer_bytes: bytes
    bundle_sha256: str
    package_sha256: str
    attachments: Mapping[str, bytes]


@dataclasses.dataclass(frozen=True)
class MemoryBlob:
    name: str
    value: bytes

    def read_bytes(self) -> bytes:
        return self.value


def read_control_file_once(path: pathlib.Path | str, label: str) -> MemoryBlob:
    supplied = pathlib.Path(path).absolute()

    def opener() -> int:
        return os.open(
            supplied,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
        )

    def require(metadata: os.stat_result) -> str | None:
        if (
            metadata.st_nlink != 1
            or metadata.st_size < 1
            or metadata.st_size > CONTROL_MAX_BYTES
        ):
            return f"{label} is not an exclusive bounded file"
        return None

    before, after, value = funnel_descriptor_read(
        opener,
        code="CONTROL_FILE_DRIFT",
        label=label,
        max_bytes=CONTROL_MAX_BYTES,
        require=require,
    )
    if (
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        or after.st_nlink != 1
        or not stat.S_ISREG(after.st_mode)
    ):
        fail("CONTROL_FILE_DRIFT", f"{label} changed during its bounded read")
    return MemoryBlob(supplied.name, value)


def _bundle_bytes(payloads: Mapping[str, bytes]) -> tuple[bytes, str]:
    if set(payloads) != set(PACKAGE_ATTACHMENTS):
        fail("BUNDLE_SCHEMA_DRIFT", "attachment path set differs")
    package_sha256 = sha256_bytes(payloads["SHA256SUMS"])
    records = [
        {
            "base64": base64.b64encode(payloads[path]).decode("ascii"),
            "bytes": len(payloads[path]),
            "mode": "0444",
            "path": path,
            "sha256": sha256_bytes(payloads[path]),
        }
        for path in sorted(payloads, key=lambda value: value.encode("utf-8"))
    ]
    outer = canonical_json(
        {
            "attachments": records,
            "kind": "gate9-package-bundle",
            "package_sha256": package_sha256,
            "schema": BUNDLE_SCHEMA,
        }
    )
    if not outer or len(outer) > BUNDLE_MAX_BYTES:
        fail("BUNDLE_SIZE_DRIFT", "canonical bundle size is outside bounds")
    return outer, package_sha256


def _decode_bundle_bytes(value: bytes, path: pathlib.Path | None) -> BundleData:
    if not value or len(value) > BUNDLE_MAX_BYTES:
        fail("BUNDLE_SIZE_DRIFT", "bundle size is outside bounds")
    try:
        document = load_canonical_json_bytes(value, "bundle", schema=BUNDLE_SCHEMA)
    except Gate9Error as error:
        fail("BUNDLE_SCHEMA_DRIFT", f"{error.code}: {error.detail}")
    if set(document) != {"attachments", "kind", "package_sha256", "schema"}:
        fail("BUNDLE_SCHEMA_DRIFT", "outer key set drift")
    if document.get("kind") != "gate9-package-bundle":
        fail("BUNDLE_SCHEMA_DRIFT", "outer kind drift")
    rows = document.get("attachments")
    if not isinstance(rows, list) or len(rows) != len(PACKAGE_ATTACHMENTS):
        fail("BUNDLE_SCHEMA_DRIFT", "attachment record count drift")
    payloads: dict[str, bytes] = {}
    observed_order: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"base64", "bytes", "mode", "path", "sha256"}:
            fail("BUNDLE_SCHEMA_DRIFT", "attachment record key drift")
        name = row.get("path")
        encoded = row.get("base64")
        if (
            not isinstance(name, str)
            or name not in PACKAGE_ATTACHMENTS
            or name in payloads
            or row.get("mode") != "0444"
            or not isinstance(encoded, str)
            or not nonnegative_int(row.get("bytes"))
        ):
            fail("BUNDLE_SCHEMA_DRIFT", "attachment identity drift")
        try:
            raw = base64.b64decode(encoded.encode("ascii"), validate=True)
        except (UnicodeEncodeError, ValueError) as error:
            fail("BUNDLE_SCHEMA_DRIFT", f"invalid base64 for {name}: {error}")
        if (
            base64.b64encode(raw).decode("ascii") != encoded
            or len(raw) != row["bytes"]
            or sha256_bytes(raw) != row.get("sha256")
        ):
            fail("BUNDLE_SCHEMA_DRIFT", f"attachment content drift: {name}")
        payloads[name] = raw
        observed_order.append(name)
    if observed_order != sorted(PACKAGE_ATTACHMENTS):
        fail("BUNDLE_SCHEMA_DRIFT", "attachment order drift")
    expected_sums = checksum_manifest(
        {name: raw for name, raw in payloads.items() if name != "SHA256SUMS"}
    )
    package_sha256 = sha256_bytes(payloads["SHA256SUMS"])
    if (
        payloads["SHA256SUMS"] != expected_sums
        or document.get("package_sha256") != package_sha256
    ):
        fail("BUNDLE_SCHEMA_DRIFT", "checksum or package identity drift")
    rebuilt, rebuilt_package = _bundle_bytes(payloads)
    if rebuilt != value or rebuilt_package != package_sha256:
        fail("BUNDLE_TRANSPORT_DRIFT", "canonical bundle reconstruction drift")
    return BundleData(path, value, sha256_bytes(value), package_sha256, payloads)


def write_atomic_bundle(attempt: int, payloads: Mapping[str, bytes]) -> BundleData:
    outer, _ = _bundle_bytes(payloads)
    parent_fd: int | None = None
    descriptor: int | None = None
    final_descriptor: int | None = None
    path: pathlib.Path | None = None
    try:
        parent_fd = os.open(
            "/tmp", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        )
        for _ in range(128):
            token = secrets.token_hex(16)
            if re.fullmatch(r"[0-9a-f]{32}", token) is None:
                fail("BUNDLE_CREATE_FAILURE", "random token is not canonical hex")
            name = f"agentic-research-gate9-attempt-{attempt}-{token}.bundle.json"
            try:
                descriptor = os.open(
                    name,
                    os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                    0o600,
                    dir_fd=parent_fd,
                )
                path = pathlib.Path("/tmp") / name
                break
            except FileExistsError:
                continue
        if descriptor is None or path is None:
            fail("BUNDLE_CREATE_FAILURE", "bundle collision budget exhausted")
        before = os.fstat(descriptor)
        offset = 0
        while offset < len(outer):
            written = os.write(descriptor, outer[offset:])
            if written <= 0:
                fail("BUNDLE_CREATE_FAILURE", "bundle write did not progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.lseek(descriptor, 0, os.SEEK_SET)
        readback = bytearray()
        while len(readback) < len(outer):
            chunk = os.read(descriptor, min(1024 * 1024, len(outer) - len(readback)))
            if not chunk:
                fail("BUNDLE_CREATE_FAILURE", "bundle readback ended early")
            readback.extend(chunk)
        if os.read(descriptor, 1):
            fail("BUNDLE_CREATE_FAILURE", "bundle readback exceeds expected size")
        after = os.fstat(descriptor)
        if (
            not stat.S_ISREG(after.st_mode)
            or after.st_nlink != 1
            or stat.S_IMODE(after.st_mode) != 0o444
            or after.st_size != len(outer)
            or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
            or bytes(readback) != outer
        ):
            fail("BUNDLE_CREATE_FAILURE", "bundle same-FD readback drift")
        entry = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        expected_metadata = (
            after.st_dev,
            after.st_ino,
            after.st_mode,
            after.st_nlink,
            after.st_size,
            after.st_mtime_ns,
        )
        if (
            not stat.S_ISREG(entry.st_mode)
            or entry.st_nlink != 1
            or stat.S_IMODE(entry.st_mode) != 0o444
            or entry.st_size != len(outer)
            or (
                entry.st_dev,
                entry.st_ino,
                entry.st_mode,
                entry.st_nlink,
                entry.st_size,
                entry.st_mtime_ns,
            )
            != expected_metadata
        ):
            fail("BUNDLE_CREATE_FAILURE", "bundle directory entry identity drift")
        os.fsync(parent_fd)
        final_descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=parent_fd,
        )
        final_before = os.fstat(final_descriptor)
        if (
            not stat.S_ISREG(final_before.st_mode)
            or final_before.st_nlink != 1
            or stat.S_IMODE(final_before.st_mode) != 0o444
            or final_before.st_size != len(outer)
            or (
                final_before.st_dev,
                final_before.st_ino,
                final_before.st_mode,
                final_before.st_nlink,
                final_before.st_size,
                final_before.st_mtime_ns,
            )
            != expected_metadata
        ):
            fail("BUNDLE_CREATE_FAILURE", "bundle final entry identity drift")
        final_readback = bytearray()
        while len(final_readback) < len(outer):
            chunk = os.read(
                final_descriptor,
                min(1024 * 1024, len(outer) - len(final_readback)),
            )
            if not chunk:
                fail("BUNDLE_CREATE_FAILURE", "bundle final readback ended early")
            final_readback.extend(chunk)
        if os.read(final_descriptor, 1):
            fail("BUNDLE_CREATE_FAILURE", "bundle final readback exceeds expected size")
        final_after = os.fstat(final_descriptor)
        if (
            (
                final_after.st_dev,
                final_after.st_ino,
                final_after.st_mode,
                final_after.st_nlink,
                final_after.st_size,
                final_after.st_mtime_ns,
            )
            != expected_metadata
            or bytes(final_readback) != outer
            or sha256_bytes(final_readback) != sha256_bytes(outer)
        ):
            fail("BUNDLE_CREATE_FAILURE", "bundle final entry readback drift")
        os.fsync(parent_fd)
        # One final paired validation, immediately after the final successful
        # parent-directory fsync. The successful completion of the second
        # member of this pair is the writer operation's linearization point;
        # no further finite pathname probe extends the publication interval.
        final_descriptor_pair = os.fstat(final_descriptor)
        if (
            final_descriptor_pair.st_dev,
            final_descriptor_pair.st_ino,
            final_descriptor_pair.st_mode,
            final_descriptor_pair.st_nlink,
            final_descriptor_pair.st_size,
            final_descriptor_pair.st_mtime_ns,
        ) != expected_metadata:
            fail("BUNDLE_CREATE_FAILURE", "bundle post-fsync descriptor drift")
        final_entry_pair = os.stat(
            name,
            dir_fd=parent_fd,
            follow_symlinks=False,
        )
        if (
            final_entry_pair.st_dev,
            final_entry_pair.st_ino,
            final_entry_pair.st_mode,
            final_entry_pair.st_nlink,
            final_entry_pair.st_size,
            final_entry_pair.st_mtime_ns,
        ) != expected_metadata:
            fail("BUNDLE_CREATE_FAILURE", "bundle post-fsync directory entry drift")
    except Gate9Error:
        raise
    except OSError as error:
        fail("BUNDLE_CREATE_FAILURE", str(error))
    finally:
        if final_descriptor is not None:
            os.close(final_descriptor)
        if descriptor is not None:
            os.close(descriptor)
        if parent_fd is not None:
            os.close(parent_fd)
    return _decode_bundle_bytes(outer, path)


def read_bundle_once(
    path: pathlib.Path | str,
    expected_bundle_sha256: str | None = None,
    expected_package_sha256: str | None = None,
) -> BundleData:
    """The first untrusted-input operation after argument parsing.

    It opens and reads the literal ``/tmp`` direct child once, validates stable
    descriptor metadata and EOF, reconstructs canonical outer bytes, and
    compares the observed literal path, ``bundle_sha256``, and
    ``package_sha256`` to the controller-trusted arguments before any authority
    preflight, semantic replay, ref discovery, projection, generator execution,
    object write, or ref publication.
    """
    supplied = pathlib.Path(path)
    if supplied.parent != pathlib.Path("/tmp") or not re.fullmatch(
        r"agentic-research-gate9-attempt-[12]-[0-9a-f]{32}\.bundle\.json",
        supplied.name,
    ):
        fail("BUNDLE_READ_FAILURE", "bundle is not a literal /tmp direct child")
    parent_fd: int | None = None
    try:
        parent_fd = os.open(
            "/tmp", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        )
    except OSError as error:
        fail("BUNDLE_READ_FAILURE", str(error))
    try:
        directory = parent_fd

        def opener() -> int:
            return os.open(
                supplied.name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
                dir_fd=directory,
            )

        def require(metadata: os.stat_result) -> str | None:
            if (
                metadata.st_nlink != 1
                or stat.S_IMODE(metadata.st_mode) != 0o444
                or metadata.st_size < 1
            ):
                return "bundle is not an exclusive 0444 regular file"
            return None

        before, after, value = funnel_descriptor_read(
            opener,
            code="BUNDLE_READ_FAILURE",
            label="bundle",
            max_bytes=BUNDLE_MAX_BYTES,
            require=require,
        )
    finally:
        os.close(parent_fd)
    if (
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        or after.st_nlink != 1
        or stat.S_IMODE(after.st_mode) != 0o444
    ):
        fail("BUNDLE_READ_FAILURE", "bundle changed during bounded read")
    data = _decode_bundle_bytes(value, supplied)
    if expected_bundle_sha256 is not None or expected_package_sha256 is not None:
        if (
            data.path is None
            or os.fspath(data.path) != os.fspath(supplied)
            or data.bundle_sha256 != expected_bundle_sha256
            or data.package_sha256 != expected_package_sha256
        ):
            fail(
                "BUNDLE_TRANSPORT_DRIFT",
                "the observed bundle receipt tuple differs from the "
                "controller-captured build receipt",
            )
    return data


def build_package(args: argparse.Namespace) -> None:
    if args.attempt not in (1, 2):
        fail("THIRD_ATTEMPT", f"attempt {args.attempt} is forbidden")
    root = gate9_repository()
    authority = authority_from_args(root, args)
    task_relative, task_path = repo_path(root, args.task)
    spec_relative, spec_path = repo_path(root, args.spec)
    plan_relative, plan_path = repo_path(root, args.plan)
    del spec_relative, plan_relative
    assert_clean_real_index(root)
    assert_task_only_worktree(root, task_relative)
    current_head = authority.live_head
    before = run_git(
        root, ["show", f"{current_head}:{task_relative.as_posix()}"]
    ).stdout
    candidate = funnel_whole_file(
        task_path, code="INPUT_READ_FAILURE", label="--task"
    )
    spec_bytes = funnel_whole_file(
        spec_path, code="INPUT_READ_FAILURE", label="--spec"
    )
    marker, _ = parse_marker(candidate)
    derived_attempt = derive_attempt(root, marker, authority)
    if args.attempt != derived_attempt:
        fail(
            "ATTEMPT_STATE_MISMATCH",
            f"derived {derived_attempt}, asserted {args.attempt}",
        )
    old_manifest = tree_manifest(root, current_head, OLD_PACK)
    new_manifest = tree_manifest(root, current_head, NEW_PACK)
    validate_pack_semantics(
        spec_bytes,
        candidate,
        new_manifest,
        old_manifest,
    )
    task_patch = _task_candidate_patch(
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
        "plan.md": funnel_whole_file(
            plan_path, code="INPUT_READ_FAILURE", label="--plan"
        ),
        "proposed-deletion.patch": projection.proposed_deletion_patch,
        "spec.md": spec_bytes,
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
    payloads["SHA256SUMS"] = checksum_manifest(payloads)
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    bundle = write_atomic_bundle(args.attempt, payloads)
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(
        canonical_json(
            {
                "bundle_path": os.fspath(bundle.path),
                "bundle_sha256": bundle.bundle_sha256,
                "package_sha256": bundle.package_sha256,
                "schema": BUILD_RECEIPT_SCHEMA,
                "state": "BUILT",
            }
        ).decode(),
        end="",
    )


def read_checksum_manifest(raw: bytes) -> dict[str, str]:
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


def verify_package_mapping(
    root: pathlib.Path,
    package: Mapping[str, bytes],
    *,
    bundle_sha256: str,
    live_reviewed_head: str,
    reviewed_code_head: str,
) -> dict[str, Any]:
    actual_paths = sorted(package)
    if actual_paths != sorted(PACKAGE_ATTACHMENTS):
        fail("ATTACHMENT_SET_DRIFT", repr(actual_paths))
    try:
        package_head = package["HEAD.txt"].decode("ascii").strip()
    except UnicodeDecodeError as error:
        fail("UNTRUSTED_PACKAGE_HEAD", f"package HEAD cannot be read: {error}")
    projection = authoritative_projection(
        root,
        package_head,
        live_reviewed_head,
        reviewed_code_head,
        expected_index=package["llm-wiki-index.md"],
        expected_coverage=package["llm-wiki-stage-category-coverage.md"],
    )
    package_doc = load_canonical_json_bytes(package["package.json"], "package.json")
    assignments = load_canonical_json_bytes(package["assignments.json"], "assignments.json")
    gates = load_canonical_json_bytes(package["gate-results.json"], "gate-results.json")
    checksums = read_checksum_manifest(package["SHA256SUMS"])
    expected_checksum_paths = sorted(set(PACKAGE_ATTACHMENTS) - {"SHA256SUMS"})
    if sorted(checksums) != expected_checksum_paths:
        fail("ATTACHMENT_SET_DRIFT", "checksum path set mismatch")
    for name, expected in checksums.items():
        if sha256_bytes(package[name]) != expected:
            fail("CHECKSUM_DRIFT", name)
    attempt = package_doc.get("attempt")
    if not nonnegative_int(attempt) or attempt not in (1, 2):
        fail("PACKAGE_SEMANTIC_DRIFT", "invalid package attempt")
    payloads = {
        name: package[name]
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
    if package["HEAD.txt"] != f"{package_head}\n".encode():
        fail("PACKAGE_SEMANTIC_DRIFT", "HEAD.txt")
    old_manifest = tree_manifest(root, package_head, OLD_PACK)
    new_manifest = tree_manifest(root, package_head, NEW_PACK)
    if package["old-manifest.tsv"] != old_manifest:
        fail("PACKAGE_SEMANTIC_DRIFT", "old-manifest.tsv")
    if package["new-manifest.tsv"] != new_manifest:
        fail("PACKAGE_SEMANTIC_DRIFT", "new-manifest.tsv")
    candidate = package["task-candidate.md"]
    validate_pack_semantics(
        package["spec.md"],
        candidate,
        new_manifest,
        old_manifest,
    )
    task_before = run_git(root, ["show", f"{package_head}:{TASK_PATH.as_posix()}"]).stdout
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
    task_patch = _task_candidate_patch(root, package_head, TASK_PATH, candidate)
    semantic_payloads = {
        "task-before.md": task_before,
        "task-before-to-candidate.patch": task_patch,
        "proposed-deletion.patch": projection.proposed_deletion_patch,
        "spec.md": run_git(root, ["show", f"{package_head}:{SPEC_PATH.as_posix()}"]).stdout,
        "plan.md": run_git(root, ["show", f"{package_head}:{PLAN_PATH.as_posix()}"]).stdout,
    }
    for name, expected in semantic_payloads.items():
        if package[name] != expected:
            fail("PACKAGE_SEMANTIC_DRIFT", name)
    if package["llm-wiki-index.md"] != projection.index_markdown:
        fail("PACKAGE_SEMANTIC_DRIFT", INDEX.as_posix())
    if (
        package["llm-wiki-stage-category-coverage.md"]
        != projection.coverage_markdown
    ):
        fail("PACKAGE_SEMANTIC_DRIFT", COVERAGE.as_posix())
    prove_live_head(root, live_reviewed_head, code="UNTRUSTED_PACKAGE_HEAD")
    return {
        "attempt": attempt,
        "assignments": assignments,
        "head": package_head,
        "package_doc": package_doc,
        "package_sha256": sha256_bytes(package["SHA256SUMS"]),
        "bundle_sha256": bundle_sha256,
    }


def verify_package(args: argparse.Namespace) -> None:
    root = gate9_repository()
    bundle = external_bundle(args)
    authority = authority_from_args(root, args)
    result = verify_package_mapping(
        root,
        bundle.attachments,
        bundle_sha256=bundle.bundle_sha256,
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(
        canonical_json(
            {
                "bundle_sha256": result["bundle_sha256"],
                "package_sha256": result["package_sha256"],
                "state": "VERIFIED",
            }
        ).decode(),
        end="",
    )


def load_attestation(
    package_result: dict[str, Any], attestation_path: pathlib.Path | MemoryBlob
) -> dict[str, Any]:
    attestation = load_canonical_json(attestation_path)
    expected_keys = {
        "assignments",
        "attempt",
        "bundle_sha256",
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
        or attestation.get("bundle_sha256") != package_result["bundle_sha256"]
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
        fail("INVALID_ATTESTATION", "reviewers must have distinct agent IDs and task paths")
    return attestation


def verify_assignments(args: argparse.Namespace) -> None:
    root = gate9_repository()
    bundle = external_bundle(args)
    authority = authority_from_args(root, args)
    package_result = verify_package_mapping(
        root,
        bundle.attachments,
        bundle_sha256=bundle.bundle_sha256,
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    attestation = read_control_file_once(args.attestation, "assignment attestation")
    load_attestation(package_result, attestation)
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    print(
        canonical_json(
            {
                "assignment_attestation_sha256": sha256_bytes(attestation.value),
                "state": "ASSIGNED",
            }
        ).decode(),
        end="",
    )


def validate_receipt(
    path: pathlib.Path | MemoryBlob,
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
        "bundle_sha256",
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
        "bundle_sha256": package_result["bundle_sha256"],
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
    package: Mapping[str, bytes],
    package_result: dict[str, Any],
    receipt_paths: Mapping[str, pathlib.Path | MemoryBlob],
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
        "bundle_sha256": package_result["bundle_sha256"],
        "evidence_ref": fixed_evidence_ref(
            package_result["attempt"], package_result["package_sha256"]
        ),
        "new_manifest_sha256": sha256_bytes(package["new-manifest.tsv"]),
        "old_manifest_sha256": sha256_bytes(package["old-manifest.tsv"]),
        "package_sha256": package_result["package_sha256"],
        "proposed_deletion_patch_sha256": sha256_bytes(
            package["proposed-deletion.patch"]
        ),
        "recovery_head": package_result["head"],
        "reviews": reviews,
        "schema": SCHEMA,
        "state": "TASK_BACKFILLED",
    }


def validate_task_state(
    package: Mapping[str, bytes],
    package_result: dict[str, Any],
    task_path: pathlib.Path,
    expect_state: str,
    receipt_paths: Mapping[str, pathlib.Path | MemoryBlob],
    receipts: Mapping[str, dict[str, Any]],
) -> None:
    candidate = package["task-candidate.md"]
    current = whole_file_bytes(
        task_path, code="INPUT_READ_FAILURE", label="--task"
    )
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
    root = gate9_repository()
    bundle = external_bundle(args)
    authority = authority_from_args(root, args)
    package = bundle.attachments
    package_result = verify_package_mapping(
        root,
        package,
        bundle_sha256=bundle.bundle_sha256,
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    attestation_path = read_control_file_once(
        args.assignment_attestation, "assignment attestation"
    )
    attestation = load_attestation(package_result, attestation_path)
    attestation_sha256 = sha256_bytes(attestation_path.read_bytes())
    receipt_paths = {
        "migration-specification": read_control_file_once(
            args.migration_receipt, "migration receipt"
        ),
        "quality": read_control_file_once(args.quality_receipt, "quality receipt"),
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
    return _mapping_patch(root, task, before, after)


def file_record(path: str, value: bytes) -> dict[str, object]:
    return {"bytes": len(value), "path": path, "sha256": sha256_bytes(value)}


def blob_record(root: pathlib.Path, value: bytes) -> dict[str, object]:
    oid = run_git(root, ["hash-object", "--stdin"], input_bytes=value).stdout.decode().strip()
    return {"blob_oid": oid, "bytes": len(value), "sha256": sha256_bytes(value)}


def checked_report(path: pathlib.Path | MemoryBlob, label: str) -> bytes:
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
    path: pathlib.Path | MemoryBlob,
    report: bytes,
    role: str,
    receipt_path: pathlib.Path | MemoryBlob,
    receipt: dict[str, Any],
    attestation_sha256: str,
    task_tuple: dict[str, Any],
) -> dict[str, Any]:
    closure = load_canonical_json(path)
    expected_keys = {
        "agent_id",
        "assignment_attestation_sha256",
        "attempt",
        "bundle_sha256",
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
        "bundle_sha256": receipt["bundle_sha256"],
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


def _evidence_tree(root: pathlib.Path, leaves: Mapping[str, bytes]) -> str:
    return build_tree_from_mapping(
        root,
        {path: ("100644", value) for path, value in leaves.items()},
    )


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


def direct_evidence_ref_oid(root: pathlib.Path, evidence_ref: str) -> str | None:
    if EVIDENCE_REF_PATTERN.fullmatch(evidence_ref) is None:
        fail("FOREIGN_REF", "evidence ref is outside the fixed Gate 9 namespace")
    result = run_git(
        root,
        [
            "for-each-ref",
            "--format=%(refname)%00%(objectname)%00%(objecttype)%00%(symref)",
            evidence_ref,
        ],
        check=False,
    )
    if result.returncode != 0 or result.stderr:
        fail("FOREIGN_REF", "evidence ref direct identity cannot be inspected")
    raw = result.stdout
    if not raw:
        symbolic = run_git(
            root,
            ["symbolic-ref", "--quiet", evidence_ref],
            check=False,
        )
        if symbolic.returncode == 0:
            fail("FOREIGN_REF", "dangling symbolic evidence refs are forbidden")
        if symbolic.returncode != 1:
            fail("FOREIGN_REF", "evidence ref absence cannot be inspected")
        return None
    if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        fail("FOREIGN_REF", "evidence ref identity is ambiguous")
    fields = raw[:-1].split(b"\0")
    width = object_format_width(root)
    if (
        len(fields) != 4
        or fields[0] != evidence_ref.encode("ascii")
        or re.fullmatch(rb"[0-9a-f]+", fields[1]) is None
        or len(fields[1]) != width
        or fields[2] != b"commit"
        or fields[3]
    ):
        fail("FOREIGN_REF", "evidence ref is not one direct commit ref")
    return fields[1].decode("ascii")


def create_or_reuse_ref(
    root: pathlib.Path,
    evidence_ref: str,
    package_head: str,
    tree_oid: str,
    message: bytes,
) -> str:
    existing = direct_evidence_ref_oid(root, evidence_ref)
    desired_identity = (package_head, tree_oid, message)

    def matches(commit: str) -> bool:
        try:
            return commit_identity(root, commit) == desired_identity
        except Gate9Error:
            return False

    if existing is not None:
        if matches(existing) and direct_evidence_ref_oid(root, evidence_ref) == existing:
            return existing
        fail("FOREIGN_REF", evidence_ref)
    commit = run_git(
        root,
        ["commit-tree", tree_oid, "-p", package_head],
        input_bytes=message,
    ).stdout.decode().strip()
    width = object_format_width(root)
    if (
        re.fullmatch(rf"[0-9a-f]{{{width}}}", commit) is None
        or run_git(root, ["cat-file", "-t", commit], check=False).stdout != b"commit\n"
        or not matches(commit)
    ):
        fail("INVALID_EVIDENCE_COMMIT", "commit-tree identity drift")
    update = run_git(
        root,
        ["update-ref", "--no-deref", evidence_ref, commit, "0" * width],
        check=False,
    )
    if update.returncode == 0:
        published = direct_evidence_ref_oid(root, evidence_ref)
        if (
            published == commit
            and matches(published)
            and direct_evidence_ref_oid(root, evidence_ref) == published
        ):
            return published
        fail("FOREIGN_REF", evidence_ref)
    raced_commit = direct_evidence_ref_oid(root, evidence_ref)
    if (
        raced_commit is not None
        and matches(raced_commit)
        and direct_evidence_ref_oid(root, evidence_ref) == raced_commit
    ):
        return raced_commit
    fail("FOREIGN_REF", evidence_ref)


def build_evidence_leaves(
    root: pathlib.Path,
    package: Mapping[str, bytes],
    package_result: dict[str, Any],
    task_relative: pathlib.PurePosixPath,
    task_path: pathlib.Path | MemoryBlob,
    state: str,
    terminal_report_path: pathlib.Path | MemoryBlob,
    attestation_path: pathlib.Path | MemoryBlob,
    optional_paths: Mapping[str, pathlib.Path | MemoryBlob | None],
) -> dict[str, bytes]:
    attestation = load_attestation(package_result, attestation_path)
    attestation_bytes = attestation_path.read_bytes()
    attestation_sha256 = sha256_bytes(attestation_bytes)
    leaves = {f"package/{name}": package[name] for name in PACKAGE_ATTACHMENTS}
    leaves["assignment-attestation.json"] = attestation_bytes
    terminal_report = checked_report(terminal_report_path, "terminal report")
    leaves["terminal/report.md"] = terminal_report
    candidate = package["task-candidate.md"]
    task_after = (
        whole_file_bytes(task_path, code="INPUT_READ_FAILURE", label="--task")
        if state == "AUTHORIZED"
        else candidate
    )
    task_patch = (
        task_transition_patch(root, candidate, task_after, task_relative)
        if state == "AUTHORIZED"
        else b""
    )
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
            fail("INVALIDATED_REASON_INVALID", drift_path.name)
        if set(drift_value) != {"kind", "reason", "schema", "state"} or (
            drift_value.get("kind") != "drift-proof"
            or drift_value.get("state") != "INVALIDATED"
        ):
            fail("INVALID_DRIFT_PROOF", drift_path.name)
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
        "bundle_sha256": package_result["bundle_sha256"],
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
    root = gate9_repository()
    bundle = external_bundle(args)
    authority = authority_from_args(root, args)
    package = bundle.attachments
    package_result = verify_package_mapping(
        root,
        package,
        bundle_sha256=bundle.bundle_sha256,
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
        name: read_control_file_once(getattr(args, name), name.replace("_", " "))
        if getattr(args, name)
        else None
        for name in optional_names
    }
    leaves = build_evidence_leaves(
        root,
        package,
        package_result,
        task_relative,
        task_path,
        args.terminal_state,
        read_control_file_once(args.terminal_report, "terminal report"),
        read_control_file_once(args.assignment_attestation, "assignment attestation"),
        optional_paths,
    )
    if set(leaves) != EVIDENCE_LEAF_PATHS:
        fail(
            "EVIDENCE_PATH_SET_DRIFT",
            repr(sorted(set(leaves) ^ EVIDENCE_LEAF_PATHS)),
        )
    prove_live_head(root, authority.live_head, code="UNTRUSTED_PACKAGE_HEAD")
    tree_oid = _evidence_tree(root, leaves)
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
                "bundle_sha256": package_result["bundle_sha256"],
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
    if (
        not isinstance(marker_ref, str)
        or EVIDENCE_REF_PATTERN.fullmatch(marker_ref) is None
    ):
        fail("INVALID_TASK_MARKER", "missing fixed evidence ref")
    if requested != "auto" and requested != marker_ref:
        fail("EVIDENCE_REF_MISMATCH", requested)
    if direct_evidence_ref_oid(repository_root(), marker_ref) is None:
        fail("MISSING_EVIDENCE_REF", marker_ref)
    return marker_ref


def read_ref_leaves(
    root: pathlib.Path, evidence_ref: str
) -> tuple[str, dict[str, bytes]]:
    commit = direct_evidence_ref_oid(root, evidence_ref)
    if commit is None:
        fail("MISSING_EVIDENCE_REF", evidence_ref)
    width = object_format_width(root)
    listing = run_git(
        root, ["ls-tree", "-r", "-z", "--full-tree", commit]
    ).stdout
    try:
        records = _parse_raw_tree_records(
            listing,
            width,
            allow_paths=True,
        )
    except Gate9Error as error:
        fail("INVALID_EVIDENCE_TREE", f"{error.code}: {error.detail}")
    leaves: dict[str, bytes] = {}
    for record in records:
        if record.mode != b"100644" or record.object_type != b"blob":
            fail("EVIDENCE_MODE_DRIFT", record.name.decode("utf-8", "replace"))
        _verify_object(root, record, "INVALID_EVIDENCE_TREE")
        try:
            path = record.name.decode("utf-8", "strict")
            _safe_mapping_path(path)
        except (UnicodeDecodeError, Gate9Error) as error:
            fail("INVALID_EVIDENCE_TREE", f"unsafe evidence path: {error}")
        if path in leaves:
            fail("INVALID_EVIDENCE_TREE", f"duplicate evidence path: {path}")
        blob = run_git(
            root,
            ["cat-file", "blob", record.oid.decode("ascii")],
            check=False,
        )
        if blob.returncode:
            fail("INVALID_EVIDENCE_TREE", f"cannot read evidence blob: {path}")
        leaves[path] = blob.stdout
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
    if direct_evidence_ref_oid(root, evidence_ref) != commit:
        fail("FOREIGN_REF", "evidence ref changed during leaf replay")
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
    package = {
        name: leaves[f"package/{name}"] for name in PACKAGE_ATTACHMENTS
    }
    outer, package_sha256 = _bundle_bytes(package)
    bundle = _decode_bundle_bytes(outer, None)
    if bundle.package_sha256 != package_sha256:
        fail("BUNDLE_TRANSPORT_DRIFT", "ref package reconstruction drift")
    package_result = verify_package_mapping(
        root,
        package,
        bundle_sha256=bundle.bundle_sha256,
        live_reviewed_head=live_reviewed_head,
        reviewed_code_head=reviewed_code_head,
    )
    evidence = load_canonical_json_bytes(leaves["evidence.json"], "evidence.json")
    state = evidence.get("state")
    if state not in {"REJECTED", "INVALIDATED"}:
        fail("ATTEMPT_STATE_MISMATCH", "attempt 1 is not pre-backfill terminal")
    expected_ref = fixed_evidence_ref(
        package_result["attempt"], package_result["package_sha256"]
    )
    if evidence_ref != expected_ref:
        fail("EVIDENCE_REF_MISMATCH", evidence_ref)
    optional_paths: dict[str, MemoryBlob | None] = {
        "migration_closure_report": None,
        "migration_closure": None,
        "quality_closure_report": None,
        "quality_closure": None,
        "drift_proof": (
            MemoryBlob("drift-proof.json", leaves["drift/drift-proof.json"])
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
            optional_paths[f"{prefix}_report"] = MemoryBlob(
                "report.md", leaves[f"reviews/{role}/report.md"]
            )
            optional_paths[f"{prefix}_receipt"] = MemoryBlob(
                "receipt.json", leaves[receipt_leaf]
            )
    reconstructed = build_evidence_leaves(
        root,
        package,
        package_result,
        TASK_PATH,
        MemoryBlob("task-after.md", leaves["task/task-after.md"]),
        state,
        MemoryBlob("report.md", leaves["terminal/report.md"]),
        MemoryBlob("assignment-attestation.json", leaves["assignment-attestation.json"]),
        optional_paths,
    )
    if reconstructed != leaves:
        fail("EVIDENCE_SCHEMA_DRIFT", evidence_ref)
    expected_tree = _evidence_tree(root, reconstructed)
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
        drift = load_canonical_json_bytes(
            leaves["drift/drift-proof.json"], "drift-proof.json"
        )
        reason = drift["reason"]
    return {
        "attempt": package_result["attempt"],
        "bundle_sha256": package_result["bundle_sha256"],
        "package_sha256": package_result["package_sha256"],
        "reason": reason,
        "state": state,
        "tree": tree_oid,
    }

def verify_authorized(args: argparse.Namespace) -> None:
    root = gate9_repository()
    external = external_bundle(args) if args.bundle else None
    authority = authority_from_args(root, args)
    task_relative, task_path = repo_path(root, args.task)
    live_task = funnel_whole_file(
        task_path, code="INPUT_READ_FAILURE", label="--task"
    )
    task_marker, _ = parse_marker(live_task)
    evidence_ref = resolve_evidence_ref(task_marker, args.evidence_ref)
    evidence_commit, leaves = read_ref_leaves(root, evidence_ref)
    preflight_evidence_ref_authority(root, evidence_commit, leaves, authority.live_head)
    external_bundle_data = external
    package = {name: leaves[f"package/{name}"] for name in PACKAGE_ATTACHMENTS}
    ref_outer, _ = _bundle_bytes(package)
    ref_bundle = _decode_bundle_bytes(ref_outer, None)
    if external_bundle_data is not None:
        if (
            external_bundle_data.package_sha256 != ref_bundle.package_sha256
            or external_bundle_data.outer_bytes != ref_bundle.outer_bytes
            or external_bundle_data.bundle_sha256 != ref_bundle.bundle_sha256
            or external_bundle_data.attachments != package
        ):
            fail("BUNDLE_TRANSPORT_DRIFT", "external and ref bundles differ")
    package_result = verify_package_mapping(
        root,
        package,
        bundle_sha256=ref_bundle.bundle_sha256,
        live_reviewed_head=authority.live_head,
        reviewed_code_head=authority.reviewed_code_head,
    )
    evidence = load_canonical_json_bytes(leaves["evidence.json"], "evidence.json")
    expected_evidence_keys = {
        "assignment", "attempt", "bundle_sha256", "closures", "drift",
        "evidence_ref", "package_head", "package_sha256", "reviews", "schema",
        "state", "task", "terminal_report",
    }
    if set(evidence) != expected_evidence_keys or evidence.get("state") != "AUTHORIZED":
        fail("NOT_AUTHORIZED", evidence_ref)
    if (
        evidence.get("attempt") != package_result["attempt"]
        or evidence.get("bundle_sha256") != package_result["bundle_sha256"]
        or evidence.get("package_head") != package_result["head"]
        or evidence.get("package_sha256") != package_result["package_sha256"]
        or evidence.get("evidence_ref") != evidence_ref
    ):
        fail("EVIDENCE_BINDING_DRIFT", evidence_ref)
    expected_message = evidence_commit_message(
        package_result["attempt"], package_result["package_sha256"], "AUTHORIZED"
    )
    commit_parent, commit_tree, commit_message = commit_identity(root, evidence_commit)
    expected_tree = _evidence_tree(root, leaves)
    if (
        commit_parent != package_result["head"]
        or commit_tree != expected_tree
        or commit_message != expected_message
    ):
        fail("EVIDENCE_COMMIT_IDENTITY_DRIFT", evidence_ref)
    if live_task != leaves["task/task-after.md"]:
        fail("TASK_AFTER_DRIFT", task_relative.as_posix())
    candidate = package["task-candidate.md"]
    expected_task_patch = task_transition_patch(root, candidate, live_task, task_relative)
    if leaves["task/task-candidate-to-after.patch"] != expected_task_patch:
        fail("TASK_PATCH_DRIFT", task_relative.as_posix())
    attestation_path = MemoryBlob(
        "assignment-attestation.json", leaves["assignment-attestation.json"]
    )
    attestation = load_attestation(package_result, attestation_path)
    attestation_sha256 = sha256_bytes(attestation_path.read_bytes())
    receipt_paths = {
        role: MemoryBlob("receipt.json", leaves[f"reviews/{role}/receipt.json"])
        for role in ROLES
    }
    receipts: dict[str, dict[str, Any]] = {}
    review_records: dict[str, dict[str, Any]] = {}
    for role in ROLES:
        report_path = f"reviews/{role}/report.md"
        receipt_leaf = f"reviews/{role}/receipt.json"
        report = checked_report(
            MemoryBlob("report.md", leaves[report_path]), f"{role} review"
        )
        receipt = validate_receipt(
            receipt_paths[role], role, package_result, attestation,
            attestation_sha256, require_approved=True,
        )
        validate_report_binding(receipt, report, role)
        receipts[role] = receipt
        review_records[role] = {
            **{
                key: receipt[key]
                for key in (
                    "agent_id", "assignment_attestation_sha256", "role", "run_id",
                    "task_path", "verdict", "findings",
                )
            },
            "receipt": file_record(receipt_leaf, leaves[receipt_leaf]),
            "report": file_record(report_path, report),
        }
    validate_task_state(
        package,
        package_result,
        MemoryBlob("task-after.md", live_task),
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
            MemoryBlob("report.md", leaves[closure_report_path]), f"{role} closure"
        )
        closure = validate_closure(
            MemoryBlob("closure.json", leaves[closure_leaf]), closure_report, role,
            receipt_paths[role], receipts[role], attestation_sha256, task_tuple,
        )
        closure_records[role] = {
            **{
                key: closure[key]
                for key in (
                    "agent_id", "role", "run_id", "task_path", "verdict", "findings",
                )
            },
            "closure": file_record(closure_leaf, leaves[closure_leaf]),
            "report": file_record(closure_report_path, closure_report),
        }
    drift = load_canonical_json_bytes(
        leaves["drift/drift-proof.json"], "drift-proof.json"
    )
    if drift != {
        "kind": "drift-proof", "schema": SCHEMA, "state": "NOT_APPLICABLE",
    }:
        fail("INVALID_DRIFT_PROOF", "AUTHORIZED drift slot")
    terminal_report = checked_report(
        MemoryBlob("report.md", leaves["terminal/report.md"]), "terminal report"
    )
    expected_evidence = {
        "assignment": file_record(
            "assignment-attestation.json", leaves["assignment-attestation.json"]
        ),
        "attempt": package_result["attempt"],
        "bundle_sha256": package_result["bundle_sha256"],
        "closures": closure_records,
        "drift": file_record("drift/drift-proof.json", leaves["drift/drift-proof.json"]),
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
                "bundle_sha256": package_result["bundle_sha256"],
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


def add_expected_receipt_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--expected-bundle-sha256")
    parser.add_argument("--expected-package-sha256")


def _flag_occurrences(argv: Sequence[str], flag: str) -> int:
    return sum(1 for value in argv if value == flag or value.startswith(f"{flag}="))


def validate_bundle_transport(args: argparse.Namespace, argv: Sequence[str]) -> None:
    """Enforce the all-or-none external-bundle transport group.

    Omission, partial supply, duplication, malformed hex, or use with
    ``--bundle-from-ref`` is a usage failure before input consumption.
    """
    if args.mode not in EXTERNAL_BUNDLE_MODES:
        return
    for flag in (
        "--bundle",
        "--expected-bundle-sha256",
        "--expected-package-sha256",
    ):
        if _flag_occurrences(argv, flag) > 1:
            fail("BUNDLE_TRANSPORT_USAGE", f"{flag} is supplied more than once")
    expected_bundle = getattr(args, "expected_bundle_sha256", None)
    expected_package = getattr(args, "expected_package_sha256", None)
    if getattr(args, "bundle_from_ref", False):
        if expected_bundle is not None or expected_package is not None:
            fail(
                "BUNDLE_TRANSPORT_USAGE",
                "--bundle-from-ref forbids --expected-bundle-sha256 and "
                "--expected-package-sha256",
            )
        return
    if getattr(args, "bundle", None) is None:
        return
    if expected_bundle is None or expected_package is None:
        fail(
            "BUNDLE_TRANSPORT_USAGE",
            "an external bundle requires --bundle, --expected-bundle-sha256, "
            "and --expected-package-sha256 together",
        )
    for flag, value in (
        ("--expected-bundle-sha256", expected_bundle),
        ("--expected-package-sha256", expected_package),
    ):
        if EXPECTED_HEX_PATTERN.fullmatch(value) is None:
            fail(
                "BUNDLE_TRANSPORT_USAGE",
                f"{flag} is not exact lowercase 64-character hex",
            )


def external_bundle(args: argparse.Namespace) -> BundleData:
    return read_bundle_once(
        args.bundle,
        args.expected_bundle_sha256,
        args.expected_package_sha256,
    )


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    build = subparsers.add_parser("build-package")
    build.add_argument("--attempt", type=int, required=True)
    build.add_argument("--spec", required=True)
    build.add_argument("--plan", required=True)
    build.add_argument("--task", required=True)
    add_authority_arguments(build)
    verify = subparsers.add_parser("verify-package")
    verify.add_argument("--bundle", required=True)
    add_expected_receipt_arguments(verify)
    add_authority_arguments(verify)
    assignments = subparsers.add_parser("verify-assignments")
    assignments.add_argument("--bundle", required=True)
    assignments.add_argument("--attestation", required=True)
    add_expected_receipt_arguments(assignments)
    add_authority_arguments(assignments)
    backfill = subparsers.add_parser("verify-backfill")
    backfill.add_argument("--bundle", required=True)
    add_expected_receipt_arguments(backfill)
    backfill.add_argument("--migration-receipt", required=True)
    backfill.add_argument("--quality-receipt", required=True)
    backfill.add_argument("--assignment-attestation", required=True)
    backfill.add_argument("--task", required=True)
    backfill.add_argument(
        "--expect-state", choices=("PACKAGE_REVIEWED", "TASK_BACKFILLED"), required=True
    )
    add_authority_arguments(backfill)
    publish = subparsers.add_parser("publish-evidence-ref")
    publish.add_argument("--bundle", required=True)
    add_expected_receipt_arguments(publish)
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
    package_source.add_argument("--bundle")
    package_source.add_argument("--bundle-from-ref", action="store_true")
    add_expected_receipt_arguments(authorized)
    authorized.add_argument("--task", required=True)
    authorized.add_argument("--evidence-ref", required=True)
    add_authority_arguments(authorized)
    authorized.add_argument("--require-clean-real-index", action="store_true")
    authorized.add_argument("--require-task-only-worktree", action="store_true")
    return parser


def main() -> int:
    parser = make_parser()
    argv = list(sys.argv[1:])
    args = parser.parse_args(argv)
    try:
        validate_bundle_transport(args, argv)
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
