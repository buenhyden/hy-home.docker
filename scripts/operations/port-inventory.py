#!/usr/bin/env python3
"""Print filtered public-source or explicitly selected synthetic port metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(
            2, "Invalid port inventory arguments; input values are not printed.\n"
        )


def _read(relative):
    from scripts.lib.document_governance.operations_catalog import read_bounded_regular

    path = PurePosixPath(relative)
    if (
        path.is_absolute()
        or ".." in path.parts
        or path.parts[:3] != ("tests", "fixtures", "port-contract")
    ):
        raise ValueError("synthetic fixture scope required")
    raw = read_bounded_regular(ROOT, path, max_bytes=65536)
    return raw, {"path": path.as_posix(), "sha256": hashlib.sha256(raw).hexdigest()}


def _unique(pairs):
    if len(pairs) != len({k for k, _ in pairs}):
        raise ValueError("duplicate environment key")
    return dict(pairs)


def main(argv=None):
    from scripts.lib.ops.port_inventory import (
        project_root,
        render_synthetic,
        validate_contract,
    )

    parser = Parser(description=__doc__)
    parser.add_argument("--synthetic-root")
    parser.add_argument("--override", action="append", default=[])
    parser.add_argument("--synthetic-env")
    args = parser.parse_args(argv)
    try:
        if not args.synthetic_root:
            if args.override or args.synthetic_env:
                raise ValueError("named synthetic inputs required")
            result = project_root(ROOT)
        else:
            if not args.synthetic_env:
                raise ValueError("explicit synthetic environment required")
            selected = [args.synthetic_root, *args.override]
            if (
                len(selected) > 8
                or len(
                    {
                        PurePosixPath(p).as_posix()
                        for p in [*selected, args.synthetic_env]
                    }
                )
                != len(selected) + 1
            ):
                raise ValueError("bounded unique synthetic inputs required")
            documents, evidence = [], []
            for relative in selected:
                raw, record = _read(relative)
                documents.append(raw)
                evidence.append(record)
            raw, record = _read(args.synthetic_env)
            environment = json.loads(raw, object_pairs_hook=_unique)
            result = render_synthetic(
                documents, environment, source=[*evidence, record]
            )
        schema = json.loads(
            (
                ROOT
                / "infra/09-platform-ops/service-integration/port-contract.schema.json"
            ).read_bytes()
        )
        validate_contract(result, schema)
    except (ValueError, TypeError, KeyError, OSError, AttributeError, RecursionError):
        print(
            "Port inventory failed; raw configuration and values are not printed.",
            file=sys.stderr,
        )
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
