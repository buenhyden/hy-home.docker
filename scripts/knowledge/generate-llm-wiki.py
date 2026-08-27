#!/usr/bin/env python3
"""Generate or check both tracked LLM Wiki reference outputs."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import errno
import fcntl
import hashlib
import hmac
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import selectors
import signal
import stat
import subprocess
import sys
import time
from typing import Mapping, Sequence


INDEX_OUTPUT = Path("docs/90.references/data/0082-llm-wiki-index/README.md")
COVERAGE_OUTPUT = Path("docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md")
GENERATOR_PATH = "scripts/knowledge/generate-llm-wiki.py"
ROOT_ENTRYPOINTS = frozenset(
    {
        ".env.example",
        ".pre-commit-config.yaml",
        "AGENTS.md",
        "CLAUDE.md",
        "AGENTS.md",
        "README.md",
        "RTK.md",
        "docker-compose.yml",
        "llms.txt",
    }
)
REQUIRED_LOCAL_PATHS = frozenset(
    {GENERATOR_PATH}
)
RETIRED_GENERATOR_WRAPPERS = frozenset(
    {
        "scripts/knowledge/generate-llm-wiki-index.sh",
        "scripts/knowledge/generate-llm-wiki-coverage.sh",
    }
)
SAFE_SUFFIXES = frozenset({".conf", ".env", ".graphql", ".json", ".md", ".proto", ".sh", ".toml", ".txt", ".yaml", ".yml"})
# Deletion-invariance for the Spec 137 retirement. The retiring research pack is
# excluded by exact trailing-slash prefix so this generated navigation surface
# carries no reference to it either before or after deletion. Ported on
# 2026-08-19 from scripts/knowledge/generate-llm-wiki-index.sh, which owned this
# property while it was the canonical generator. Measured before the port: a
# regeneration without it injects 20 clickable retiring-pack links into the
# index and gate 4's hard clickable_links=0 fails.
RETIRING_PACK_PREFIX = "docs/90.references/research/0001-agentic-research-pack-refresh/"
ARCHIVE_NONCURRENT_PREFIXES = (
    "docs/98.archive/changes/",
    "docs/98.archive/tombstones/",
)
EXCLUDED_PREFIXES = (
    ".git/",
    "graphify-out/",
    "node_modules/",
    "projects/storybook/nextjs/.next/",
    "projects/storybook/nextjs/node_modules/",
    "volumes/",
    RETIRING_PACK_PREFIX,
    *ARCHIVE_NONCURRENT_PREFIXES,
)
EXCLUDED_PARTS = frozenset({".cache", ".next", "coverage", "dist", "node_modules", "vendor"})
GENERATED_OR_LOCK_FILES = (".min.css", ".min.js", "package-lock.json", "pnpm-lock.yaml", "yarn.lock")
CATEGORY_ORDER = (
    "Root entrypoints",
    "LLM Wiki reference",
    "Agent governance",
    "Runtime surfaces",
    "Active stage docs",
    "Operations docs",
    "Reference and template docs",
    "Infrastructure source",
    "Scripts and validators",
    "GitHub workflow surface",
    "Secret-handling policy",
    "Other tracked source",
)
MANIFEST_ENV_NAMES = (
    "GATE9_LLM_MANIFEST_FD",
    "GATE9_LLM_MANIFEST_SIZE",
    "GATE9_LLM_MANIFEST_SHA256",
)
MANIFEST_SCHEMA = b"schema=agentic-research-llm-wiki-manifest/v1"
MAX_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_TRACKED_PATHS = 10_000
MAX_GIT_SECONDS = 30.0
MAX_GIT_STDOUT_BYTES = 10_000_000
MAX_GIT_STDERR_BYTES = 1_000_000
MAX_GIT_TOTAL_BYTES = 11_000_000
MAX_CANDIDATE_FILE_BYTES = 10_000_000
MAX_CANDIDATE_TOTAL_BYTES = 300_000_000
MAX_OUTPUT_BYTES = 10_000_000
REQUIRED_SEALS = (
    fcntl.F_SEAL_SEAL
    | fcntl.F_SEAL_SHRINK
    | fcntl.F_SEAL_GROW
    | fcntl.F_SEAL_WRITE
)


class GeneratorError(RuntimeError):
    """Fail-closed generator boundary violation."""


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: bytes
    stderr: bytes


@dataclass(frozen=True, order=True)
class Candidate:
    path: str
    category: str
    bucket: str
    role: str


def _kill_and_reap(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            try:
                process.kill()
            except OSError:
                pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            pass
        process.wait()


def _run_git_bounded(
    repo_root: Path,
    arguments: Sequence[str],
    *,
    timeout_seconds: float = MAX_GIT_SECONDS,
    max_stdout: int = MAX_GIT_STDOUT_BYTES,
    max_stderr: int = MAX_GIT_STDERR_BYTES,
    max_total: int = MAX_GIT_TOTAL_BYTES,
) -> GitResult:
    """Run Git with a deadline, concurrent bounded drains, and group cleanup."""

    if not arguments or any(not isinstance(item, str) or "\0" in item for item in arguments):
        raise GeneratorError("git arguments must be nonempty text")
    if min(timeout_seconds, max_stdout, max_stderr, max_total) <= 0:
        raise GeneratorError("git bounds must be positive")
    deadline_seconds = min(float(timeout_seconds), MAX_GIT_SECONDS)
    stdout_limit = min(max_stdout, MAX_GIT_STDOUT_BYTES)
    stderr_limit = min(max_stderr, MAX_GIT_STDERR_BYTES)
    total_limit = min(max_total, MAX_GIT_TOTAL_BYTES)
    try:
        process = subprocess.Popen(
            ["git", *arguments],
            cwd=repo_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            close_fds=True,
        )
    except OSError as error:
        raise GeneratorError(f"git start failed: {error}") from error
    assert process.stdout is not None and process.stderr is not None
    streams = {
        process.stdout: ("stdout", stdout_limit),
        process.stderr: ("stderr", stderr_limit),
    }
    output = {"stdout": bytearray(), "stderr": bytearray()}
    selector = selectors.DefaultSelector()
    failure: GeneratorError | None = None
    started = time.monotonic()
    try:
        for stream in streams:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline_seconds - (time.monotonic() - started)
            if remaining <= 0:
                failure = GeneratorError("git deadline exceeded")
                break
            for key, _ in selector.select(min(remaining, 0.1)):
                stream = key.fileobj
                label, limit = streams[stream]
                try:
                    chunk = os.read(stream.fileno(), 65_536)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(stream)
                    stream.close()
                    continue
                output[label].extend(chunk)
                if len(output[label]) > limit:
                    failure = GeneratorError(f"git {label} bound exceeded")
                    break
                if len(output["stdout"]) + len(output["stderr"]) > total_limit:
                    failure = GeneratorError("git total output bound exceeded")
                    break
            if failure is not None:
                break
        if failure is not None:
            _kill_and_reap(process)
            raise failure
        remaining = deadline_seconds - (time.monotonic() - started)
        if remaining <= 0:
            _kill_and_reap(process)
            raise GeneratorError("git deadline exceeded")
        try:
            returncode = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            _kill_and_reap(process)
            raise GeneratorError("git deadline exceeded") from error
        return GitResult(returncode, bytes(output["stdout"]), bytes(output["stderr"]))
    finally:
        for stream in streams:
            try:
                selector.unregister(stream)
            except (KeyError, ValueError):
                pass
            if not stream.closed:
                stream.close()
        selector.close()
        if process.poll() is None:
            _kill_and_reap(process)


def _validate_relative_path(path_text: str) -> str:
    if (
        not path_text
        or path_text.startswith("/")
        or path_text.endswith("/")
        or "\\" in path_text
        or any(ord(character) < 0x20 or ord(character) == 0x7F for character in path_text)
    ):
        raise GeneratorError(f"unsafe tracked path: {path_text!r}")
    if any(part in {"", ".", ".."} for part in path_text.split("/")):
        raise GeneratorError(f"unsafe tracked path component: {path_text!r}")
    return path_text


def _git_ls_files(repo_root: Path) -> set[str]:
    result = _run_git_bounded(repo_root, ["ls-files", "--cached", "-z"])
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise GeneratorError(f"git ls-files failed: {detail or result.returncode}")
    if result.stdout and not result.stdout.endswith(b"\0"):
        raise GeneratorError("git ls-files returned a non-NUL-terminated inventory")
    records = result.stdout.split(b"\0")
    if records and records[-1] == b"":
        records.pop()
    if len(records) > MAX_TRACKED_PATHS:
        raise GeneratorError("tracked path count bound exceeded")
    paths: list[str] = []
    for raw in records:
        try:
            path_text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise GeneratorError("tracked path is not strict UTF-8") from error
        paths.append(_validate_relative_path(path_text))
    if len(paths) != len(set(paths)):
        raise GeneratorError("tracked inventory contains duplicate paths")
    return set(paths)


def _open_parent_no_follow(path: Path, *, create: bool = False) -> tuple[int, str]:
    path = Path(os.path.abspath(path))
    parts = path.parts
    if len(parts) < 2 or any(part in {"", ".", ".."} for part in parts[1:]):
        raise GeneratorError(f"unsafe filesystem path: {path}")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(parts[0], flags)
    try:
        for part in parts[1:-1]:
            try:
                before = os.stat(part, dir_fd=descriptor, follow_symlinks=False)
            except FileNotFoundError:
                if not create:
                    raise GeneratorError(f"file is missing: {path}")
                os.mkdir(part, 0o755, dir_fd=descriptor)
                before = os.stat(part, dir_fd=descriptor, follow_symlinks=False)
            if stat.S_ISLNK(before.st_mode):
                raise GeneratorError(f"symlink parent is not allowed: {path}")
            if not stat.S_ISDIR(before.st_mode):
                raise GeneratorError(f"non-directory parent is not allowed: {path}")
            next_descriptor = os.open(part, flags, dir_fd=descriptor)
            opened = os.fstat(next_descriptor)
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                os.close(next_descriptor)
                raise GeneratorError(f"parent changed during open: {path}")
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor, parts[-1]
    except Exception:
        os.close(descriptor)
        raise


def _read_bounded_regular_path(path: Path, *, max_bytes: int) -> bytes:
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1:
        raise GeneratorError("file bound must be a positive integer")
    parent_descriptor, name = _open_parent_no_follow(path)
    descriptor: int | None = None
    try:
        before_path = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        if stat.S_ISLNK(before_path.st_mode):
            raise GeneratorError(f"symlink file is not allowed: {path}")
        if not stat.S_ISREG(before_path.st_mode):
            raise GeneratorError(f"file is not regular: {path}")
        if before_path.st_size > max_bytes:
            raise GeneratorError(f"file size bound exceeded: {path}")
        descriptor = os.open(
            name,
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_NONBLOCK", 0),
            dir_fd=parent_descriptor,
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or (before_path.st_dev, before_path.st_ino) != (before.st_dev, before.st_ino)
        ):
            raise GeneratorError(f"file changed before read: {path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65_536, max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise GeneratorError(f"file read bound exceeded: {path}")
        after = os.fstat(descriptor)
        after_path = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        identity = (before.st_dev, before.st_ino)
        if (
            identity != (after.st_dev, after.st_ino)
            or identity != (after_path.st_dev, after_path.st_ino)
            or before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):
            raise GeneratorError(f"file changed during read: {path}")
        if total != before.st_size:
            raise GeneratorError(f"premature EOF while reading file: {path}")
        return b"".join(chunks)
    except FileNotFoundError as error:
        raise GeneratorError(f"file is missing: {path}") from error
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise GeneratorError(f"symlink file is not allowed: {path}") from error
        raise GeneratorError(f"file cannot be read safely: {path}: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_descriptor)


def is_safe_candidate(path_text: str) -> bool:
    if path_text in RETIRED_GENERATOR_WRAPPERS:
        return False
    if any(path_text.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    if path_text.startswith("secrets/") and path_text != "secrets/README.md":
        return False
    if path_text.endswith(GENERATED_OR_LOCK_FILES):
        return False
    path = PurePosixPath(path_text)
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if path.name.startswith(".") and path_text not in ROOT_ENTRYPOINTS:
        return path_text.startswith((".claude/", ".codex/", ".github/"))
    if path.suffix and path.suffix not in SAFE_SUFFIXES:
        return False
    return path_text in ROOT_ENTRYPOINTS or path_text.startswith((".claude/", ".codex/", ".github/", "docs/", "infra/", "scripts/")) or path_text == "secrets/README.md"


def classify(path_text: str) -> str:
    if path_text in ROOT_ENTRYPOINTS:
        return "Root entrypoints"
    if path_text.startswith((
        "docs/90.references/data/0082-llm-wiki-index/",
        "docs/90.references/data/0083-repository-map/",
    )) or path_text == "llms.txt":
        return "LLM Wiki reference"
    if path_text.startswith("docs/00.agent-governance/"):
        return "Agent governance"
    if path_text.startswith((".claude/", ".codex/")):
        return "Runtime surfaces"
    if path_text.startswith("docs/05.operations/"):
        return "Operations docs"
    if path_text.startswith(("docs/01.requirements/", "docs/02.architecture/", "docs/03.specs/", "docs/04.execution/")):
        return "Active stage docs"
    if path_text.startswith(("docs/90.references/", "docs/99.templates/")) or path_text == "docs/README.md":
        return "Reference and template docs"
    if path_text.startswith("infra/"):
        return "Infrastructure source"
    if path_text.startswith("scripts/"):
        return "Scripts and validators"
    if path_text.startswith(".github/"):
        return "GitHub workflow surface"
    if path_text == "secrets/README.md":
        return "Secret-handling policy"
    return "Other tracked source"


def source_bucket(path_text: str) -> str:
    if path_text in ROOT_ENTRYPOINTS:
        return "root"
    parts = PurePosixPath(path_text).parts
    if path_text.startswith("docs/") and len(parts) >= 2:
        return f"docs/{parts[1]}"
    return parts[0]


def role_for(path_text: str) -> str:
    name = PurePosixPath(path_text).name
    if name == "README.md":
        return "folder index"
    if path_text.endswith((".py", ".sh")):
        return "script"
    if path_text.endswith((".yml", ".yaml")):
        return "YAML config"
    if path_text.endswith(".json"):
        return "JSON registry"
    if path_text.endswith(".md"):
        return "Markdown reference"
    if path_text.endswith(".txt"):
        return "text entrypoint"
    return "source path"


def collect_candidates(repo_root: Path) -> list[Candidate]:
    """Select and classify safe paths exactly once for both outputs."""

    tracked = _git_ls_files(repo_root)
    selected = {path for path in tracked if is_safe_candidate(path)}
    selected.update(REQUIRED_LOCAL_PATHS)
    aggregate_bytes = 0
    safe_paths: list[str] = []
    for relative in sorted(selected):
        _validate_relative_path(relative)
        try:
            payload = _read_bounded_regular_path(
                repo_root / relative,
                max_bytes=MAX_CANDIDATE_FILE_BYTES,
            )
        except GeneratorError as error:
            if "missing" in str(error):
                continue
            raise
        aggregate_bytes += len(payload)
        if aggregate_bytes > MAX_CANDIDATE_TOTAL_BYTES:
            raise GeneratorError("candidate aggregate byte bound exceeded")
        safe_paths.append(relative)
    return [Candidate(path, classify(path), source_bucket(path), role_for(path)) for path in safe_paths]


def candidates_from_manifest(paths: Sequence[str]) -> list[Candidate]:
    """Project a sealed path inventory without consulting the mutable worktree."""

    if len(paths) > MAX_TRACKED_PATHS:
        raise GeneratorError("manifest path count bound exceeded")
    unique = sorted(set(paths))
    if len(unique) != len(paths):
        raise GeneratorError("manifest paths must be unique")
    return [
        Candidate(path, classify(path), source_bucket(path), role_for(path))
        for path in unique
        if path == GENERATOR_PATH or is_safe_candidate(_validate_relative_path(path))
    ]


def _link(path_text: str, output: Path) -> str:
    return f"[{path_text}]({os.path.relpath(path_text, output.parent)})"


def render_index(candidates: Sequence[Candidate]) -> str:
    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        if candidate.path == INDEX_OUTPUT.as_posix():
            continue
        grouped[candidate.category].append(candidate)
    lines = [
        "---", "profile_id: data", "status: active", "artifact_id: DATA-0082", "artifact_type: data", "parent_ids: []", "created: 2026-08-19", "updated: 2026-08-23", "observed_at: 2026-08-23", f"generated_by: {GENERATOR_PATH}", "---", "",
        "# LLM Wiki Generated Index", "", "## Purpose", "",
        "이 문서는 `hy-home.docker`의 LLM Wiki가 사용하는 generated tracked repo-local index다. LLM 에이전트가 먼저 확인할 수 있는 안전한 경로 목록을 제공하되, 각 파일의 내용이나 runtime truth를 복제하지 않는다.", "",
        "Provide a deterministic path index for repo-local AI agents without creating a public site, a full-content bundle, or a replacement for canonical source files.", "",
        "## Schema", "", "Each inventory row contains a repository-relative path and a lightweight role derived from the tracked file name or suffix.", "",
        "## Provenance", "", "This generated tracked repo-local index complements `llms.txt` and the DATA-0083 repository map. Runtime truth remains in `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.", "",
        "Graphify output is advisory navigation context only. This index is generated from repository path metadata and does not treat `graphify-out/` as source material.", "",
        "### In Scope", "", "- Repo-relative path links for safe tracked source entrypoints.", "- Governance, runtime, documentation, infrastructure, script, and secret-handling policy surfaces.", f"- Deterministic refresh through `python3 {GENERATOR_PATH} --write`.", "",
        "### Out of Scope", "", "- Public website or public wiki deployment.", "- `llms-full.txt` or any full-content export.", "- External model calls, network publishing, deployment workflow, or Docker runtime behavior.", "- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.", "",
        "## Inventory", "",
    ]
    for category in CATEGORY_ORDER:
        entries = grouped.get(category, [])
        if entries:
            lines.extend([f"### {category}", "", "| Path | Role |", "| --- | --- |"])
            lines.extend(f"| {_link(item.path, INDEX_OUTPUT)} | {item.role} |" for item in entries)
            lines.append("")
    lines.extend([
        "## Refresh", "", "- **Owner**: `doc-writer` using the `knowledge-map-agent` function", "- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change", f"- **Update Trigger**: Run `python3 {GENERATOR_PATH} --write` after in-scope path changes and `python3 {GENERATOR_PATH} --check` during validation", "",
        "## Consumers", "", "`llms.txt`, repository readers, documentation validators, and AI agents consume this package as navigation evidence only.", "",
        "## Traceability", "", "- [llms.txt](../../../../llms.txt) - root LLM entrypoint and boundary statement", "- [LLM Wiki repository map](../0083-repository-map/README.md)", f"- [generate-llm-wiki.py](../../../../{GENERATOR_PATH})", "- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)", "- [Agent governance hub](../../../00.agent-governance/README.md)",
    ])
    return "\n".join(lines) + "\n"


def _examples(items: Sequence[Candidate], output: Path, limit: int = 3) -> str:
    return "<br>".join(_link(item.path, output) for item in sorted(items)[:limit])


def render_coverage(candidates: Sequence[Candidate]) -> str:
    categories: dict[str, list[Candidate]] = defaultdict(list)
    buckets: dict[str, list[Candidate]] = defaultdict(list)
    roles: dict[str, list[Candidate]] = defaultdict(list)
    selected = [
        candidate
        for candidate in candidates
        if candidate.path not in {INDEX_OUTPUT.as_posix(), COVERAGE_OUTPUT.as_posix()}
    ]
    for candidate in selected:
        categories[candidate.category].append(candidate)
        buckets[candidate.bucket].append(candidate)
        roles[candidate.role].append(candidate)
    lines = [
        "---", "profile_id: data", "status: active", "artifact_id: DATA-0076", "artifact_type: data", "parent_ids: []", "created: 2026-08-19", "updated: 2026-08-23", "observed_at: 2026-08-23", f"generated_by: {GENERATOR_PATH}", "---", "",
        "# LLM Wiki Stage Category Coverage", "", "## Purpose", "", "This generated reference summarizes the safe tracked source paths that feed the repo-local LLM Wiki index by source bucket, LLM Wiki category, and path role.", "", "Provide audit consumers with a compact coverage snapshot without duplicating the full generated index or changing canonical source ownership.", "",
        "## Schema", "", "Counts are grouped by source bucket, navigation category, and derived path role, with representative repository-relative links.", "",
        "## Provenance", "", "This package is generated from the same safe tracked candidate set as DATA-0082. Runtime truth remains in canonical tracked sources.", "",
        "### In Scope", "", "- Counts by source bucket, LLM Wiki category, and path role.", "- Representative links for each category.", f"- Deterministic freshness through `python3 {GENERATOR_PATH} --check`.", "",
        "### Out of Scope", "", "- Full-content export or public website generation.", "- Runtime behavior, deployment workflow, network publishing, or external model calls.", "- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.", "",
        "## Inventory", "", f"- Safe tracked source paths: `{len(selected)}`", f"- Source buckets: `{len(buckets)}`", f"- LLM Wiki categories: `{len(categories)}`", f"- Path roles: `{len(roles)}`", "",
        "## Source Bucket Coverage", "", "| Source Bucket | Paths | Representative Paths |", "| --- | ---: | --- |",
    ]
    lines.extend(f"| `{bucket}` | {len(items)} | {_examples(items, COVERAGE_OUTPUT)} |" for bucket, items in sorted(buckets.items()))
    lines.extend(["", "## LLM Wiki Category Coverage", "", "| Category | Paths | Representative Paths |", "| --- | ---: | --- |"])
    for category in CATEGORY_ORDER:
        if categories.get(category):
            lines.append(f"| {category} | {len(categories[category])} | {_examples(categories[category], COVERAGE_OUTPUT)} |")
    lines.extend(["", "## Path Role Coverage", "", "| Role | Paths |", "| --- | ---: |"])
    lines.extend(f"| {role} | {len(items)} |" for role, items in sorted(roles.items()))
    lines.extend([
        "", "## Refresh", "", "- **Owner**: `doc-writer` using the `knowledge-map-agent` function.", "- **Review Cadence**: Review after root entrypoint, governance, operations, script inventory, infrastructure index, or LLM Wiki path changes.", f"- **Update Trigger**: Run `python3 {GENERATOR_PATH} --write` after in-scope path changes and `python3 {GENERATOR_PATH} --check` during validation.", "",
        "## Consumers", "", "Audit tooling, documentation validators, and AI agents consume this package as coverage evidence only.", "",
        "## Traceability", "", "- [LLM Wiki generated index](../0082-llm-wiki-index/README.md)", "- [LLM Wiki repository map](../0083-repository-map/README.md)", f"- [generate-llm-wiki.py](../../../../{GENERATOR_PATH})", "- [Reference data](../README.md)", "- [Reference index](../../README.md)", "- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)",
    ])
    return "\n".join(lines) + "\n"


def build_outputs_from_candidates(candidates: Sequence[Candidate]) -> dict[Path, str]:
    return {
        INDEX_OUTPUT: render_index(candidates),
        COVERAGE_OUTPUT: render_coverage(candidates),
    }


def build_outputs(repo_root: Path) -> dict[Path, str]:
    return build_outputs_from_candidates(collect_candidates(repo_root))


def check_outputs(outputs: Mapping[Path, str]) -> int:
    stale = False
    for path, expected in outputs.items():
        try:
            current = _read_bounded_regular_path(path, max_bytes=MAX_OUTPUT_BYTES).decode(
                "utf-8", errors="strict"
            )
        except GeneratorError as error:
            if "missing" not in str(error):
                raise
            print(f"FAIL: missing generated LLM Wiki output: {path}", file=sys.stderr)
            stale = True
            continue
        except UnicodeDecodeError as error:
            raise GeneratorError(f"generated output is not strict UTF-8: {path}") from error
        if current != expected:
            print(f"FAIL: stale generated LLM Wiki output: {path}", file=sys.stderr)
            stale = True
    if stale:
        print(f"Run: python3 {GENERATOR_PATH} --write", file=sys.stderr)
        return 1
    print("PASS: both generated LLM Wiki outputs are fresh")
    return 0


def _atomic_write_regular(path: Path, content: str) -> None:
    payload = content.encode("utf-8")
    if len(payload) > MAX_OUTPUT_BYTES:
        raise GeneratorError(f"generated output exceeds byte bound: {path}")
    parent_descriptor, name = _open_parent_no_follow(path, create=True)
    temporary_name: str | None = None
    descriptor: int | None = None
    try:
        try:
            previous = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            previous = None
        if previous is not None:
            if stat.S_ISLNK(previous.st_mode):
                raise GeneratorError(f"symlink output is not allowed: {path}")
            if not stat.S_ISREG(previous.st_mode):
                raise GeneratorError(f"output is not regular: {path}")
        for _ in range(32):
            candidate = f".{name}.llm-wiki-{secrets.token_hex(8)}.tmp"
            try:
                descriptor = os.open(
                    candidate,
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | getattr(os, "O_CLOEXEC", 0)
                    | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                    dir_fd=parent_descriptor,
                )
                temporary_name = candidate
                break
            except FileExistsError:
                continue
        if descriptor is None or temporary_name is None:
            raise GeneratorError(f"cannot allocate same-directory temporary output: {path}")
        remaining = memoryview(payload)
        while remaining:
            written = os.write(descriptor, remaining)
            if written <= 0:
                raise GeneratorError(f"output write made no progress: {path}")
            remaining = remaining[written:]
        os.fchmod(descriptor, stat.S_IMODE(previous.st_mode) if previous is not None else 0o644)
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None

        try:
            current = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            current = None
        if previous is None:
            if current is not None:
                raise GeneratorError(f"output appeared before atomic publish: {path}")
        elif current is None or (
            previous.st_dev,
            previous.st_ino,
            previous.st_mode,
        ) != (
            current.st_dev,
            current.st_ino,
            current.st_mode,
        ):
            raise GeneratorError(f"output changed before atomic publish: {path}")
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        temporary_name = None
        os.fsync(parent_descriptor)
        if _read_bounded_regular_path(path, max_bytes=MAX_OUTPUT_BYTES) != payload:
            raise GeneratorError(f"published output verification failed: {path}")
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise GeneratorError(f"symlink output is not allowed: {path}") from error
        raise GeneratorError(f"output cannot be written safely: {path}: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        os.close(parent_descriptor)


def write_outputs(outputs: Mapping[Path, str]) -> None:
    for path, content in outputs.items():
        _atomic_write_regular(path, content)
        print(f"Generated {path}")


def apply_mode(outputs: Mapping[Path, str], mode: str) -> int:
    if mode == "check":
        return check_outputs(outputs)
    if mode == "write":
        write_outputs(outputs)
        return 0
    raise ValueError(mode)


def _canonical_decimal(value: str, label: str) -> int:
    if re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise GeneratorError(f"invalid Gate 9 LLM manifest: {label} is not canonical decimal")
    return int(value)


def _manifest_path(path_bytes: bytes) -> str:
    if not path_bytes or any(byte < 0x20 or byte == 0x7F for byte in path_bytes):
        raise GeneratorError("invalid Gate 9 LLM manifest: path contains unsafe bytes")
    try:
        return _validate_relative_path(path_bytes.decode("utf-8", errors="strict"))
    except UnicodeDecodeError as error:
        raise GeneratorError("invalid Gate 9 LLM manifest: path is not strict UTF-8") from error


def read_gate9_manifest(mode: str) -> list[str] | None:
    unexpected = sorted(
        name
        for name in os.environ
        if name.startswith("GATE9_LLM_MANIFEST_") and name not in MANIFEST_ENV_NAMES
    )
    if unexpected:
        raise GeneratorError(
            f"invalid Gate 9 LLM manifest: unexpected environment variable: {unexpected[0]}"
        )
    present = tuple(name in os.environ for name in MANIFEST_ENV_NAMES)
    if any(present) and not all(present):
        raise GeneratorError("invalid Gate 9 LLM manifest: environment is partial")
    if not any(present):
        return None
    if mode != "stdout":
        raise GeneratorError("invalid Gate 9 LLM manifest: internal mode requires --stdout")

    descriptor = _canonical_decimal(os.environ[MANIFEST_ENV_NAMES[0]], "fd")
    declared_size = _canonical_decimal(os.environ[MANIFEST_ENV_NAMES[1]], "size")
    declared_digest = os.environ[MANIFEST_ENV_NAMES[2]]
    if declared_size == 0 or declared_size > MAX_MANIFEST_BYTES:
        raise GeneratorError("invalid Gate 9 LLM manifest: size is outside the 1..8 MiB bound")
    if re.fullmatch(r"[0-9a-f]{64}", declared_digest) is None:
        raise GeneratorError("invalid Gate 9 LLM manifest: SHA-256 is not canonical lowercase hex")
    try:
        before = os.fstat(descriptor)
        current_offset = os.lseek(descriptor, 0, os.SEEK_CUR)
        seals = fcntl.fcntl(descriptor, fcntl.F_GET_SEALS)
        descriptor_target = os.readlink(f"/proc/self/fd/{descriptor}")
    except (OSError, ValueError) as error:
        raise GeneratorError(
            f"invalid Gate 9 LLM manifest: descriptor validation failed: {error}"
        ) from error
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 0:
        raise GeneratorError("invalid Gate 9 LLM manifest: descriptor is not an unlinked regular file")
    if not descriptor_target.startswith("/memfd:") or not descriptor_target.endswith(" (deleted)"):
        raise GeneratorError("invalid Gate 9 LLM manifest: descriptor is not a memfd")
    if current_offset != 0:
        raise GeneratorError("invalid Gate 9 LLM manifest: descriptor offset is not zero")
    if before.st_size != declared_size:
        raise GeneratorError("invalid Gate 9 LLM manifest: declared size does not match descriptor size")
    if seals & REQUIRED_SEALS != REQUIRED_SEALS:
        raise GeneratorError("invalid Gate 9 LLM manifest: descriptor lacks required seals")
    chunks: list[bytes] = []
    remaining = declared_size
    try:
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                raise GeneratorError("invalid Gate 9 LLM manifest: descriptor ended early")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1) != b"":
            raise GeneratorError("invalid Gate 9 LLM manifest: descriptor has trailing bytes")
        after = os.fstat(descriptor)
    except OSError as error:
        raise GeneratorError(f"invalid Gate 9 LLM manifest: descriptor read failed: {error}") from error
    if (
        before.st_dev,
        before.st_ino,
        before.st_mode,
        before.st_nlink,
        before.st_size,
    ) != (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_nlink,
        after.st_size,
    ):
        raise GeneratorError("invalid Gate 9 LLM manifest: descriptor identity changed during read")
    payload = b"".join(chunks)
    if not hmac.compare_digest(hashlib.sha256(payload).hexdigest(), declared_digest):
        raise GeneratorError("invalid Gate 9 LLM manifest: SHA-256 mismatch")
    if not payload.endswith(b"\0"):
        raise GeneratorError("invalid Gate 9 LLM manifest: payload lacks terminal NUL")
    records = payload.split(b"\0")[:-1]
    if len(records) < 5 or records[0] != MANIFEST_SCHEMA:
        raise GeneratorError("invalid Gate 9 LLM manifest: schema record is missing or invalid")
    object_format_record = records[1]
    if object_format_record == b"object-format=sha1":
        oid_length = 40
    elif object_format_record == b"object-format=sha256":
        oid_length = 64
    else:
        raise GeneratorError("invalid Gate 9 LLM manifest: object format is invalid")
    oid_pattern = re.compile(rb"[0-9a-f]{" + str(oid_length).encode() + rb"}")
    for record, prefix, label in (
        (records[2], b"live-commit=", "live commit"),
        (records[3], b"projected-tree=", "projected tree"),
    ):
        if not record.startswith(prefix):
            raise GeneratorError(f"invalid Gate 9 LLM manifest: {label} record is missing")
        oid = record[len(prefix) :]
        if oid_pattern.fullmatch(oid) is None or oid == b"0" * oid_length:
            raise GeneratorError(f"invalid Gate 9 LLM manifest: {label} OID is invalid")
    if not records[4].startswith(b"count="):
        raise GeneratorError("invalid Gate 9 LLM manifest: count record is missing")
    try:
        count = _canonical_decimal(records[4][len(b"count=") :].decode("ascii"), "count")
    except UnicodeDecodeError as error:
        raise GeneratorError("invalid Gate 9 LLM manifest: count is not ASCII") from error
    path_records = records[5:]
    if len(path_records) != count or count > MAX_TRACKED_PATHS:
        raise GeneratorError("invalid Gate 9 LLM manifest: count does not match bounded paths")
    if path_records != sorted(path_records) or len(set(path_records)) != len(path_records):
        raise GeneratorError("invalid Gate 9 LLM manifest: paths are not byte-sorted and unique")
    manifest_paths = [_manifest_path(record) for record in path_records]
    path_set = set(manifest_paths)
    for path_text in manifest_paths:
        prefix = ""
        for part in path_text.split("/")[:-1]:
            prefix = f"{prefix}/{part}" if prefix else part
            if prefix in path_set:
                raise GeneratorError("invalid Gate 9 LLM manifest: file/directory prefix collision")
    return manifest_paths


def _repository_root(start: Path) -> Path:
    result = _run_git_bounded(
        start,
        ["rev-parse", "--show-toplevel"],
        max_stdout=16_384,
        max_stderr=16_384,
        max_total=32_768,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise GeneratorError(f"git rev-parse failed: {detail or result.returncode}")
    try:
        root_text = result.stdout.decode("utf-8", errors="strict").strip()
    except UnicodeDecodeError as error:
        raise GeneratorError("repository root is not strict UTF-8") from error
    if not root_text or "\n" in root_text or not os.path.isabs(root_text):
        raise GeneratorError("git returned an invalid repository root")
    return Path(root_text)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", dest="mode", action="store_const", const="check")
    modes.add_argument("--write", dest="mode", action="store_const", const="write")
    modes.add_argument("--stdout", dest="mode", action="store_const", const="stdout")
    parser.add_argument("--artifact", choices=("index", "coverage"), help=argparse.SUPPRESS)
    parser.set_defaults(mode="check")
    args = parser.parse_args(argv)
    if args.mode == "stdout" and args.artifact is None:
        parser.error("--stdout requires --artifact")
    try:
        manifest_paths = read_gate9_manifest(args.mode)
        if manifest_paths is None:
            repo_root = _repository_root(Path.cwd())
            os.chdir(repo_root)
            candidates = collect_candidates(repo_root)
        else:
            if args.artifact is None:
                raise GeneratorError("sealed manifest mode requires --artifact")
            candidates = candidates_from_manifest(manifest_paths)
        outputs = build_outputs_from_candidates(candidates)
        if args.artifact == "index":
            outputs = {INDEX_OUTPUT: outputs[INDEX_OUTPUT]}
        elif args.artifact == "coverage":
            outputs = {COVERAGE_OUTPUT: outputs[COVERAGE_OUTPUT]}
        if args.mode == "stdout":
            sys.stdout.buffer.write(next(iter(outputs.values())).encode("utf-8"))
            return 0
        return apply_mode(outputs, args.mode)
    except GeneratorError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
