#!/usr/bin/env python3
"""Validate repository document links through one mode-driven Python CLI."""

from __future__ import annotations

import argparse
import pathlib
import re
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


DOC_ROOT = pathlib.Path("docs")
SUPPORT_DOCS = (
    pathlib.Path("README.md"),
    pathlib.Path("scripts/README.md"),
)
# A document whose status records a past observation is not a current route.
# Its links are evidence of what resolved when it was written.
NON_ROUTING_STATUSES = frozenset({"superseded", "retired"})
_STATUS = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)


def _routing_status(path: pathlib.Path) -> bool:
    """True when the document claims to be a current route."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    if not text.startswith("---"):
        return True
    end = text.find("\n---", 3)
    if end == -1:
        return True
    match = _STATUS.search(text[3:end])
    return match is None or match.group(1) not in NON_ROUTING_STATUSES


def _paths(root: pathlib.Path) -> list[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    stage = root / DOC_ROOT
    if stage.is_dir():
        paths.update(
            path
            for path in stage.rglob("*.md")
            if path.is_file() and _routing_status(path)
        )
    paths.update(
        root / relative
        for relative in SUPPORT_DOCS
        if (root / relative).is_file() and _routing_status(root / relative)
    )
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
