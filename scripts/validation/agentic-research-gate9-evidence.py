#!/usr/bin/env python3
"""Create and validate durable evidence for Spec 137 pre-deletion Gate 9."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from typing import Any, Final


SCHEMA: Final = "agentic-research-gate9/v1"
OLD_PACK: Final = pathlib.PurePosixPath(
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh"
)
NEW_PACK: Final = pathlib.PurePosixPath(
    "docs/90.references/research/2026-08-08-agentic-engineering-research-pack"
)
INDEX: Final = pathlib.PurePosixPath(
    "docs/90.references/llm-wiki/llm-wiki-index.md"
)
COVERAGE: Final = pathlib.PurePosixPath(
    "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md"
)
INDEX_GENERATOR: Final = pathlib.PurePosixPath(
    "scripts/knowledge/generate-llm-wiki-index.sh"
)
COVERAGE_GENERATOR: Final = pathlib.PurePosixPath(
    "scripts/knowledge/generate-llm-wiki-coverage.sh"
)
REF_PREFIX: Final = "refs/codex/review-evidence/agentic-research/gate9/v1"
SPEC_PATH: Final = pathlib.PurePosixPath(
    "docs/03.specs/137-agentic-research-pack-rebuild/spec.md"
)
PLAN_PATH: Final = pathlib.PurePosixPath(
    "docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md"
)
TASK_PATH: Final = pathlib.PurePosixPath(
    "docs/04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md"
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


class Gate9Error(RuntimeError):
    """A stable fail-closed Gate 9 contract error."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def fail(code: str, detail: str) -> None:
    raise Gate9Error(code, detail)


def run_git(
    root: pathlib.Path,
    args: Sequence[str],
    *,
    env: Mapping[str, str] | None = None,
    input_bytes: bytes | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        env=command_env,
        input=input_bytes,
        capture_output=True,
        check=False,
    )
    if check and result.returncode:
        stderr = result.stderr.decode("utf-8", "replace").strip()
        fail("GIT_FAILURE", f"git {' '.join(args)}: {stderr}")
    return result


def repository_root() -> pathlib.Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail("NOT_A_REPOSITORY", result.stderr.strip())
    return pathlib.Path(result.stdout.strip()).resolve()


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


def load_canonical_json(path: pathlib.Path) -> dict[str, Any]:
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
        ["ls-tree", "-r", "--full-tree", commit, "--", prefix.as_posix()],
    ).stdout
    rows: list[bytes] = []
    for line in raw.splitlines():
        metadata, separator, path = line.partition(b"\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            fail("INVALID_TREE_MANIFEST", line.decode("utf-8", "replace"))
        rows.append(b"\t".join((*fields, path)) + b"\n")
    return b"".join(sorted(rows))


def manifest_paths(value: bytes) -> list[str]:
    paths: list[str] = []
    for line in value.splitlines():
        fields = line.split(b"\t", 3)
        if len(fields) != 4:
            fail("INVALID_TREE_MANIFEST", line.decode("utf-8", "replace"))
        paths.append(fields[3].decode("utf-8"))
    return paths


def write_task_patch_and_deletion_patch(
    root: pathlib.Path,
    commit: str,
    task: pathlib.PurePosixPath,
    candidate: bytes,
) -> tuple[bytes, bytes]:
    with tempfile.TemporaryDirectory(prefix="gate9-index-") as temporary:
        index_path = pathlib.Path(temporary) / "index"
        environment = {"GIT_INDEX_FILE": os.fspath(index_path)}
        run_git(root, ["read-tree", commit], env=environment)
        candidate_oid = run_git(root, ["hash-object", "-w", "--stdin"], input_bytes=candidate).stdout.decode().strip()
        run_git(
            root,
            ["update-index", "--cacheinfo", "100644", candidate_oid, task.as_posix()],
            env=environment,
        )
        task_patch = run_git(
            root,
            ["diff", "--cached", "--binary", "--full-index", commit, "--", task.as_posix()],
            env=environment,
        ).stdout
        run_git(root, ["read-tree", commit], env=environment)
        run_git(
            root,
            ["rm", "--cached", "-r", "--quiet", "--", OLD_PACK.as_posix()],
            env=environment,
        )
        deletion_patch = run_git(
            root,
            ["diff", "--cached", "--binary", "--full-index", commit, "--", OLD_PACK.as_posix()],
            env=environment,
        ).stdout
    return task_patch, deletion_patch


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


def prove_owned_worktree_root(
    holding: pathlib.Path,
    worktree: pathlib.Path,
    expected: tuple[int, int] | None = None,
) -> tuple[int, int]:
    try:
        holding_metadata = holding.lstat()
        worktree_metadata = worktree.lstat()
        holding_literal = holding.absolute()
        worktree_literal = worktree.absolute()
        holding_canonical = holding.resolve(strict=True)
        worktree_canonical = worktree.resolve(strict=True)
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"literal worktree path cannot be inspected: {error}",
        )
    identity = (worktree_metadata.st_dev, worktree_metadata.st_ino)
    if (
        not stat.S_ISDIR(holding_metadata.st_mode)
        or not stat.S_ISDIR(worktree_metadata.st_mode)
        or holding_canonical != holding_literal
        or worktree_canonical != worktree_literal
        or worktree_literal.parent != holding_literal
        or worktree_literal.name != "detached"
        or (expected is not None and identity != expected)
    ):
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            "temporary worktree is not the literal owned holding child",
        )
    return identity


def control_file_target(
    path: pathlib.Path,
    anchor: pathlib.Path,
    *,
    prefix: bytes = b"",
) -> pathlib.Path:
    _, _, value = exclusive_regular_bytes(
        path,
        "DETACHED_PROJECTION_SCOPE_DRIFT",
        "linked-worktree control file",
    )
    if not value.startswith(prefix):
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            "linked-worktree control file has the wrong prefix",
        )
    raw_target = value[len(prefix) :]
    if not raw_target.endswith(b"\n") or b"\n" in raw_target[:-1]:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            "linked-worktree control file is malformed",
        )
    target = pathlib.Path(os.fsdecode(raw_target[:-1]))
    if not target.is_absolute():
        target = anchor / target
    try:
        return target.resolve(strict=True)
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"linked-worktree control target cannot be resolved: {error}",
        )


def owned_linked_git_dir(
    root: pathlib.Path,
    holding: pathlib.Path,
    worktree: pathlib.Path,
    worktree_identity: tuple[int, int],
) -> tuple[pathlib.Path, pathlib.Path]:
    prove_owned_worktree_root(holding, worktree, worktree_identity)
    common_value = run_git(
        root,
        ["rev-parse", "--path-format=absolute", "--git-common-dir"],
    ).stdout.decode().strip()
    try:
        common_dir = pathlib.Path(common_value).resolve(strict=True)
        git_file = worktree.absolute() / ".git"
        admin_parent = (common_dir / "worktrees").resolve(strict=True)
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"linked-worktree ownership path cannot be resolved: {error}",
        )
    candidates: list[pathlib.Path] = []
    try:
        entries = tuple(admin_parent.iterdir())
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"linked-worktree registry cannot be inspected: {error}",
        )
    for entry in entries:
        try:
            metadata = entry.lstat()
            backlink = control_file_target(entry / "gitdir", entry)
        except Gate9Error:
            continue
        if stat.S_ISDIR(metadata.st_mode) and backlink == git_file:
            candidates.append(entry.resolve(strict=True))
    if len(candidates) != 1:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"expected one owned linked-worktree registry entry, found {len(candidates)}",
        )
    git_dir = candidates[0]
    if git_dir.parent != admin_parent:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            "owned Git directory is outside the linked-worktree registry",
        )
    return common_dir, git_dir


