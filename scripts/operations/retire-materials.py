#!/usr/bin/env python3
"""CLI for the canonical exact private-file retirement helper."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.lib.ops.retire_materials import main

if __name__ == "__main__":
    raise SystemExit(main())
