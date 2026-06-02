#!/usr/bin/env bash
set -euo pipefail

# Validate that active Stage 01-05 documentation does not drift away from
# tracked repository implementation surfaces. This check intentionally covers
# implementation-truth alignment, not only link or template shape.

python3 - <<'PY'
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(".")
DOC_ROOTS = [
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/05.operations"),
]
SUPPORT_DOCS = [
    pathlib.Path("README.md"),
    pathlib.Path("docs/README.md"),
    pathlib.Path("docs/00.agent-governance/rules/documentation-protocol.md"),
    pathlib.Path("docs/00.agent-governance/rules/stage-authoring-matrix.md"),
    pathlib.Path("docs/00.agent-governance/scopes/qa.md"),
    pathlib.Path("docs/00.agent-governance/rules/github-governance.md"),
    pathlib.Path("docs/99.templates/README.md"),
    pathlib.Path("scripts/README.md"),
]
KNOWN_ROOT_PREFIXES = (
    "docs/",
    "infra/",
    "scripts/",
    ".github/",
    ".claude/",
    ".codex/",
    "secrets/",
    "projects/",
    "tests/",
)
KNOWN_ROOT_FILES = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "RTK.md",
    "docker-compose.yml",
    "llms.txt",
    ".env.example",
}

URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