def detached_index_environment(
    holding: pathlib.Path,
    worktree: pathlib.Path,
    worktree_identity: tuple[int, int],
    common_dir: pathlib.Path,
    git_dir: pathlib.Path,
    real_index: tuple[pathlib.Path, tuple[int, int], int, bytes],
) -> dict[str, str]:
    prove_real_index_unchanged(real_index)
    prove_owned_worktree_root(holding, worktree, worktree_identity)
    owned_worktree = worktree.absolute()
    git_file = owned_worktree / ".git"
    pointer = control_file_target(git_file, owned_worktree, prefix=b"gitdir: ")
    backlink = control_file_target(git_dir / "gitdir", git_dir)
    linked_common = control_file_target(git_dir / "commondir", git_dir)
    if pointer != git_dir or backlink != git_file or linked_common != common_dir:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            "temporary worktree Git ownership is not bidirectional",
        )
    values = {
        "git_dir": run_git(worktree, ["rev-parse", "--absolute-git-dir"]),
        "common_dir": run_git(
            worktree,
            ["rev-parse", "--path-format=absolute", "--git-common-dir"],
        ),
        "index": run_git(
            worktree,
            ["rev-parse", "--path-format=absolute", "--git-path", "index"],
        ),
        "top_level": run_git(worktree, ["rev-parse", "--show-toplevel"]),
    }
    try:
        proven = {
            name: pathlib.Path(result.stdout.decode().strip()).resolve(strict=True)
            for name, result in values.items()
        }
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"detached Git identity cannot be resolved: {error}",
        )
    expected_index = git_dir / "index"
    try:
        expected_index_resolved = expected_index.resolve(strict=True)
        index_metadata = expected_index.lstat()
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"linked-worktree index identity cannot be inspected: {error}",
        )
    index_identity = (index_metadata.st_dev, index_metadata.st_ino)
    real_index_identity = real_index[1]
    if (
        proven["git_dir"] != git_dir
        or proven["common_dir"] != common_dir
        or proven["index"] != expected_index_resolved
        or proven["top_level"] != owned_worktree
        or not stat.S_ISREG(index_metadata.st_mode)
        or index_metadata.st_nlink != 1
        or index_identity == real_index_identity
    ):
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            "index is not exclusively owned by the temporary linked worktree",
        )
    return {"GIT_INDEX_FILE": os.fspath(expected_index)}


def restore_owned_git_pointer(
    worktree: pathlib.Path,
    git_dir: pathlib.Path,
) -> str | None:
    git_file = worktree / ".git"
    expected = f"gitdir: {git_dir}\n".encode()
    try:
        metadata = git_file.lstat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            return "temporary .git pointer is not exclusive and regular"
        if git_file.read_bytes() == expected:
            return None
        descriptor = os.open(
            git_file,
            os.O_WRONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        try:
            opened = os.fstat(descriptor)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_nlink != 1
                or (opened.st_dev, opened.st_ino)
                != (metadata.st_dev, metadata.st_ino)
            ):
                return "temporary .git pointer changed before cleanup"
            os.ftruncate(descriptor, 0)
            os.write(descriptor, expected)
        finally:
            os.close(descriptor)
    except OSError as error:
        return f"temporary .git pointer restoration failed: {error}"
    return None


def nul_paths(value: bytes) -> list[str]:
    if not value:
        return []
    if not value.endswith(b"\0"):
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "Git path output is not NUL-terminated")
    return [
        raw.decode("utf-8", "surrogateescape")
        for raw in value[:-1].split(b"\0")
    ]


def prove_detached_projection_source(
    worktree: pathlib.Path,
    commit: str,
    environment: Mapping[str, str],
) -> list[str]:
    if head(worktree) != commit:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "detached worktree HEAD differs")
    symbolic = run_git(worktree, ["symbolic-ref", "--quiet", "HEAD"], check=False)
    if symbolic.returncode == 0:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "temporary worktree is not detached")
    if symbolic.returncode != 1:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "detached HEAD cannot be proven")
    committed_tree = run_git(
        worktree, ["rev-parse", f"{commit}^{{tree}}"]
    ).stdout.decode().strip()
    indexed_tree = run_git(
        worktree, ["write-tree"], env=environment
    ).stdout.decode().strip()
    if indexed_tree != committed_tree:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "detached index differs from HEAD")
    expected_paths = sorted(manifest_paths(tree_manifest(worktree, commit, OLD_PACK)))
    tracked_paths = sorted(
        nul_paths(
            run_git(
                worktree,
                ["ls-files", "-z", "--", OLD_PACK.as_posix()],
                env=environment,
            ).stdout
        )
    )
    if tracked_paths != expected_paths or len(expected_paths) != 20:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "retiring path set differs from HEAD")
    return expected_paths


def prove_detached_projected_index(
    worktree: pathlib.Path,
    commit: str,
    expected_paths: Sequence[str],
    environment: Mapping[str, str],
) -> None:
    if head(worktree) != commit:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "detached worktree HEAD changed")
    remaining = nul_paths(
        run_git(
            worktree,
            ["ls-files", "-z", "--", OLD_PACK.as_posix()],
            env=environment,
        ).stdout
    )
    if remaining:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "retiring paths remain indexed")
    raw_status = run_git(
        worktree,
        ["diff", "--cached", "--name-status", "--no-renames", "-z", commit, "--"],
        env=environment,
    ).stdout
    fields = nul_paths(raw_status)
    if len(fields) % 2:
        fail("DETACHED_PROJECTION_SCOPE_DRIFT", "projected status is malformed")
    statuses = sorted(
        (fields[index], fields[index + 1])
        for index in range(0, len(fields), 2)
    )
    expected = sorted(("D", path) for path in expected_paths)
    if statuses != expected:
        fail(
            "DETACHED_PROJECTION_SCOPE_DRIFT",
            f"expected exact retiring deletions, found {statuses!r}",
        )


def materialize_trusted_generator(
    root: pathlib.Path,
    commit: str,
    generator: pathlib.PurePosixPath,
    destination: pathlib.Path,
) -> pathlib.Path:
    value = run_git(root, ["show", f"{commit}:{generator.as_posix()}"]).stdout
    destination.write_bytes(value)
    destination.chmod(0o500)
    return destination


