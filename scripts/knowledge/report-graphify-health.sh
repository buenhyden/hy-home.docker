#!/usr/bin/env bash
set -u

# Reports Graphify corpus health as advisory evidence.
# This script reads only graphify-out/manifest.json, graphify-out/graph.json,
# and graphify-out/GRAPH_REPORT.md. It never prints file contents.

repo_root="${HYHOME_DOCKER_ROOT:-$(pwd)}"
cd "$repo_root" || exit 0

if ! command -v python3 >/dev/null 2>&1; then
  echo "Graphify health report"
  echo "status=advisory"
  echo "advisory_reasons=python3_missing"
  echo "guidance=Graphify health could not be evaluated. Treat graph output as advisory and corroborate claims against tracked source files and canonical docs."
  exit 0
fi

python3 - <<'PY' || true
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

GRAPHIFY_DIR = Path("graphify-out")
MANIFEST_PATH = GRAPHIFY_DIR / "manifest.json"
GRAPH_PATH = GRAPHIFY_DIR / "graph.json"
REPORT_PATH = GRAPHIFY_DIR / "GRAPH_REPORT.md"

# Current gitlink/submodule roots known to this repository. Keep this local and
# explicit so the report does not inspect worktree contents outside graphify-out.
GITLINK_PREFIXES = ("projects/storybook/mcp",)
GENERATED_HINTS = (
    "/node_modules/",
    "/dist/",
    "/build/",
    "/.next/",
    "/coverage/",
    "/generated/",
    "/__generated__/",
    ".min.js",
)


