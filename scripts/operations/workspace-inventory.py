#!/usr/bin/env python3
"""Scan public source evidence, compare dated inventories, or validate metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.ops.workspace_inventory import (
    InventoryError,
    atomic_write,
    compare,
    load_public,
    render_inventory,
    scan,
    validate,
)


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "Invalid inventory arguments; input values are not printed.\n")


def main(argv=None):
    parser = Parser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=Parser)
    scanning = commands.add_parser("scan")
    scanning.add_argument("--root", type=Path, default=Path.cwd())
    scanning.add_argument("--output", required=True)
    scanning.add_argument("--private-output")
    scanning.add_argument("--curation")
    scanning.add_argument("--reviews")
    scanning.add_argument("--render", action="store_true")
    scanning.add_argument("--render-inputs")
    scanning.add_argument("--connections", action="store_true")
    scanning.add_argument("--public-path", action="append", default=[])
    comparing = commands.add_parser("compare")
    comparing.add_argument("--root", type=Path, default=Path.cwd())
    comparing.add_argument("--before", required=True)
    comparing.add_argument("--after", required=True)
    checking = commands.add_parser("validate")
    checking.add_argument("--root", type=Path, default=Path.cwd())
    checking.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            if args.render_inputs and not args.render:
                raise InventoryError("Synthetic render inputs require rendering.")
            reviews = load_public(args.root, args.reviews) if args.reviews else []
            outputs = [
                args.output,
                *([args.private_output] if args.private_output else []),
            ]
            public, private = scan(
                args.root,
                public_paths=args.public_path,
                excluded_outputs=outputs,
                reviews=reviews,
                connections=args.connections,
            )
            curation = load_public(args.root, args.curation) if args.curation else {}
            allowed = {
                "requirements",
                "acceptance_reuse",
                "ownership",
                "research",
                "coverage_tiers",
                "coverage_learning",
                "handoffs",
            }
            if not isinstance(curation, dict) or not set(curation) <= allowed:
                raise InventoryError("Invalid curation sections.")
            public = {**public, **curation}
            validate(public)
            if args.render:
                options = (
                    {"case_inputs": load_public(args.root, args.render_inputs)}
                    if args.render_inputs
                    else {}
                )
                public = render_inventory(args.root, public, **options)
            if args.private_output:
                if (
                    not args.private_output.startswith(
                        "_workspace/repo-support/analysis/"
                    )
                    or args.private_output == args.output
                ):
                    raise InventoryError("Private metadata output boundary refused.")
                atomic_write(args.root, args.private_output, private)
            atomic_write(args.root, args.output, public)
            result = {
                "result": "PASS",
                "coverage": public["coverage"],
                "private_metadata_written": bool(args.private_output),
            }
        elif args.command == "compare":
            result = compare(
                load_public(args.root, args.before), load_public(args.root, args.after)
            )
        else:
            validate(load_public(args.root, args.input))
            result = {
                "result": "PASS",
                "meaning": "Metadata consistency only; no live or semantic acceptance.",
            }
    except KeyboardInterrupt:
        print("Inventory cancelled; no acceptance claimed.", file=sys.stderr)
        return 130
    except (InventoryError, OSError, TypeError, KeyError, RecursionError):
        print(
            "Inventory failed; values and raw errors are not printed.", file=sys.stderr
        )
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
