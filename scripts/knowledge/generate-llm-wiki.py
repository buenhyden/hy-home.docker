#!/usr/bin/env python3
"""Generate or check both tracked LLM Wiki reference outputs."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
from typing import Mapping, Sequence


INDEX_OUTPUT = Path("docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md")
COVERAGE_OUTPUT = Path("docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md")
GENERATOR_PATH = "scripts/knowledge/generate-llm-wiki.py"
ROOT_ENTRYPOINTS = frozenset(
    {
        ".env.example",
        ".pre-commit-config.yaml",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "README.md",
        "RTK.md",
        "docker-compose.yml",
        "llms.txt",
    }
)
REQUIRED_LOCAL_PATHS = frozenset(
    {GENERATOR_PATH}
)
SAFE_SUFFIXES = frozenset({".conf", ".env", ".graphql", ".json", ".md", ".proto", ".sh", ".toml", ".txt", ".yaml", ".yml"})
# Deletion-invariance for the Spec 137 retirement. The retiring research pack is
# excluded by exact trailing-slash prefix so this generated navigation surface
# carries no reference to it either before or after deletion. Ported on
# 2026-08-19 from scripts/knowledge/generate-llm-wiki-index.sh, which owned this
# property while it was the canonical generator. Measured before the port: a
# regeneration without it injects 20 clickable retiring-pack links into the
# index and gate 4's hard clickable_links=0 fails.
RETIRING_PACK_PREFIX = "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/"
EXCLUDED_PREFIXES = (".git/", "graphify-out/", "node_modules/", "projects/storybook/nextjs/.next/", "projects/storybook/nextjs/node_modules/", "volumes/", RETIRING_PACK_PREFIX)
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


@dataclass(frozen=True, order=True)
class Candidate:
    path: str
    category: str
    bucket: str
    role: str


def _git_ls_files(repo_root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "-z"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=False,
    )
    return {
        raw.decode("utf-8", "surrogateescape")
        for raw in result.stdout.split(b"\0")
        if raw
    }


def is_safe_candidate(path_text: str) -> bool:
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
    if path_text.startswith("docs/90.references/llm-wiki/") or path_text == "llms.txt":
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
    safe_paths = {
        path
        for path in tracked
        if (repo_root / path).is_file()
        and not (repo_root / path).is_symlink()
        and is_safe_candidate(path)
    }
    for relative in REQUIRED_LOCAL_PATHS:
        path = repo_root / relative
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(repo_root.resolve(strict=True))
        except (OSError, RuntimeError, ValueError):
            continue
        if path.is_file() and not path.is_symlink():
            safe_paths.add(relative)
    safe_paths = sorted(safe_paths)
    return [Candidate(path, classify(path), source_bucket(path), role_for(path)) for path in safe_paths]


def _link(path_text: str, output: Path) -> str:
    return f"[{path_text}]({os.path.relpath(path_text, output.parent)})"


def render_index(candidates: Sequence[Candidate]) -> str:
    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        if candidate.path == INDEX_OUTPUT.as_posix():
            continue
        grouped[candidate.category].append(candidate)
    lines = [
        "---", "status: active", f"generated_by: {GENERATOR_PATH}", "---", "",
        "# Reference: LLM Wiki Generated Index", "", "## Overview", "",
        "이 문서는 `hy-home.docker`의 LLM Wiki가 사용하는 generated tracked repo-local index다. LLM 에이전트가 먼저 확인할 수 있는 안전한 경로 목록을 제공하되, 각 파일의 내용이나 runtime truth를 복제하지 않는다.", "",
        "## Purpose", "", "Provide a deterministic path index for repo-local AI agents without creating a public site, a full-content bundle, or a replacement for canonical source files.", "",
        "## Repository Role", "", "This generated tracked repo-local index complements `llms.txt` and `repository-map.md`. Runtime truth remains in `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.", "",
        "Graphify output is advisory navigation context only. This index is generated from repository path metadata and does not treat `graphify-out/` as source material.", "",
        "## Scope", "", "### In Scope", "", "- Repo-relative path links for safe tracked source entrypoints.", "- Governance, runtime, documentation, infrastructure, script, and secret-handling policy surfaces.", f"- Deterministic refresh through `python3 {GENERATOR_PATH} --write`.", "",
        "### Out of Scope", "", "- Public website or public wiki deployment.", "- `llms-full.txt` or any full-content export.", "- External model calls, network publishing, deployment workflow, or Docker runtime behavior.", "- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.", "",
        "## Definitions / Facts", "", "- **Generated tracked repo-local index**: a committed Markdown path index regenerated from safe repository paths.", "- **Tracked source boundary**: `git ls-files` plus present, non-ignored Task-local generator paths is the path source.", "- **Runtime truth**: files that define actual behavior, such as Compose files, registry JSON files, scripts, and agent governance docs.", "- **Advisory graph context**: generated Graphify output that can assist navigation but does not replace tracked source files.", "",
        "## Source Rules", "", "- Prefer canonical tracked source paths over generated artifacts.", "- Keep links repo-relative; never use absolute filesystem links or filesystem URI links.", "- Exclude secret contents and treat `secrets/README.md` as policy context only.", "- Exclude `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/`.", "- Regenerate this file after changes to root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files.", "",
        "## Generated Index", "",
    ]
    for category in CATEGORY_ORDER:
        entries = grouped.get(category, [])
        if entries:
            lines.extend([f"### {category}", "", "| Path | Role |", "| --- | --- |"])
            lines.extend(f"| {_link(item.path, INDEX_OUTPUT)} | {item.role} |" for item in entries)
            lines.append("")
    lines.extend([
        "## Sources", "", "- [llms.txt](../../../llms.txt) - root LLM entrypoint and boundary statement", "- [ref-0083-repository-map.md](./ref-0083-repository-map.md) - curated canonical source map", f"- [generate-llm-wiki.py](../../../{GENERATOR_PATH}) - deterministic two-output generator", "- [check-script-manifest.py](../../../scripts/validation/check-script-manifest.py) - aggregate generated-output freshness gate", "",
        "## Maintenance", "", "- **Owner**: `doc-writer` using the `knowledge-map-agent` function", "- **Review Cadence**: Review when root entrypoints, governance, operations docs, script inventory, infrastructure indexes, or LLM Wiki files change", f"- **Update Trigger**: Run `python3 {GENERATOR_PATH} --write` after in-scope path changes and `python3 {GENERATOR_PATH} --check` during validation", "",
        "## Related Documents", "", "- [LLM Wiki references](./README.md)", "- [LLM Wiki repository map](./ref-0083-repository-map.md)", "- [LLM Wiki maintenance guide](../../05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md)", "- [Agent governance hub](../../00.agent-governance/README.md)",
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
        "---", "status: active", f"generated_by: {GENERATOR_PATH}", "---", "",
        "# Reference: LLM Wiki Stage Category Coverage", "", "## Overview", "", "This generated reference summarizes the safe tracked source paths that feed the repo-local LLM Wiki index by source bucket, LLM Wiki category, and path role.", "",
        "## Purpose", "", "Provide audit consumers with a compact coverage snapshot without duplicating the full generated index or changing canonical source ownership.", "",
        "## Repository Role", "", "This file is generated reference data. Runtime truth remains in tracked source files such as `docs/00.agent-governance/`, `infra/`, `scripts/`, Docker Compose files, and registry JSON files.", "",
        "## Scope", "", "### In Scope", "", "- Counts by source bucket, LLM Wiki category, and path role.", "- Representative links for each category.", f"- Deterministic freshness through `python3 {GENERATOR_PATH} --check`.", "",
        "### Out of Scope", "", "- Full-content export or public website generation.", "- Runtime behavior, deployment workflow, network publishing, or external model calls.", "- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.", "",
        "## Definitions / Facts", "", "- **Safe tracked source path**: a repository path that passes the LLM Wiki allowlist and exclusion rules.", "- **Source bucket**: the top-level repository surface or docs stage that owns a path.", "- **LLM Wiki category**: the navigation category used by the generated LLM Wiki index.", "- **Path role**: a lightweight type label derived from file name or suffix.", "",
        "## Source Rules", "", "- This snapshot and the generated LLM Wiki index are excluded from coverage counts.", "- `secrets/README.md` is counted as policy context; secret content paths are excluded.", "- `graphify-out/`, `volumes/`, dependency trees, generated/minified artifacts, and lockfiles are excluded.", "- Use this file as coverage/navigation evidence only; read canonical source files for implementation truth.", "",
        "## Coverage Summary", "", f"- Safe tracked source paths: `{len(selected)}`", f"- Source buckets: `{len(buckets)}`", f"- LLM Wiki categories: `{len(categories)}`", f"- Path roles: `{len(roles)}`", "",
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
        "", "## Sources", "", "- [LLM Wiki generated index](../../llm-wiki/ref-0082-llm-wiki-index.md) - full safe path index", "- [LLM Wiki repository map](../../llm-wiki/ref-0083-repository-map.md) - curated canonical source map", f"- [generate-llm-wiki.py](../../../../{GENERATOR_PATH}) - deterministic two-output generator", "- [script manifest checker](../../../../scripts/validation/check-script-manifest.py) - aggregate generated-output freshness gate", "",
        "## Maintenance", "", "- **Owner**: `doc-writer` using the `knowledge-map-agent` function.", "- **Review Cadence**: Review after root entrypoint, governance, operations, script inventory, infrastructure index, or LLM Wiki path changes.", f"- **Update Trigger**: Run `python3 {GENERATOR_PATH} --write` after in-scope path changes and `python3 {GENERATOR_PATH} --check` during validation.", "",
        "## Related Documents", "", "- [Knowledge reference data](./README.md)", "- [Reference data](../README.md)", "- [LLM Wiki references](../../llm-wiki/README.md)", "- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md)",
    ])
    return "\n".join(lines) + "\n"


def build_outputs(repo_root: Path) -> dict[Path, str]:
    candidates = collect_candidates(repo_root)
    return {
        INDEX_OUTPUT: render_index(candidates),
        COVERAGE_OUTPUT: render_coverage(candidates),
    }


def check_outputs(outputs: Mapping[Path, str]) -> int:
    stale = False
    for path, expected in outputs.items():
        if not path.is_file():
            print(f"FAIL: missing generated LLM Wiki output: {path}", file=sys.stderr)
            stale = True
        elif path.read_text(encoding="utf-8") != expected:
            print(f"FAIL: stale generated LLM Wiki output: {path}", file=sys.stderr)
            stale = True
    if stale:
        print(f"Run: python3 {GENERATOR_PATH} --write", file=sys.stderr)
        return 1
    print("PASS: both generated LLM Wiki outputs are fresh")
    return 0


def write_outputs(outputs: Mapping[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Generated {path}")


def apply_mode(outputs: Mapping[Path, str], mode: str) -> int:
    if mode == "check":
        return check_outputs(outputs)
    if mode == "write":
        write_outputs(outputs)
        return 0
    raise ValueError(mode)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", dest="mode", action="store_const", const="check")
    modes.add_argument("--write", dest="mode", action="store_const", const="write")
    parser.set_defaults(mode="check")
    args = parser.parse_args(argv)
    repo_root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], text=True, check=True, capture_output=True).stdout.strip())
    os.chdir(repo_root)
    return apply_mode(build_outputs(repo_root), args.mode)


if __name__ == "__main__":
    raise SystemExit(main())
