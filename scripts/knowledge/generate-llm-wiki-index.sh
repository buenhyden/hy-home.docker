#!/usr/bin/env bash
set -euo pipefail

manifest_env_count=0
if [[ ${GATE9_LLM_MANIFEST_FD+x} == x ]]; then
  manifest_env_count=$((manifest_env_count + 1))
fi
if [[ ${GATE9_LLM_MANIFEST_SIZE+x} == x ]]; then
  manifest_env_count=$((manifest_env_count + 1))
fi
if [[ ${GATE9_LLM_MANIFEST_SHA256+x} == x ]]; then
  manifest_env_count=$((manifest_env_count + 1))
fi

if (( manifest_env_count != 0 && manifest_env_count != 3 )); then
  echo "FAIL: Gate 9 LLM manifest environment must be all-or-none" >&2
  exit 1
elif (( manifest_env_count == 3 )); then
  if (( $# != 1 )) || [[ $1 != "--stdout" ]]; then
    echo "FAIL: Gate 9 LLM manifest mode requires sole argument --stdout" >&2
    exit 1
  fi
else
  BASE_DIR="$(git rev-parse --show-toplevel)"
  cd "$BASE_DIR"
fi

usage() {
  cat <<'EOF'
Usage: bash scripts/knowledge/generate-llm-wiki-index.sh [--check|--stdout]

Generate the repo-local LLM Wiki path index.

Options:
  --check   Fail when docs/90.references/llm-wiki/llm-wiki-index.md is stale.
  --stdout  Write the rendered Markdown to stdout without modifying the repository.
  -h, --help
            Show this help.
EOF
}

mode="write"
if (( $# > 1 )); then
  usage >&2
  exit 2
fi
case "${1:-}" in
  "")
    ;;
  --check)
    mode="check"
    ;;
  --stdout)
    mode="stdout"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

python3 - "$mode" <<'PY'
from __future__ import annotations

import os
import fcntl
import hashlib
import hmac
import pathlib
import re
import stat
import subprocess
import sys

MODE = sys.argv[1]
OUTPUT = pathlib.Path("docs/90.references/llm-wiki/llm-wiki-index.md")
OUTPUT_PARENT = OUTPUT.parent

ROOT_ENTRYPOINTS = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "RTK.md",
    "llms.txt",
    "docker-compose.yml",
    ".env.example",
    ".pre-commit-config.yaml",
}

REQUIRED_LOCAL_PATHS = {
    "scripts/knowledge/generate-llm-wiki-index.sh",
    "docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md",
    "docs/00.agent-governance/agents/agents/doc-writer.md",
    "docs/00.agent-governance/agents/functions/knowledge-map-agent.md",
    ".claude/agents/doc-writer.md",
    "docs/03.specs/096-llm-wiki-agent-first-completion/spec.md",
    "docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md",
    "docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md",
}

