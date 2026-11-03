#!/usr/bin/env python3
"""Explicit, read-only secret metadata comparison."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.lib.ops.secret_structure import main

if __name__ == "__main__":
    raise SystemExit(main())