def projection_output_identity(
    holding: pathlib.Path,
    worktree: pathlib.Path,
    worktree_identity: tuple[int, int],
    relative: pathlib.PurePosixPath,
    expected: tuple[int, int] | None = None,
) -> tuple[pathlib.Path, tuple[int, int]]:
    prove_owned_worktree_root(holding, worktree, worktree_identity)
    try:
        owned_worktree = worktree.absolute()
        root_metadata = owned_worktree.lstat()
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_OUTPUT_UNSAFE",
            f"projection root cannot be inspected: {error}",
        )
    if not stat.S_ISDIR(root_metadata.st_mode):
        fail("DETACHED_PROJECTION_OUTPUT_UNSAFE", "projection root is not a directory")
    parent = owned_worktree
    for part in relative.parts[:-1]:
        parent /= part
        try:
            metadata = parent.lstat()
        except OSError as error:
            fail(
                "DETACHED_PROJECTION_OUTPUT_UNSAFE",
                f"projection output parent cannot be inspected: {error}",
            )
        if not stat.S_ISDIR(metadata.st_mode):
            fail(
                "DETACHED_PROJECTION_OUTPUT_UNSAFE",
                f"projection output parent is not a real directory: {relative}",
            )
    target = parent / relative.name
    try:
        metadata = target.lstat()
        resolved = target.resolve(strict=True)
        resolved.relative_to(owned_worktree)
    except (OSError, ValueError) as error:
        fail(
            "DETACHED_PROJECTION_OUTPUT_UNSAFE",
            f"projection output cannot be contained: {error}",
        )
    identity = (metadata.st_dev, metadata.st_ino)
    if (
        resolved != target
        or not stat.S_ISREG(metadata.st_mode)
        or stat.S_IMODE(metadata.st_mode) != 0o644
        or metadata.st_nlink != 1
        or (expected is not None and identity != expected)
    ):
        fail(
            "DETACHED_PROJECTION_OUTPUT_UNSAFE",
            f"projection output is not an exclusive tracked regular file: {relative}",
        )
    return target, identity


def seed_projection_output(
    target: pathlib.Path,
    identity: tuple[int, int],
    sentinel: bytes,
) -> None:
    try:
        descriptor = os.open(
            target,
            os.O_WRONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or stat.S_IMODE(metadata.st_mode) != 0o644
                or metadata.st_nlink != 1
                or (metadata.st_dev, metadata.st_ino) != identity
            ):
                fail(
                    "DETACHED_PROJECTION_OUTPUT_UNSAFE",
                    "projection output changed before sentinel write",
                )
            os.ftruncate(descriptor, 0)
            offset = 0
            while offset < len(sentinel):
                offset += os.write(descriptor, sentinel[offset:])
        finally:
            os.close(descriptor)
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_OUTPUT_UNSAFE",
            f"projection sentinel cannot be written safely: {error}",
        )


def read_projection_output(
    target: pathlib.Path,
    identity: tuple[int, int],
) -> bytes:
    try:
        descriptor = os.open(
            target,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or stat.S_IMODE(metadata.st_mode) != 0o644
                or metadata.st_nlink != 1
                or (metadata.st_dev, metadata.st_ino) != identity
            ):
                fail(
                    "DETACHED_PROJECTION_OUTPUT_UNSAFE",
                    "projection output changed before safe read",
                )
            chunks: list[bytes] = []
            while chunk := os.read(descriptor, 1024 * 1024):
                chunks.append(chunk)
            return b"".join(chunks)
        finally:
            os.close(descriptor)
    except OSError as error:
        fail(
            "DETACHED_PROJECTION_OUTPUT_UNSAFE",
            f"projection output cannot be read safely: {error}",
        )


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


