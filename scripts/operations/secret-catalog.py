#!/usr/bin/env python3
"""Narrow P02 public metadata and staging-view entrypoint."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.lib.ops.secret_catalog import main

if __name__ == "__main__":
    raise SystemExit(main())
