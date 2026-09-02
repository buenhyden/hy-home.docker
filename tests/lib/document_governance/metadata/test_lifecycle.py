"""Metadata lifecycle and transition-evidence tests."""

from __future__ import annotations

import pathlib
import tempfile
import unittest

from scripts.lib.document_governance.metadata import lifecycle as lifecycle_module
from tests.lib.document_governance.metadata._support import REGISTRY, metadata


class TransitionOverrideEvidencePathTests(unittest.TestCase):
    """The override's evidence path must name a Task form this repository has.

    `load_transition_overrides` required `docs/03.specs/spec-<slug>/task.md`.
    This repository has zero documents in that form and fifteen in the
    co-located `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` form, so
    every override was rejected while the error text said the evidence "must be
    an existing co-located Task". SPEC-0155 acceptance item 13 owns the
    correction.
    """

    def _override_file(self, root: pathlib.Path, evidence: str) -> pathlib.Path:
        override = root / "override.yaml"
        override.write_text(
            "transition_overrides:\n"
            "- path: docs/03.specs/0001-fixture/spec.md\n"
            "  previous_status: completed\n"
            "  new_status: active\n"
            f"  evidence_task: {evidence}\n"
            "  approval: reviewer\n"
            "  reason: corrects a mis-recorded status\n",
            encoding="utf-8",
        )
        return override

    def _tree(self, root: pathlib.Path, evidence: str) -> None:
        target = root / "docs/03.specs/0001-fixture/spec.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# Fixture\n", encoding="utf-8")
        witness = root / evidence
        witness.parent.mkdir(parents=True, exist_ok=True)
        witness.write_text("# Task\n", encoding="utf-8")

    def test_co_located_task_evidence_is_accepted(self) -> None:
        evidence = "docs/03.specs/0001-fixture/tasks/tsk-0001-fixture.md"
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, evidence)
            overrides = metadata.load_transition_overrides(
                self._override_file(root, evidence),
                root,
                metadata.build_registry_profiles(metadata.load_registry(REGISTRY)),
            )
        self.assertEqual(1, len(overrides))

    def test_the_retired_spec_slash_task_form_is_rejected(self) -> None:
        evidence = "docs/03.specs/spec-0001-fixture/task.md"
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            self._tree(root, evidence)
            with self.assertRaises(metadata.ProfileError):
                metadata.load_transition_overrides(
                    self._override_file(root, evidence),
                    root,
                    metadata.build_registry_profiles(metadata.load_registry(REGISTRY)),
                )
