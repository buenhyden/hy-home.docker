#!/usr/bin/env python3
"""Plan, apply, or verify an owned-isolated Open Notebook model registration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.lib.ops._notebook_models_http import (
    ApiError,
    OpenNotebookClient,
    validate_loopback_endpoint,
)
from scripts.lib.ops.notebook_models import (
    PolicyError,
    apply_policy,
    atomic_write_receipt,
    load_policy,
    plan_policy,
    read_password_file,
    verify_policy,
)


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "Invalid model registration arguments; values are not printed.\n")


def _arguments(argv=None):
    parser = Parser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=Parser)
    for name in ("plan", "apply", "verify"):
        command = commands.add_parser(name)
        command.add_argument("--endpoint", required=True)
        command.add_argument("--policy", required=True, type=Path)
        command.add_argument("--password-file", required=True, type=Path)
        command.add_argument("--receipt", type=Path)
        if name == "apply":
            command.add_argument("--owned-isolated", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    try:
        arguments = _arguments(argv)
        if arguments.command == "apply" and (
            not arguments.owned_isolated or arguments.receipt is None
        ):
            raise PolicyError("apply_boundary_refused")
        endpoint = validate_loopback_endpoint(arguments.endpoint)
        policy, fingerprint = load_policy(arguments.policy)
        password = read_password_file(arguments.password_file)
        client = OpenNotebookClient(endpoint, password, total_seconds=300)
        if arguments.command == "plan":
            receipt = plan_policy(policy, client, fingerprint)
        elif arguments.command == "apply":
            receipt = apply_policy(
                policy,
                client,
                fingerprint,
                owned_isolated=arguments.owned_isolated,
            )
        else:
            receipt = verify_policy(policy, client, fingerprint)
        if arguments.receipt is not None:
            atomic_write_receipt(arguments.receipt, receipt)
        print(json.dumps(receipt, ensure_ascii=True, sort_keys=True))
        return 0
    except KeyboardInterrupt:
        print("Model registration cancelled; no completion claimed.", file=sys.stderr)
        return 130
    except (PolicyError, ApiError, OSError, TypeError, ValueError):
        print(
            "Model registration failed; input values and API bodies are not printed.",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