failures: list[str] = []


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def is_relative_to(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def strip_fragment(target: str) -> str:
    return target.split("#", 1)[0].split("?", 1)[0]


def tracked_stage_docs() -> list[pathlib.Path]:
    docs: list[pathlib.Path] = []
    for root in DOC_ROOTS:
        docs.extend(sorted(root.rglob("*.md")))
    return [path for path in docs if "docs/98.archive" not in path.as_posix()]


def scan_link_targets(paths: list[pathlib.Path]) -> tuple[int, int]:
    checked = 0
    archive_direct = 0
    for path in paths:
        if not path.exists():
            continue
        text = read(path)
        for match in MD_LINK_RE.finditer(text):
            raw = match.group(1)
            if not raw or raw.startswith("#") or URL_RE.match(raw):
                continue
            target = strip_fragment(raw)
            if not target:
                continue
            if target.startswith("/"):
                failures.append(f"{path}: absolute repo-local Markdown link is not allowed: {raw}")
                checked += 1
                continue
            if target.startswith(("./", "../")):
                resolved = (path.parent / target).resolve().relative_to(REPO.resolve())
            elif target in KNOWN_ROOT_FILES or target.startswith(KNOWN_ROOT_PREFIXES):
                resolved = pathlib.Path(target)
            else:
                continue

            checked += 1
            resolved_text = resolved.as_posix()
            if resolved_text.startswith("docs/98.archive/") and resolved_text != "docs/98.archive/README.md":
                archive_direct += 1
                failures.append(f"{path}: active docs may link only to docs/98.archive/README.md: {raw}")
                continue
            if not (REPO / resolved).exists():
                failures.append(f"{path}: missing repo-local Markdown link target: {raw} -> {resolved_text}")
    return checked, archive_direct


def parse_root_includes() -> tuple[set[str], set[str]]:
    active: set[str] = set()
    optional: set[str] = set()
    include_section = False
    for line in read(pathlib.Path("docker-compose.yml")).splitlines():
        stripped = line.strip()
        if stripped == "include:":
            include_section = True
            continue
        if not include_section:
            continue
        if stripped.startswith("# - "):
            optional.add(stripped.removeprefix("# - ").strip())
        elif stripped.startswith("- "):
            active.add(stripped.removeprefix("- ").strip())
    return active, optional


SERVICE_ALIAS = {
    "ksqldb": "ksql",
    "prometheus-recovery": "prometheus",
    "airflow-worker-recovery": "airflow",
}
NON_SERVICE_STEMS = {
    "0012-standardize-infra-net",
    "01.lgtm-stack",
    "01.setup",
    "01.airflow-dag-dev",
    "01.iac-automation",
    "01.llm-inference",
    "01.retention",
    "02.n8n-automation",
    "02.rag-workflow",
    "airflow-dag-basics",
    "backup-policy",
    "common-optimizations-template-exceptions",
    "dag-deployment",
    "developer-setup",
    "env-key-comparison",
    "gpu-recovery",
    "harness-agent-first-engineering",
    "harness-agent-first-engineering-validation",
    "iac-deployment-policy",
    "infra-service-optimization-catalog",
    "ksql-streaming",
    "llm-wiki-maintenance",
    "local-llm-setup",
    "new-service-onboarding",
    "optimization-hardening",
    "performance-testing",
    "release-management",
    "sensitive-env-vars-comparison",
    "storage-exhaustion",
}


def has_tracked_impl(service_dir: pathlib.Path) -> bool:
    if not service_dir.is_dir():
        return False
    if (service_dir / "README.md").is_file():
        return True
    return any(service_dir.glob("docker-compose*.yml")) or any(service_dir.glob("docker-compose*.yaml"))


def scan_operations_implementation() -> tuple[int, int, int]:
    checked = 0
    active_links = 0
    optional_links = 0
    active_includes, optional_includes = parse_root_includes()

    ops_root = pathlib.Path("docs/05.operations")
    for bucket in ("guides", "policies", "runbooks"):
        bucket_root = ops_root / bucket
        for path in sorted(bucket_root.rglob("*.md")):
            if path.name == "README.md":
                continue
            rel = path.relative_to(bucket_root)
            if len(rel.parts) < 2:
                continue
            tier = rel.parts[0]
            if not re.match(r"^\d\d-[A-Za-z0-9-]+$", tier):
                continue
            stem = path.stem
            if stem in NON_SERVICE_STEMS:
                continue

            service = SERVICE_ALIAS.get(stem, stem)
            if len(rel.parts) >= 3:
                candidate = pathlib.Path("infra") / tier / pathlib.Path(*rel.parts[1:-1]) / service
            else:
                candidate = pathlib.Path("infra") / tier / service
            checked += 1
            if not has_tracked_impl(candidate):
                failures.append(f"{path}: no tracked infra implementation for operations service doc: {candidate}")
                continue

            compose_files = {p.as_posix() for p in candidate.glob("docker-compose*.yml")}
            compose_files.update(p.as_posix() for p in candidate.glob("docker-compose*.yaml"))
            if compose_files & active_includes:
                active_links += 1
            elif compose_files & optional_includes:
                optional_links += 1
    return checked, active_links, optional_links


def scan_removed_template_names(paths: list[pathlib.Path]) -> int:
    hits = 0
    for path in paths:
        if not path.exists():
            continue
        text = read(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "operation.template.md" in line:
                hits += 1
                failures.append(f"{path}:{line_no}: removed operations template name remains: operation.template.md")
    return hits


stage_docs = tracked_stage_docs()
scan_paths = sorted(set(stage_docs + [path for path in SUPPORT_DOCS if path.exists()]))
link_total, archive_direct_total = scan_link_targets(scan_paths)
removed_template_hits = scan_removed_template_names(scan_paths)
ops_checked, root_active_ops, root_optional_ops = scan_operations_implementation()

print("Doc implementation alignment check")
print(f"stage_docs_total={len(stage_docs)}")
print(f"repo_local_markdown_links_checked={link_total}")
print(f"removed_template_mentions_total={removed_template_hits}")
print(f"archive_direct_links_total={archive_direct_total}")
print(f"operations_service_docs_checked={ops_checked}")
print(f"operations_service_docs_root_active={root_active_ops}")
print(f"operations_service_docs_root_optional={root_optional_ops}")
print(f"failures={len(failures)}")

if failures:
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    sys.exit(1)

print("PASS: active docs align with tracked implementation surfaces")
PY
