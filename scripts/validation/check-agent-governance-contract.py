#!/usr/bin/env python3
"""CLI for the typed Stage 00 agent-governance contract validator."""

from __future__ import annotations

import argparse
import pathlib
import sys

from agent_governance_contract import (
    ContractLoadError,
    load_contract_bundle,
    render_findings,
    validate_contract_bundle,
    validate_repository,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate typed Stage 00 agent-governance contracts."
    )
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--mode", choices=("contract", "repository"), required=True)
    parser.add_argument(
        "--section",
        choices=("catalog", "providers", "harness", "all"),
        help="Required only for repository mode.",
    )
    args = parser.parse_args(argv)
    if args.mode == "contract" and args.section is not None:
        parser.error("--section requires --mode repository")
    if args.mode == "repository" and args.section is None:
        parser.error("--mode repository requires --section")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        bundle = load_contract_bundle(args.root)
    except ContractLoadError as error:
        print(str(error), file=sys.stderr)
        return 1

    contract_findings = validate_contract_bundle(args.root, bundle)
    if contract_findings:
        print(render_findings(contract_findings), file=sys.stderr)
        return 1

    if args.mode == "repository":
        repository_findings = validate_repository(args.root, bundle, args.section)
        if repository_findings:
            print(render_findings(repository_findings), file=sys.stderr)
            return 1
        print(
            "agent_governance_contract: PASS "
            f"mode=repository section={args.section} failures=0"
        )
        return 0

    print(
        "agent_governance_contract: PASS "
        f"contracts=3 agents={len(bundle.catalog['agents'])} "
        f"functions={len(bundle.catalog['functions'])} "
        f"providers={len(bundle.providers['providers'])} failures=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
