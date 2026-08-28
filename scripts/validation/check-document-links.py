#!/usr/bin/env python3
"""Validate repository document links through one mode-driven Python CLI."""

from __future__ import annotations

import argparse
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.document_governance.links import (  # noqa: E402
    MODE_HANDLERS,
    archive_direct_link_total,
    build_document_graph,
    removed_template_mention_total,
    run_mode,
    traceability_pair_total,
)


DOC_ROOTS = (
    pathlib.Path("docs/01.requirements"),
    pathlib.Path("docs/02.architecture"),
    pathlib.Path("docs/03.specs"),
    pathlib.Path("docs/04.execution"),
    pathlib.Path("docs/05.operations"),
)
SUPPORT_DOCS = (
    pathlib.Path("README.md"),
    pathlib.Path("docs/README.md"),
    pathlib.Path("docs/00.agent-governance/policies/documentation-protocol.md"),
    pathlib.Path("docs/00.agent-governance/policies/stage-authoring-matrix.md"),
    pathlib.Path("docs/00.agent-governance/roles/qa.md"),
    pathlib.Path("docs/00.agent-governance/policies/github-governance.md"),
    pathlib.Path("docs/99.templates/README.md"),
    pathlib.Path("scripts/README.md"),
)


def _paths(root: pathlib.Path) -> list[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    for relative in DOC_ROOTS:
        stage = root / relative
        if stage.is_dir():
            paths.update(path for path in stage.rglob("*.md") if path.is_file())
    paths.update(root / relative for relative in SUPPORT_DOCS if (root / relative).is_file())
    return sorted(paths)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument(
        "--mode", required=True, choices=(*tuple(MODE_HANDLERS), "all")
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    graph = build_document_graph(_paths(root), repo_root=root)
    modes = tuple(MODE_HANDLERS) if args.mode == "all" else (args.mode,)
    findings = tuple(
        finding
        for mode in modes
        for finding in run_mode(mode, graph)
    )
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
