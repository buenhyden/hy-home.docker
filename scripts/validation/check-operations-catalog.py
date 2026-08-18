#!/usr/bin/env python3
"""Validate the frozen Operations catalog migration manifest."""

from __future__ import annotations

import argparse
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.document_governance.operations_catalog import (  # noqa: E402
    ManifestError,
    load_operations_catalog_manifest,
    validate_operations_catalog_manifest,
)


MANIFEST = (
    ROOT
    / "docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md"
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("manifest", "structure", "executed", "complete"),
        required=True,
    )
    parser.add_argument(
        "--domains",
        help="comma-separated exact domain slice; accepted only by executed mode",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.mode == "executed" and not args.domains:
        parser.error("--mode executed requires --domains")
    if args.mode != "executed" and args.domains:
        parser.error("--domains is accepted only by --mode executed")
    domains = tuple(args.domains.split(",")) if args.domains else ()
    if any(not domain or domain.strip() != domain for domain in domains):
        parser.error("--domains must be a comma-separated list without empty values")
    try:
        manifest = load_operations_catalog_manifest(MANIFEST)
    except ManifestError as error:
        print(f"FAIL {error.code}: {error}")
        return 1
    findings = validate_operations_catalog_manifest(
        ROOT,
        manifest,
        mode=args.mode,
        domains=domains,
    )
    for finding in findings:
        print(f"FAIL {finding.code}: {finding.path}: {finding.message}")
    if findings:
        print(f"operations-catalog: FAIL findings={len(findings)}")
        return 1
    print(
        "operations-catalog: PASS "
        f"mode={args.mode} subjects={len(manifest.subjects)} "
        f"files={len(manifest.files)} approval={manifest.approval.status}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