def safe_json_load(path: Path) -> tuple[Any | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception:
        return None, "unparseable"


def safe_report_load(path: Path) -> tuple[str, str | None]:
    if not path.is_file():
        return "", "missing"
    try:
        return path.read_text(encoding="utf-8", errors="ignore"), None
    except Exception:
        return "", "unreadable"


def rel_path(value: str) -> str:
    text = value.replace("\\", "/")
    cwd = str(Path.cwd().resolve()).replace("\\", "/")
    if text == cwd:
        return "."
    if text.startswith(cwd + "/"):
        text = text[len(cwd) + 1 :]
    while text.startswith("./"):
        text = text[2:]
    return text


def is_volume_path(value: str) -> bool:
    rel = rel_path(value)
    return rel == "volumes" or rel.startswith("volumes/") or "/volumes/" in rel


def is_gitlink_path(value: str) -> bool:
    rel = rel_path(value)
    return any(rel == prefix or rel.startswith(prefix + "/") for prefix in GITLINK_PREFIXES)


def is_generated_path(value: str) -> bool:
    rel = "/" + rel_path(value)
    return any(hint in rel for hint in GENERATED_HINTS)


def collect_source_files(value: Any, output: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "source_file" and isinstance(child, str):
                output.add(child)
            else:
                collect_source_files(child, output)
    elif isinstance(value, list):
        for child in value:
            collect_source_files(child, output)


def god_node_labels(report: str) -> list[str]:
    labels: list[str] = []
    in_section = False
    for line in report.splitlines():
        if line.startswith("## God Nodes"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        match = re.match(r"\s*\d+\.\s+`([^`]+)`", line)
        if match:
            labels.append(match.group(1))
    return labels


def is_meaningless_god_node(label: str) -> bool:
    base = label[:-2] if label.endswith("()") else label
    return bool(re.fullmatch(r"[A-Za-z]", base) or re.fullmatch(r"\d+", base))


def report_surprising_counts(report: str) -> tuple[int, int]:
    inferred = 0
    cross_root = 0
    in_section = False
    current_inferred = False
    for line in report.splitlines():
        if line.startswith("## Surprising Connections"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            current_inferred = "[INFERRED]" in stripped
            if current_inferred:
                inferred += 1
            continue
        if current_inferred and "→" in stripped:
            left, right = [part.strip() for part in stripped.split("→", 1)]
            left_root = rel_path(left).split("/", 1)[0]
            right_root = rel_path(right).split("/", 1)[0]
            if (
                left_root != right_root
                or is_volume_path(left)
                or is_volume_path(right)
                or is_gitlink_path(left)
                or is_gitlink_path(right)
            ):
                cross_root += 1
            current_inferred = False
    return inferred, cross_root


def count_where(values: set[str] | list[str], predicate) -> int:
    return sum(1 for value in values if predicate(value))


def main() -> None:
    advisory_reasons: list[str] = []

    manifest, manifest_error = safe_json_load(MANIFEST_PATH)
    graph, graph_error = safe_json_load(GRAPH_PATH)
    report, report_error = safe_report_load(REPORT_PATH)

    for name, error in (
        ("manifest", manifest_error),
        ("graph", graph_error),
        ("report", report_error),
    ):
        if error:
            advisory_reasons.append(f"{name}_{error}")

    manifest_paths: list[str] = list(manifest.keys()) if isinstance(manifest, dict) else []
    manifest_volume = count_where(manifest_paths, is_volume_path)
    manifest_gitlink = count_where(manifest_paths, is_gitlink_path)
    manifest_generated = count_where(manifest_paths, is_generated_path)

    graph_source_files: set[str] = set()
    if graph is not None:
        collect_source_files(graph, graph_source_files)
    graph_volume = count_where(graph_source_files, is_volume_path)
    graph_gitlink = count_where(graph_source_files, is_gitlink_path)
    graph_generated = count_where(graph_source_files, is_generated_path)
    graph_contamination = graph_volume + graph_gitlink + graph_generated

    meaningless_god_nodes = count_where(god_node_labels(report), is_meaningless_god_node)
    surprising_inferred, surprising_cross_root = report_surprising_counts(report)

    if manifest_volume:
        advisory_reasons.append("manifest_runtime_volume_paths")
    if manifest_gitlink:
        advisory_reasons.append("manifest_gitlink_paths")
    if manifest_generated:
        advisory_reasons.append("manifest_generated_or_minified_paths")
    if graph_contamination:
        advisory_reasons.append("graph_source_file_contamination")
    if meaningless_god_nodes:
        advisory_reasons.append("meaningless_god_nodes")
    if surprising_cross_root:
        advisory_reasons.append("surprising_cross_root_inferred_edges")

    status = "advisory" if advisory_reasons else "clean"

    print("Graphify health report")
    print(f"status={status}")
    print(f"manifest_paths_total={len(manifest_paths)}")
    print(f"manifest_volume_paths={manifest_volume}")
    print(f"manifest_gitlink_paths={manifest_gitlink}")
    print(f"manifest_generated_or_minified_paths={manifest_generated}")
    print(f"graph_source_files_total={len(graph_source_files)}")
    print(f"graph_source_file_contamination_count={graph_contamination}")
    print(f"graph_source_file_volume_paths={graph_volume}")
    print(f"graph_source_file_gitlink_paths={graph_gitlink}")
    print(f"graph_source_file_generated_or_minified_paths={graph_generated}")
    print(f"meaningless_god_nodes={meaningless_god_nodes}")
    print(f"surprising_inferred_edges={surprising_inferred}")
    print(f"surprising_cross_root_inferred_edges={surprising_cross_root}")
    print("advisory_reasons=" + (",".join(sorted(set(advisory_reasons))) or "none"))
    print(
        "guidance="
        "Use Graphify as a navigation aid only when status=clean. "
        "When status=advisory, corroborate architecture and codebase claims "
        "against tracked source files, docs/00.agent-governance, and stage docs."
    )


try:
    main()
except Exception:
    print("Graphify health report")
    print("status=advisory")
    print("advisory_reasons=report_runtime_error")
    print(
        "guidance="
        "Graphify health could not be evaluated. Treat graph output as advisory "
        "and corroborate claims against tracked source files and canonical docs."
    )
PY

exit 0
