#!/usr/bin/env python3
"""Evaluate one bounded public root-resource assessment document."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.ops.root_resource_assessment import (  # noqa: E402
    PublicInputError,
    evaluate_file,
)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("ERROR INVALID_ARGUMENTS", file=sys.stderr)
        return 2
    try:
        result = evaluate_file(argv[0])
    except PublicInputError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] == "REVIEWABLE" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
