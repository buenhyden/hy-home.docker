#!/usr/bin/env python3
"""CLI adapter for the shared document metadata contract."""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.document_governance import metadata_contract as _contract  # noqa: E402
from scripts.lib.document_governance import metadata_validator as _validator  # noqa: E402


main = _validator.main


def __getattr__(name: str) -> object:
    """Preserve the validator's import surface during the contract extraction."""

    if hasattr(_contract, name):
        return getattr(_contract, name)
    return getattr(_validator, name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(dir(_contract)) | set(dir(_validator)))


if __name__ == "__main__":
    raise SystemExit(main())
