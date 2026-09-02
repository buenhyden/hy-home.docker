"""Structural mirror for promoted lifecycle ownership.

The pre-split suite has no dedicated promoted TestCase to move without
splitting or duplicating assertions. Promoted behavior remains covered by the
existing responsibility contract and the registered check-promoted Gate.
"""

from __future__ import annotations

from scripts.lib.document_governance.lifecycle import promoted as promoted_module


__all__ = ("promoted_module",)
