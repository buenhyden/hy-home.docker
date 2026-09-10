#!/usr/bin/env python3
"""Validate repository document links through one mode-driven Python CLI."""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.document_governance.frontmatter import (  # noqa: E402
    FrontmatterError,
    parse_frontmatter_text,
)
from scripts.lib.document_governance.links import (  # noqa: E402
    MODE_HANDLERS,
    archive_direct_link_total,
    build_document_graph,
    removed_template_mention_total,
    run_mode,
    traceability_pair_total,
)
from scripts.lib.document_governance.operations_catalog import (  # noqa: E402
    OperationsAuthorityError,
    read_bounded_regular,
    tracked_paths,
)
from scripts.lib.document_governance.registry import (  # noqa: E402
    DocumentRegistry,
    classify_path,
    declares_frozen_legacy_status,
    load_registry,
)

DOC_ROOT = pathlib.Path("docs")
# The graph reads every tracked Markdown document plus the LLM entry point.
# An explicit support list used to decide which documents outside `docs/` were
# checked, so a README that linked into a stage was simply not looked at; the
# tracked set removes that blind spot without letting untracked trees such as
# `projects/**/node_modules` into the graph.
# The provider adapters and the LLM entry point stay named rather than tracked-
# derived: a symlinked provider directory takes its contents out of the tracked
# set, and the graph has to report that escape instead of quietly skipping it.
SUPPORT_DOCS = (
    pathlib.Path(".claude/provider.md"),
    pathlib.Path(".codex/provider.md"),
    pathlib.Path("llms.txt"),
)
# A document whose status records a past observation is not a current route.
# Its links are evidence of what resolved when it was written.
NON_ROUTING_STATUSES = frozenset({"superseded", "retired"})


def _routing_status(
    root: pathlib.Path, path: pathlib.Path, registry: DocumentRegistry | None = None
) -> bool:
    """True when the document claims to be a current route."""
    try:
        text = read_bounded_regular(
            root, path.relative_to(root), max_bytes=4 * 1024 * 1024
        ).decode("utf-8")
    except (OSError, OperationsAuthorityError, UnicodeError):
        # Keep unsafe inputs visible so the graph reports its input finding.
        return True
    try:
        status = parse_frontmatter_text(text).get("status")
    except FrontmatterError:
        return True
    if registry is not None:
        relative = path.relative_to(root).as_posix()
        profile_id = classify_path(relative, registry)
        if profile_id is not None and declares_frozen_legacy_status(
            registry.profiles[profile_id], relative, status
        ):
            return False
    return not isinstance(status, str) or status not in NON_ROUTING_STATUSES


def _paths(root: pathlib.Path) -> list[pathlib.Path]:
    registry_path = root / "docs/99.templates/registry.json"
    registry = load_registry(registry_path) if registry_path.exists() else None
    candidates = {
        root / relative.as_posix()
        for relative in tracked_paths(root)
        if relative.suffix == ".md"
    }
    candidates.update(root / relative for relative in SUPPORT_DOCS)
    return sorted(
        path
        for path in candidates
        if (path.is_file() or path.is_symlink())
        and _routing_status(root, path, registry)
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--mode", required=True, choices=(*tuple(MODE_HANDLERS), "all"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    graph = build_document_graph(_paths(root), repo_root=root)
    modes = tuple(MODE_HANDLERS) if args.mode == "all" else (args.mode,)
    findings = tuple(finding for mode in modes for finding in run_mode(mode, graph))
    for finding in findings:
        print(
            f"{finding.code}: {finding.path}: {finding.message}",
            file=sys.stderr,
        )
    print(
        "document links: "
        f"mode={args.mode} documents={len(graph.nodes)} links={len(graph.links)} "
        f"catalog_pairs_total={traceability_pair_total(graph)} "
        f"archive_direct_links_total={archive_direct_link_total(graph)} "
        f"removed_template_mentions_total={removed_template_mention_total(graph)} "
        f"failures={len(findings)}"
    )
    if findings:
        return 1
    print(f"PASS: document link mode {args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
