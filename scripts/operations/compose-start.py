#!/usr/bin/env python3
"""Plan a source-bound explicit Compose selection, or run an operator plan."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.lib.ops.compose_start import (  # noqa: E402
    create_plan,
    execute_plan,
    load_plan,
)


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, '{"result":"BLOCKED"}\n')


def main(argv=None):
    parser = SafeParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    selection = plan.add_mutually_exclusive_group(required=True)
    selection.add_argument("--selection", choices=["HOME"])
    selection.add_argument("--profile", action="append")
    selection.add_argument("--target", action="append")
    plan.add_argument("--dev-data-expected", choices=["on", "off"])
    up = commands.add_parser("up")
    up.add_argument("--plan", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            mode = "home" if args.selection else "profile" if args.profile else "target"
            values = args.profile or args.target or []
            result = create_plan(
                args.root,
                mode=mode,
                values=values,
                dev_data_expected=args.dev_data_expected,
            )
        else:
            if args.root != ROOT:
                raise ValueError("unsupported_execution_root")
            result = execute_plan(args.root, load_plan(args.root, args.plan))
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({"result": "BLOCKED"}))
        return 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 1 if result.get("result") == "START_FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
