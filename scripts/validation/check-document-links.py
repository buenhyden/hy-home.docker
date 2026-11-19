#!/usr/bin/env python3
"""Validate repository document links through one mode-driven Python CLI."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import posixpath
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.document_governance.links import (  # noqa: E402
    MODE_HANDLERS,
    DocumentGraph,
    build_document_graph,
    inbound_link_lookup,
    relation_lookup,
    removed_template_mention_total,
    run_mode,
    select_changed_documents,
    traceability_pair_total,
)
from scripts.lib.document_governance.operations_catalog import (  # noqa: E402
    OperationsAuthorityError,
    tracked_paths,
)
from scripts.lib.document_governance.registry import (  # noqa: E402
    DEFAULT_REGISTRY,
    DocumentRegistry,
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


def _paths(root: pathlib.Path) -> list[pathlib.Path]:
    """Select tracked inputs and named support files, including unsafe links."""
    candidates = {
        root / relative.as_posix()
        for relative in tracked_paths(root)
        if relative.suffix == ".md"
    }
    candidates.update(root / relative for relative in SUPPORT_DOCS)
    return [path for path in sorted(candidates) if path.is_file() or path.is_symlink()]


def _current_graph(
    root: pathlib.Path, registry: DocumentRegistry | None = None
) -> DocumentGraph:
    return build_document_graph(
        _paths(root),
        repo_root=root,
        excluded_statuses=NON_ROUTING_STATUSES,
        registry=registry,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="check changed documents and inbound consumers",
    )
    parser.add_argument("--base-ref", help="comparison base for --changed")
    parser.add_argument(
        "--changed-path",
        action="append",
        default=[],
        help="explicit changed path; repeat for a scoped input",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mode", choices=(*tuple(MODE_HANDLERS), "all"))
    mode.add_argument(
        "--impact",
        type=pathlib.PurePosixPath,
        help="report derived reverse relations and inbound references by link type",
    )
    return parser


def _changed_paths(root: pathlib.Path, base_ref: str | None) -> set[str]:
    from scripts.lib.document_governance.metadata.identity import (
        _decode_git_paths,
        _run_git,
    )
    from scripts.lib.document_governance.metadata.lifecycle import (
        resolve_base_selection,
    )
    from scripts.lib.document_governance.metadata.profile import ProfileError

    base = resolve_base_selection(
        root, base_ref or os.environ.get("TEMPLATE_GATE_BASE")
    )
    if base.merge_base is None:
        raise ProfileError(
            "changed link validation requires a readable comparison base"
        )
    commands = (
        [
            "diff",
            "--name-only",
            "-z",
            "--no-renames",
            "--diff-filter=ACDMRT",
            f"{base.merge_base}...HEAD",
        ],
        [
            "diff",
            "--cached",
            "--name-only",
            "-z",
            "--no-renames",
            "--diff-filter=ACDMRT",
        ],
        ["diff", "--name-only", "-z", "--no-renames", "--diff-filter=ACDMRT"],
        ["ls-files", "-z", "--others", "--exclude-standard"],
    )
    changed: set[str] = set()
    for command in commands:
        result = _run_git(root, command, operation="changed link discovery")
        if result.returncode:
            raise ProfileError("cannot establish changed link inputs")
        changed.update(
            path.as_posix()
            for path in _decode_git_paths(result.stdout, "changed link discovery")
        )
    return changed


def _print_impact(root: pathlib.Path, target: pathlib.PurePosixPath) -> int:
    """Print derived reverse lookups and Change Impact; a report, not a gate."""

    if target.is_absolute():
        try:
            target = pathlib.PurePosixPath(
                pathlib.Path(target).resolve().relative_to(root).as_posix()
            )
        except ValueError:
            pass
    target = pathlib.PurePosixPath(posixpath.normpath(target.as_posix()))
    try:
        registry_path = root / "docs/99.templates/registry.json"
        registry = load_registry(
            registry_path if registry_path.exists() else DEFAULT_REGISTRY
        )
        graph = _current_graph(root, registry)
        if target not in {node.path for node in graph.nodes}:
            print(f"impact: {target} is not a current document", file=sys.stderr)
            return 2
        inbound = inbound_link_lookup(graph, target, registry)
    except (OSError, ValueError, TypeError, KeyError, OperationsAuthorityError):
        print(
            "document-link-input-invalid: bounded document or Registry input is invalid",
            file=sys.stderr,
        )
        return 1
    for name, paths in (*relation_lookup(graph, target).items(), *inbound.items()):
        print(f"{name}: {len(paths)}")
        for path in paths:
            print(f"  {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if (args.base_ref is not None or args.changed_path) and not args.changed:
        _parser().error("--base-ref and --changed-path require --changed")
    if args.impact is not None and args.changed:
        _parser().error("--changed cannot be combined with --impact")
    root = args.root.resolve()
    if args.impact is not None:
        return _print_impact(root, args.impact)
    try:
        modes = tuple(MODE_HANDLERS) if args.mode == "all" else (args.mode,)
        registry_path = root / "docs/99.templates/registry.json"
        registry = load_registry(registry_path) if registry_path.exists() else None
        graph = _current_graph(root, registry)
        if args.changed:
            changes = _changed_paths(root, args.base_ref)
            graph = select_changed_documents(graph, changes | set(args.changed_path))
        findings = tuple(finding for mode in modes for finding in run_mode(mode, graph))
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        OperationsAuthorityError,
    ):
        print(
            "document-link-input-invalid: bounded document or Registry input is invalid",
            file=sys.stderr,
        )
        return 1
    failures = sum(finding.severity != "warning" for finding in findings)
    warnings = len(findings) - failures
    for finding in findings:
        print(
            json.dumps(
                f"{finding.code}: {finding.path}: {finding.message}", ensure_ascii=True
            )[1:-1][:2048],
            file=sys.stderr,
        )
    print(
        "document links: "
        f"mode={args.mode} documents={len(graph.nodes)} links={len(graph.links)} "
        f"selected_documents={len(graph.nodes) if graph.selected_paths is None else len(graph.selected_paths)} "
        f"catalog_pairs_total={traceability_pair_total(graph)} "
        f"removed_template_mentions_total={removed_template_mention_total(graph)} "
        f"failures={failures} warnings={warnings} historical_documents=0"
    )
    if failures:
        return 1
    if graph.selected_paths == frozenset():
        print("NOT_APPLICABLE: no changed documents or inbound consumers")
        return 0
    print(f"PASS: document link mode {args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