SAFE_SUFFIXES = {
    ".conf",
    ".env",
    ".graphql",
    ".json",
    ".md",
    ".proto",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

RETIRING_PACK_PREFIX = (
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/"
)

EXCLUDED_PREFIXES = (
    "graphify-out/",
    "volumes/",
    "node_modules/",
    ".git/",
    "projects/storybook/nextjs/.next/",
    "projects/storybook/nextjs/node_modules/",
    RETIRING_PACK_PREFIX,
)

EXCLUDED_PARTS = {
    ".cache",
    ".next",
    "coverage",
    "dist",
    "node_modules",
    "vendor",
}

GENERATED_OR_LOCK_FILES = (
    ".min.css",
    ".min.js",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
)

MANIFEST_ENV_NAMES = (
    "GATE9_LLM_MANIFEST_FD",
    "GATE9_LLM_MANIFEST_SIZE",
    "GATE9_LLM_MANIFEST_SHA256",
)
MANIFEST_SCHEMA = b"schema=agentic-research-llm-wiki-manifest/v1"
MAX_MANIFEST_BYTES = 8 * 1024 * 1024
REQUIRED_SEALS = (
    fcntl.F_SEAL_SEAL
    | fcntl.F_SEAL_SHRINK
    | fcntl.F_SEAL_GROW
    | fcntl.F_SEAL_WRITE
)


def manifest_error(detail: str) -> None:
    print(f"FAIL: invalid Gate 9 LLM manifest: {detail}", file=sys.stderr)
    raise SystemExit(1)


def canonical_decimal(value: str, label: str) -> int:
    if re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        manifest_error(f"{label} is not canonical decimal")
    return int(value)


def validate_manifest_path(path_bytes: bytes) -> str:
    if not path_bytes:
        manifest_error("path is empty")
    if any(byte < 0x20 or byte == 0x7F for byte in path_bytes):
        manifest_error("path contains a control byte")
    try:
        path_text = path_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        manifest_error("path is not strict UTF-8")
    if path_text.startswith("/") or path_text.endswith("/") or "\\" in path_text:
        manifest_error("path is not a complete relative POSIX path")
    parts = path_text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        manifest_error("path has an unsafe POSIX component")
    return path_text


def read_gate9_manifest() -> list[str] | None:
    unexpected = sorted(
        name
        for name in os.environ
        if name.startswith("GATE9_LLM_MANIFEST_") and name not in MANIFEST_ENV_NAMES
    )
    if unexpected:
        manifest_error(f"unexpected environment variable: {unexpected[0]}")
    present = tuple(name in os.environ for name in MANIFEST_ENV_NAMES)
    if any(present) and not all(present):
        manifest_error("environment is partial")
    if not any(present):
        return None
    if MODE != "stdout":
        manifest_error("internal mode requires --stdout")

    descriptor = canonical_decimal(os.environ[MANIFEST_ENV_NAMES[0]], "fd")
    declared_size = canonical_decimal(os.environ[MANIFEST_ENV_NAMES[1]], "size")
    declared_digest = os.environ[MANIFEST_ENV_NAMES[2]]
    if declared_size == 0 or declared_size > MAX_MANIFEST_BYTES:
        manifest_error("size is outside the 1..8 MiB bound")
    if re.fullmatch(r"[0-9a-f]{64}", declared_digest) is None:
        manifest_error("SHA-256 is not canonical lowercase hex")

    try:
        before = os.fstat(descriptor)
        current_offset = os.lseek(descriptor, 0, os.SEEK_CUR)
        seals = fcntl.fcntl(descriptor, fcntl.F_GET_SEALS)
        descriptor_target = os.readlink(f"/proc/self/fd/{descriptor}")
    except (OSError, ValueError) as error:
        manifest_error(f"descriptor validation failed: {error}")
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 0:
        manifest_error("descriptor is not an unlinked regular file")
    if not descriptor_target.startswith("/memfd:") or not descriptor_target.endswith(
        " (deleted)"
    ):
        manifest_error("descriptor is not a memfd")
    if current_offset != 0:
        manifest_error("descriptor offset is not zero")
    if before.st_size != declared_size:
        manifest_error("declared size does not match descriptor size")
    if seals & REQUIRED_SEALS != REQUIRED_SEALS:
        manifest_error("descriptor lacks required seals")

    chunks: list[bytes] = []
    remaining = declared_size
    try:
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                manifest_error("descriptor ended before declared size")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1) != b"":
            manifest_error("descriptor has bytes beyond declared size")
        after = os.fstat(descriptor)
    except OSError as error:
        manifest_error(f"descriptor read failed: {error}")
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
        manifest_error("descriptor identity changed during read")

    payload = b"".join(chunks)
    if not hmac.compare_digest(hashlib.sha256(payload).hexdigest(), declared_digest):
        manifest_error("SHA-256 mismatch")
    if not payload.endswith(b"\0"):
        manifest_error("payload lacks terminal NUL")
    records = payload.split(b"\0")
    records.pop()
    if len(records) < 5 or records[0] != MANIFEST_SCHEMA:
        manifest_error("schema record is missing or invalid")

    object_format_record = records[1]
    if object_format_record == b"object-format=sha1":
        oid_length = 40
    elif object_format_record == b"object-format=sha256":
        oid_length = 64
    else:
        manifest_error("object format is invalid")
    oid_pattern = re.compile(rb"[0-9a-f]{" + str(oid_length).encode() + rb"}")
    for record, prefix, label in (
        (records[2], b"live-commit=", "live commit"),
        (records[3], b"projected-tree=", "projected tree"),
    ):
        if not record.startswith(prefix):
            manifest_error(f"{label} record is missing")
        oid = record[len(prefix) :]
        if oid_pattern.fullmatch(oid) is None or oid == b"0" * oid_length:
            manifest_error(f"{label} OID is invalid")

    if not records[4].startswith(b"count="):
        manifest_error("count record is missing")
    try:
        count_text = records[4][len(b"count=") :].decode("ascii", errors="strict")
    except UnicodeDecodeError:
        manifest_error("count is not ASCII")
    count = canonical_decimal(count_text, "count")
    path_records = records[5:]
    if len(path_records) != count:
        manifest_error("count does not match path records")
    if path_records != sorted(path_records) or len(set(path_records)) != len(
        path_records
    ):
        manifest_error("paths are not byte-sorted and unique")
    manifest_paths = [validate_manifest_path(path_bytes) for path_bytes in path_records]
    path_set = set(manifest_paths)
    for path_text in manifest_paths:
        prefix = ""
        for part in path_text.split("/")[:-1]:
            prefix = f"{prefix}/{part}" if prefix else part
            if prefix in path_set:
                manifest_error("paths have a file/directory prefix collision")
    return manifest_paths