def projected_generated_outputs(root: pathlib.Path, commit: str) -> tuple[bytes, bytes]:
    real_index = capture_real_index(root)
    registry_before = run_git(root, ["worktree", "list", "--porcelain"]).stdout
    holding = pathlib.Path(tempfile.mkdtemp(prefix="gate9-worktree-holding-"))
    worktree = holding / "detached"
    result: tuple[bytes, bytes] | None = None
    primary_error: BaseException | None = None
    cleanup_errors: list[str] = []
    owned_git_dir: pathlib.Path | None = None
    worktree_identity: tuple[int, int] | None = None
    try:
        run_git(root, ["worktree", "add", "--quiet", "--detach", os.fspath(worktree), commit])
        prove_real_index_unchanged(real_index)
        worktree_identity = prove_owned_worktree_root(holding, worktree)
        common_dir, owned_git_dir = owned_linked_git_dir(
            root,
            holding,
            worktree,
            worktree_identity,
        )
        environment = detached_index_environment(
            holding,
            worktree,
            worktree_identity,
            common_dir,
            owned_git_dir,
            real_index,
        )
        prove_real_index_unchanged(real_index)
        prove_owned_worktree_root(holding, worktree, worktree_identity)
        expected_paths = prove_detached_projection_source(
            worktree, commit, environment
        )
        prove_real_index_unchanged(real_index)
        prove_owned_worktree_root(holding, worktree, worktree_identity)
        run_git(
            worktree,
            ["rm", "--cached", "-r", "-f", "--", OLD_PACK.as_posix()],
            env=environment,
        )
        prove_real_index_unchanged(real_index)
        prove_owned_worktree_root(holding, worktree, worktree_identity)
        prove_detached_projected_index(
            worktree, commit, expected_paths, environment
        )
        trusted_generators = holding / "trusted-generators"
        trusted_generators.mkdir()
        output_paths = (INDEX, COVERAGE)
        outputs = {
            output: projection_output_identity(
                holding,
                worktree,
                worktree_identity,
                output,
            )
            for output in output_paths
        }
        trusted_bash = trusted_system_tool("bash")
        trusted_git = pathlib.Path(trusted_system_tool("git"))
        trusted_python = pathlib.Path(trusted_system_tool("python3"))
        trusted_path = os.pathsep.join(
            dict.fromkeys(
                (os.fspath(trusted_git.parent), os.fspath(trusted_python.parent))
            )
        )
        generator_environment = {
            "GIT_INDEX_FILE": environment["GIT_INDEX_FILE"],
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": trusted_path,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
            "PYTHONSAFEPATH": "1",
        }
        generators = (
            (INDEX_GENERATOR, INDEX),
            (COVERAGE_GENERATOR, COVERAGE),
        )
        for ordinal, (generator, output) in enumerate(generators):
            prove_real_index_unchanged(real_index)
            for checked_output, (_, identity) in outputs.items():
                projection_output_identity(
                    holding,
                    worktree,
                    worktree_identity,
                    checked_output,
                    identity,
                )
            target, identity = outputs[output]
            sentinel = (
                b"GATE9-PROJECTION-SENTINEL\0"
                + hashlib.sha256(f"{commit}:{output}".encode()).digest()
            )
            seed_projection_output(target, identity, sentinel)
            projection_output_identity(
                holding,
                worktree,
                worktree_identity,
                output,
                identity,
            )
            if read_projection_output(target, identity) != sentinel:
                fail(
                    "DETACHED_PROJECTION_OUTPUT_UNSAFE",
                    f"projection sentinel was not written exactly: {output}",
                )
            trusted_generator = materialize_trusted_generator(
                root,
                commit,
                generator,
                trusted_generators / f"generator-{ordinal}.sh",
            )
            generator_result = subprocess.run(
                [trusted_bash, os.fspath(trusted_generator)],
                cwd=worktree,
                env=generator_environment,
                capture_output=True,
                check=False,
            )
            if generator_result.returncode:
                fail(
                    "GENERATOR_FAILURE",
                    f"{generator}: {generator_result.stderr.decode('utf-8', 'replace').strip()}",
                )
            prove_real_index_unchanged(real_index)
            for checked_output, (_, checked_identity) in outputs.items():
                projection_output_identity(
                    holding,
                    worktree,
                    worktree_identity,
                    checked_output,
                    checked_identity,
                )
        prove_real_index_unchanged(real_index)
        prove_owned_worktree_root(holding, worktree, worktree_identity)
        prove_detached_projected_index(
            worktree, commit, expected_paths, environment
        )
        projected_index = read_projection_output(*outputs[INDEX])
        projected_coverage = read_projection_output(*outputs[COVERAGE])
        tracked_index = run_git(root, ["show", f"{commit}:{INDEX.as_posix()}"]).stdout
        tracked_coverage = run_git(root, ["show", f"{commit}:{COVERAGE.as_posix()}"]).stdout
        if projected_index != tracked_index or projected_coverage != tracked_coverage:
            fail("GENERATED_OUTPUT_DRIFT", "projected LLM Wiki outputs differ from HEAD")
        result = projected_index, projected_coverage
    except BaseException as error:
        primary_error = error
    finally:
        owned_root = False
        if worktree_identity is not None:
            try:
                prove_owned_worktree_root(holding, worktree, worktree_identity)
                owned_root = True
            except Gate9Error as error:
                if primary_error is None:
                    primary_error = error
        if owned_git_dir is not None and owned_root:
            pointer_error = restore_owned_git_pointer(worktree, owned_git_dir)
            if pointer_error is not None:
                cleanup_errors.append(pointer_error)
        redirected_root = False
        try:
            if stat.S_ISLNK(worktree.lstat().st_mode):
                worktree.unlink()
                redirected_root = True
        except FileNotFoundError:
            pass
        except OSError as error:
            cleanup_errors.append(f"redirected worktree unlink failed: {error}")
        registry_during = run_git(root, ["worktree", "list", "--porcelain"], check=False)
        if registry_during.returncode:
            cleanup_errors.append("cannot inspect worktree registry")
        elif f"worktree {worktree.absolute()}\n".encode() in registry_during.stdout:
            if redirected_root:
                prune = run_git(
                    root, ["worktree", "prune", "--expire", "now"], check=False
                )
                if prune.returncode:
                    cleanup_errors.append("git worktree prune failed")
            else:
                removal = run_git(
                    root,
                    ["worktree", "remove", "--force", os.fspath(worktree)],
                    check=False,
                )
                if removal.returncode:
                    cleanup_errors.append("git worktree remove failed")
                    try:
                        if worktree.is_symlink():
                            worktree.unlink()
                        elif worktree.exists():
                            shutil.rmtree(worktree)
                    except OSError as error:
                        cleanup_errors.append(
                            f"worktree directory cleanup failed: {error}"
                        )
                    prune = run_git(
                        root, ["worktree", "prune", "--expire", "now"], check=False
                    )
                    if prune.returncode:
                        cleanup_errors.append("git worktree prune failed")
        try:
            if holding.exists():
                shutil.rmtree(holding)
        except OSError as error:
            cleanup_errors.append(f"temporary directory cleanup failed: {error}")
        registry_after = run_git(root, ["worktree", "list", "--porcelain"], check=False)
        if registry_after.returncode or registry_after.stdout != registry_before:
            cleanup_errors.append("worktree registry was not restored")
        try:
            prove_real_index_unchanged(real_index)
        except Gate9Error as error:
            if primary_error is None:
                primary_error = error
            elif not (
                isinstance(primary_error, Gate9Error)
                and primary_error.code == "REAL_INDEX_SCOPE_DRIFT"
            ):
                cleanup_errors.append(str(error))
    if cleanup_errors:
        fail("WORKTREE_CLEANUP_FAILURE", "; ".join(cleanup_errors))
    if primary_error is not None:
        raise primary_error
    if result is None:
        fail("GENERATOR_FAILURE", "projection produced no outputs")
    return result


def assignment_run_id(commit: str, attempt: int, role: str) -> str:
    return sha256_bytes(f"{commit}\0{attempt}\0{role}".encode())


def fixed_evidence_ref(attempt: int, package_sha256: str) -> str:
    return f"{REF_PREFIX}/attempt-{attempt}/{package_sha256}"


def existing_evidence_refs(root: pathlib.Path) -> list[str]:
    result = run_git(
        root,
        ["for-each-ref", "--format=%(refname)", f"{REF_PREFIX}/"],
    )
    return sorted(filter(None, result.stdout.decode().splitlines()))


