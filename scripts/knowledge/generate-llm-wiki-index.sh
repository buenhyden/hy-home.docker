#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

usage() {
  cat <<'EOF'
Usage: bash scripts/knowledge/generate-llm-wiki-index.sh [--check]

Generate the repo-local LLM Wiki path index.

Options:
  --check   Fail when docs/90.references/data/llm-wiki/index.md is stale.
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
import pathlib
import subprocess
import sys

MODE = sys.argv[1]
OUTPUT = pathlib.Path("docs/90.references/data/llm-wiki/index.md")
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
    "docs/05.operations/guides/90-knowledge/llm-wiki-maintenance.md",
    "docs/00.agent-governance/agents/agents/wiki-curator.md",
    ".claude/agents/wiki-curator.md",
    "docs/03.specs/llm-wiki-agent-first-completion/spec.md",
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
    if path_text.startswith("docs/90.references/data/llm-wiki/") or path_text == "llms.txt":
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
        "<!-- Target: docs/90.references/data/llm-wiki/index.md -->",
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
        "This generated tracked repo-local index complements `llms.txt` and `repository-map.md`. Runtime truth remains in `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.",
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
        "- [llms.txt](../../../../llms.txt) - root LLM entrypoint and boundary statement",
        "- [repository-map.md](./repository-map.md) - curated canonical source map",
        "- [generate-llm-wiki-index.sh](../../../../scripts/knowledge/generate-llm-wiki-index.sh) - deterministic generator",
        "- [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) - freshness and safety validator",
        "",
        "## Maintenance",
        "",
        "- **Owner**: `wiki-curator`",
        "- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change",
        "- **Update Trigger**: Run `bash scripts/knowledge/generate-llm-wiki-index.sh` after in-scope path changes and `bash scripts/knowledge/generate-llm-wiki-index.sh --check` during validation",
        "",
        "## Related Documents",
        "",
        "- [LLM Wiki references](./README.md)",
        "- [LLM Wiki repository map](./repository-map.md)",
        "- [LLM Wiki maintenance guide](../../../05.operations/guides/90-knowledge/llm-wiki-maintenance.md)",
        "- [Agent governance hub](../../../00.agent-governance/README.md)",
    ])
    return "\n".join(lines) + "\n"


tracked = git_ls_files()
tracked.update(path for path in REQUIRED_LOCAL_PATHS if pathlib.Path(path).exists())
safe_paths = sorted(path for path in tracked if pathlib.Path(path).exists() and is_safe_candidate(path))
generated = render(safe_paths)

if MODE == "check":
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
