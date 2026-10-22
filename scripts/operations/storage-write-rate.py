#!/usr/bin/env python3
"""Take a SPEC-0246 W7 write-rate snapshot or compare two of them."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.ops import storage_write_rate as rate  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    collect = sub.add_parser("collect")
    collect.add_argument("directory", type=Path)
    collect.add_argument("label")
    collect.add_argument("--devices", default="sda,sdb")
    compare = sub.add_parser("compare")
    compare.add_argument("directory", type=Path)
    compare.add_argument("--t0", default="t0")
    compare.add_argument("--t1", default="t1")
    compare.add_argument("--ssd-device", default="sda")
    compare.add_argument("--smart-used-percent", type=float)
    compare.add_argument("--smart-host-bytes", type=int)
    args = parser.parse_args(argv)
    try:
        if args.command == "collect":
            rate.collect(args.directory, args.label, tuple(args.devices.split(",")))
            return 0
        result = rate.compare(
            rate.read_snapshot(args.directory, args.t0),
            rate.read_snapshot(args.directory, args.t1),
            ssd_device=args.ssd_device,
            smart_used_percent=args.smart_used_percent,
            smart_host_bytes=args.smart_host_bytes,
        )
        output = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    except (OSError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    print(output)
    return 0 if all(s["status"] == "valid" for s in result["stores"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