def derive_attempt(root: pathlib.Path, marker: dict[str, Any]) -> int:
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
        terminal = replay_terminal_evidence_ref(root, evidence_ref)
        terminal_state = terminal["state"]
        package_sha256 = terminal["package_sha256"]
        tree_oid = terminal["tree"]
        reason = terminal["reason"]
        if terminal["attempt"] != 1:
            fail("ATTEMPT_STATE_MISMATCH", "attempt 1 ref identity mismatch")
        expected_attempt_1 = {
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
    root: pathlib.Path, attempt: int, marker: dict[str, Any]
) -> None:
    if attempt == 1:
        return
    if attempt != 2 or marker.get("state") != "ATTEMPT_2_PENDING":
        fail("ATTEMPT_PREHISTORY_INVALID", "package is not a bounded attempt 2")
    attempt_one = marker.get("attempt_1")
    expected_keys = {
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
        terminal = replay_terminal_evidence_ref(root, evidence_ref)
    except Gate9Error as error:
        fail("ATTEMPT_PREHISTORY_INVALID", f"{error.code}: {error.detail}")
    expected_attempt_one = {
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


def ensure_empty_output(path: pathlib.Path) -> None:
    if path.exists():
        if not path.is_dir() or any(path.iterdir()):
            fail("OUTPUT_NOT_EMPTY", os.fspath(path))
    else:
        path.mkdir(parents=True)


def write_package(output: pathlib.Path, payloads: Mapping[str, bytes]) -> str:
    for name, value in payloads.items():
        (output / name).write_bytes(value)
    sums = checksum_manifest(payloads)
    (output / "SHA256SUMS").write_bytes(sums)
    package_id = sha256_bytes(sums)
    for attachment in output.iterdir():
        attachment.chmod(0o444)
    return package_id


def build_package(args: argparse.Namespace) -> None:
    if args.attempt not in (1, 2):
        fail("THIRD_ATTEMPT", f"attempt {args.attempt} is forbidden")
    root = repository_root()
    task_relative, task_path = repo_path(root, args.task)
    spec_relative, spec_path = repo_path(root, args.spec)
    plan_relative, plan_path = repo_path(root, args.plan)
    del spec_relative, plan_relative
    assert_clean_real_index(root)
    assert_task_only_worktree(root, task_relative)
    current_head = head(root)
    before = run_git(root, ["show", f"{current_head}:{task_relative.as_posix()}"]).stdout
    candidate = task_path.read_bytes()
    marker, _ = parse_marker(candidate)
    derived_attempt = derive_attempt(root, marker)
    if args.attempt != derived_attempt:
        fail("ATTEMPT_STATE_MISMATCH", f"derived {derived_attempt}, asserted {args.attempt}")
    old_manifest = tree_manifest(root, current_head, OLD_PACK)
    new_manifest = tree_manifest(root, current_head, NEW_PACK)
    if len(manifest_paths(old_manifest)) != 20 or len(manifest_paths(new_manifest)) != 20:
        fail("PACK_CARDINALITY", "old and new packs must each contain exactly 20 files")
    task_patch, deletion_patch = write_task_patch_and_deletion_patch(
        root, current_head, task_relative, candidate
    )
    projected_index, projected_coverage = projected_generated_outputs(root, current_head)
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
        "llm-wiki-index.md": projected_index,
        "llm-wiki-stage-category-coverage.md": projected_coverage,
        "new-manifest.tsv": new_manifest,
        "old-manifest.tsv": old_manifest,
        "plan.md": plan_path.read_bytes(),
        "proposed-deletion.patch": deletion_patch,
        "spec.md": spec_path.read_bytes(),
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
    output = pathlib.Path(args.output).resolve()
    ensure_empty_output(output)
    package_id = write_package(output, payloads)
    print(canonical_json({"package_sha256": package_id, "state": "BUILT"}).decode(), end="")


def read_checksum_manifest(package: pathlib.Path) -> dict[str, str]:
    raw = (package / "SHA256SUMS").read_bytes()
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


def verify_package_path(
    root: pathlib.Path,
    package: pathlib.Path,
    *,
    require_live_head: bool,
    require_read_only: bool = True,
) -> dict[str, Any]:
    if not package.is_dir():
        fail("MISSING_PACKAGE", os.fspath(package))
    actual_paths = sorted(path.name for path in package.iterdir())
    if actual_paths != sorted(PACKAGE_ATTACHMENTS):
        fail("ATTACHMENT_SET_DRIFT", repr(actual_paths))
    if require_read_only:
        for path in package.iterdir():
            metadata = path.lstat()
            if not stat.S_ISREG(metadata.st_mode):
                fail("ATTACHMENT_TYPE_DRIFT", path.name)
            if stat.S_IMODE(metadata.st_mode) != 0o444:
                fail("ATTACHMENT_MODE_DRIFT", path.name)
    package_doc = load_canonical_json(package / "package.json")
    assignments = load_canonical_json(package / "assignments.json")
    gates = load_canonical_json(package / "gate-results.json")
    checksums = read_checksum_manifest(package)
    expected_checksum_paths = sorted(set(PACKAGE_ATTACHMENTS) - {"SHA256SUMS"})
    if sorted(checksums) != expected_checksum_paths:
        fail("ATTACHMENT_SET_DRIFT", "checksum path set mismatch")
    for name, expected in checksums.items():
        if sha256_bytes((package / name).read_bytes()) != expected:
            fail("CHECKSUM_DRIFT", name)
    package_head = (package / "HEAD.txt").read_text(encoding="ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", package_head):
        fail("INVALID_PACKAGE_HEAD", package_head)
    if run_git(root, ["cat-file", "-e", f"{package_head}^{{commit}}"], check=False).returncode:
        fail("INVALID_PACKAGE_HEAD", package_head)
    if require_live_head and head(root) != package_head:
        fail("STALE_HEAD", f"live HEAD differs from package HEAD {package_head}")
    attempt = package_doc.get("attempt")
    if not nonnegative_int(attempt) or attempt not in (1, 2):
        fail("PACKAGE_SEMANTIC_DRIFT", "invalid package attempt")
    payloads = {
        name: (package / name).read_bytes()
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
    if (package / "HEAD.txt").read_bytes() != f"{package_head}\n".encode():
        fail("PACKAGE_SEMANTIC_DRIFT", "HEAD.txt")
    old_manifest = tree_manifest(root, package_head, OLD_PACK)
    new_manifest = tree_manifest(root, package_head, NEW_PACK)
    if (package / "old-manifest.tsv").read_bytes() != old_manifest:
        fail("PACKAGE_SEMANTIC_DRIFT", "old-manifest.tsv")
    if (package / "new-manifest.tsv").read_bytes() != new_manifest:
        fail("PACKAGE_SEMANTIC_DRIFT", "new-manifest.tsv")
    old_paths = manifest_paths(old_manifest)
    if len(old_paths) != 20 or len(manifest_paths(new_manifest)) != 20:
        fail("PACK_CARDINALITY", "manifest cardinality")
    del old_paths
    task_before = run_git(root, ["show", f"{package_head}:{TASK_PATH.as_posix()}"]).stdout
    candidate = (package / "task-candidate.md").read_bytes()
    candidate_marker, _ = parse_marker(candidate)
    expected_state = "PACKAGE_REVIEW_PENDING" if attempt == 1 else "ATTEMPT_2_PENDING"
    if candidate_marker.get("attempt") != attempt or candidate_marker.get("state") != expected_state:
        fail("PACKAGE_SEMANTIC_DRIFT", "task-candidate.md marker")
    validate_package_prehistory(root, attempt, candidate_marker)
    task_patch, deletion_patch = write_task_patch_and_deletion_patch(
        root, package_head, TASK_PATH, candidate
    )
    semantic_payloads = {
        "task-before.md": task_before,
        "task-before-to-candidate.patch": task_patch,
        "proposed-deletion.patch": deletion_patch,
        "spec.md": run_git(root, ["show", f"{package_head}:{SPEC_PATH.as_posix()}"]).stdout,
        "plan.md": run_git(root, ["show", f"{package_head}:{PLAN_PATH.as_posix()}"]).stdout,
    }
    for name, expected in semantic_payloads.items():
        if (package / name).read_bytes() != expected:
            fail("PACKAGE_SEMANTIC_DRIFT", name)
    tracked_index = run_git(root, ["show", f"{package_head}:{INDEX.as_posix()}"]).stdout
    tracked_coverage = run_git(root, ["show", f"{package_head}:{COVERAGE.as_posix()}"]).stdout
    if (package / "llm-wiki-index.md").read_bytes() != tracked_index:
        fail("PACKAGE_SEMANTIC_DRIFT", INDEX.as_posix())
    if (package / "llm-wiki-stage-category-coverage.md").read_bytes() != tracked_coverage:
        fail("PACKAGE_SEMANTIC_DRIFT", COVERAGE.as_posix())
    return {
        "attempt": attempt,
        "assignments": assignments,
        "head": package_head,
        "package_doc": package_doc,
        "package_sha256": sha256_bytes((package / "SHA256SUMS").read_bytes()),
    }


def verify_package(args: argparse.Namespace) -> None:
    root = repository_root()
    result = verify_package_path(
        root,
        pathlib.Path(args.package).resolve(),
        require_live_head=args.require_live_head,
    )
    print(canonical_json({"package_sha256": result["package_sha256"], "state": "VERIFIED"}).decode(), end="")


def load_attestation(
    package_result: dict[str, Any], attestation_path: pathlib.Path
) -> dict[str, Any]:
    attestation = load_canonical_json(attestation_path)
    expected_keys = {
        "assignments",
        "attempt",
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
        fail("IDENTITY_COLLISION", "reviewers must have distinct agent IDs and task paths")
    return attestation


def verify_assignments(args: argparse.Namespace) -> None:
    root = repository_root()
    package_result = verify_package_path(
        root, pathlib.Path(args.package).resolve(), require_live_head=False
    )
    attestation_path = pathlib.Path(args.attestation).resolve()
    load_attestation(package_result, attestation_path)
    print(
        canonical_json(
            {
                "assignment_attestation_sha256": sha256_bytes(attestation_path.read_bytes()),
                "state": "ASSIGNED",
            }
        ).decode(),
        end="",
    )


def validate_receipt(
    path: pathlib.Path,
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
    package: pathlib.Path,
    package_result: dict[str, Any],
    receipt_paths: Mapping[str, pathlib.Path],
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
        "evidence_ref": fixed_evidence_ref(
            package_result["attempt"], package_result["package_sha256"]
        ),
        "new_manifest_sha256": sha256_bytes((package / "new-manifest.tsv").read_bytes()),
        "old_manifest_sha256": sha256_bytes((package / "old-manifest.tsv").read_bytes()),
        "package_sha256": package_result["package_sha256"],
        "proposed_deletion_patch_sha256": sha256_bytes(
            (package / "proposed-deletion.patch").read_bytes()
        ),
        "recovery_head": package_result["head"],
        "reviews": reviews,
        "schema": SCHEMA,
        "state": "TASK_BACKFILLED",
    }


def validate_task_state(
    package: pathlib.Path,
    package_result: dict[str, Any],
    task_path: pathlib.Path,
    expect_state: str,
    receipt_paths: Mapping[str, pathlib.Path],
    receipts: Mapping[str, dict[str, Any]],
) -> None:
    candidate = (package / "task-candidate.md").read_bytes()
    current = task_path.read_bytes()
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
    root = repository_root()
    package = pathlib.Path(args.package).resolve()
    package_result = verify_package_path(root, package, require_live_head=False)
    attestation_path = pathlib.Path(args.assignment_attestation).resolve()
    attestation = load_attestation(package_result, attestation_path)
    attestation_sha256 = sha256_bytes(attestation_path.read_bytes())
    receipt_paths = {
        "migration-specification": pathlib.Path(args.migration_receipt).resolve(),
        "quality": pathlib.Path(args.quality_receipt).resolve(),
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
    print(canonical_json({"state": args.expect_state}).decode(), end="")


def task_transition_patch(
    root: pathlib.Path,
    before: bytes,
    after: bytes,
    task: pathlib.PurePosixPath,
) -> bytes:
    with tempfile.TemporaryDirectory(prefix="gate9-task-transition-") as temporary:
        environment = {"GIT_INDEX_FILE": os.fspath(pathlib.Path(temporary) / "index")}
        run_git(root, ["read-tree", "--empty"], env=environment)
        before_oid = run_git(
            root, ["hash-object", "-w", "--stdin"], env=environment, input_bytes=before
        ).stdout.decode().strip()
        run_git(
            root,
            ["update-index", "--add", "--cacheinfo", "100644", before_oid, task.as_posix()],
            env=environment,
        )
        before_tree = run_git(root, ["write-tree"], env=environment).stdout.decode().strip()
        after_oid = run_git(
            root, ["hash-object", "-w", "--stdin"], env=environment, input_bytes=after
        ).stdout.decode().strip()
        run_git(
            root,
            ["update-index", "--cacheinfo", "100644", after_oid, task.as_posix()],
            env=environment,
        )
        return run_git(
            root,
            [
                "diff",
                "--cached",
                "--binary",
                "--full-index",
                before_tree,
                "--",
                task.as_posix(),
            ],
            env=environment,
        ).stdout


def file_record(path: str, value: bytes) -> dict[str, object]:
    return {"bytes": len(value), "path": path, "sha256": sha256_bytes(value)}


def blob_record(root: pathlib.Path, value: bytes) -> dict[str, object]:
    oid = run_git(root, ["hash-object", "--stdin"], input_bytes=value).stdout.decode().strip()
    return {"blob_oid": oid, "bytes": len(value), "sha256": sha256_bytes(value)}


def checked_report(path: pathlib.Path, label: str) -> bytes:
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
    path: pathlib.Path,
    report: bytes,
    role: str,
    receipt_path: pathlib.Path,
    receipt: dict[str, Any],
    attestation_sha256: str,
    task_tuple: dict[str, Any],
) -> dict[str, Any]:
    closure = load_canonical_json(path)
    expected_keys = {
        "agent_id",
        "assignment_attestation_sha256",
        "attempt",
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


def write_evidence_tree(root: pathlib.Path, leaves: Mapping[str, bytes]) -> str:
    with tempfile.TemporaryDirectory(prefix="gate9-evidence-index-") as temporary:
        environment = {"GIT_INDEX_FILE": os.fspath(pathlib.Path(temporary) / "index")}
        run_git(root, ["read-tree", "--empty"], env=environment)
        for path in sorted(leaves):
            oid = run_git(
                root,
                ["hash-object", "-w", "--stdin"],
                env=environment,
                input_bytes=leaves[path],
            ).stdout.decode().strip()
            run_git(
                root,
                ["update-index", "--add", "--cacheinfo", "100644", oid, path],
                env=environment,
            )
        return run_git(root, ["write-tree"], env=environment).stdout.decode().strip()


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


def create_or_reuse_ref(
    root: pathlib.Path,
    evidence_ref: str,
    package_head: str,
    tree_oid: str,
    message: bytes,
) -> str:
    existing_result = run_git(root, ["show-ref", "--verify", "--hash", evidence_ref], check=False)
    existing = existing_result.stdout.decode().strip() if existing_result.returncode == 0 else ""
    desired_identity = (package_head, tree_oid, message)

    def matches(commit: str) -> bool:
        try:
            return commit_identity(root, commit) == desired_identity
        except Gate9Error:
            return False

    if existing:
        if matches(existing):
            return existing
        fail("FOREIGN_REF", evidence_ref)
    commit = run_git(
        root,
        ["commit-tree", tree_oid, "-p", package_head],
        input_bytes=message,
    ).stdout.decode().strip()
    update = run_git(
        root,
        ["update-ref", evidence_ref, commit, "0" * 40],
        check=False,
    )
    if update.returncode == 0:
        return commit
    raced = run_git(root, ["show-ref", "--verify", "--hash", evidence_ref], check=False)
    raced_commit = raced.stdout.decode().strip() if raced.returncode == 0 else ""
    if raced_commit and matches(raced_commit):
        return raced_commit
    fail("FOREIGN_REF", evidence_ref)


def build_evidence_leaves(
    root: pathlib.Path,
    package: pathlib.Path,
    package_result: dict[str, Any],
    task_relative: pathlib.PurePosixPath,
    task_path: pathlib.Path,
    state: str,
    terminal_report_path: pathlib.Path,
    attestation_path: pathlib.Path,
    optional_paths: Mapping[str, pathlib.Path | None],
) -> dict[str, bytes]:
    attestation = load_attestation(package_result, attestation_path)
    attestation_bytes = attestation_path.read_bytes()
    attestation_sha256 = sha256_bytes(attestation_bytes)
    leaves = {
        f"package/{name}": (package / name).read_bytes() for name in PACKAGE_ATTACHMENTS
    }
    leaves["assignment-attestation.json"] = attestation_bytes
    terminal_report = checked_report(terminal_report_path, "terminal report")
    leaves["terminal/report.md"] = terminal_report
    candidate = (package / "task-candidate.md").read_bytes()
    task_after = task_path.read_bytes() if state == "AUTHORIZED" else candidate
    task_patch = task_transition_patch(root, candidate, task_after, task_relative) if state == "AUTHORIZED" else b""
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
            fail("INVALIDATED_REASON_INVALID", os.fspath(drift_path))
        if set(drift_value) != {"kind", "reason", "schema", "state"} or (
            drift_value.get("kind") != "drift-proof"
            or drift_value.get("state") != "INVALIDATED"
        ):
            fail("INVALID_DRIFT_PROOF", os.fspath(drift_path))
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
    root = repository_root()
    package = pathlib.Path(args.package).resolve()
    package_result = verify_package_path(root, package, require_live_head=False)
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
        name: pathlib.Path(getattr(args, name)).resolve() if getattr(args, name) else None
        for name in optional_names
    }
    leaves = build_evidence_leaves(
        root,
        package,
        package_result,
        task_relative,
        task_path,
        args.terminal_state,
        pathlib.Path(args.terminal_report).resolve(),
        pathlib.Path(args.assignment_attestation).resolve(),
        optional_paths,
    )
    if set(leaves) != EVIDENCE_LEAF_PATHS:
        fail(
            "EVIDENCE_PATH_SET_DRIFT",
            repr(sorted(set(leaves) ^ EVIDENCE_LEAF_PATHS)),
        )
    tree_oid = write_evidence_tree(root, leaves)
    message = evidence_commit_message(
        package_result["attempt"], package_result["package_sha256"], args.terminal_state
    )
    evidence_commit = create_or_reuse_ref(
        root, evidence_ref, package_result["head"], tree_oid, message
    )
    print(
        canonical_json(
            {
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
    if not isinstance(marker_ref, str) or not marker_ref.startswith(f"{REF_PREFIX}/attempt-"):
        fail("INVALID_TASK_MARKER", "missing fixed evidence ref")
    if requested != "auto" and requested != marker_ref:
        fail("EVIDENCE_REF_MISMATCH", requested)
    return marker_ref


def read_ref_leaves(
    root: pathlib.Path, evidence_ref: str
) -> tuple[str, dict[str, bytes]]:
    ref_result = run_git(
        root, ["show-ref", "--verify", "--hash", evidence_ref], check=False
    )
    if ref_result.returncode:
        fail("MISSING_EVIDENCE_REF", evidence_ref)
    commit = ref_result.stdout.decode().strip()
    listing = run_git(root, ["ls-tree", "-r", "--full-tree", commit]).stdout
    leaves: dict[str, bytes] = {}
    for line in listing.splitlines():
        metadata, separator, raw_path = line.partition(b"\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            fail("INVALID_EVIDENCE_TREE", line.decode("utf-8", "replace"))
        mode, object_type, _ = fields
        path = raw_path.decode("utf-8")
        if mode != b"100644" or object_type != b"blob":
            fail("EVIDENCE_MODE_DRIFT", path)
        leaves[path] = run_git(root, ["show", f"{commit}:{path}"]).stdout
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
    return commit, leaves


def materialize_evidence(leaves: Mapping[str, bytes], root: pathlib.Path) -> None:
    for relative, value in leaves.items():
        path = root / pathlib.Path(*pathlib.PurePosixPath(relative).parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)
        path.chmod(0o444)


def replay_terminal_evidence_ref(
    root: pathlib.Path, evidence_ref: str
) -> dict[str, object]:
    evidence_commit, leaves = read_ref_leaves(root, evidence_ref)
    with tempfile.TemporaryDirectory(prefix="gate9-terminal-replay-") as temporary:
        evidence_root = pathlib.Path(temporary)
        materialize_evidence(leaves, evidence_root)
        package = evidence_root / "package"
        package_result = verify_package_path(
            root, package, require_live_head=False
        )
        evidence = load_canonical_json(evidence_root / "evidence.json")
        state = evidence.get("state")
        if state not in {"REJECTED", "INVALIDATED"}:
            fail("ATTEMPT_STATE_MISMATCH", "attempt 1 is not pre-backfill terminal")
        expected_ref = fixed_evidence_ref(
            package_result["attempt"], package_result["package_sha256"]
        )
        if evidence_ref != expected_ref:
            fail("EVIDENCE_REF_MISMATCH", evidence_ref)
        optional_paths: dict[str, pathlib.Path | None] = {
            "migration_closure_report": None,
            "migration_closure": None,
            "quality_closure_report": None,
            "quality_closure": None,
            "drift_proof": (
                evidence_root / "drift/drift-proof.json"
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
                optional_paths[f"{prefix}_report"] = evidence_root / f"reviews/{role}/report.md"
                optional_paths[f"{prefix}_receipt"] = evidence_root / receipt_leaf
        reconstructed = build_evidence_leaves(
            root,
            package,
            package_result,
            TASK_PATH,
            evidence_root / "task/task-after.md",
            state,
            evidence_root / "terminal/report.md",
            evidence_root / "assignment-attestation.json",
            optional_paths,
        )
        if reconstructed != leaves:
            fail("EVIDENCE_SCHEMA_DRIFT", evidence_ref)
        expected_tree = write_evidence_tree(root, reconstructed)
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
            drift = load_canonical_json(evidence_root / "drift/drift-proof.json")
            reason = drift["reason"]
        return {
            "attempt": package_result["attempt"],
            "package_sha256": package_result["package_sha256"],
            "reason": reason,
            "state": state,
            "tree": tree_oid,
        }


def verify_authorized(args: argparse.Namespace) -> None:
    root = repository_root()
    task_relative, task_path = repo_path(root, args.task)
    live_task = task_path.read_bytes()
    task_marker, _ = parse_marker(live_task)
    evidence_ref = resolve_evidence_ref(task_marker, args.evidence_ref)
    evidence_commit, leaves = read_ref_leaves(root, evidence_ref)
    with tempfile.TemporaryDirectory(prefix="gate9-ref-replay-") as temporary:
        evidence_root = pathlib.Path(temporary)
        materialize_evidence(leaves, evidence_root)
        package = evidence_root / "package"
        package_result = verify_package_path(
            root, package, require_live_head=args.require_live_head
        )
        if args.package:
            external_package = pathlib.Path(args.package).resolve()
            external_result = verify_package_path(
                root, external_package, require_live_head=args.require_live_head
            )
            if external_result["package_sha256"] != package_result["package_sha256"]:
                fail("PACKAGE_ID_DRIFT", os.fspath(external_package))
            for name in PACKAGE_ATTACHMENTS:
                if (external_package / name).read_bytes() != (package / name).read_bytes():
                    fail("PACKAGE_ATTACHMENT_DRIFT", name)
        evidence = load_canonical_json(evidence_root / "evidence.json")
        expected_evidence_keys = {
            "assignment",
            "attempt",
            "closures",
            "drift",
            "evidence_ref",
            "package_head",
            "package_sha256",
            "reviews",
            "schema",
            "state",
            "task",
            "terminal_report",
        }
        if set(evidence) != expected_evidence_keys or evidence.get("state") != "AUTHORIZED":
            fail("NOT_AUTHORIZED", evidence_ref)
        if (
            evidence.get("attempt") != package_result["attempt"]
            or evidence.get("package_head") != package_result["head"]
            or evidence.get("package_sha256") != package_result["package_sha256"]
            or evidence.get("evidence_ref") != evidence_ref
        ):
            fail("EVIDENCE_BINDING_DRIFT", evidence_ref)
        expected_message = evidence_commit_message(
            package_result["attempt"], package_result["package_sha256"], "AUTHORIZED"
        )
        commit_parent, commit_tree, commit_message = commit_identity(root, evidence_commit)
        expected_tree = write_evidence_tree(root, leaves)
        if (
            commit_parent != package_result["head"]
            or commit_tree != expected_tree
            or commit_message != expected_message
        ):
            fail("EVIDENCE_COMMIT_IDENTITY_DRIFT", evidence_ref)
        if live_task != leaves["task/task-after.md"]:
            fail("TASK_AFTER_DRIFT", task_relative.as_posix())
        candidate = leaves["package/task-candidate.md"]
        expected_task_patch = task_transition_patch(root, candidate, live_task, task_relative)
        if leaves["task/task-candidate-to-after.patch"] != expected_task_patch:
            fail("TASK_PATCH_DRIFT", task_relative.as_posix())
        attestation_path = evidence_root / "assignment-attestation.json"
        attestation = load_attestation(package_result, attestation_path)
        attestation_sha256 = sha256_bytes(attestation_path.read_bytes())
        receipt_paths = {
            role: evidence_root / f"reviews/{role}/receipt.json" for role in ROLES
        }
        receipts: dict[str, dict[str, Any]] = {}
        review_records: dict[str, dict[str, Any]] = {}
        for role in ROLES:
            report_path = f"reviews/{role}/report.md"
            receipt_leaf = f"reviews/{role}/receipt.json"
            report = checked_report(evidence_root / report_path, f"{role} review")
            receipt = validate_receipt(
                receipt_paths[role],
                role,
                package_result,
                attestation,
                attestation_sha256,
                require_approved=True,
            )
            validate_report_binding(receipt, report, role)
            receipts[role] = receipt
            review_records[role] = {
                **{
                    key: receipt[key]
                    for key in (
                        "agent_id",
                        "assignment_attestation_sha256",
                        "role",
                        "run_id",
                        "task_path",
                        "verdict",
                        "findings",
                    )
                },
                "receipt": file_record(receipt_leaf, leaves[receipt_leaf]),
                "report": file_record(report_path, report),
            }
        validate_task_state(
            package,
            package_result,
            task_path,
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
                evidence_root / closure_report_path, f"{role} closure"
            )
            closure = validate_closure(
                evidence_root / closure_leaf,
                closure_report,
                role,
                receipt_paths[role],
                receipts[role],
                attestation_sha256,
                task_tuple,
            )
            closure_records[role] = {
                **{
                    key: closure[key]
                    for key in (
                        "agent_id",
                        "role",
                        "run_id",
                        "task_path",
                        "verdict",
                        "findings",
                    )
                },
                "closure": file_record(closure_leaf, leaves[closure_leaf]),
                "report": file_record(closure_report_path, closure_report),
            }
        drift = load_canonical_json(evidence_root / "drift/drift-proof.json")
        if drift != {
            "kind": "drift-proof",
            "schema": SCHEMA,
            "state": "NOT_APPLICABLE",
        }:
            fail("INVALID_DRIFT_PROOF", "AUTHORIZED drift slot")
        terminal_report = checked_report(
            evidence_root / "terminal/report.md", "terminal report"
        )
        expected_evidence = {
            "assignment": file_record(
                "assignment-attestation.json", leaves["assignment-attestation.json"]
            ),
            "attempt": package_result["attempt"],
            "closures": closure_records,
            "drift": file_record(
                "drift/drift-proof.json", leaves["drift/drift-proof.json"]
            ),
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
    if args.require_live_head and head(root) != package_result["head"]:
        fail("STALE_HEAD", package_result["head"])
    print(
        canonical_json(
            {
                "evidence_commit": evidence_commit,
                "evidence_ref": evidence_ref,
                "state": "AUTHORIZED",
            }
        ).decode(),
        end="",
    )


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    build = subparsers.add_parser("build-package")
    build.add_argument("--attempt", type=int, required=True)
    build.add_argument("--output", required=True)
    build.add_argument("--spec", required=True)
    build.add_argument("--plan", required=True)
    build.add_argument("--task", required=True)
    verify = subparsers.add_parser("verify-package")
    verify.add_argument("--package", required=True)
    verify.add_argument("--require-live-head", action="store_true")
    assignments = subparsers.add_parser("verify-assignments")
    assignments.add_argument("--package", required=True)
    assignments.add_argument("--attestation", required=True)
    backfill = subparsers.add_parser("verify-backfill")
    backfill.add_argument("--package", required=True)
    backfill.add_argument("--migration-receipt", required=True)
    backfill.add_argument("--quality-receipt", required=True)
    backfill.add_argument("--assignment-attestation", required=True)
    backfill.add_argument("--task", required=True)
    backfill.add_argument(
        "--expect-state", choices=("PACKAGE_REVIEWED", "TASK_BACKFILLED"), required=True
    )
    publish = subparsers.add_parser("publish-evidence-ref")
    publish.add_argument("--package", required=True)
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
    authorized = subparsers.add_parser("verify-authorized")
    package_source = authorized.add_mutually_exclusive_group(required=True)
    package_source.add_argument("--package")
    package_source.add_argument("--package-from-ref", action="store_true")
    authorized.add_argument("--task", required=True)
    authorized.add_argument("--evidence-ref", required=True)
    authorized.add_argument("--require-live-head", action="store_true")
    authorized.add_argument("--require-clean-real-index", action="store_true")
    authorized.add_argument("--require-task-only-worktree", action="store_true")
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    try:
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
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
