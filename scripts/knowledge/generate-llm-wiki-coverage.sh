#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/knowledge/generate-llm-wiki-coverage.sh [--check]

Generate the Stage 90 LLM Wiki stage/category coverage snapshot.

Options:
  --check   Fail when docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md is stale.
  -h, --help
            Show this help.
EOF
}

mode="write"
case "${1:-}" in
  "")
    ;;
  --check)
    mode="check"
    ;;
  -h | --help)
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

import collections
import os
import pathlib
import subprocess
import sys

MODE = sys.argv[1]
OUTPUT = pathlib.Path("docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md")
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
    "scripts/knowledge/generate-llm-wiki-coverage.sh",
    "docs/90.references/data/knowledge/README.md",
    "docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md",
    "docs/00.agent-governance/agents/agents/doc-writer.md",
    "docs/00.agent-governance/agents/functions/knowledge-map-agent.md",
    ".claude/agents/doc-writer.md",
    "docs/03.specs/096-llm-wiki-agent-first-completion/spec.md",
    "docs/03.specs/113-llm-wiki-stage-category-coverage/spec.md",
    "docs/04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md",
    "docs/04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md",
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

EXCLUDED_PREFIXES = (
    "graphify-out/",
    "volumes/",
    "node_modules/",
    ".git/",
    "projects/storybook/nextjs/.next/",
    "projects/storybook/nextjs/node_modules/",
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
    if path_text == "docs/90.references/llm-wiki/llm-wiki-index.md":
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


def wiki_category(path_text: str) -> str:
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


def source_bucket(path_text: str) -> str:
    if path_text in ROOT_ENTRYPOINTS:
        return "root"
    if path_text.startswith("docs/"):
        parts = pathlib.PurePosixPath(path_text).parts
        if len(parts) >= 2:
            return f"docs/{parts[1]}"
        return "docs"
    if path_text.startswith(".github/"):
        return ".github"
    if path_text.startswith(".claude/"):
        return ".claude"
    if path_text.startswith(".codex/"):
        return ".codex"
    if path_text.startswith(".agents/"):
        return ".agents"
    return pathlib.PurePosixPath(path_text).parts[0]


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


def examples_for(paths: list[str], limit: int = 3) -> str:
    selected = sorted(paths)[:limit]
    return "<br>".join(link_for(path) for path in selected)


def render(paths: list[str]) -> str:
    category_paths: dict[str, list[str]] = collections.defaultdict(list)
    bucket_paths: dict[str, list[str]] = collections.defaultdict(list)
    role_paths: dict[str, list[str]] = collections.defaultdict(list)

    for path_text in paths:
        category_paths[wiki_category(path_text)].append(path_text)
        bucket_paths[source_bucket(path_text)].append(path_text)
        role_paths[role_for(path_text)].append(path_text)

    category_order = [
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
        "generated_by: scripts/knowledge/generate-llm-wiki-coverage.sh",
        "---",
        "",
        "<!-- Target: docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md -->",
        "",
        "# Reference: LLM Wiki Stage Category Coverage",
        "",
        "## Overview",
        "",
        "This generated reference summarizes the safe tracked source paths that feed the repo-local LLM Wiki index by source bucket, LLM Wiki category, and path role.",
        "",
        "## Purpose",
        "",
        "Provide audit consumers with a compact coverage snapshot without duplicating the full generated index or changing canonical source ownership.",
        "",
        "## Repository Role",
        "",
        "This file is generated reference data. Runtime truth remains in tracked source files such as `docs/00.agent-governance/`, `infra/`, `scripts/`, Docker Compose files, and registry JSON files.",
        "",
        "## Scope",
        "",
        "### In Scope",
        "",
        "- Counts by source bucket, LLM Wiki category, and path role.",
        "- Representative links for each category.",
        "- Deterministic freshness through `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check`.",
        "",
        "### Out of Scope",
        "",
        "- Full-content export or public website generation.",
        "- Runtime behavior, deployment workflow, network publishing, or external model calls.",
        "- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.",
        "",
        "## Definitions / Facts",
        "",
        "- **Safe tracked source path**: a `git ls-files` path that passes the LLM Wiki allowlist and exclusion rules.",
        "- **Source bucket**: the top-level repository surface or docs stage that owns a path.",
        "- **LLM Wiki category**: the navigation category used by the generated LLM Wiki index.",
        "- **Path role**: a lightweight type label derived from file name or suffix.",
        "",
        "## Source Rules",
        "",
        "- This snapshot excludes itself and the generated LLM Wiki index from coverage counts.",
        "- `secrets/README.md` is counted as policy context; secret content paths are excluded.",
        "- `graphify-out/`, `volumes/`, dependency trees, generated/minified artifacts, and lockfiles are excluded.",
        "- Use this file as coverage/navigation evidence only; read canonical source files for implementation truth.",
        "",
        "## Coverage Summary",
        "",
        f"- Safe tracked source paths: `{len(paths)}`",
        f"- Source buckets: `{len(bucket_paths)}`",
        f"- LLM Wiki categories: `{len(category_paths)}`",
        f"- Path roles: `{len(role_paths)}`",
        "",
        "## Source Bucket Coverage",
        "",
        "| Source Bucket | Paths | Representative Paths |",
        "| --- | ---: | --- |",
    ]
    for bucket, bucket_items in sorted(bucket_paths.items()):
        lines.append(f"| `{bucket}` | {len(bucket_items)} | {examples_for(bucket_items)} |")

    lines.extend([
        "",
        "## LLM Wiki Category Coverage",
        "",
        "| Category | Paths | Representative Paths |",
        "| --- | ---: | --- |",
    ])
    for category in category_order:
        category_items = category_paths.get(category, [])
        if not category_items:
            continue
        lines.append(f"| {category} | {len(category_items)} | {examples_for(category_items)} |")

    lines.extend([
        "",
        "## Path Role Coverage",
        "",
        "| Role | Paths |",
        "| --- | ---: |",
    ])
    for role, role_items in sorted(role_paths.items()):
        lines.append(f"| {role} | {len(role_items)} |")

    lines.extend([
        "",
        "## Sources",
        "",
        "- [LLM Wiki generated index](../../llm-wiki/llm-wiki-index.md) - full safe path index",
        "- [LLM Wiki repository map](../../llm-wiki/repository-map.md) - curated canonical source map",
        "- [generate-llm-wiki-index.sh](../../../../scripts/knowledge/generate-llm-wiki-index.sh) - generated index source",
        "- [generate-llm-wiki-coverage.sh](../../../../scripts/knowledge/generate-llm-wiki-coverage.sh) - this coverage snapshot generator",
        "- [repo contract checker](../../../../scripts/validation/check-repo-contracts.sh) - freshness gate",
        "",
        "## Maintenance",
        "",
        "- **Owner**: `doc-writer` using the `knowledge-map-agent` function.",
        "- **Review Cadence**: Review after root entrypoint, governance, operations, script inventory, infrastructure index, or LLM Wiki path changes.",
        "- **Update Trigger**: Run `bash scripts/knowledge/generate-llm-wiki-coverage.sh` after in-scope path changes and `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` during validation.",
        "",
        "## Related Documents",
        "",
        "- [Knowledge reference data](./README.md)",
        "- [Reference data](../README.md)",
        "- [LLM Wiki references](../../llm-wiki/README.md)",
        "- [LLM Wiki maintenance guide](../../../05.operations/guides/00-workspace/llm-wiki-maintenance.md)",
    ])
    return "\n".join(lines) + "\n"


tracked = git_ls_files()
tracked.update(path for path in REQUIRED_LOCAL_PATHS if pathlib.Path(path).exists())
safe_paths = sorted(path for path in tracked if pathlib.Path(path).exists() and is_safe_candidate(path))
generated = render(safe_paths)

if MODE == "check":
    if not OUTPUT.is_file():
        print(f"FAIL: missing generated LLM Wiki coverage snapshot: {OUTPUT}", file=sys.stderr)
        sys.exit(1)
    current = OUTPUT.read_text()
    if current != generated:
        print(f"FAIL: stale generated LLM Wiki coverage snapshot: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/knowledge/generate-llm-wiki-coverage.sh", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: generated LLM Wiki coverage snapshot is fresh: {OUTPUT}")
else:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated)
    print(f"Generated {OUTPUT} with {len(safe_paths)} safe paths")
PY
