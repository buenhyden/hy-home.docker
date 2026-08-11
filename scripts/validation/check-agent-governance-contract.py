#!/usr/bin/env python3
"""CLI for the typed Stage 00 agent-governance contract validator."""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import stat
import sys


_ROOT_ERROR = "FAIL: invalid HYHOME_CI_GATE_ROOT"


def _repository_root() -> pathlib.Path:
    fallback = pathlib.Path(__file__).resolve().parents[2]
    override = os.environ.get("HYHOME_CI_GATE_ROOT")
    if override is None:
        return fallback
    match = re.fullmatch(r"/proc/self/fd/(0|[1-9][0-9]*)", override)
    if match is None:
        raise SystemExit(_ROOT_ERROR)
    try:
        descriptor = os.fstat(int(match.group(1)))
        direct = fallback.stat()
    except (OSError, ValueError, OverflowError):
        raise SystemExit(_ROOT_ERROR) from None
    if not stat.S_ISDIR(descriptor.st_mode) or (
        descriptor.st_dev,
        descriptor.st_ino,
    ) != (direct.st_dev, direct.st_ino):
        raise SystemExit(_ROOT_ERROR)
    # The descriptor is now proven to name the same directory inode as the
    # script-relative root, which is the whole point of the handoff check.
    # Return that real path rather than the /proc/self/fd magic symlink:
    # agent_governance_contract opens every root-confined component with
    # O_NOFOLLOW, so handing it a symlink root fails with ELOOP and surfaces
    # as AGC-CONTRACT-UNSAFE-FILE. Resolving here keeps both the runner's
    # pin-by-descriptor verification and the reader's no-symlink guarantee.
    return fallback


ROOT = _repository_root()
_VALIDATION_DIRECTORY = str(ROOT / "scripts/validation")
if _VALIDATION_DIRECTORY not in sys.path:
    sys.path.insert(0, _VALIDATION_DIRECTORY)

from agent_governance_contract import (  # noqa: E402
    ContractLoadError,
    load_contract_bundle,
    render_findings,
    validate_contract_bundle,
    validate_repository,
)


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