def git_ls_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def is_safe_candidate(path_text: str) -> bool:
    if path_text == str(OUTPUT):
        return False
    if any(path_text.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    if path_text.startswith("secrets/") and path_text != "secrets/README.md":
        return False
    if path_text.endswith(GENERATED_OR_LOCK_FILES):
        return False

    path = pathlib.PurePosixPath(path_text)
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if path.name.startswith(".") and path_text not in ROOT_ENTRYPOINTS:
        return path_text.startswith(".github/") or path_text.startswith(".claude/") or path_text.startswith(".codex/")
    if path.suffix and path.suffix not in SAFE_SUFFIXES:
        return False

    return (
        path_text in ROOT_ENTRYPOINTS
        or path_text.startswith(".github/")
        or path_text.startswith(".claude/")
        or path_text.startswith(".codex/")
        or path_text.startswith("docs/")
        or path_text.startswith("infra/")
        or path_text.startswith("scripts/")
        or path_text == "secrets/README.md"
    )


def classify(path_text: str) -> str:
    if path_text in ROOT_ENTRYPOINTS:
        return "Root entrypoints"
    if path_text.startswith("docs/90.references/llm-wiki/") or path_text == "llms.txt":
        return "LLM Wiki reference"
    if path_text.startswith("docs/00.agent-governance/"):
        return "Agent governance"
    if path_text.startswith(".claude/") or path_text.startswith(".codex/"):
        return "Runtime surfaces"
    if path_text.startswith("docs/05.operations/"):
        return "Operations docs"
    if path_text.startswith("docs/01.requirements/") or path_text.startswith("docs/02.architecture/") or path_text.startswith("docs/03.specs/") or path_text.startswith("docs/04.execution/"):
        return "Active stage docs"
    if path_text.startswith("docs/90.references/") or path_text.startswith("docs/99.templates/") or path_text == "docs/README.md":
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


def role_for(path_text: str) -> str:
    name = pathlib.PurePosixPath(path_text).name
    if name == "README.md":
        return "folder index"
    if name.endswith(".sh"):
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


def link_for(path_text: str) -> str:
    relative = os.path.relpath(path_text, OUTPUT_PARENT)
    return f"[{path_text}]({relative})"


def render(paths: list[str]) -> str:
    grouped: dict[str, list[str]] = {}
    for path_text in paths:
        grouped.setdefault(classify(path_text), []).append(path_text)

    sections = [
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
    ]

    lines: list[str] = [
        "---",
        "status: active",
        "generated_by: scripts/knowledge/generate-llm-wiki-index.sh",
        "---",
        "",
        "<!-- Target: docs/90.references/llm-wiki/llm-wiki-index.md -->",
        "",
        "# Reference: LLM Wiki Generated Index",
        "",
        "## Overview",
        "",
        "이 문서는 `hy-home.docker`의 LLM Wiki가 사용하는 generated tracked repo-local index다. LLM 에이전트가 먼저 확인할 수 있는 안전한 경로 목록을 제공하되, 각 파일의 내용이나 runtime truth를 복제하지 않는다.",
        "",
        "## Purpose",
        "",
        "Provide a deterministic path index for repo-local AI agents without creating a public site, a full-content bundle, or a replacement for canonical source files.",
        "",
        "## Repository Role",
        "",
        "This generated tracked repo-local index complements `llms.txt` and `ref-0083-repository-map.md`. Runtime truth remains in `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.",
        "",
        "Graphify output is advisory navigation context only. This index is generated from repository path metadata and does not treat `graphify-out/` as source material.",
        "",
        "## Scope",
        "",
        "### In Scope",
        "",
        "- Repo-relative path links for safe tracked source entrypoints.",
        "- Governance, runtime, documentation, infrastructure, script, and secret-handling policy surfaces.",
        "- Deterministic refresh through `bash scripts/knowledge/generate-llm-wiki-index.sh`.",
        "",
        "### Out of Scope",
        "",
        "- Public website or public wiki deployment.",
        "- `llms-full.txt` or any full-content export.",
        "- External model calls, network publishing, deployment workflow, or Docker runtime behavior.",
        "- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.",
        "",
        "## Definitions / Facts",
        "",
        "- **Generated tracked repo-local index**: a committed Markdown path index regenerated from safe repository paths.",
        "- **Tracked source boundary**: `git ls-files` is the primary path source; known in-progress LLM Wiki contract files are included only when present locally.",
        "- **Runtime truth**: files that define actual behavior, such as Compose files, registry JSON files, scripts, and agent governance docs.",
        "- **Advisory graph context**: generated Graphify output that can assist navigation but does not replace tracked source files.",
        "",
        "## Source Rules",
        "",
        "- Prefer canonical tracked source paths over generated artifacts.",
        "- Keep links repo-relative; never use absolute filesystem links or filesystem URI links.",
        "- Exclude secret contents and treat `secrets/README.md` as policy context only.",
        "- Exclude `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/`.",
        "- Regenerate this file after changes to root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files.",
        "",
        "## Generated Index",
        "",
    ]

    for section in sections:
        entries = grouped.get(section, [])
        if not entries:
            continue
        lines.extend([
            f"### {section}",
            "",
            "| Path | Role |",
            "| --- | --- |",
        ])
        for path_text in entries:
            lines.append(f"| {link_for(path_text)} | {role_for(path_text)} |")
        lines.append("")

    lines.extend([
        "## Sources",
        "",
        "- [llms.txt](../../../llms.txt) - root LLM entrypoint and boundary statement",
        "- [ref-0083-repository-map.md](./ref-0083-repository-map.md) - curated canonical source map",
        "- [generate-llm-wiki-index.sh](../../../scripts/knowledge/generate-llm-wiki-index.sh) - deterministic generator",
        "- [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) - freshness and safety validator",
        "",
        "## Maintenance",
        "",
        "- **Owner**: `doc-writer` using the `knowledge-map-agent` function",
        "- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change",
        "- **Update Trigger**: Run `bash scripts/knowledge/generate-llm-wiki-index.sh` after in-scope path changes and `bash scripts/knowledge/generate-llm-wiki-index.sh --check` during validation",
        "",
        "## Related Documents",
        "",
        "- [LLM Wiki references](./README.md)",
        "- [LLM Wiki repository map](./ref-0083-repository-map.md)",
        "- [LLM Wiki maintenance guide](../../05.operations/guides/00-workspace/llm-wiki-maintenance.md)",
        "- [Agent governance hub](../../00.agent-governance/README.md)",
    ])
    return "\n".join(lines) + "\n"


manifest_paths = read_gate9_manifest()
if manifest_paths is None:
    tracked = git_ls_files()
    tracked.update(path for path in REQUIRED_LOCAL_PATHS if pathlib.Path(path).exists())
    safe_paths = sorted(
        path
        for path in tracked
        if pathlib.Path(path).exists() and is_safe_candidate(path)
    )
else:
    safe_paths = [path for path in manifest_paths if is_safe_candidate(path)]
generated = render(safe_paths)

if MODE == "stdout":
    sys.stdout.buffer.write(generated.encode("utf-8"))
elif MODE == "check":
    if not OUTPUT.is_file():
        print(f"FAIL: missing generated LLM Wiki index: {OUTPUT}", file=sys.stderr)
        sys.exit(1)
    current = OUTPUT.read_text()
    if current != generated:
        print(f"FAIL: stale generated LLM Wiki index: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/knowledge/generate-llm-wiki-index.sh", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: generated LLM Wiki index is fresh: {OUTPUT}")
else:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated)
    print(f"Generated {OUTPUT} with {len(safe_paths)} paths")
PY
