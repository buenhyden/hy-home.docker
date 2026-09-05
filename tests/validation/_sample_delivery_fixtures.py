"""Builders for sample-delivery verdict variants written to temporary roots."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def verdict_variant(source: Path, **changes: Any) -> dict[str, Any]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload.update(changes)
    return payload


def write_verdict_variant(
    directory: Path,
    source: Path,
    name: str,
    **changes: Any,
) -> Path:
    path = directory / name
    path.write_text(
        json.dumps(verdict_variant(source, **changes), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path
